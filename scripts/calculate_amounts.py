from __future__ import division
from argparse import ArgumentParser
from genologics.lims import Lims
from genologics.config import BASEURI, USERNAME, PASSWORD
from genologics.entities import Process

DESC = """ Calculate the sample metrics based on new and previous measurements. Intended to run between the steps of the
Nanopore ligation library prep.

Alfred Kedhammar, NGI SciLifeLab
"""

def main(lims, args):
        
        currentStep = Process(lims, id=args.pid)

        art_tuples = [art_tuple for art_tuple in currentStep.input_output_maps if art_tuple[1]["output-type"] == "Analyte"]


def fetch_last_udf(currentStep, art_tuple, target_udf):

    # Return udf if present in input of current step
    if target_udf in [item_tuple[0] for item_tuple in art_tuple[0]["uri"].udf.items()]:
        return art_tuple[0]["uri"].udf[target_udf]

    # Start looking though previous steps. Use input articles.
    else:
        input_art = art_tuple[0]["uri"]
        # Traceback of artifact ID, step and UDFs
        history = [(input_art.id, currentStep.type.name, art_tuple[1]["uri"].udf.items())]
        
        while True:
            if input_art.parent_process:
                pp = input_art.parent_process
                pp_tuples = pp.input_output_maps

                # Find the input whose output is the current artifact
                pp_input_art = [pp_tuple[0]["uri"] for pp_tuple in pp_tuples if pp_tuple[1]["uri"].id == input_art.id][0]
                history.append((pp_input_art.id, pp.type.name, pp_input_art.udf.items()))

                if target_udf in [tuple[0] for tuple in pp_input_art.udf.items()]:
                    return pp_input_art.udf[target_udf]
                else:
                    input_art = pp_input_art

            else:
                return None


if __name__ == "__main__":
    parser = ArgumentParser(description=DESC)
    parser.add_argument('--pid',
                        help='Lims id for current Process')
    args = parser.parse_args()

    lims = Lims(BASEURI, USERNAME, PASSWORD)
    lims.check_version()
    main(lims, args)