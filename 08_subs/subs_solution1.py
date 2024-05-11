#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-11
Purpose: Find a motif in a DNA sequence
"""

import argparse
from typing import NamedTuple


class Args(NamedTuple):
    """ Command-line arguments """
    seq: str
    subseq: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Find a motif in a DNA sequence',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('seq',
                        metavar='SEQ',
                        help='DNA sequence',
                        type=str)

    parser.add_argument('subseq',
                        metavar='SUBSEQ',
                        help='DNA motif',
                        type=str)

    args = parser.parse_args()

    return Args(args.seq, args.subseq)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    print(' '.join(find_motifs(args.seq, args.subseq)))


# --------------------------------------------------
def find_motifs(seq, subseq) -> list:
    """ Finds positions of subseq in seq """

    positions = []

    while -1 not in positions:
        if not positions:
            positions.append(seq.find(subseq))
        else:
            positions.append(seq.find(subseq, positions[-1]+1))

    return [str(x+1) for x in positions[:-1]]


# --------------------------------------------------
if __name__ == '__main__':
    main()
