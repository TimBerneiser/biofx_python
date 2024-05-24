#!/usr/bin/env python3
""" Annotate BLAST output """

import argparse
import csv
from typing import NamedTuple, TextIO
import pandas as pd


class Args(NamedTuple):
    """ Command-line arguments """
    hits: TextIO
    annotations: TextIO
    outfile: TextIO
    delimiter: str
    pctid: float


# --------------------------------------------------
def get_args():
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Annotate BLAST output',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-b',
                        '--blasthits',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='BLAST -outfmt 6',
                        required=True)

    parser.add_argument('-a',
                        '--annotations',
                        help='Annotations file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        required=True)

    parser.add_argument('-o',
                        '--outfile',
                        help='Output file',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='out.csv')

    parser.add_argument('-d',
                        '--delimiter',
                        help='Output field delimiter',
                        metavar='DELIM',
                        type=str,
                        default='')

    parser.add_argument('-p',
                        '--pctid',
                        help='Minimum percent identity',
                        metavar='PCTID',
                        type=float,
                        default=0.)

    args = parser.parse_args()

    return Args(hits=args.blasthits,
                annotations=args.annotations,
                outfile=args.outfile,
                delimiter=args.delimiter or guess_delimiter(args.outfile.name),
                pctid=args.pctid)


# --------------------------------------------------
def main():
    """ Make a jazz noise here """

    args = get_args()

    annots = pd.read_csv(args.annotations, sep=',', 
                         usecols=['seq_id', 'depth', 'lat_lon'], index_col='seq_id')
    hits = pd.read_csv(args.hits, sep=',', usecols=[0, 2], 
                       names=['qseqid', 'pident'], index_col='qseqid')

    merged = hits[hits['pident'] >= args.pctid].join(annots, how='inner')

    merged.to_csv(args.outfile,
                  index=True,
                  index_label='qseqid',
                  sep=args.delimiter)

    print(f'Exported {merged.shape[0]:,} to "{args.outfile.name}".')


# --------------------------------------------------
def guess_delimiter(filename: str) -> str:
    """ Guess delimiter from file extension """

    if filename[-3:] in ['txt', 'tsv', 'tab', '']:
        return '\t'

    return ','


# --------------------------------------------------
def test_guess_delimiter() -> None:
    """ Test guess_delimiter """

    assert guess_delimiter('/foo/bar.csv') == ','
    assert guess_delimiter('/foo/bar.txt') == '\t'
    assert guess_delimiter('/foo/bar.tsv') == '\t'
    assert guess_delimiter('/foo/bar.tab') == '\t'
    assert guess_delimiter('') == '\t'


# --------------------------------------------------
if __name__ == '__main__':
    main()
