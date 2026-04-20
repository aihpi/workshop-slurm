#!/bin/bash
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:10:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --job-name=mnist_sweep
#SBATCH --output=logs/06_sweep_%A_%a.log
#SBATCH --error=logs/06_sweep_%A_%a.err
#SBATCH --array=0-3

# ========================================
# Usage: sbatch scripts/06_array_jobs.sh
# Check status: squeue --me
# View output: cat logs/06_sweep_<array_job_id>_<task_id>.log
# View errors: cat logs/06_sweep_<array_job_id>_<task_id>.err
# ========================================

# --array=0-3 launches 4 jobs with SLURM_ARRAY_TASK_ID = 0, 1, 2, 3
# In the output filenames: %A = array job ID, %a = array task ID

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "Start time: $(date)"
echo "========================================"
echo ""


echo "Array Job ID: $SLURM_ARRAY_JOB_ID"
echo "Array Task ID: $SLURM_ARRAY_TASK_ID"

uv run python scripts/06_array_jobs.py --task-id $SLURM_ARRAY_TASK_ID


echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "Runtime: ${SECONDS}s"
echo "========================================"
