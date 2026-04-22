#!/bin/bash
#SBATCH --job-name=data_setup
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --exclude=ga03 # Exclude ARM node (ga03)
#SBATCH --output=logs/04_data_%j.log
#SBATCH --error=logs/04_data_%j.err

# ========================================
# Usage: sbatch scripts/04_data_setup.sh
# Check status: squeue --me
# View output: cat logs/04_data_<job_id>.log
# View errors: cat logs/04_data_<job_id>.err
# ========================================
#
# Shared Project Storage vs. Home Directory
# ------------------------------------------
# On the cluster, you have two main storage locations:
#
#   /sc/home/<username>/          Your personal home directory.
#                                 Limited space (200 GB quota). Good for code, configs, small files.
#
#   /sc/projects/sci-aisc/        Shared project storage for your team.
#                                 Much more space. Use this for datasets, model checkpoints,
#                                 and anything large or shared across team members.
#                                 IMPORTANT: Create a subfolder for your project (e.g. /sc/projects/sci-aisc/my-project/) to keep things organized!
#
# Rule of thumb: code in /sc/home/, data in /sc/projects/sci-aisc/my-project/.
#
#
# Securing a Shared Folder
# ------------------------
# When you create a new folder in /sc/projects/sci-aisc/, other team members
# may need access. You can control permissions with:
#
#   mkdir /sc/projects/sci-aisc/my-project
#   chgrp <your-project-id> /sc/projects/sci-aisc/my-project   # Set group ownership to your team. IMPORTANT: You can ask for your project id by contacting the cluster admins.
#   chmod 770 /sc/projects/sci-aisc/my-project         # Owner + group: full access, others: none
#
# The "770" means:
#   7 (owner)  = read (4) + write (2) + execute (1)
#   7 (group)  = read (4) + write (2) + execute (1)
#   0 (others) = no access (0)
# (none - 0, execute - 1, write - 2, read - 4; add them up for combinations)
#
# Symlinks
# --------
# A symlink (symbolic link) is a shortcut that points to another location.
# Instead of using long paths like /sc/projects/sci-aisc/workshop-slurm/data
# in every script, you can create a symlink in your repo:
#
#   ln -s /sc/projects/sci-aisc/workshop-slurm/data ./data
#
# Now ./data points to the shared storage. Your code can use "./data" as if
# the data were local, but it actually lives in the shared project folder.
# This keeps your scripts clean and portable.
#
#
# Best Practices & Caution
# ------------------------
# - Be careful with shared data! Coordinate with your team before deleting!
# - Use symlinks to keep your code paths short and portable
# - Don't duplicate datasets — download once to shared storage, reference from there
#

echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Running on node: $(hostname)"
echo "Start time: $(date)"
echo "========================================"
echo ""

DATA_DIR="/sc/projects/sci-aisc/workshop-slurm/data"

# Create the shared data directory if it doesn't exist
mkdir -p "$DATA_DIR"

echo "Downloading datasets to shared storage: $DATA_DIR"
echo ""
uv run python scripts/04_data_setup.py

# Create a symlink from ./data to the shared storage location
# This lets scripts reference "./data" while the actual data lives in shared storage.
if [ ! -L "./data" ]; then
    ln -s "$DATA_DIR" ./data
    echo ""
    echo "Created symlink: ./data -> $DATA_DIR"
else
    echo ""
    echo "Symlink already exists: ./data -> $(readlink ./data)"
fi

echo ""
echo "========================================"
echo "Job finished!"
echo "End time: $(date)"
echo "Runtime: ${SECONDS}s"
echo "========================================"
