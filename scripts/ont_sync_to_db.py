#!/usr/bin/env python

import logging
import os
import re
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime as dt

import pandas as pd
from couchdb.client import Database, Document, Row, ViewResults
from generate_minknow_samplesheet import generate_MinKNOW_samplesheet, strip_characters
from genologics.config import BASEURI, PASSWORD, USERNAME
from genologics.entities import Artifact, Process
from genologics.lims import Lims
from ont_send_reloading_info_to_db import get_ONT_db

from epp_utils import udf_tools
from scilifelab_epps.epp import traceback_to_step, upload_file

DESC = """Script for finishing the step to start ONT sequencing in LIMS.

Makes sure there are no discprepancies in the provided information and
appends LIMS-specific information to the ONT run in StatusDB.
"""

TIMESTAMP: str = dt.now().strftime("%y%m%d_%H%M%S")
SCRIPT_NAME: str = os.path.basename(__file__).split(".")[0]


def assert_samplesheet(process: Process, args: Namespace, lims: Lims):
    """Check that there isn't a loaded samplesheet that is contradicted by the step UDFs."""

    # Get ONT samplesheet file artifact
    file_art: Artifact = [
        op for op in process.all_outputs() if op.name == args.samplesheet
    ][0]

    # If samplesheet file is loaded
    if file_art.files:
        logging.info("Detected samplesheet.")
        samplesheet_contents: str = lims.get_file_contents(uri=file_art.files[0].uri)

        logging.info("Checking that the loaded samplesheet is up to date...")
    else:
        logging.info("No samplesheet file loaded.")
        return True

    # Generate new samplesheet from step, then read it and remove the file
    new_samplesheet_path = generate_MinKNOW_samplesheet(process=process, qc=args.qc)
    new_samplesheet_contents = open(new_samplesheet_path).read()
    os.remove(new_samplesheet_path)

    # Check step samplesheet is up-to-date with step UDFs
    if samplesheet_contents != new_samplesheet_contents:
        logging.error(
            f"The current sample sheet doesn't correspond to the current UDFs.\nCurrent sample sheet:\n{samplesheet_contents}\nNew sample sheet:\n{new_samplesheet_contents}"
        )
        raise AssertionError(
            "The current sample sheet doesn't correspond to the current UDFs."
        )
    else:
        logging.info("Samplesheet is up to date.")
        return True


def udfs_matches_run_name(art: Artifact) -> bool:
    """Check that artifact run name is not contradicted by other UDFs."""

    matches: bool = True
    _yyyymmdd, _hhmm, pos, fc_id, _hash = art.udf["ONT run name"].split("_")

    if art.udf["ONT flow cell ID"] != fc_id:
        matches = False
        msg = f"Mismatch between UDFs 'ONT flow cell ID': '{art.udf['ONT flow cell ID']}' and 'ONT run name': '{art.udf['ONT run name']}'"
        logging.error(msg)
    if art.udf["ONT flow cell position"] != pos:
        matches = False
        msg = f"Mismatch between UDFs 'ONT flow cell position': '{art.udf['ONT flow cell position']}' and 'ONT run name': '{art.udf['ONT run name']}'"
        logging.error(msg)

    return matches


def get_matching_db_rows(
    art: Artifact,
    process: Process,
    view: ViewResults,
    run_name: str | None,
    qc: bool,
) -> list[Row]:
    """Find the rows in the database view that match the given artifact."""
    matching_rows = []

    # If run name is not supplied, try to find it in the database, assuming it follows the samplesheet naming convention
    if run_name is None:
        minknow_sample_name = (
            strip_characters(art.name) if not qc else f"QC_{strip_characters(art.name)}"
        )
        minknow_experiment_name = process.id if not qc else f"QC_{process.id}"
        # Define query pattern
        if art.udf["ONT flow cell position"]:
            pattern = rf"{minknow_experiment_name}/{minknow_sample_name}/[^/]*_{art.udf['ONT flow cell position']}_{art.udf['ONT flow cell ID']}_[^/]*"
        else:
            pattern = rf"{minknow_experiment_name}/{minknow_sample_name}/[^/]*_{art.udf['ONT flow cell ID']}_[^/]*"
        logging.info(
            f"No run name supplied. Quering the database for run with path pattern '{pattern}'."
        )

        for row in view.rows:
            query = row.value["TACA_run_path"]
            if re.match(pattern, query):
                matching_rows.append(row)

    # If the run name is supplied, query the database directly
    else:
        logging.info(
            f"Full run name supplied. Quering the database for run '{run_name}'."
        )
        for row in view.rows:
            if run_name == row.key:
                matching_rows.append(row)

    return matching_rows


def get_sample_dataframe(library: Artifact, args: Namespace) -> pd.DataFrame:
    """For an ONT sequencing library, compile a dataframe with sample-level information.

    Will necessitate none, single or double demultiplexing.
    """

    logging.info(f"Compiling sample-level information for library '{library.name}'...")

    # Instantiate rows list
    rows = []

    # See if library can be backtracked to an ONT pooling step
    ont_pooling_step, ont_pooling_inputs = traceback_to_step(library, args.pooling_step)

    # If there was ONT pooling...
    if ont_pooling_step:
        # Iterate across ONT pooling inputs
        for ont_pooling_input in ont_pooling_inputs:
            assert len(ont_pooling_input.reagent_labels) == 1
            ont_barcode = ont_pooling_input.reagent_labels[0]

            if args.qc:
                logging.info(
                    "Library assumed to consist of ONT-barcoded Illumina library pool(s) with sample indexes."
                )

                # Trace the ONT pooling input back to the barcoding step to elucidate samples and indexes
                ont_barcoding_step, illumina_pools = traceback_to_step(
                    ont_pooling_input, args.barcoding_step
                )
                assert ont_barcoding_step
                assert len(illumina_pools) == 1
                illumina_pool = illumina_pools[0]

                # ONT barcode AND Illumina index-level demultiplexing
                for illumina_sample, illumina_index in zip(
                    illumina_pool.samples, illumina_pool.reagent_labels
                ):
                    rows.append(
                        {
                            "sample_name": illumina_sample.name,
                            "sample_id": illumina_sample.id,
                            "project_name": illumina_sample.project.name,
                            "project_id": illumina_sample.project.id,
                            "illumina_index": illumina_index,
                            "illumina_pool_name": illumina_pool.name,
                            "illumina_pool_id": illumina_pool.id,
                            "ont_barcode": ont_barcode,
                            "ont_pool_name": ont_pooling_input.name,
                            "ont_pool_id": ont_pooling_input.id,
                        }
                    )

            else:
                logging.info("Library assumed to consist of ONT-barcoded sample(s).")
                assert len(ont_pooling_input.reagent_labels) == 1

                # ONT barcode-level demultiplexing
                for ont_sample, ont_barcode in zip(
                    ont_pooling_input.samples, ont_pooling_input.reagent_labels
                ):
                    rows.append(
                        {
                            "sample_name": ont_sample.name,
                            "sample_id": ont_sample.id,
                            "project_name": ont_sample.project.name,
                            "project_id": ont_sample.project.id,
                            "ont_barcode": ont_barcode,
                            "ont_pool_name": ont_pooling_input.name,
                            "ont_pool_id": ont_pooling_input.id,
                        }
                    )
    # If there was no ONT pooling...
    else:
        if args.qc:
            logging.info(
                "Library assumed to consist of single Illumina library pool with sample indexes."
            )

            # Illumina index-level demultiplexing
            for illumina_sample, illumina_index in zip(
                library.samples, library.reagent_labels
            ):
                rows.append(
                    {
                        "sample_name": illumina_sample.name,
                        "sample_id": illumina_sample.id,
                        "project_name": illumina_sample.project.name,
                        "project_id": illumina_sample.project.id,
                        "illumina_index": illumina_index,
                        "illumina_pool_name": illumina_pool.name,
                        "illumina_pool_id": illumina_pool.id,
                        "ont_barcode": ont_barcode,
                        "ont_pool_name": ont_pooling_input.name,
                        "ont_pool_id": ont_pooling_input.id,
                    }
                )
        else:
            logging.info("Library assumed to consist of single ONT library.")

            # No demultiplexing
            rows.append(
                {
                    "sample_name": library.name,
                    "sample_id": library.id,
                    "project_name": library.project.name,
                    "project_id": library.project.id,
                }
            )

    df = pd.DataFrame(rows)

    return df


def write_to_doc(
    doc: Document, db: Database, process: Process, art: Artifact, args: Namespace
):
    """Update a given document with the given artifact's loading information."""

    sample_df = get_sample_dataframe(art, args)

    # Info to add to the db doc
    dict_to_add = {
        "step_name": process.type.name,
        "step_id": process.id,
        "timestamp": TIMESTAMP,
        "operator": process.technician.name,
        "load_fmol": art.udf["ONT flow cell loading amount (fmol)"],
        "load_vol": art.udf["Volume to take (uL)"],
        "sample_data": sample_df.to_dict(orient="records"),
    }

    if "lims" not in doc:
        doc["lims"] = {}
    if "loading" not in doc["lims"]:
        doc["lims"]["loading"] = []
    doc["lims"]["loading"].append(dict_to_add)

    db[doc.id] = doc


def sync_runs_to_db(process: Process, args: Namespace, lims: Lims):
    """Executive script, called once."""

    # Assert samplesheet, if any, makes sense in the context of the step UDFs
    assert_samplesheet(process=process, args=args, lims=lims)

    arts: list[Artifact] = [
        art for art in process.all_outputs() if art.type == "Analyte"
    ]

    # Keep track of which artifacts were successfully updated
    arts_successful = []

    db: Database = get_ONT_db()
    view: ViewResults = db.view("info/all_stats")

    for art in arts:
        logging.info(f"Processing '{art.name}'...")

        run_name: str | None = udf_tools.fetch(art, "ONT run name", on_fail=None)
        if run_name is not None:
            # Assert run name is not contradicted by other UDFs
            if not udfs_matches_run_name(art):
                logging.warning("Run name contradicted by other UDFs. Skipping.")
                continue

        # Get matching run docs
        matching_rows: list[Row] = get_matching_db_rows(
            art, process, view, run_name, args.qc
        )

        if len(matching_rows) == 0:
            logging.warning("Run was not found in the database. Skipping.")
            continue

        elif len(matching_rows) > 1:
            matching_run_names = [row.key for row in matching_rows]
            logging.warning("Query was found in multiple instances in the database: ")
            for matching_run_name in matching_run_names:
                logging.warning(f"Matching run name: '{matching_run_name}'.")
            logging.warning("Contact a database administrator. Skipping.")
            continue

        doc_run_name: str = matching_rows[0].key
        doc_id: str = matching_rows[0].id
        doc: Document = db[doc_id]

        logging.info(f"Found matching run '{doc_run_name}' in the database.")

        if run_name is not None and run_name != doc_run_name:
            logging.error(
                f"UDF Run name '{run_name}' contradicted by database run name '{doc_run_name}'. Skipping."
            )
            continue

        logging.info(f"Assigning UDF 'ONT run name': '{doc_run_name}'.")
        udf_tools.put(art, "ONT run name", doc_run_name)

        write_to_doc(doc, db, process, art, args)
        logging.info(f"'{doc_run_name}' was found and updated successfully.")
        arts_successful.append(art)

    if len(arts_successful) < len(arts):
        raise AssertionError(
            f"Only {len(arts_successful)} out of {len(arts)} artifacts were successfully updated. Check log."
        )


def main():
    # Parse args
    parser = ArgumentParser(description=DESC)
    parser.add_argument("--pid", type=str, help="Lims ID for current Process")
    parser.add_argument("--log", type=str, help="Which log file slot to use")
    parser.add_argument(
        "--samplesheet", type=str, help="Which samplesheet file slot to use"
    )
    parser.add_argument("--qc", action="store_true", help="Whether run is QC")
    parser.add_argument(
        "--pooling_step", type=str, help="Name of pooling step to traceback to"
    )
    parser.add_argument(
        "--barcoding_step", type=str, help="Name of barcoding step to traceback to"
    )
    args: Namespace = parser.parse_args()

    # Set up LIMS
    lims = Lims(BASEURI, USERNAME, PASSWORD)
    lims.check_version()
    process = Process(lims, id=args.pid)

    # Set up logging
    log_filename: str = (
        "_".join(
            [
                SCRIPT_NAME,
                process.id,
                TIMESTAMP,
                process.technician.name.replace(" ", ""),
            ]
        )
        + ".log"
    )

    logging.basicConfig(
        filename=log_filename,
        filemode="w",
        format="%(filename)s - %(funcName)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # Start logging
    logging.info(f"Script '{SCRIPT_NAME}' started at {TIMESTAMP}.")
    logging.info(
        f"Launched in step '{process.type.name}' ({process.id}) by {process.technician.name}."
    )
    args_str = "\n\t".join([f"'{arg}': {getattr(args, arg)}" for arg in vars(args)])
    logging.info(f"Script called with arguments: \n\t{args_str}")

    try:
        sync_runs_to_db(process=process, lims=lims, args=args)
    except Exception as e:
        # Post error to LIMS GUI
        logging.error(e, exc_info=True)
        logging.shutdown()
        upload_file(
            file_path=log_filename,
            file_slot=args.log,
            process=process,
            lims=lims,
        )
        sys.stderr.write(str(e))
        sys.exit(2)
    else:
        logging.info("Script completed successfully.")
        logging.shutdown()
        upload_file(
            file_path=log_filename,
            file_slot=args.log,
            process=process,
            lims=lims,
        )
        sys.exit(0)


if __name__ == "__main__":
    main()