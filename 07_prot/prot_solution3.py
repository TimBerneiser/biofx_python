#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-11
Purpose: Translate mRNA to protein
"""

import argparse
import os
from typing import NamedTuple
from Bio import Seq


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

    print(Seq.translate(args.RNA, to_stop=True))


# --------------------------------------------------
if __name__ == '__main__':
    main()
