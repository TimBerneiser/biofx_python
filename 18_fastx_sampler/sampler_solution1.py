#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-23
Purpose: Probabilistically subset FASTA files
"""

import argparse
from typing import NamedTuple, TextIO, Optional
import os
import random
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: TextIO
    file_format: str
    percent: float
    max_reads: int
    seed: Optional[int]
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Probabilistically subset FASTA files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='Input FASTA/Q file(s)')

    parser.add_argument('-f',
                        '--format',
                        metavar='format',
                        type=str,
                        choices=['fasta', 'fastq'],
                        default='fasta',
                        help='Input file format')

    parser.add_argument('-p',
                        '--percent',
                        metavar='reads',
                        type=float,
                        default=.1,
                        help='Percent of reads')

    parser.add_argument('-m',
                        '--max',
                        metavar='max',
                        type=int,
                        default=0,
                        help='Maximum number of reads')

    parser.add_argument('-s',
                        '--seed',
                        metavar='seed',
                        type=int,
                        default=None,
                        help='Random seed value')

    parser.add_argument('-o',
                        '--outdir',
                        metavar='DIR',
                        type=str,
                        default='out',
                        help='Output directory')

    args = parser.parse_args()

    if not 0 < args.percent < 1:
        parser.error(f'--percent "{args.percent}" must be between 0 and 1')

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    return Args(files=args.file, file_format=args.format, percent=args.percent,
                max_reads=args.max, seed=args.seed, outdir=args.outdir)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    random.seed(args.seed)
    reads = 0
    file_num = 0

    for fh in args.files:
        file_num+=1
        with open(f'./{args.outdir}/{os.path.basename(fh.name)}', 'wt') as f:
            print(f'  {file_num}: {os.path.basename(fh.name)}')
            for seq in SeqIO.parse(fh, args.file_format):
                if random.random() <= args.percent:
                    f.write(f'>{seq.name}\n{seq.seq}\n')
                    reads +=1
                if args.max_reads and reads >= args.max_reads:
                    break
            if args.max_reads and reads >= args.max_reads:
                break

    print(f'Wrote {reads:,} sequence{'s' if reads>1 else ''} '
          f'from {file_num:,} file{'s' if file_num>1 else ''} '
          f'to directory "{args.outdir}".')


# --------------------------------------------------
if __name__ == '__main__':
    main()
