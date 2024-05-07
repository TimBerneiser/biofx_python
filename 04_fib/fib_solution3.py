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

    print(fib(args.generations, args.litter))



# --------------------------------------------------
def fib(gen: int, lit: int) -> int:
    """ Calculates the fibonacci sequence and returns the last value """

    litter = [1, 1]
    generations = gen - 2

    for _ in range(generations):
        litter.append(litter[-1] + litter[-2]*lit)

    return litter[gen-1]


# --------------------------------------------------
if __name__ == '__main__':
    main()
