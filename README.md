<div style="background-color: #ffffff; color: #000000; padding: 10px;">
<img src="00_aisc/img/logo_aisc_bmftr.jpg">
<h1> AISC Cluster Workshop: Introduction to SLURM</h1>
</div>

This repository contains materials for the **2-hour HPC Cluster Workshop** by the [AI Service Centre Berlin-Brandenburg (AISC)](http://hpi.de/kisz). Participants learn how to access the AISC/HPI cluster, understand the basics of SLURM, and run GPU workloads independently.

For those not attending a workshop, we recommend reviewing the accompanying presentation PDF in the slides folder.

## Workshop Structure

| Part | Topic | Duration |
|------|-------|----------|
| **I** | Introduction and Motivation | 10 min |
| **I** | Interactive: Cluster access setup | 20 min |
| **I** | Slides: partitions, nodes, SLURM, Interactive vs. Batch | 10 min |
| **I** | Interactive: VSCode Installation | 5 min |
| | *Break* | |
| **II** | Interactive SLURM workflow | 10-20 min |
| **II** | Slides: Basics of CPUs/GPUs and fairshare | 10-20 min |
| **II** | Interactive: Cloning of repository | 5 min |
| **II** | Interactive: Batch scripts (`01`-`08`) | 20 min |
| **II** | Conclusion and Feedback | 5 min |

## Getting Started

### Cluster Access Setup

You can find all of this information in the [Scientific Compute Documentation](https://docs.sc.hpi.de). 
Please note that the Docs provide information for the [general HPI HPC](https://docs.sc.hpi.de/cluster/Resources/Partitions/), of which the [AISC infrastructure](https://docs.sc.hpi.de/aisc/) is a part of.
We outline the important steps below:

1. Get access via the AISC portal by submitting a [proposal](https://aisc.hpi.de/portal/cfp/): 
2. When your account is created, you should receive a .zip file via mail, containing your username, initial password, and, crucially, an .ovpn file.
3. Set your password via the steps explained in the .zip file
4. Set up a [VPN connection](https://docs.sc.hpi.de/VPN/) and keep it running
5. With your VPN connection **active**, connect to the cluster through your terminal (Windows: Powershell) via the command: 
   `ssh user.name@hpc.sci.hpi.de` 

> ***Optional:***
> Set up a SSH connection with the cluster by following the steps outlined to the left in [SSH guide](https://docs.sc.hpi.de/ssh/).
> Instead of typing the full address every time, create or edit `~/.ssh/config` and add:
> ```
> Host hpi-hpc
>     HostName hpc.sci.hpi.de
>     User user.name
> ```
> After saving, you can connect with just `ssh hpi-hpc`.
> You can replace `hpi-hpc` with any alias you prefer.

6. Once you are connected, please take some time to familiarise yourself with the basic concepts of [SLURM](https://docs.sc.hpi.de/cluster/SLURM/Basics/), [jobs](https://docs.sc.hpi.de/cluster/SLURM/Job-Examples/#playground-examples) (especially SBatch files), [partitions](https://docs.sc.hpi.de/cluster/Resources/Partitions/) (only the aisc-... partitions are relevant for you), and [run nodes](https://docs.sc.hpi.de/cluster/Resources/Run-Nodes/), `nvidia-smi`, ...

### Setting up a Connection with VSCode

When you log in via `ssh user.name@hpc.sci.hpi.de` you are connected with one of the [login nodes](https://docs.sc.hpi.de/cluster/Resources/Login-Nodes/), e.g. `lx01`. The login nodes are only intended for submitting jobs to Compute nodes, inspect the cluster status, and manage your files. You cannot execute scripts on the login nodes. *They are also not intended for a connection to VSCode.* For this, please use one of the [run nodes](https://docs.sc.hpi.de/cluster/Resources/Run-Nodes/). 

0. In VSCode, install the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension from Microsoft, by searching for it in the extensions search bar on the left
1. In VSCode, open the Command Palette: Shift + Command + P (Mac) / Ctrl + Shift + P (Windows/Linux).
2. Enter `Remote-SSH: Add New SSH Host...`
3. Enter your username and the run node address in the following format: `user.name@rx01.hpc.sci.hpi.de` / `user.name@rx02.hpc.sci.hpi.de`
4. This will write the following information to your `~/.ssh/config` file: 
>      Host rx01.hpc.sci.hpi.de
>         HostName rx01.hpc.sci.hpi.de
>         User user.name
5. Now you should be able to connect easily to the run nodes via the Remote Explorer on the left in VSCode:

<img src="00_aisc/img/Screenshot1.png" alt="Alt text" width="300">

6. Once you are connected, you should see the following in the bottom left corner:

<img src="00_aisc/img/Screenshot2.png" alt="Alt text" width="200">

7. After your session is finished, click on the blue button in the bottom left and `Close Remote Connection`


## Interactive SLURM Workflow

We provide a tool for interactive SSH sessions on SLURM compute nodes, with VSCode Remote-SSH integration. For full documentation, see [tool-interactive-slurm](https://github.com/aihpi/tool-interactive-slurm).

**Installation** (run on your local machine):
```bash
git clone https://github.com/aihpi/tool-interactive-slurm.git
cd tool-interactive-slurm
./setup.sh          # macOS/Linux
# .\setup.ps1       # Windows (PowerShell)
```

The setup script generates SSH keys, installs scripts on the cluster, and configures VSCode integration.

**Usage:**

| Command | Purpose |
|---------|---------|
| `ssh slurm-cpu` | Connect to a CPU compute node |
| `remote list` | Display running jobs |
| `remote h100 [count]` | Reserve H100 GPUs (1-8) |
| `remote exit` | Terminate all interactive sessions |


## SBATCH Scripts

The `scripts/` directory contains a progressive series of SLURM batch scripts (`.sh`) and their corresponding Python scripts (`.py`). Each builds on the concepts from the previous one.

| Script | Topic | Command |
|--------|-------|---------|
| `01_hello_world` | Basic SLURM job submission and logging | `sbatch scripts/01_hello_world.sh` |
| `02_setup_uv` | Install UV and Python dependencies. For more information on UV, please read the [UV docs](https://docs.astral.sh/uv/) | `sbatch scripts/02_setup_uv.sh` |
| `03_gpu_basic` | Verify GPU allocation with `nvidia-smi` | `sbatch scripts/03_gpu_basic.sh` |
| `04_data_setup` | Download datasets to shared project storage | `sbatch scripts/04_data_setup.sh` |
| `05_python_training` | Train a simple CNN on MNIST (single GPU) | `sbatch scripts/05_python_training.sh` |
| `06_array_jobs` | Hyperparameter sweep with SLURM array jobs | `sbatch scripts/06_array_jobs.sh` |
| `07_single_gpu` | Train ResNet-18 on CIFAR-100 (single GPU) | `sbatch scripts/07_single_gpu.sh` |
| `08_multi_gpu` | Train ResNet-18 on CIFAR-100 (4 GPUs with Accelerate) | `sbatch scripts/08_multi_gpu.sh` |

Scripts `05`-`06` use MNIST with a small CNN for fast iteration. Scripts `07`-`08` switch to CIFAR-100 with ResNet-18 — a larger model and dataset that makes the multi-GPU speedup clearly visible.

## FAQ & Troubleshooting

For general cluster issues, see the [Scientific Compute FAQ](https://docs.sc.hpi.de/FAQ/).

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
ToDo: Add troubleshooting section

## References

- [Scientific Compute Documentation](https://docs.sc.hpi.de)
- [AISC Infrastructure](https://docs.sc.hpi.de/aisc/)
- [SLURM Basics](https://docs.sc.hpi.de/cluster/SLURM/Basics/)
- [SLURM Job Examples](https://docs.sc.hpi.de/cluster/SLURM/Job-Examples/)

## Author
- [David Goll](https://github.com/golldavid)
- [Felix Boelter](https://github.com/felixboelter)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements
<img src="00_aisc/img/logo_bmftr_de.png" alt="drawing" style="width:170px;"/>

The [AI Service Centre Berlin Brandenburg](http://hpi.de/kisz) is funded by the [Federal Ministry of Research, Technology and Space](https://www.bmbf.de/) under the funding code 01IS22092.
