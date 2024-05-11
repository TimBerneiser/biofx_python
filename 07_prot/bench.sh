#!/usr/bin/env bash

# Benchmark all the solutions
hyperfine -m 1000 -L prg ./prot_solution1.py,./prot_solution2.py,\
./prot_solution2_map.py,./prot_solution3.py \
'{prg} AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA' \
--prepare 'rm -rf __pycache__'
