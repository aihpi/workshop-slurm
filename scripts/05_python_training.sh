#!/bin/bash
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:10:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --job-name=mnist_training
#SBATCH --output=logs/05_mnist_%j.log
#SBATCH --error=logs/05_mnist_%j.err

# ========================================
# Usage: sbatch scripts/05_python_training.sh
# Check status: squeue --me
# View output: cat logs/05_mnist_<job_id>.log
# View errors: cat logs/05_mnist_<job_id>.err
# ========================================

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "Start time: $(date)"
echo "========================================"
echo ""


echo "=== Starting training ==="
uv run python scripts/05_python_training.py


echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "Runtime: ${SECONDS}s"
echo "========================================"
