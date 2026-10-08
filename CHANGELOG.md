# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/).

## [Unreleased]

### Added
- Interactive SLURM workflow documentation in README with install/usage instructions for [tool-interactive-slurm](https://github.com/aihpi/tool-interactive-slurm)
- `--constraint=ARCH:X86` to the CPU scripts `01`, `02`, `04` (avoid the ARM node, which is incompatible with the uv binary)
- Typed GPU request `--gpus=h100:N` in the GPU scripts `03` and `05`-`08` (only H100 nodes, not the ARM L40 node or the A30 node)
- `--nodes=1` in the GPU scripts `03` and `05`-`08` (the cluster warns on every GPU job without `--nodes`)
- `04_data_setup` skips the download when the datasets already exist in shared project storage
- `02_setup_uv` tells the user to run `source ~/.local/bin/env` before submitting `03`
- `example_logs/` with the logs of a complete run of all scripts from a fresh account

### Changed
- Reworked workshop structure table with updated time slots and topics
- Moved `--job-name` to top of SBATCH directives for consistency across all scripts
- Partition `aisc-batch` renamed to `pot-hpi-aisc-batch` in all scripts and the README (the old names no longer exist)
- `02_setup_uv` time limit raised from 10 to 30 min (a first install took 6 min for one user)
- `08_multi_gpu` requests 16 CPUs (4 per GPU, as in `07`) instead of 8
- Slides use the partition names `pot-hpi-aisc-*` (slides 13, 31, 32), the current compute node names (slides 11, 31) and `--gpus` instead of `--gres=gpu` (slide 25), as the scripts do
- `slides/workshop-slurm.pdf` and `.pptx` re-exported from the Keynote file, so all three formats match

### Fixed
- Changed `data/` to `data` in `.gitignore` to also match the symlink
- `08_multi_gpu` computes the test accuracy over all GPUs with `accelerator.gather_for_metrics()` instead of only the main GPU's share
- Slide 8 says "consult our FAQ" instead of "consolidate"; the template footer on the break slide (19) is removed

## [0.3.0] - 2026-04-20

### Added
- New `04_data_setup` script: downloads MNIST and CIFAR-100 to shared project storage, documents shared vs home storage, permissions, symlinks, and best practices
- `.python-version` file to pin Python 3.12
- UV documentation in `02_setup_uv.sh` (key concepts, cluster behavior)
- Inline change markers (`← NEW` / `← CHANGED`) in `08_multi_gpu.py` to highlight differences from single-GPU version
- Runtime tracking (`${SECONDS}s`) in all shell scripts
- Scripts overview table in README
- FAQ & Troubleshooting section in README
- `.DS_Store` and `.claude` to `.gitignore`

### Changed
- Renumbered scripts: inserted `04_data_setup`, shifted training (04→05), array jobs (05→06), single GPU (06→07), multi GPU (07→08)
- All training scripts now use shared project storage (`/sc/projects/sci-aisc/workshop-slurm/data`) with `download=False`
- Updated README workshop structure table to reflect new script numbering (01-08)
- Improved `02_setup_uv.sh` documentation and resolved TODO about `.venv` distribution

### Fixed
- Typo in README: "blue bottom" → "blue button"
- Removed `.DS_Store` from git tracking

## [0.2.0] - 2026-04-17

### Added
- Part 2 slides
- CIFAR-100 single/multi-GPU training scripts (06)
- Progressive sbatch workshop scripts (01-05)

## [0.1.0] - 2026-04-14

### Added
- Initial repository structure with README, scripts, and naming schema
- Getting started guide with cluster access and SSH setup
- UV setup and Python environment configuration
