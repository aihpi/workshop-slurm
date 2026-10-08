## Slide 1
Workshop 
How to use our HPC Cluster
Felix Boelter and David Goll

## Slide 2
KI-Servicezentrum Berlin-Brandenburg
Hasso-Plattner-Institut gGmbH 
•Bildet mit Universität Potsdam die Digital Engineering 
Fakultät 
•Vereint Forschung, Lehre mit den Vorteilen einer privat 
finanzierten, gebührenfreien Institution 
•Besteht aus Einrichtungen wie der E-School, der D-School,  
•dem Mittelstandsdigitalzentrum und dem KI-
Servicezentrum  
Ziel:  
Barrieren der Implementierung von KI-
Anwendungen in Gesellschaft und 
Wirtschaft reduzieren
kisz@hpi.de    
hpi.de/kisz
Göttingen I Kassel I Hannover 
Sensible und kritische Infrastrukturen
Medizin & Energie
Potsdam | Berlin
Bildungs- und Beratungsangebote,
Einsatz von KI in Wirtschaft & Gesellschaft
Bonn | St. Augustin | Aachen | Jülich | 
Dortmund | Paderborn 
KI-Hardware, KI-Beratung, KI-Schulungen 
sowie multimodale und transferierbare KI-
Modelle
Darmstadt
Erklärbarkeit, Generalisierbarkeit
und kontextuelle Anpassung
BILDUNG
BERATUNG
INFRA- 
STRUKTUR
FORSCHUNG

## Slide 3
 
Talks
•Gastvorträge zu Forschung und Innovation
tele-task.de/series/1463
Work
shops
•Praxisnahe Themen
•Beispielthemen: Speech2summary, Docker für ML, 
semantische Suche
aimaker.community
MOOCs
•ChatGPT: Was bedeutet generative KI für unsere 
Gesellschaft?
•Profitable KI
•KI Biases verstehen und vermeiden
open.hpi.de/channels/ai-service-center
BILDUNG
Newsletter


## Slide 4
BERATUNG
KI-Sprechstunde 
•Beantwortung von Fragen: 
⚬zu KI-Infrastruktur 
⚬zu KI-Modellen & Frameworks 
KI-Pilotprojekte 
•Co-Entwicklung eines Prototyps 
•Bewerbung alle drei Monate 
•Auswahlkriterien z.B. KI-Reife, Gemeinwohl 
•Veröffentlichung der Ergebnisse 
Kooperationen 
•Gemeinsam organisierte Netzwerktreffen 
Jetzt bewerben!github.com/aihpi/leichte-sprache
Bisherige KI-Pilotprojekte 
•Generierung Mathematik-Problemen 
•Leichte Sprache 
•Generierung von Upcycling Vorschlägen 
•Reduzierung von Food Waste 
•Datierung mittels Handschrift 
Sprechstunde buchen


## Slide 5
INFRASTRUKTUR 
Training 
•64 NVIDIA H100 
GPU 
Inferenz 
•40 NVIDIA A30 
GPU 
ARM Server 
•Ampere Altra 
Max M128-30 
CPU 
•2 x NVIDIA L40 
GPUs 
GPU Server 
•AMD Epyc CPU 
•8 x NVIDIA L40S 
GPU
aisc.hpi.de
Zugangsanfrage
•Zugang kostenfrei 
•Kein Produktionsbetrieb 
⚬Daten sollten anonymisiert oder 
synthetisiert sein 
⚬kein Hosting von Produkten 
•Reporting & Veröffentlichung durch 
Nutzende 
•Altrechte bleiben bei Nutzenden 
•Neurechte bleiben bei Nutzenden 
⚬Einräumen von Nutzungsrechten für 
Forschung und Lehre
Edge 
•ARMv8 CPU 
•NVIDIA Jetson 
AGX Module 
Neuromorph 
•288 SpiNNaker2 
Chips 
Speicher 
•1.5 PB NVRAM 
Netwerk 
•400 Gb/s 
Infiniband 
•200 Gb/s 
Ethernet


## Slide 6
AGENDA


## Slide 7
Motivation 
Scale: Train models that don’t fit on 
consumer hardware 
Speed: Powerful GPUs, run experiments 
in parallel 
Freedom: Submit and disconnect 
Collaboration: Shared environment 
across your team 
Cost: Free for AISC projects 


## Slide 8
Documentation 
Please make yourself familiar with 
the HPC documentation! 
If you have questions or need 
assistance, consolidate our FAQ or 
reach out to us:  
For technical issues:  
aisc-helpdesk@hpi.de 
For organizational issues:  
ki-servicezentrum@hpi.de 


## Slide 9
Initial Setup
https://github.com/aihpi/workshop-slurm


## Slide 10
Cluster Basics 


## Slide 11
Nodes
Cluster Basics 
•Cluster = many computers (nodes) connected over a network 
•Each node has its own CPUs, RAM, (sometimes) GPUs, … 
•Three types of nodes on our cluster 
1. Login node (lx01) 
•Entry point, like a lobby  
•Used only for file management, submitting jobs, …  
2. Run node (rx01/rx02) 
•Lightweight interactive work, VSCode, … 
•Shared usage. Per-user limit: 4 CPUs, 8GB RAM 
3. Compute node (gx[07-13], gx15v01, …)   
•Any computation (also interactive), ML training, data processing, …  
•Exclusive usage. Via SLURM only!

## Slide 12
SLURM Basics
What is SLURM? 
•Job scheduler: manages who gets what resources and when 
•You request resources through SLURM  
•Jobs are prioritised based on availability and fairness 
Image source: https://support.pdc.kth.se/doc/run_jobs/queueing_jobs/

## Slide 13
Key Concepts
•Partition: group of nodes with shared rules (time limits, hardware type) 
Partition Time Limit Use Case
aisc-shortrun 1h Quick tests
aisc-interactive 8h Interactive terminal, testing
aisc-batch 7 days Long training runs  
(only accessible via sbatch jobs)
•Account: Your project’s billing code. In our case it is always `aisc`. 
      —> You can find out which accounts you have via `saccount` 
•Quality of Service (QOS): Used to prioritize certain jobs. We use `aisc`.  
        —> You will likely not need to use this

## Slide 14
SLURM 
Commands
https://docs.sc.hpi.de/cluster/SLURM/Basics/

## Slide 15
Two ways to 
work on 
compute nodes
Interactive Batch
Commandsrun salloc/sblock sbatch
Output Live in terminalLive in terminalWritten to log file
Best forQuick commands, 
sanity checks
Interactive workTraining runs, 
anything serious


## Slide 16
Two ways to 
work on 
compute nodes
Interactive Batch
Commandsrun salloc/sblock sbatch
Output Live in terminalLive in terminalWritten to log file
Best forQuick commands, 
sanity checks
Interactive workTraining runs, 
anything serious


## Slide 17
Rules and Best 
Practices
Where to run things: 
- rx01/02 are for lightweight tasks only, not a substitute for compute nodes 
Resource usage: 
- Always specify expected time/memory usage! 
Batch jobs: 
- Prefer sbatch over interactive jobs for anything serious 
Being a good cluster citizen: 
- Don’t leave idle interactive sessions running. Release resources you’re not using. 
Read the Terms of Usage: https://docs.sc.hpi.de/Terms-of-Usage

## Slide 18
VSCode Setup


## Slide 19
Fußzeile
Short Break
19.03.2024 19

## Slide 20
Interactive SLURM 
Using our Cluster with VSCode interactively. 
Follow along! 

## Slide 21
Part II 
CPUs, GPUs & AI Workloads 


## Slide 22
CPU
Central Processing Unit 
•Few powerful cores, optimized for sequential tasks 
•Handles logic, branching, control flow, I/O 
•Our H100 nodes:  
•2x Intel Xeon 8480C, 112 cores (224 threads)
Core 1Core 2Core 3Core 4
Core 5Core 6Core 7Core 8
CPU
Each core handles 
one task at a time

## Slide 23
GPU
Graphics Processing Unit 
•Originally designed for rendering pixels on screen 
•Thousands of small, simple cores working in parallel 
•One H100 has 16,896 CUDA cores (vs 112 CPU cores on the same node) 
•Key insight: the same parallelism that renders pixels also powers matrix 
multiplications in neural networks
Thousands of cores each 
doing one simple operation
GPU

## Slide 24
CPU vs GPU
CPU excels at GPU excels at
•Data loading and preprocessing 
(pandas, file I/O) 
•Control flow and branching logic 
•Classical ML models (sklearn, 
XGBoost on small data) 
•Orchestrating the training 
pipeline 
•Matrix multiplications (core of 
every neural network) 
•Model Training and Inference 
•Applying the same operation to 
lots of data in parallel  
(Single Instruction Multiple 
Data, SIMD)

## Slide 25
CPU + GPU
GPU
Forward pass
Compute loss
Backward pass
Update weights
CPU
Load data
Augmentations
Create batch
CPU
Log metrics
Save checkpoint
Loop
•CPU feeds data, GPU does the math 
•CPU too slow → GPU sits idle ("CPU bottleneck") 
•Request both in SLURM: --cpus-per-task and --gres=gpu 
•Rule of thumb: 4-8 CPUs per GPU 
•Our H100 nodes: up to 14 CPU cores per GPU available

## Slide 26
CPU + RAM
RAM vs VRAM
System Memory (~2 TB) GPU Memory  
(80 GB)
GPU + VRAM
RAM (system memory): 
used by the CPU. Holds your dataset, 
preprocessing pipelines, OS, and 
everything else. Our H100 nodes 
have ~2 TB.
Data Transfer 
(PCIe / NVLink)
VRAM (GPU memory): 
dedicated memory on the GPU. 
Holds model weights, activations, 
and gradients during training. An 
H100 has 80 GB.

## Slide 27
CPU + RAM
RAM vs VRAM
System Memory (~2 TB) GPU Memory  
(80 GB)
GPU + VRAM
•7B parameter model in fp16 ≈ 14 GB just for weights. Add activations 
and gradients → easily fills 80 GB 
•Out of RAM → job gets killed 
•Out of VRAM → CUDA out of memory
Data Transfer 
(PCIe / NVLink)

## Slide 28
Training vs 
Inference
Input Layer 1 Loss
Update all layers
Training
… Layer N
Input Layer 1 Output
Inference
… Layer N
•Training: forward + backward pass, store activations, update weights. 
Repeat millions of times. 
•Inference: forward pass only. Less VRAM, less compute. 
•H100s (80 GB) for training, A30s (24 GB) for inference. 
•Our inference infrastructure runs on Kubernetes with ArgoCD. 
•Future workshop planned for model deployment.

## Slide 29
Multi-GPU
Data Parallelism
Data
GPU 1 
Model 
Batch 1
…
GPU 8 
Model 
Batch 8
Average across  
GPUs & update
•Same model copied to every GPU, each gets a different batch 
•GPUs compute in parallel, then sync gradients 
•Most common approach, scales training speed roughly linearly 
•Frameworks: torchrun, Hugging Face Accelerate, DeepSpeed 
•This is what we will use in the hands-on exercise

## Slide 30
Model Parallelism
Data
GPU 1 
Layer 1-3
Multi-GPU
•Model is split across GPUs, each holds a portion of the layers 
•Needed when the model doesn't fit on a single GPU 
•Example: 70B LLM in fp16 ≈ 140 GB, doesn't fit on one H100 (80 GB) 
•More complex to set up, use when data parallelism isn't enough 
•More common in inference, where large models need multiple GPUs 
just to be loaded 
•Start with one GPU, scale up when you hit a bottleneck
GPU 8 
Layer 22-24… Output

## Slide 31
Our GPUs at a 
Glance
GPU Count VRAM Best for
H100 64 80 GBLarge model training, multi-GPU jobs
A30 40 24 GB Inference, smaller training,  
interactive queues
L40s 8 48 GB Mixed workloads
L40 2 48 GB Mixed workloads (ARM server)
Note: aisc-interactive runs on A30s, aisc-batch runs on H100s.
H100 Node (gx07-gx13)
•2x Intel Xeon 8480C, 112 cores / 224 threads 
•~2 TB RAM · 8x H100 80 GB per node · 28 TB NVMe 
•NDR InfiniBand + 100G Ethernet 
→ 14 CPU cores and ~256 GB RAM per GPU

## Slide 32
Fairshare
Priority 
(0-100)
0
25
50
75
100
Mon Tue Wed Thu Fri Sat Sun
Good Share
Bad Share
Note: Your priority recovers over time when you're not using 
resources
•Everyone wants GPUs. SLURM Fairshare decides who goes first. 
•Use more → priority drops. Stop using → priority recovers. 
•Check your score: sshare -u $USER 
•Test your pipeline in aisc-interactive first, then submit long runs via 
aisc-batch. 
•Important: don't request more than you need, don't leave jobs idle.

## Slide 33
Clone the repository 
github.com/aihpi/workshop-slurm 
On the cluster: 
git clone https://github.com/aihpi/workshop-slurm.git 
cd workshop-slurm 
Then open the repository in VSCode


## Slide 34
SBATCH Jobs 
Submit jobs via scripts. 
Follow along! 

## Slide 35
kisz@hpi.de    
hpi.de/kisz
Ihre Meinung ist 
uns wichtig!
QR-Code zum Feedback-Formular
