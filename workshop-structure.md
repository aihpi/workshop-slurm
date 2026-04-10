# Structure of our Cluster Workshop (2h)

## Part I:
1. SLIDES: 5-10 min introduction powerpoint slides. What is a cluster? What is the aisc cluster? (FB/DG)
2. INTERACTIVE: Installation (30 min max - timer): GUIDE users to Docs! They should read it! -> Breakout sessions for Debugging. -> Goal should be that all users are connected to the cluster via VSCode at rx01 (DG)
3. SLIDES (20 min): Explain Basics of SLURM, partitions, gpus/cpus, accounts, saccount (DG beginning, FB takes over later)
4. Final SLIDE (5 min): rules and best practices (FB)
5. Explain VSCode connection with rx01/rx02

short break

## Part II:
1. Felix Tool (Mac should work easily) - download could take about 5-10 min (FB)
2. git clone workshop-slurm... (in VScode)
3. Felix explains interactive workflow (Handout in markdown so users can save the most frequent commands) (FB)
4. SLIDES: Explain Basics of CPUs/GPUs 
4. sshare erklären (Beispiel zwischen guten und schlechtem fairshare)
5. uv installation --> then restart terminal (DG) 
6. Bash scripte sukzessiv erklären: einfach -> komplex (für die Batch Sripte ein simples MNIST gpu programm schreiben, mit einem data loader)
7. Homework task: Write your own bash script to allocate GPUs for training a simple MNIST classification model


