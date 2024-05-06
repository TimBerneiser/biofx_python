#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2023-11-25
Purpose: tetranucleotide frequency
"""

import argparse
import os
from typing import NamedTuple, Tuple


class Args(NamedTuple):
    """ Command-line arguments """
    dna: str

# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='tetranucleotide frequency',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dna',
                        metavar='DNA',
                        help='Input DNA sequence')

    args = parser.parse_args()
    
    if os.path.isfile(args.dna):
        args.dna = open(args.dna).read().rstrip()

    return Args(args.dna)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    
    counts = get_counts(args.dna)
    
    print("{} {} {} {}".format(*counts))
                
    
def get_counts(dna: str) -> Tuple[int, int, int, int]:
    
        
    return (dna.count("A"), dna.count("C"), dna.count("G"), dna.count("T"))


# --------------------------------------------------
if __name__ == '__main__':
    main()
