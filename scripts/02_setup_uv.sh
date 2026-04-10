#!/bin/bash
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --job-name=setup_uv
#SBATCH --output=logs/02_setup_uv_%j.log
#SBATCH --error=logs/02_setup_uv_%j.err

# ========================================
# Usage: sbatch scripts/02_setup_uv.sh
# Check status: squeue --me
# View output: cat logs/02_setup_uv_<job_id>.log
# View errors: cat logs/02_setup_uv_<job_id>.err
# ========================================

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "Start time: $(date)"
echo "========================================"
echo ""


# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env
else
    echo "uv already installed: $(uv --version)"
fi

# Install project dependencies from pyproject.toml
# TODO: Add Explanation what uv sync does and how it installs a .venv throughout all compute nodes in the cluster
echo "Installing dependencies..."
uv sync

# Verify that all imports work
echo ""
echo "Testing imports..."
uv run python scripts/02_setup_uv.py

echo ""
echo "Setup complete! You can now run the remaining scripts."


echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "========================================"
