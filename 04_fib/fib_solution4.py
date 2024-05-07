#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-07
Purpose: Calculate Fibonacci
"""

import argparse
from typing import NamedTuple, Generator


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
    gen = fib(args.litter)
    seq = [next(gen) for _ in range(args.generations + 1)]
    print(seq[-1])


# --------------------------------------------------
def fib(k: int) -> Generator[int, None, None]:
    """ Generator function for the Fibonacci sequence """
    x, y = 0, 1
    
    yield x

    while True:
        yield y
        x, y = y*k, x+y



# --------------------------------------------------
if __name__ == '__main__':
    main()
