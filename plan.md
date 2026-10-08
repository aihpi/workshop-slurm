# How to use our HPC cluster

## 1. Header

- Level: workshop
- Format(s): workshop
- Language: en-US (TBD: slides 2 to 5 and 35 are German; translate or keep?)
- Slot: 180 min assumed (TBD: README says "2 to 3 hours"; confirm)
- Setting: TBD (room or online, group size, own laptops)
- Notebook flavour: none
- Template: TBD (current deck is Keynote, `slides/workshop-slurm.key`)
- Quiz: none
- Inspiration: none
- Status log:
  - 2026-10-07 review mode; component split confirmed by Felix
  - 2026-10-07 audience, whole workshop, complete (see review.md)
  - 2026-10-07 presenter, whole workshop, full, complete (see review.md)
  - 2026-10-07 refine round 1: learner clarified (approved proposal only, not researchers); CPU vs GPU slides stay; partitions renamed to pot-hpi-aisc-* in scripts and README; script 04 skips the download when shared data exists; all participants are in the aisc-storage group, so they can read the shared data

## 2. Learner

New AISC cluster users whose proposal has been approved, so each participant has an account and the VPN zip before the day. They are not ML researchers, who usually know SLURM already. Most can write some Python; many are new to the terminal, SSH, Linux and SLURM. They like to rehearse the CPU vs GPU basics, so slides 22 to 24 stay in the main path.

- Segment: TBD
- Profile: AI Engineer, Generalist:in
- Technische Tiefe: mittel bis hoch-technisch
- "I aim to ...": TBD (proposal: run my own training job on the H100s without help)
- "I need ...": TBD (proposal: a job script template I trust and the commands to check and cancel jobs)

## 3. Results

| Level | Result | Statement |
|---|---|---|
| Cognitive | Key Message | TBD (proposal: compute nodes are reached only through SLURM, and a job script is a resource request plus a command) |
| Skill-based | Final Destination | TBD (proposal: a cloned repo with logs from a GPU job, an array sweep and a 1 vs 4 GPU timing comparison, submitted with sbatch) |
| Affective | Transfer Value | TBD (proposal: "the cluster is not scary"; moment: the 4 GPU epoch time against the 1 GPU epoch time in their own logs) |

## 4. Learning goals

TBD. Proposals for the next refine round:

| # | Kompetenz (Niveau) | Profile | Participants can ... | Observable as |
|---|---|---|---|---|
| G1 | Verstehen & Einordnen (2) | all | distinguish login, run and compute nodes by what each may be used for | picks the right node for a given task |
| G2 | Anwenden (2) | all | adapt a given sbatch script (partition, time, memory, CPUs, GPUs) and submit it | own job runs and writes a log |
| G3 | Analysieren & Bewerten (2) | all | read the state and log of a failed job and name the cause | uses sacct and the .err file to explain a failure |
| G4 | Anwenden (2) | researchers | run a hyperparameter sweep as an array job | four logs with different configs |
| G5 | Analysieren & Bewerten (2) | researchers | request CPUs and GPUs for a training job with a reason | justifies a CPU per GPU ratio |

## 5. Structure

### Workshop

| Session | Subject | Minutes | Goals served |
|---|---|---|---|
| S1 | Access and SLURM basics | 57 | TBD |
| Break | | 15 | |
| S2 | GPUs and batch jobs | 77 | TBD |

Minutes are the presenter estimates from review.md (total 149 of 180).

#### S1 Access and SLURM basics

| # | Component | Subject | Minutes |
|---|---|---|---|
| S1.1 | Input (slides) | AISC intro, motivation, docs | 12.5 |
| S1.2 | Hands-on exercise | Cluster access: VPN, SSH | 26 |
| S1.3 | Input (slides) | Nodes, SLURM, partitions, interactive vs batch, rules | 12 |
| S1.4 | Hands-on exercise | VSCode Remote-SSH to a run node | 6.5 |

#### S2 GPUs and batch jobs

| # | Component | Subject | Minutes |
|---|---|---|---|
| S2.1 | Live demonstration | Interactive SLURM with tool-interactive-slurm | 19.5 |
| S2.2 | Input (slides) | CPU, GPU, memory, multi-GPU, our GPUs, fairshare | 19.5 |
| S2.3 | Hands-on exercise | Clone the repository | 6.5 |
| S2.4 | Hands-on exercise | Batch scripts 01 to 08 | 26 |
| S2.5 | Reflection and transfer | Feedback | 5 |

Deck file: `slides/workshop-slurm.key`. Owned by the meta level: title slide, agenda (slide 6), section dividers (10, 21), break (19).

##### Interface blocks

| ID, type | Minutes | Goals | Entry state | Exit state | Assets | File | Version |
|---|---|---|---|---|---|---|---|
| S1.1, slides | 12.5 | TBD | arrived, laptop open | knows what AISC offers and where to get help | none | deck slides 1 to 9 | 1 |
| S1.2, hands-on | 26 | TBD | approved account and VPN zip received before the day | shell on lx01 | README §1 | README §1 | 1 |
| S1.3, slides | 12 | G1 | shell on lx01 | knows node types, partitions, interactive vs batch | none | deck slides 10 to 17 | 1 |
| S1.4, hands-on | 6.5 | G1 | VSCode installed (TBD: prerequisite) | VSCode connected to rx01 | README §1 VSCode, screenshots | README §1 | 1 |
| S2.1, demo | 19.5 | TBD | VSCode on rx01 | interactive session on a compute node | tool-interactive-slurm | deck slide 20, README §4 | 1 |
| S2.2, slides | 19.5 | G5 | used a compute node | knows CPU/GPU split, memory limits, data parallelism, fairshare | none | deck slides 21 to 32 | 1 |
| S2.3, hands-on | 6.5 | G2 | VSCode on rx01 | repo cloned, `logs/` present (TBD: see R1) | none | deck slide 33 | 1 |
| S2.4, hands-on | 26 | G2, G3, G4, G5 | repo cloned | logs from 01 to 08 | `scripts/`, shared data dir | deck slide 34, README §2 to 3 | 1 |

Speaker note for S2.4: after 02 has finished, tell everyone to read the end of its log and run `source ~/.local/bin/env` once before submitting 03. Without it, 03 fails with `uv: command not found` in the `.err` file while the job still shows COMPLETED.

Speaker note for 08: 4 free H100s on one node are often not available, so 08 may wait in the queue for a long time. Show `/usr/bin/squeue --me --start` live (plain `squeue` is aliased to `sci-squeue.py`, which rejects `--start`), then use `example_logs/07_single_*.log` and `example_logs/08_multi_*.log` for the comparison. Measured on 2026-10-07: 07 started after 5 s and ran 3.5 min; 08 waited 1 h 37 min in the queue and ran 1 min 42 s. Fairshare is charged per GPU (billing 1000 vs 4000), so 08 costs about 8 GPU-minutes against 3.5 for 07.
| S2.5, reflection | 5 | none | logs from 01 to 08 | feedback given | QR code | deck slide 35 | 1 |

## 6. Bridges

| From | To | The one new thought |
|---|---|---|
| S1.1 | S1.2 | Step one is getting a shell on the cluster. |
| S1.2 | S1.3 | You landed on lx01; here is where that sits among the node types. |
| S1.3 | S1.4 | Run nodes are for light work such as an editor. |
| S1.4 | S2.1 | TBD (missing: link the tool back to srun/salloc on slide 15) |
| S2.1 | S2.2 | TBD (missing; Part II divider sits after S2.1) |
| S2.2 | S2.3 | TBD (missing; proposal: "Now we request exactly these resources in a script.") |
| S2.4 | S2.5 | TBD (missing recap) |

## 7. Parking lot

See review.md, section "Move to FAQ or appendix".

## 8. Expectations and pre-communication

- Told beforehand: TBD (none today; see review.md gap 2)
- Expectation check on the day: TBD (none today)
- Interaction: hands-on in S1.2, S1.4, S2.1, S2.3, S2.4; no quiz, poll or discussion
- Time-content balance: 149 of 180 min (83 %); 164 min (91 %) with a second break

## 9. Change log

| # | Date | Component | Field | Old | New | Reason | Status |
|---|---|---|---|---|---|---|---|
