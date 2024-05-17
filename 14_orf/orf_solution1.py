#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-17
Purpose: Open Reading Frames
"""

import argparse
from typing import NamedTuple, TextIO, List
import re
from Bio import SeqIO, Seq


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Open Reading Frames',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FASTA',
                        type=argparse.FileType('rt'),
                        help='A FASTA file')

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    for rec in SeqIO.parse(args.file, 'fasta'):
        rna = str(rec.seq).replace('T', 'U')
        for start in find_start(rna):
            seq = rna[start:]
            if not re.findall(r'UAG|UAA|UGA', seq):
                break
            while (len(seq) % 3) != 0:
                seq += 'N'
            for i in range(0, len(seq), 3):
                if seq[i:i+3] in ('UAG', 'UAA', 'UGA'):
                    print(Seq.translate(seq, to_stop=True))
                    break

        rna = Seq.reverse_complement(rna).replace('T', 'U')
        for start in find_start(rna):
            seq = rna[start:]
            while (len(seq) % 3) != 0:
                seq += 'N'
            for i in range(0, len(seq), 3):
                if seq[i:i+3] in ('UAG', 'UAA', 'UGA'):
                    print(Seq.translate(seq, to_stop=True))
                    break


# --------------------------------------------------
def find_start(rna: str) -> List[int]:
    """ Find start codon locations with regex """

    return [(match.start()) for match in re.finditer('(?=(AUG))', rna)]


# --------------------------------------------------
def test_find_start() -> None:
    """ Test find_start """

    assert find_start('') == []
    assert find_start('AC') == []
    assert find_start('ACCCTTATACCATTAAUGTTCTAAUGATCCTA') == [15, 23]
    assert find_start('AUGAUGAUG') == [0, 3, 6]


# --------------------------------------------------
if __name__ == '__main__':
    main()
