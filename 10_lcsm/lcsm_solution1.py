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
    shared = False

    for i in range(len(min(seqs)), -1, -1):
        i +=1
        motifs = [extract_kmer(seq,i) for seq in seqs]
        if shared_motif(motifs):
            shared = True
            print(shared_motif(motifs))
            break

    if not shared:
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
if __name__ == '__main__':
    main()
