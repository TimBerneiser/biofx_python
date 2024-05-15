#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-14
Purpose: Longest Common Substring
"""

import argparse
from typing import NamedTuple, TextIO
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Longest Common Substring',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='FASTA file',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    seqs = [str(fasta.seq) for fasta in SeqIO.parse(args.file, 'fasta')]
    highest = binary_search(len(min(seqs)), 0, seqs)

    if shared_motif([extract_kmer(seq, highest) for seq in seqs]):
        print(shared_motif([extract_kmer(seq, highest) for seq in seqs]))
    else:
        print('No common subsequence.')

# --------------------------------------------------
def extract_kmer(seq, k) -> list:
    """ Extracts all kmers from a sequence """

    return [seq[i:i+k] for i in range(len(seq)-k)]


# --------------------------------------------------
def shared_motif(motifs) -> str:
    """ Returns the shared motif of a list of lists """

    shared = False

    for i in range(len(motifs[0])-1):
        for j in range(len(motifs)):
            if motifs[0][i] in motifs[j]:
                shared = True
            else:
                shared = False
                break
        if shared:
            return motifs[0][i]

    return False


# --------------------------------------------------
def binary_search(high, low, seqs):
    """ Binary search for highest k-mer with shared motif """

    mid = int((high+low)//2)

    if high-mid <= 1:
        return mid

    if shared_motif([extract_kmer(seq, high) for seq in seqs]):
        return high

    if shared_motif([extract_kmer(seq, mid) for seq in seqs]):
        return binary_search(high, mid, seqs)

    return binary_search(mid, low, seqs)


# --------------------------------------------------
if __name__ == '__main__':
    main()
