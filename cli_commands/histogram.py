import argparse
from pathlib import Path

import empress
from empress.histogram import histogram_main
import cli_commands._shared_utils


def add_histogram_to_parser(histogram_parser: argparse.ArgumentParser):
    cli_commands._shared_utils.add_recon_input_args_to_parser(histogram_parser)
    cli_commands._shared_utils.add_dtl_costs_to_parser(histogram_parser)

    histogram_parser.add_argument("--histogram", metavar="<filename>", default="unset",
                                  nargs="?", help="output the histogram at the path provided. If no filename is "
                                                  "provided, outputs to a filename based on the input host file")
    histogram_parser.add_argument("--xnorm", action="store_true",
                                  help="normalize the x-axis so that the distances range between 0 and 1")
    histogram_parser.add_argument("--ynorm", action="store_true",
                                  help="normalize the y-axis so that the histogram is a probability distribution")
    histogram_parser.add_argument("--omit-zeros", action="store_true",
                                  help="omit the zero column of the histogram, which will always be the "
                                  "total number of reconciliations")
    histogram_parser.add_argument("--cumulative", action="store_true",
                                  help="make the histogram cumulative")
    histogram_parser.add_argument("--csv", metavar="<filename>",
                                  help="output the histogram as a .csv file at the path provided. If no filename is "
                                       "provided, outputs to a filename based on the input host file")

    # Statistics to print
    histogram_parser.add_argument("--stats", action="store_true",
                                  help="output statistics including the total number of MPRs, the diameter of "
                                       "MPR-space, and the average distance between MPRs")

    # Time it
    histogram_parser.add_argument("--time", action="store_true",
                                  help="time the diameter algorithm")


def run_histogram(args):
    recon_input = empress.ReconInputWrapper.from_files(args.host, args.parasite, args.mapping)
    fname = Path(args.host)
    cost_suffix = "histogram.{}-{}-{}".format(args.dup_cost, args.trans_cost, args.loss_cost)
    # TODO: check that the specified path has a matplotlib-compatible extension?
    # If args is unset, use the original .newick file path but replace .newick with .pdf
    if args.histogram is None:
        args.histogram = str(fname.with_suffix(cost_suffix + ".pdf"))
    # If it wasn't set by the arg parser, then set it to None (the option wasn't present)
    elif args.histogram == "unset":
        args.histogram = None
    # Set the CSV path
    cli_commands._shared_utils.set_csv_path(args, "histogram")
    print("Output .csv to {}".format(args.csv))
    if args.histogram is not None:
        print("Output histogram to {}".format(args.histogram))
    histogram_main.compute_pdv(args.host, recon_input, args.dup_cost, args.trans_cost, args.loss_cost, args)
