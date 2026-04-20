#!/bin/bash
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:15:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8
#SBATCH --gpus=4
#SBATCH --job-name=cifar100_multi
#SBATCH --output=logs/07_multi_%j.log
#SBATCH --error=logs/07_multi_%j.err

# ========================================
# Usage: sbatch scripts/07_multi_gpu.sh
# Check status: squeue --me
# View output: cat logs/07_multi_<job_id>.log
# View errors: cat logs/07_multi_<job_id>.err
# ========================================

# Note: We use "accelerate launch" instead of "python" to distribute
# the training across all allocated GPUs automatically.

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "GPUs allocated: $SLURM_GPUS"
echo "Start time: $(date)"
echo "========================================"
echo ""

uv run accelerate launch --num_processes=4 scripts/07_multi_gpu.py

echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "Runtime: ${SECONDS}s"
echo "========================================"
