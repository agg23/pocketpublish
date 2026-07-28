#!/usr/bin/env python3

from helpers import *
from sys import argv


def main():
    print("Reversing")
    reverse_bitstream(argv[1], argv[2])


if __name__ == "__main__":
    main()
