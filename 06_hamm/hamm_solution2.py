#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-09
Purpose: Compute Hamming distance
"""

import argparse
from typing import NamedTuple
from itertools import zip_longest


class Args(NamedTuple):
    """ Command-line arguments """
    seq1: str
    seq2: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Compute Hamming distance',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('seq1',
                        metavar='DNA',
                        help='Sequence 1')

    parser.add_argument('seq2',
                        metavar='DNA',
                        help='Sequence 2')

    args = parser.parse_args()

    return Args(args.seq1, args.seq2)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    print(get_hamm(args.seq1, args.seq2))


# --------------------------------------------------
def get_hamm(seq1, seq2) -> int:
    """ Get Hamming distance """

    edits = sum((1 for c1, c2 in zip_longest(seq1, seq2) if c1 != c2))

    return edits

# --------------------------------------------------
def test_get_hamm() -> None:
    """ Test get_hamm """

    assert get_hamm('', '') == 0
    assert get_hamm('AA', 'AA') == 0
    assert get_hamm('AACC', 'AA') == 2
    assert get_hamm('ACGCAACG', 'CGAGCCGA') == 8
    assert get_hamm('AACCGGCCAA', 'ACCGGCCAAT') == 5


# --------------------------------------------------
if __name__ == '__main__':
    main()
