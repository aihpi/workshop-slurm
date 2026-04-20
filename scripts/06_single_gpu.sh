#!/bin/bash
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:15:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --job-name=cifar100_single
#SBATCH --output=logs/06_single_%j.log
#SBATCH --error=logs/06_single_%j.err

# ========================================
# Usage: sbatch scripts/06_single_gpu.sh
# Check status: squeue --me
# View output: cat logs/06_single_<job_id>.log
# View errors: cat logs/06_single_<job_id>.err
# ========================================

# Note: We store the dataset in the shared project storage, not in your home folder.
# Home folders have limited space — large datasets should go to /sc/projects/sci-aisc/.

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "Start time: $(date)"
echo "========================================"
echo ""

uv run python scripts/06_single_gpu.py

echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "Runtime: ${SECONDS}s"
echo "========================================"
