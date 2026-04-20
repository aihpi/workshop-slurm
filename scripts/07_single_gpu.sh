#!/bin/bash
#SBATCH --job-name=cifar100_single
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:15:00
#SBATCH --mem=16G
#SBATCH --exclude=ga03 # Exclude ARM node (ga03)
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --output=logs/07_single_%j.log
#SBATCH --error=logs/07_single_%j.err

# ========================================
# Usage: sbatch scripts/07_single_gpu.sh
# Check status: squeue --me
# View output: cat logs/07_single_<job_id>.log
# View errors: cat logs/07_single_<job_id>.err
# ========================================

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "Start time: $(date)"
echo "========================================"
echo ""

uv run python scripts/07_single_gpu.py

echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "Runtime: ${SECONDS}s"
echo "========================================"
