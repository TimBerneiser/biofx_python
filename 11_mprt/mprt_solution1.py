#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-15
Purpose: Find locations of N-glycosylation motif
"""

import argparse
from typing import NamedTuple, TextIO, List
import os
import sys
import requests
import re
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO
    download_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Find locations of N-glycosylation motif',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Input text file of UniProt IDs')

    parser.add_argument('-d',
                        '--download_dir',
                        metavar='DIR',
                        type=str,
                        help='Download directory',
                        default='fasta')

    args = parser.parse_args()

    return Args(args.file, args.download_dir)

# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    motif = re.compile('(?=(N[^P][ST][^P]))')

    ids = [prot_id for prot_id in map(str.rstrip, args.file)]
    files = download_prot(ids, args.download_dir)
    for file in files:
        prot_id, _ = os.path.splitext(os.path.basename(file))
        recs = SeqIO.parse(file, 'fasta')
        if rec := next(recs):
            if matches := list(motif.finditer(str(rec.seq))):
                print(prot_id)
                print(*[match.start() + 1 for match in matches])


# --------------------------------------------------
def download_prot(ids, dir) -> List:
    """ Download protein sequences from uniprot ID """

    if not os.path.isdir(dir):
        os.makedirs(dir)

    files = []
    for id in ids:
        fasta = os.path.join(dir, id + '.fasta')
        if not os.path.isfile(fasta):
            url = f'https://www.uniprot.org/uniprotkb/{id}.fasta'
            response = requests.get(url)
            if response.status_code == 200:
                print(response.text, file=open(fasta, 'wt'))
            else:
                print(f'Error fetching "{url}": "{response.status_code}"',
                      file=sys.stderr)
                continue
        files.append(fasta)

    return files


# --------------------------------------------------
if __name__ == '__main__':
    main()
