#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-06
Purpose: Print reverse complement
"""

import argparse
import os
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    dna: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Print reverse complement',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dna',
                        metavar='DNA',
                        help='Enter a DNA sequence')


    args = parser.parse_args()
    
    if os.path.isfile(args.dna):
        args.dna = open(args.dna).read().rstrip()

    return Args(args.dna)

# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    
    print(get_revc(args.dna))
    
    
def get_revc(dna: str):
    
    reverse = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C",
        "a": "t",
        "t": "a",
        "c": "g",
        "g": "c",
    }
    
    revc = ""
    for i in range(len(dna)):
        base = dna[-(i+1)]
        if base in reverse:
            revc = revc + reverse[base]
        else:
            print("Enter a valid DNA sequence!")
            exit()
    
    return(revc)
    


# --------------------------------------------------
if __name__ == '__main__':
    main()
