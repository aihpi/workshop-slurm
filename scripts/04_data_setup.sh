#!/bin/bash
#SBATCH --job-name=data_setup
#SBATCH --account=aisc
#SBATCH --partition=aisc-batch
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --constraint=ARCH:X86
#SBATCH --output=logs/04_data_%j.log
#SBATCH --error=logs/04_data_%j.err

# ========================================
# Usage: sbatch scripts/04_data_setup.sh
# Check status: squeue --me
# View output: cat logs/04_data_<job_id>.log
# View errors: cat logs/04_data_<job_id>.err
# ========================================
#
# This script downloads MNIST and CIFAR-100 to shared project storage.
# The comment block below covers the two storage tiers this workshop uses
# (home and project) and points at the docs for the scratch tiers you'll
# want once your jobs get larger.
#
#
# The two storage tiers we use in this workshop
# ---------------------------------------------
#   /sc/home/<user>/                 Your personal home directory.
#                                    Persistent. 200 GiB hard quota (enforced).
#                                    Use for: code, configs, trained models
#                                    small enough to keep long-term.
#
#   /sc/projects/<group>/<project>/  Shared project storage for your team.
#                                    Persistent. Soft ~10 TB target per project.
#                                    Use for: datasets and anything the team
#                                    shares. Create a project subfolder to stay
#                                    organized.
#
# Rule of thumb: code in /sc/home/, data in /sc/projects/<group>/<project>/.
#
#
# There's more: scratch space (not used in this workshop)
# -------------------------------------------------------
# For larger training jobs, the cluster also provides two scratch tiers —
# local per-node NVMe ($SLURM_SCRATCH) and a global parallel filesystem
# (/sc/scratch). They are faster than project storage and don't count against
# the ~10 TB project soft-target, but they are TEMPORARY: local scratch is
# deleted when the job ends, and global scratch may be wiped without warning.
#
# The recommended workflow is: copy your dataset into $SLURM_SCRATCH at the
# start of the job, write checkpoints and results there during training, and
# copy the results back to /sc/home/ before the job ends. See the docs:
#
#   Storage overview: https://docs.sc.hpi.de/cluster/Storage/Overview/
#   Quotas:           https://docs.sc.hpi.de/cluster/Storage/Quotas/
#   Scratch space:    https://docs.sc.hpi.de/cluster/Storage/Scratch-Space/
#   Data transfer:    https://docs.sc.hpi.de/cluster/Storage/Data-Transfer/
#
#
# Securing a shared folder
# ------------------------
# When you create a new folder under /sc/projects/, control access with:
#
#   mkdir /sc/projects/sci-aisc/my-project
#   chgrp <your-project-id> /sc/projects/sci-aisc/my-project
#   chmod 770 /sc/projects/sci-aisc/my-project
#
# The "770" means:
#   7 (owner) = read(4) + write(2) + execute(1)
#   7 (group) = read(4) + write(2) + execute(1)
#   0 (others) = no access
# Contact the cluster admins to get your project's group ID.
#
#
# Symlinks
# --------
# Instead of typing /sc/projects/sci-aisc/workshop-slurm/data in every script,
# create a symlink in your repo:
#
#   ln -s /sc/projects/sci-aisc/workshop-slurm/data ./data
#
# Now ./data points to shared storage. Scripts can reference "./data" as if
# it were local, keeping paths short and portable.
#
#
# Best practices
# --------------
# - Datasets: download once to /sc/projects/, everyone in your teamreads from there.
# - Coordinate with your team before deleting anything in /sc/projects/.
# - Be careful in /sc/projects/sci-aisc/ — it's shared with all other AISC users. Don't delete or overwrite anything you don't own.
# - `rm` is permanent — no recycle bin from the terminal.
# - Home quota is hard (200 GiB). Check usage with `du -hd 1 ~ | sort -hr`.

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
