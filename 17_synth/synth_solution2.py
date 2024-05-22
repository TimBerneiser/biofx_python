#!/usr/bin/env python3
"""
Author : tim <tim@localhost>
Date   : 2024-05-22
Purpose: Create synthetic DNA with Markov chain
"""

import argparse
from typing import NamedTuple, TextIO, List, Optional, Dict
import random
import io
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    outfile: TextIO
    fformat: str
    number: int
    max_len: int
    min_len: int
    kmer: int
    seed: Optional[int]


WeightedChoices = Dict[str, float]
Weights = Dict[str, WeightedChoices]


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Create synthetic DNA with Markov chain',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        nargs='+',
                        type=argparse.FileType('rt'),
                        help='Training file(s)')

    parser.add_argument('-o',
                        '--outfile',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='out.fa',
                        help='Output filename')

    parser.add_argument('-f',
                        '--format',
                        metavar='format',
                        type=str,
                        choices=['fasta', 'fastq'],
                        default='fasta',
                        help='Input file format')

    parser.add_argument('-n',
                        '--number',
                        metavar='number',
                        type=int,
                        default=100,
                        help='Number of sequences generated')

    parser.add_argument('-m',
                        '--min_len',
                        metavar='min',
                        type=int,
                        default=50,
                        help='Minimum sequence length')

    parser.add_argument('-x',
                        '--max_len',
                        metavar='max',
                        type=int,
                        default=75,
                        help='Maximum sequence length')

    parser.add_argument('-k',
                        '--kmer',
                        metavar='kmer',
                        type=int,
                        default=10,
                        help='Size of kmer for Markov')

    parser.add_argument('-s',
                        '--seed',
                        metavar='seed',
                        type=int,
                        default=None,
                        help='Random seed value')

    args = parser.parse_args()

    return Args(files=args.file, outfile=args.outfile,
                fformat=args.format, number=args.number,
                max_len=args.max_len, min_len=args.min_len,
                kmer=args.kmer, seed=args.seed)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    random.seed(args.seed)
    weights = read_training(args.files, args.fformat, args.kmer)

    out_file = open(args.outfile.name, 'wt')
    i = 1
    while i < args.number+1:
        if seq := gen_seq(weights, args.kmer, args.min_len, args.max_len):
            out_file.write(f'>{i}\n{seq}\n')
            i +=1


# --------------------------------------------------
def read_training(files: List[TextIO], fformat: str, k) -> Weights:
    """Calculate Markov chains """

    markov = {}
    kmers = []

    for fh in files:
        for rec in SeqIO.parse(fh, fformat):
            kmers.extend(find_kmers(str(rec.seq), k))
    chains = {}

    for kmer in kmers:
        if kmer[:-1] not in chains:
            chains[kmer[:-1]] = {}

        if kmer[-1] not in chains[kmer[:-1]]:
            chains[kmer[:-1]][kmer[-1]] = 0

        chains[kmer[:-1]][kmer[-1]] +=1

    for key in chains:
        weights = {}
        for base in chains[key]:
            weights[base] = chains[key][base]/sum(chains[key].values())
        markov[key] = weights

    return markov


# --------------------------------------------------
def test_read_training() -> None:
    """ Test calc_markov """


    f1 = io.StringIO('>1\nACGTACGC\n')
    assert read_training([f1], 'fasta', 4) == {
        'ACG': {'T': 0.5, 'C': 0.5},
        'CGT': {'A': 1.0 },
        'GTA': {'C': 1.0 },
        'TAC': {'G': 1.0}
    }

    f2 = io.StringIO('@1\nACGTACGC\n+\n!!!!!!!!')
    assert read_training([f2], 'fastq', 5) == {
        'ACGT': { 'A': 1.0 }, 
        'CGTA': { 'C': 1.0 },
        'GTAC': { 'G': 1.0 },
        'TACG': { 'C': 1.0 }
    }


# --------------------------------------------------
def gen_seq(weighting: Weights, k: int, min_len: int, max_len: int) -> Optional[str]:
    """ Generate a sequence """

    seq = random.choice(list(weighting.keys()))
    seq_len = random.randint(min_len, max_len)

    while len(seq) < seq_len:
        if seq[-k+1:] not in weighting.keys():
            break
        pop = list(weighting[seq[-k+1:]].keys())
        chance = list(weighting[seq[-k+1:]].values())
        seq += random.choices(population=pop, weights=chance, k=1)[0]

    return seq if len(seq) >= min_len else None


# --------------------------------------------------
def test_gen_seq() -> None:
    """ Test gen_seq """


# --------------------------------------------------
def find_kmers(seq: str, k: int) -> List[str]:
    """ Create a list of all k-mers in a sequence """

    return [seq[i:i+k] for i in range(len(seq)-k+1)]


# --------------------------------------------------
def test_find_kmers() -> None:
    """ Test find_kmers """

    assert find_kmers('', 4) == []
    assert find_kmers('AACC', 3) == ['AAC', 'ACC']
    assert find_kmers('ACTG', 1) == ['A', 'C', 'T', 'G']
    assert find_kmers('ACTGCGTCA', 10) == []
    assert find_kmers('ACTGCGTCA', 4) == ['ACTG', 'CTGC', 'TGCG', 'GCGT', 'CGTC', 'GTCA']


# --------------------------------------------------
if __name__ == '__main__':
    main()
