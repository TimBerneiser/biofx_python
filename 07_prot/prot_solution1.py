#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-11
Purpose: Translate mRNA to protein
"""

import argparse
import os
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    RNA: str

# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Translate mRNA to protein',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('RNA',
                        help='Enter mRNA sequence or sequence file',
                        metavar='SEQ')


    args = parser.parse_args()

    if os.path.isfile(args.RNA):
        args.RNA = open(args.RNA.read().rstrip())

    return Args(args.RNA)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    print(translate(args.RNA, stop=True))


# --------------------------------------------------
def translate(RNA, stop=False) -> str:
    """ Translates an RNA sequence into an aa sequence """

    codons = {
        "UUU" : "F", "CUU" : "L", "AUU" : "I", "GUU" : "V",
        "UUC" : "F", "CUC" : "L", "AUC" : "I", "GUC" : "V",
        "UUA" : "L", "CUA" : "L", "AUA" : "I", "GUA" : "V",
        "UUG" : "L", "CUG" : "L", "AUG" : "M", "GUG" : "V",
        "UCU" : "S", "CCU" : "P", "ACU" : "T", "GCU" : "A",
        "UCC" : "S", "CCC" : "P", "ACC" : "T", "GCC" : "A",
        "UCA" : "S", "CCA" : "P", "ACA" : "T", "GCA" : "A",
        "UCG" : "S", "CCG" : "P", "ACG" : "T", "GCG" : "A",
        "UAU" : "Y", "CAU" : "H", "AAU" : "N", "GAU" : "D",
        "UAC" : "Y", "CAC" : "H", "AAC" : "N", "GAC" : "D",
        "UAA" : "*", "CAA" : "Q", "AAA" : "K", "GAA" : "E",
        "UAG" : "*", "CAG" : "Q", "AAG" : "K", "GAG" : "E",
        "UGU" : "C", "CGU" : "R", "AGU" : "S", "GGU" : "G",
        "UGC" : "C", "CGC" : "R", "AGC" : "S", "GGC" : "G",
        "UGA" : "*", "CGA" : "R", "AGA" : "R", "GGA" : "G",
        "UGG" : "W", "CGG" : "R", "AGG" : "R", "GGG" : "G"
    }
    aa_seq = ''

    for i in range(0, len(RNA), 3):
        aa_seq += codons.get(RNA[i:i+3])
        if stop==True and aa_seq[-1]=='*':
            aa_seq = aa_seq[:-1]
            break

    return aa_seq


# --------------------------------------------------
def test_translate() -> None:
    """ Tests Translate """

    assert(translate('AAC')) == 'N'
    assert(translate('ACCUGACGG')) == 'T*R'
    assert(translate('ACCUGACGG', stop=True)) == 'T'


# --------------------------------------------------
if __name__ == '__main__':
    main()
