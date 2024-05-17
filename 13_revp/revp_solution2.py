#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-15
Purpose: Locate restriction sites
"""

import argparse
from typing import NamedTuple, TextIO, List, Tuple
from Bio import SeqIO, Seq


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

    seq = ''
    seqs = SeqIO.parse(args.file, 'fasta')
    for fasta in seqs:
        seq = str(fasta.seq)

    for i, j in locate_palis(seq):
        print(i, j)


# --------------------------------------------------
def find_kmers(seq: str, k: int) -> List[int]:
    """ Create a list of all k-mers in a sequence """

    return [seq[i:i+k] for i in range(len(seq)-k+1)]


# --------------------------------------------------
def test_find_kmers() -> None:
    """ Test find_kmers """

    assert find_kmers('', 4) == []
    assert find_kmers('AACC', 3) == ['AAC', 'ACC']
    assert find_kmers('ACTG', 1) == ['A', 'C', 'T', 'G']
    assert find_kmers('ACTGCGTCA', 10) == []
    assert find_kmers('ACTGCGTCA', 4) == ['ACTG', 'CTGC', 'TGCG', 'GCGT', 'CGTC', 'GTCA']


# --------------------------------------------------
def find_palis(kmers: List[int]) -> List[int]:
    """ Find palindrome positions in a list of kmers """

    reverse = [Seq.reverse_complement(seq) for seq in kmers]
    return [i+1 for i in range(len(kmers)) if kmers[i] == reverse[i]]


# --------------------------------------------------
def test_find_palis() -> None:
    """ Test find_palis """

    assert find_palis(['AC']) == []
    assert find_palis(['ATAT']) == [1]
    assert find_palis(['ATAT', 'TCCA', 'CGCG', 'TAAC']) == [1, 3]


# --------------------------------------------------
def locate_palis(seq: str, low=4, high=12) -> List[Tuple[int, int]]:
    """ Takes a sequence and locates all palindromes"""

    pali_positions = []

    for k in range(low, high+1):
        if find_palis(find_kmers(seq, k)):
            for i in sorted(find_palis(find_kmers(seq, k))):
                pali_positions.append((i, k))

    return pali_positions


# --------------------------------------------------
def test_locate_palis() -> None:
    """ Test locate_palis """

    assert locate_palis('') == []
    assert locate_palis('ATATCAATATGACAGT') == [(4, 1), (4, 7)]


# --------------------------------------------------
if __name__ == '__main__':
    main()
