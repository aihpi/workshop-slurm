#!/bin/bash
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:01:00 # 1 minute
#SBATCH --mem=1G

python 01_minimal.py
