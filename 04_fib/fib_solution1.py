#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-07
Purpose: Calculate Fibonacci
"""

import argparse
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    generations: int
    litter: int


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Calculate Fibonacci',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('generation',
                        metavar='GEN',
                        type=int,
                        help='Litter generation')

    parser.add_argument("litter",
                        type=int,
                        help='Size of the litter',
                        metavar='LIT')

    args = parser.parse_args()

    if not 1 <= args.generation <= 40:
        parser.error(f'generations "{args.generation}" must be between 1 and 40')

    if not 1 <= args.litter <= 5:
        parser.error(f'litter "{args.litter}" must be between 1 and 5')

    return Args(generations = args.generation, litter = args.litter)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    
    litter_size = 0
    previous_litter = 0
    temp = 0
    
    for i in range(args.generations):
        if i == 0:
            litter_size += 1
        else:
            temp = litter_size
            litter_size += (previous_litter*args.litter)
            previous_litter = temp
    
    print(litter_size)
            
    
    


# --------------------------------------------------
if __name__ == '__main__':
    main()
