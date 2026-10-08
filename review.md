# Review of the SLURM workshop

Review date 2026-10-07. The material reviewed was the deck (`slides/workshop-slurm.pdf`, 35 slides, read as text extracted from the PDF), `README.md` and `scripts/01` to `08`. The reviewers assumed a mixed group of new AISC cluster users: ML researchers fluent in Python, and beginners who are also new to the terminal, SSH and Linux. The slot was assumed to be 180 min. Because the text was extracted from the PDF, speaker notes are missing, and slides 6, 14, 18 and 20 (image only) could not be checked.

The one-line verdict: the workshop fits the slot. The batch-script part probably fails on a fresh clone, and the access part stalls for anyone without an account.

## Audience findings

### Where each learner stops following

| Learner | Stops at | Why |
|---|---|---|
| Beginner | README §1 step 1 | Without an approved proposal, a VPN zip and a working terminal, there is nothing to do for 20 min. |
| Beginner | Slide 13 | Partition, account ("billing code" for a free service) and QOS arrive in one step. |
| Researcher | Slides 2 to 5 | German marketing slides in an English workshop. |
| Researcher | Slides 22 to 24, 28 | CPU vs GPU basics they already know; Kubernetes/ArgoCD is off topic. |
| Both | First `sbatch` | No log appears (see runtime failures), and `scancel`, `sacct` and job states were never taught. |

### Missing ideas

The `#SBATCH` header lines (`--account`, `--partition`, `--time`, `--mem`, `--constraint`, `--output`, `%j`) are never explained on a slide, yet script 01 uses all of them. Slides 14 and 34 carry no text. `squeue --me` appears only in script comments; `scancel`, `sacct` and `sinfo` appear nowhere, although slide 17 asks learners to release resources. Nobody says where to run `sbatch` (lx01 or the VSCode terminal on rx01), or that it must run from the repo root because the scripts use relative paths.

### Steps with two or more new thoughts

| Step | New thoughts at once |
|---|---|
| Slide 13 | partition, account, QOS |
| Slide 15 | srun, salloc, sblock, sbatch, two interactive modes, no example |
| README §4 tool | SSH keys, local install, VSCode config, `remote` commands, GPU types; no link back to slide 15 |
| Slide 27 | parameters to bytes, fp16, activations and gradients |
| Script 01 | the whole `#SBATCH` grammar, stdout vs stderr, `%j` |
| Script 04 | four storage tiers, Unix permissions, chgrp, symlinks |
| Script 08 | multi-process launch, Accelerate wrapping, gradient sync |

### Steps that add nothing in the text

Slides 6, 14, 16, 18, 20, 21 and 34 are empty or repeat the previous slide in the text outline; they may carry images or speaker notes. README §3 repeats the comment block of script 04.

### Links

The tele-task.de link on slide 3 fails with a TLS error. open.hpi.de could not be fetched and needs a manual check. On slide 4, "Jetzt bewerben!" points to `github.com/aihpi/leichte-sprache`, which is a code repository and not an application page. aimaker.community now redirects to Eventbrite. The README's SSH guide text says the key steps are "outlined to the left", but they are on a subpage. The README says "especially SBatch files" for the Job-Examples anchor, which shows only srun one-liners. The bmbf.de link redirects to bmftr.bund.de. All other links resolve and say what the material claims.

## Presenter findings

### Timing

| Part | Planned (README) | Estimated |
|---|---|---|
| S1.1 Intro slides 1 to 9 | 10 | 12.5 |
| S1.2 Cluster access | 20 | 26 |
| S1.3 SLURM slides 10 to 17 | 10 | 12 |
| S1.4 VSCode | 5 | 6.5 |
| Break | not given | 15 |
| S2.1 Interactive SLURM | 10 to 20 | 19.5 |
| S2.2 CPU/GPU slides 21 to 32 | 10 to 20 | 19.5 |
| S2.3 Clone | 5 | 6.5 |
| S2.4 Batch scripts | 20 | 26 |
| S2.5 Feedback | 5 | 5 |
| Total | about 120 | 149 (83 % of 180) |

A second break, which a 180 min slot needs, brings the total to 164 min (91 %). The README promises "2 to 3 hours", but its own table adds up to about two hours. Two risks fall outside the heuristic. S1.2 cannot finish in 20 min if accounts or VPN are not ready. In S2.4 each participant requests 11 GPU allocations; with 20 participants that is about 220 allocations against 56 H100s, so queue waits inside the 20 min are likely.

### Structure

S1.3 and S2.2 start with theory. Learners meet `sbatch` on slide 15 and first use it about 90 min later. There is no expectation check, no quiz or poll, no recap before the feedback slide, and no stated learning goals. The "Part II" divider (slide 21) comes after the first Part II component (slide 20). Three bridges are missing: from slide 20 to 21, from 32 to 33, and from the last script to the feedback slide. Slide 15 is never connected to the `remote h100` tool.

### Runtime failures, checked against the material

| # | Problem | Verdict | Fix |
|---|---|---|---|
| R1 | `logs/` is gitignored and absent. | refuted by test on 2026-10-07 | None. SLURM on this cluster creates the missing output directory itself (tested with and without `mkdir`). |
| R2 | 02 sources `~/.local/bin/env` only inside its own job. Later jobs inherit the submitting shell's PATH, so 03 to 08 can fail with `uv: command not found`. | likely | Tell learners to run `source ~/.local/bin/env` or log in again after 02. |
| R3 | 02 has `--time=00:10:00` to download torch cu128 and the NVIDIA wheels (several GB) for every participant at the same time. | risk | Raise the limit to 30 min; say a resubmit resumes from the uv cache. |
| R4 | Everyone runs 04 against the same `/sc/projects/sci-aisc/workshop-slurm/data`. Two first runs can race; directory permissions follow the first creator's umask; write access is not stated. The `./data` symlink is never used by 05 to 08. | confirmed | Presenter pre-populates the data or runs 04 once as a demo. |
| R5 | 01 ends in state COMPLETED despite the traceback, because the last command is `echo` and there is no `set -e`. | confirmed | Explain it as a teaching moment with `sacct`, or exit with the Python status. |
| R6 | 08 gives 8 CPUs to 4 GPUs with `num_workers=2` each, which is 2 CPUs per GPU. Slide 25 says 4 to 8. `Resize(224)` runs on the CPU, so the speedup shown is too small. | confirmed | `--cpus-per-task=16` or more. |
| R7 | 07 vs 08 is not like for like. `BATCH_SIZE=128` is per process (global 512), with the same learning rate and a quarter of the optimizer steps. 08 reports accuracy on the main process's shard only. | confirmed | Compare time per epoch only and say so, or scale batch and LR; gather metrics with `accelerator.gather_for_metrics`. |

### Inconsistencies

| Topic | One source | Other source |
|---|---|---|
| GPU flag | slide 25 `--gres=gpu` | scripts `--gpus=N` |
| Where to test | slides 13 and 32: shortrun or interactive first | all scripts, even the 1 min hello world, use aisc-batch |
| H100 in aisc-batch | slide 31: aisc-batch runs on H100s | 03 excludes ARM and A30 nodes; 05 to 08 use only `ARCH:X86`, which keeps the A30 node |
| Partition names | slides and scripts `aisc-*` | docs Partitions page `pot-hpi-aisc-*` |
| Interactive GPU | slide 31: interactive runs on A30 | README §4 `remote h100` |
| sblock | slide 15 lists it | docs say it is deprecated |
| Node names | slide 11 `gx15v01` | script 03 `gx17v1` |
| Multi-GPU count | README and 08: 4 GPUs | slide 29: 8 GPUs |
| SSH key | README: optional | docs: needed for compute nodes; the interactive tool generates one |
| Storage path | README `/sc/projects/sci-aisc/<project>/` | 04 comment and docs `/sc/projects/<group>/<project>/` |
| Agenda | README: "VSCode Installation" | no step installs VSCode |
| CHANGELOG | "`--exclude=ga03` added to all scripts" | scripts use `--constraint=ARCH:X86` instead |

Smaller leftovers: slide 19 footer reads "Fußzeile" and "19.03.2024"; slide 8 says "consolidate our FAQ" instead of "consult"; README §5 FAQ is an empty table with "ToDo"; slides 2 to 5 and 35 are German.

## Questions and answers

| # | Learner question | Answer from the material | Source |
|---|---|---|---|
| 1 | Do I need an account, the VPN zip and a working SSH login before the workshop? What do I do without one? | The steps are listed, but nothing says to do them beforehand, and there is no fallback. | no answer |
| 2 | Must I create `logs/` before the first sbatch? | No. SLURM creates it (tested on 2026-10-07). | outside knowledge |
| 3 | Do I need a new shell after 02 for `uv`? | Yes, or `source ~/.local/bin/env`. | outside knowledge |
| 4 | Where do I type `sbatch`? | Slide 11: login nodes are for submitting, from the repo root. Whether rx01 works is not stated. | partly in material |
| 5 | How do I see a job's state and cancel it? | `squeue --me` is in script comments. `sacct` and `scancel` are missing. | outside knowledge |
| 6 | Can all of us write to the shared data dir, and run 04 at once? | Write access is not stated. Sequential reruns are safe; parallel first runs are not. | no answer |
| 7 | Which GPU do 05 to 08 get, and what is the partition called? | `aisc-batch` in all scripts. The material contradicts itself on the hardware. | contradictory |
| 8 | What replaces sblock, and how does `remote h100` relate to slide 15? | Not answered. | no answer |
| 9 | `--gres` or `--gpus`, and how many CPUs per GPU? | Slide 25: 4 to 8 per GPU. Both flags work. Do not copy 08. | outside knowledge |
| 10 | Is my username firstname.lastname, and is an SSH key optional? | The username is in the zip. Key need for compute nodes is unclear. | partly in material |

## Gaps to close in the main path

These answers needed outside knowledge or had none, so they belong in the slides, README or scripts.

1. Fix R2 (`uv` on PATH). R1 was refuted by a test run.
2. Send prerequisites before the day: approved account, VPN working, `ssh` login tested, VSCode with Remote-SSH, local git. Give a fallback for anyone without access (pair with a neighbor).
3. Add one slide that explains the `#SBATCH` header of script 01, line by line, right before the first submit.
4. Add `squeue --me`, `sacct -j <id>`, `scancel <id>` and how to read job states (PENDING, RUNNING, COMPLETED, FAILED, TIMEOUT). Show them on 01, using R5 as the hook.
5. Say where to submit from (login node, repo root).
6. Decide who runs 04 (R4) and say so.
7. Resolve the hardware contradictions: which partition, which GPUs, sblock, `--gres` vs `--gpus`, `remote h100` vs "interactive = A30".
8. Fix 08 (R6, R7) so the multi-GPU comparison shows what the README promises.

## Move to FAQ or appendix

These items are already in the material but cost main-path time, or can be looked up later.

| Item | Destination | Reason |
|---|---|---|
| Slides 2 to 4 (KISZ education and consulting) | appendix or 1 slide | Not needed to use the cluster; German in an English slot. |
| Slide 28 Kubernetes/ArgoCD line | drop | Not used today. |
| Slide 30 model parallelism | appendix | Not practised; "start with one GPU" fits on slide 29. |
| Script 04 comment on chmod, chgrp, scratch | README FAQ | Four topics in one step; only "data in project, code in home" is needed today. |
| README §3 storage table | keep, remove repeat from 04 | One place for the storage tiers. |
| README §1 step 6 "familiarise yourself" | README FAQ or references | Homework inside a hands-on slot. |
| README §5 FAQ | fill with R1 to R7 and questions 1 to 10 | Currently empty. |

## Plan skeleton

`plan.md` next to this file holds the meta plan skeleton with the confirmed component split, interface blocks and open `TBD` fields.

## Status log

- 2026-10-07 component split confirmed by Felix (10 components)
- 2026-10-07 audience, whole workshop, no check type, complete
- 2026-10-07 presenter, whole workshop, full, complete
