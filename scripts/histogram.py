"""Thin wrapper to call R."""

import os
import argparse

HERE = os.path.dirname(os.path.realpath(__file__))
RSCRIPT = os.path.join(HERE, "histogram.R")


def generate_histogram(cellinfo_fpath, mean_output_fpath, sum_output_fpath):
    cmd = "Rscript {} {} {} {}".format(RSCRIPT,
                                       cellinfo_fpath,
                                       mean_output_fpath,
                                       sum_output_fpath)
    return os.system(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_fpath")
    parser.add_argument("output_fpath")
    args = parser.parse_args()

    generate_histogram(args.input_fpath, args.output_fpath)
