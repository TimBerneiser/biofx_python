#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-15
Purpose: Locate restriction sites
"""

import argparse
from typing import NamedTuple, TextIO
from Bio import SeqIO, Seq
import re


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO

# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Locate restriction sites',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        help='Input FASTA file',
                        type=argparse.FileType('rt'))

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    seq, id =  '', ''
    seqs = SeqIO.parse(args.file, 'fasta')
    for fasta in seqs:
        seq, id = str(fasta.seq), fasta.id
    palindromes = list()

    for i in range(4, 13, 1):
        if pali_kmers(seq,i):
            for palindrome in pali_kmers(seq,i):
                palindromes.extend([(match.start()+1, i) for match in re.finditer(f'(?=({palindrome}))', seq)])

    for i, j in sorted(set(palindromes), key=lambda tup: (tup[1], tup[0])):
        print(i, j)


# --------------------------------------------------
def pali_kmers(seq: str, k: int):
    """ Create a list of all palindromic kmers in a sequence """

    return [seq[i:i+k] for i in range(len(seq)-k) if seq[i:i+k]==Seq.reverse_complement(seq[i:i+k])]


# --------------------------------------------------
if __name__ == '__main__':
    main()
