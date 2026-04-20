# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/).

## [Unreleased]

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
