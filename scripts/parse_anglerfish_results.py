#!/usr/bin/env python
import glob
import logging
import os
from argparse import ArgumentParser
from datetime import datetime as dt

import pandas as pd
from genologics.config import BASEURI, PASSWORD, USERNAME
from genologics.entities import Artifact, Process
from genologics.lims import Lims

from epp_utils import formula
from epp_utils.udf_tools import fetch, put


def find_latest_flowcell_run(currentStep: Process) -> str:
    flowcell_id: str = currentStep.udf["ONT flow cell ID"].upper().strip()
    run_query = f"/srv/ngi-nas-ns/minion_data/qc/*{flowcell_id}*"
    logging.info(f"Looking for path {run_query}")

    run_glob = glob.glob(run_query)
    assert (
        len(run_glob) != 0
    ), f"No runs with flowcell ID {flowcell_id} found on path {run_query}"
    if len(run_glob) > 1:
        runs_list = "\n".join(run_glob)
        logging.warning(
            f"Multiple runs with flowcell ID {flowcell_id} detected:\n{runs_list}"
        )
    latest_flowcell_run_path = max(run_glob, key=os.path.getctime)

    logging.info(f"Using latest flowcell run {latest_flowcell_run_path}")
    return latest_flowcell_run_path


def find_latest_anglerfish_run(latest_flowcell_run_path: str) -> str:
    anglerfish_query = f"{latest_flowcell_run_path}/*anglerfish_run*"
    anglerfish_glob = glob.glob(anglerfish_query)

    assert (
        len(anglerfish_glob) != 0
    ), f"No Anglerfish runs found for query {anglerfish_query}"

    if len(anglerfish_glob) > 1:
        runs_list = "\n".join(anglerfish_glob)
        logging.warning(f"Multiple Anglerfish runs detected:\n{runs_list}")
    latest_anglerfish_run_path = max(anglerfish_glob, key=os.path.getctime)
    logging.info(f"Using latest Anglerfish run {latest_anglerfish_run_path}")

    return latest_anglerfish_run_path


def upload_anglerfish_text_results(
    lims: Lims, currentStep: Process, latest_anglerfish_run_path: str
):
    logging.info("Uploading Anglerfish results .txt-file to LIMS")

    anglerfish_file_slot: Artifact = [
        outart
        for outart in currentStep.all_outputs()
        if outart.name == "Anglerfish Result File"
    ][0]

    file_name = os.path.join(latest_anglerfish_run_path, "anglerfish_stats.txt")
    assert os.path.exists(file_name), f"File {file_name} does not exist"

    # Upload results to LIMS
    lims.upload_new_file(anglerfish_file_slot, file_name)


def get_anglerfish_dataframe(latest_anglerfish_run_path: str) -> pd.DataFrame:
    file_name = "anglerfish_dataframe.csv"
    file_path = os.path.join(latest_anglerfish_run_path, file_name)
    assert os.path.exists(file_path), f"File {file_path} does not exist"

    df_raw = pd.read_csv(file_path)

    return df_raw


def parse_data(df_raw: pd.DataFrame):
    df = df_raw.copy()

    # Add additional metrics
    df["repr_total_pc"] = df["num_reads"] / df["num_reads"].sum() * 100
    df["repr_within_barcode_pc"] = df.apply(
        # Sample reads divided by sum of all sample reads w. the same barcode
        lambda row: row["num_reads"]
        / df[df["ont_barcode"] == row["ont_barcode"]]["num_reads"].sum()
        * 100,
        axis=1,
    )

    return df


def ont_barcode_well2name(barcode_well: str) -> str:
    # Add colon if not present
    if ":" not in barcode_well:
        barcode_well = f"{barcode_well[0]}:{barcode_well[1:]}"

    # Get the number corresponding to the well (column-wise)
    barcode_num_str = str(formula.well_name2num_96plate[barcode_well])

    # Pad barcode number with leading zero if necessary
    if len(barcode_num_str) < 2:
        barcode_num_str = f"0{barcode_num_str}"
    barcode_name = f"barcode{barcode_num_str}"

    return barcode_name


def fill_udfs(currentStep: Process, df: pd.DataFrame):
    # Dictate which LIMS UDF corresponds to which column in the dataframe
    udfs_to_cols = {
        "# Reads": "num_reads",
        "Avg. Read Length": "mean_read_len",
        "Std. Read Length": "std_read_len",
        "Representation Within Run (%)": "repr_total_pc",
        "Representation Within Barcode (%)": "repr_within_barcode_pc",
    }

    # Get Illumina pools
    illumina_pools = [
        input_art
        for input_art in currentStep.all_inputs()
        if input_art.type == "Analyte"
    ]

    for illumina_pool in illumina_pools:
        try:
            # Get Illumina samples in the current pool
            illumina_samples = [
                output
                for output in currentStep.all_outputs()
                if output.type == "ResultFile"
                and output.input_artifact_list()[0].name == illumina_pool.name
                and output.name in list(df["sample_name"])
            ]

            for illumina_sample in illumina_samples:
                try:
                    barcode_name = ont_barcode_well2name(
                        fetch(illumina_sample, "ONT Barcode Well")
                    )

                    # Subset df to the current ONT barcode
                    df_barcode = df[df["ont_barcode"] == barcode_name]

                    # Further subset df to the current Illumina sample
                    df_sample = df_barcode[
                        df_barcode["sample_name"] == illumina_sample.name
                    ]

                    assert (
                        len(df_sample) == 1
                    ), f"Multiple entries matching both Illumina sample name {illumina_sample.name} and ONT barcode {barcode_name} was found in the dataframe."

                    # Start putting UDFs
                    for udf, col in udfs_to_cols.items():
                        try:
                            value = float(df_sample[col].values[0])
                            put(
                                illumina_sample,
                                udf,
                                value,
                            )
                        except:
                            logging.error(
                                f"Could not assign UDF '{udf}' value '{value}' for sample {illumina_sample.name}"
                            )
                            continue

                except:
                    logging.error(f"Could not process sample {illumina_sample.name}")
                    continue

        except:
            logging.error(f"Could not process pool {illumina_pool.name}")
            continue


def upload_log(currentStep: Process, lims: Lims, log_filename):
    log_file_slot = [
        slot
        for slot in currentStep.all_outputs()
        if slot.name == "Parse Anglerfish Results Log"
    ][0]
    for f in log_file_slot.files:
        lims.request_session.delete(f.uri)
    lims.upload_new_file(log_file_slot, log_filename)

    # Remove originally written file
    os.remove(log_filename)


def main(lims: Lims, currentStep: Process):
    latest_flowcell_run_path = find_latest_flowcell_run(currentStep)
    latest_anglerfish_run_path = find_latest_anglerfish_run(latest_flowcell_run_path)

    upload_anglerfish_text_results(lims, currentStep, latest_anglerfish_run_path)

    # Get file contents
    df_raw: pd.DataFrame = get_anglerfish_dataframe(latest_anglerfish_run_path)

    # Parse the Anglerfish output
    df_parsed: pd.DataFrame = parse_data(df_raw)

    # Populate sample fields with Anglerfish results
    fill_udfs(currentStep, df_parsed)

    # Add sample comments
    # TODO

    # Upload log
    upload_log(currentStep, lims, log_filename)


if __name__ == "__main__":
    # Parse script arguments
    parser = ArgumentParser()
    parser.add_argument(
        "--pid", default="24-594126", dest="pid", help="Lims id for current Process"
    )
    args = parser.parse_args()

    # Set up LIMS instance
    lims = Lims(BASEURI, USERNAME, PASSWORD)
    lims.check_version()
    currentStep = Process(lims, id=args.pid)

    # Set up logging
    timestamp = dt.now().strftime("%y%m%d_%H%M%S")
    log_filename = f"parse_anglerfish_results_log_{currentStep.id}_{timestamp}_{currentStep.technician.name.replace(' ','')}"
    logging.basicConfig(
        filename=log_filename,
        filemode="w",
        format="%(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    main(lims, currentStep)
