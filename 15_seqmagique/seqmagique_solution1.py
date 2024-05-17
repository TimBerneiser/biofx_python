#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-17
Purpose: Mimic seqmagick
"""

import argparse
from typing import NamedTuple, TextIO, List
from tabulate import tabulate
import statistics
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    tablefmt: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Mimic seqmagick',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+',
                        help='Input FASTA file(s)')

    parser.add_argument('-t',
                        '--tablefmt',
                        type=str,
                        choices=[
                            'plain', 'simple', 'grid', 'pipe', 'orgtbl', 'rst',
                            'mediawiki', 'latex', 'latex_raw', 'latex_booktabs'
                        ],
                        default='plain',
                        help='Tabulate table style')

    args = parser.parse_args()

    return Args(args.file, args.tablefmt)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    seqs_info = []
    for fh in args.files:
        if seqs:= [rec for rec in SeqIO.parse(fh, 'fasta')]:
            name = fh.name
            min_len = min([len(str(seq.seq)) for seq in seqs])
            max_len = max([len(str(seq.seq)) for seq in seqs])
            avg_len = statistics.fmean([len(str(seq.seq)) for seq in seqs])
            num_seqs = len(seqs)
            seqs_info.append((name, min_len, max_len, avg_len, num_seqs))
        else:
            seqs_info.append((fh.name, 0, 0, 0.00, 0))

    headers = ['name', 'min_len', 'max_len', 'avg_len', 'num_seqs']
    
    print(tabulate(seqs_info, headers=headers, tablefmt=args.tablefmt, floatfmt='.2f'))

# --------------------------------------------------
if __name__ == '__main__':
    main()
