#!/bin/bash
#SBATCH --job-name=setup_uv
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --exclude=ga03 # Exclude ARM node (ga03)
#SBATCH --output=logs/02_setup_uv_%j.log
#SBATCH --error=logs/02_setup_uv_%j.err

# ========================================
# Usage: sbatch scripts/02_setup_uv.sh
# Check status: squeue --me
# View output: cat logs/02_setup_uv_<job_id>.log
# View errors: cat logs/02_setup_uv_<job_id>.err
# ========================================
#
# What is UV?
# -----------
# UV (https://docs.astral.sh/uv/) is a fast Python package manager by Astral.
# Think of it as a replacement for pip + virtualenv, but much faster.
#
# Key concepts:
#   - .python-version  Pins the Python version (e.g. 3.12). Without this, uv uses whatever
#                       Python is installed on the system, which may differ between machines.
#   - pyproject.toml   Lists the project's Python dependencies (like a requirements.txt).
#   - uv.lock          Locks exact versions for reproducibility (auto-generated).
#   - uv sync          Reads .python-version and pyproject.toml, creates a .venv/, and
#                       installs the pinned Python version + all dependencies.
#   - uv run <cmd>     Runs a command inside the .venv without activating it manually.
#                       e.g. "uv run python train.py" instead of "source .venv/bin/activate && python train.py"
#
# What happens if you run uv sync on the cluster?
# -----------
# Your home folder is shared across all nodes via a network filesystem.
# This means "uv sync" only needs to run once — the .venv/ it creates
# is immediately available on every compute node. No need to reinstall
# dependencies per node.
#

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "Start time: $(date)"
echo "========================================"
echo ""


# Install uv if not already installed (only has to be installed once per user, not per project)
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env
else
    echo "uv already installed: $(uv --version)"
fi

# Install project dependencies from pyproject.toml into .venv/
# See pyproject.toml for the list of packages (torch, torchvision, accelerate).
echo "Installing dependencies..."
uv sync

# Verify that all imports work (Cuda will not be available because we did not request a GPU for this job. We will do so in the next script, 03_gpu_basic.sh).
echo ""
echo "Testing imports..."
uv run python scripts/02_setup_uv.py


echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "Runtime: ${SECONDS}s"
echo "========================================"
