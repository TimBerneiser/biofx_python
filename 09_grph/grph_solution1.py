#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-11
Purpose: Overlap Graphs
"""

import argparse
from typing import NamedTuple, TextIO, List, Tuple
import sys
from Bio import SeqIO
import logging


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO
    k: int
    debug: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Overlap Graphs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=sys.stdin,
                        help="a FASTA file")

    parser.add_argument('-k',
                        '--overlap',
                        help='Size of overlap',
                        metavar='OVER',
                        type=int,
                        default=3)

    parser.add_argument('-d',
                        '--debug',
                        help='Debug',
                        action='store_true')

    args = parser.parse_args()

    if args.overlap < 1:
        parser.error(f'-k "{args.overlap}" must be > 0')

    return Args(args.file, args.overlap, args.debug)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    logging.basicConfig(
        filename='.log',
        filemode='w',
        level=logging.DEBUG if args.debug else logging.CRITICAL
    )

    logging.debug('input file = "%s"', args.file.name)

    for id1, id2 in get_graphs(args.file, args.k):
        print(id1, id2)


# --------------------------------------------------
def get_graphs(file, overlap) -> List[Tuple[str, str]]:
    """ Make graphs """

    seqs = [(fasta.id, fasta[0:overlap].seq, fasta[-overlap:].seq)
            for fasta in SeqIO.parse(file, 'fasta')]

    graphs = list(tuple())

    for i in range(len(seqs)):
        for j in range(len(seqs)):
            if i!= j and seqs[i][2] == seqs[j][1]:
                graphs.append((seqs[i][0], seqs[j][0]))

    return graphs


# --------------------------------------------------
if __name__ == '__main__':
    main()
