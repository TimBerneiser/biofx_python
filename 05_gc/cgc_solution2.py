#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-08
Purpose: Compute GC content
"""

import argparse
from typing import NamedTuple, TextIO
import sys
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Compute GC content',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='?',
                        default=sys.stdin,
                        help='A FASTA file')

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    recs = SeqIO.parse(args.file, 'fasta')
    highest = ['', 0.]

    for fasta in recs:
        if find_gc(fasta) > highest[1]:
            highest = [fasta.id, find_gc(fasta)]

    print(f"{highest[0]} {highest[1]:.6f}")


# --------------------------------------------------
def find_gc(sequence: str) -> float:
    """ Calculates the GC percentage of a given sequence """

    if not sequence:
        return 0.

    gc = sequence.count("G") + sequence.count("C")
    
    return 100*gc/len(sequence)


# --------------------------------------------------
def test_find_gc():
    """ Test find_gc """
    
    assert find_gc('') == 0.
    assert find_gc('CC') == 100.
    assert find_gc('GG') == 100.
    assert find_gc('CG') == 100.
    assert find_gc('AACC') == 50.
    assert find_gc('ACAC') == 50.
    assert find_gc('ACGA') == 50.
    assert find_gc('ATCTGCACAG') == 50.
    assert find_gc('AAGATTGTCCCG') == 50.
    assert find_gc('AAAAAAATTTTATATATTA') == 0

# --------------------------------------------------
if __name__ == '__main__':
    main()
