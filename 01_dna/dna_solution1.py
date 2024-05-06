#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2023-11-25
Purpose: tetranucleotide frequency
"""

import argparse
import os
from typing import NamedTuple, Tuple


class Args(NamedTuple):
    """ Command-line arguments """
    dna: str

# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='tetranucleotide frequency',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dna',
                        metavar='DNA',
                        help='Input DNA sequence')

    args = parser.parse_args()

    if os.path.isfile(args.dna):
        args.dna = open(args.dna).read().rstrip()

    return Args(args.dna)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    count_a, count_c, count_g, count_t = get_counts(args.dna)

    print(f"{count_a} {count_c} {count_g} {count_t}")


def get_counts(dna: str) -> Tuple[int, int, int, int]:
    """ Gets counts for each DNA base (A, C, T, G)"""

    count_a, count_c, count_g, count_t = 0, 0, 0, 0

    for base in dna:
        if base in ("A", "a"):
            count_a += 1
        elif base in ("G", "g"):
            count_g += 1
        elif base in ("C", "c"):
            count_c += 1
        elif base in ("T", "t"):
            count_t += 1
        else:
            print("not a valid DNA sequence")
            break

    return (count_a, count_c, count_g, count_t)


# --------------------------------------------------
if __name__ == '__main__':
    main()
