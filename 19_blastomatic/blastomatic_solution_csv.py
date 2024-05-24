#!/usr/bin/env python3
""" Annotate BLAST output """

import argparse
import csv
from typing import NamedTuple, TextIO


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

    annots = {row['seq_id']: row for row in csv.DictReader(args.annotations, delimiter=",")}

    hits = csv.DictReader(args.hits, delimiter=',', fieldnames=[
                              'qseqid', 'sseqid', 'pident', 'length',
                              'mismatch', 'gapopen', 'qstart', 'qend',
                              'sstart', 'send', 'evalue', 'bitscore'
                          ])

    headers = ['qseqid', 'pident', 'depth', 'lat_lon']
    args.outfile.write(args.delimiter.join(headers) + '\n')
    file_counter = 0

    for hit in hits:
        if float(hit.get('pident', -1)) >= args.pctid:
            elements=[hit.get('qseqid'),
                      hit.get('pident'),
                      annots[hit.get('qseqid')]['depth'],
                      f'"{annots[hit.get('qseqid')]['lat_lon']}"']

            args.outfile.write(args.delimiter.join(elements) + '\n')

            file_counter+=1

    print(f'Exported {file_counter} to "{args.outfile.name}".')


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
