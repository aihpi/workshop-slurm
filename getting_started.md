# Getting Started

## Cluster Access Setup
You can find all of this information in the [Scientific Compute Documentation](https://docs.sc.hpi.de). 
Please note that the Docs provide information for the [general HPI HPC](https://docs.sc.hpi.de/cluster/Resources/Partitions/), of which the [AISC infrastructure](https://docs.sc.hpi.de/aisc/) is a part of.
We outline the important steps below:

1. Get access via the AISC portal by submitting a [proposal](https://aisc.hpi.de/portal/cfp/): 
2. When your account is created, you should receive a .zip file via mail, containing your username, initial password, and, crucially, an .ovpn file.
3. Set your password via the steps explained in the .zip file
4. Set up a [VPN connection](https://docs.sc.hpi.de/VPN/) and keep it running
5. Set up a SSH connection with the cluster by following the steps outlined to the left in [SSH guide](https://docs.sc.hpi.de/ssh/)
6. With your VPN connection **active**, connect to the cluster via SSH: 
   `ssh user.name@hpc.sci.hpi.de` 

> ***Optional:***
> Instead of typing the full address every time, create or edit `~/.ssh/config` and add:
> ```
> Host hpi-hpc
>     HostName hpc.sci.hpi.de
>     User user.name
> ```
> After saving, you can connect with just `ssh hpi-hpc`.
> You can replace `hpi-hpc` with any alias you prefer.

7. Once you are connected, please take some time to familiarise yourself with the basic concepts of [SLURM](https://docs.sc.hpi.de/cluster/SLURM/Basics/), [jobs](https://docs.sc.hpi.de/cluster/SLURM/Job-Examples/#playground-examples) (especially SBatch files), [partitions](https://docs.sc.hpi.de/cluster/Resources/Partitions/) (only the aisc-... partitions are relevant for you), and [run nodes](https://docs.sc.hpi.de/cluster/Resources/Run-Nodes/), `nvidia-smi`, ...

### Setting up a Connection with VSCode

When you log in via `ssh user.name@hpc.sci.hpi.de` you are connected with one of the [login nodes](https://docs.sc.hpi.de/cluster/Resources/Login-Nodes/), e.g. `lx01`. The login nodes are only intended for submitting jobs to Compute nodes, inspect the cluster status, and manage your files. You cannot execute scripts on the login nodes. *They are also not intended for a connection to VSCode.* For this, please use one of the [run nodes](https://docs.sc.hpi.de/cluster/Resources/Run-Nodes/). 

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

7. After your session is finished, click on the blue bottom in the bottom left and `Close Remote Connection`