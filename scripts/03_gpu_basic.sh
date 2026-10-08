#!/bin/bash
#SBATCH --job-name=gpu_basic
#SBATCH --account=aisc
#SBATCH --partition=pot-hpi-aisc-batch
#SBATCH --time=00:05:00
#SBATCH --mem=4G
#SBATCH --output=logs/03_gpu_basic_%j.log
#SBATCH --error=logs/03_gpu_basic_%j.err
#SBATCH --nodes=1
#SBATCH --gpus=h100:1 # One H100. The type keeps the job off the ARM L40 node (ga03) and the A30 node (gx17v1)

# ========================================
# Usage: sbatch scripts/03_gpu_basic.sh
# Check status: squeue --me
# View output: cat logs/03_gpu_basic_<job_id>.log
# View errors: cat logs/03_gpu_basic_<job_id>.err
# ========================================

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "Start time: $(date)"
echo "========================================"
echo ""


echo "=== GPU Allocation Check ==="
nvidia-smi

echo ""
echo "=== GPU check from Python ==="
uv run python scripts/03_gpu_basic.py


echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "Runtime: ${SECONDS}s"
echo "========================================"
