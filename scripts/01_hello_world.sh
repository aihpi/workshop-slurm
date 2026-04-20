#!/bin/bash
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:01:00
#SBATCH --mem=1G
#SBATCH --job-name=hello_world
#SBATCH --output=logs/01_hello_%j.log
#SBATCH --error=logs/01_hello_%j.err

# ========================================
# Usage: sbatch scripts/01_hello_world.sh
# Check status: squeue --me
# View output: cat logs/01_hello_<job_id>.log
# View errors: cat logs/01_hello_<job_id>.err
# ========================================

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "Start time: $(date)"
echo "========================================"
echo ""


# create logs directory if it doesn't exist
mkdir -p logs

# Run the simple Python script that prints "Hello, World!" and produces an error to demonstrate logging
python scripts/01_hello_world.py


echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "Runtime: ${SECONDS}s"
echo "========================================"