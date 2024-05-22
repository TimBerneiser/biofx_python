#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-21
Purpose: Grep through fastx files
"""

import argparse
from typing import NamedTuple, TextIO, List
import sys
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    pattern: str
    files: List[TextIO]
    input_format: str
    output_format: str
    outfile: TextIO
    insensitive: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Grep through fastx files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('pattern',
                        metavar='str',
                        type=str,
                        help='grep pattern')

    parser.add_argument('files',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+',
                        help='Input file(s)')

    parser.add_argument('-f',
                        '--format',
                        metavar='str',
                        type=str,
                        choices=['fasta', 'fastq'],
                        default='',
                        help='Input file format (default: )')

    parser.add_argument('-O',
                        '--outfmt',
                        metavar='str',
                        type=str,
                        choices=['fasta', 'fastq', 'fasta-2line'],
                        default='',
                        help='Output file format (default: )')

    parser.add_argument('-o',
                        '--outfile',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default=sys.stdout,
                        help='Output file')

    parser.add_argument('-i',
                        '--insensitive',
                        help='Case-insensitive search',
                        action='store_true')

    args = parser.parse_args()

    return Args(pattern=args.pattern, files=args.files,
                input_format=args.format, output_format=args.outfmt,
                outfile=args.outfile, insensitive=args.insensitive)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    file = ''
    if args.outfile.name=='<stdout>':
        file = sys.stdout

    for fh in args.files:
        input_format = guess_format(fh.name)

        if not input_format:
            sys.exit(f'Please specify file format for "{fh.name}"')

        output_format = args.output_format or input_format

        if not file:
            file = open(f'./{args.outfile.name}', 'wt')

        for seq in SeqIO.parse(fh, input_format):
            if args.insensitive:
                if seq.id.lower().find(args.pattern)!=-1 or seq.id.upper().find(args.pattern)!=-1:
                    file.write(seq.format(output_format))
            else:
                if seq.id.find(args.pattern) != -1:
                    file.write(seq.format(output_format))


# --------------------------------------------------
def guess_format(filename: str) -> str:
    """ Guess the file format from extension """

    fasta_ext = ['fasta', 'fa', 'fna', 'faa']
    fastq_ext = ['fq', 'fastq']
    handle = filename.split('.')[-1]

    if handle in fasta_ext:
        return 'fasta'

    if handle in fastq_ext:
        return 'fastq'

    return ''


# --------------------------------------------------
def test_guess_format() -> None:
    """ Test guess_format """

    assert guess_format('/foo/bar.fasta') == 'fasta'
    assert guess_format('/foo/bar.fa') == 'fasta'
    assert guess_format('/foo/bar.fna') == 'fasta'
    assert guess_format('/foo/bar.faa') == 'fasta'
    assert guess_format('/foo/bar.fq') == 'fastq'
    assert guess_format('/foo/bar.fastq') == 'fastq'
    assert guess_format('/foo/bar.jsd') == ''


# --------------------------------------------------
if __name__ == '__main__':
    main()
