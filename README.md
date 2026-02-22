# HERMES - Hazardous Environment Reconnaissance and Mapping Exploration System

This project comprises of a system that can be deployed on a cheap Raspberry Pi robot
to explore and find victims in environemtns that may be too hazardous for rescuers to fully explore.
The core of HERMES is architected on ROS 2, utilizing packages that contain nodes that execute the 
desired behavior.

HERMES uses Git submodules to link to separate repos for each component/subsystem.

## Cloning the Repo

Always include `--recurse-submodules` when cloning so the submodule folders aren't empty:

```bash
git clone --recurse-submodules git@github.com:bcchau1/HERMES.git
```

If you already cloned without that flag, run this from inside the repo:

```bash
git submodule init
git submodule update
```

## Pulling Updates

A regular `git pull` only updates the main repo. To also update the submodules to the commits HERMES expects:

```bash
git pull
git submodule update
```

Or do it all at once:

```bash
git pull --recurse-submodules
```

## Making Changes in a Submodule

Submodules check out a specific commit, not a branch, so you'll be in "detached HEAD" by default. Always checkout a branch before making changes. For example,

```bash
cd HERMES-driver        
git checkout main
# make your changes
git add .
git commit -m "your message"
git push
```

Then go back to the main repo and record the updated submodule reference so everyone else later pulling this main repo is caught up to date :

```bash
cd ..
git add HERMES-driver
git commit -m "update HERMES-driver submodule"
git push
```
