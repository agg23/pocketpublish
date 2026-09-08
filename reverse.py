#!/usr/bin/env python3

"""Reverses the bitstream of an RBF file."""

import argparse
import sys

from helpers import *


def main(argv: list[str]) -> int | None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("output")
    opts = parser.parse_args(argv)

    print("Reversing")
    reverse_bitstream(opts.input, opts.output)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
