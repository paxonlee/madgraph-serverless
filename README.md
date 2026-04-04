# MadGraph Serverless

[![Deploy on Runpod](https://flat.badgen.net/badge/runpod/Deploy%20on%20Runpod/602CF0/?icon=https://public.startown.ai/icons/runpod-white.svg&label)](https://console.runpod.io/hub/paxonlee/madgraph-serverless)
![Image size](https://flat.badgen.net/docker/size/startown/madgraph-serverless/0.1.12/amd64/?icon=docker&label=Image%20size)

Run MadGraph5_aMC@NLO on Runpod Serverless with a simple HTTP request.

MadGraph5_aMC@NLO is a widely used tool in high energy physics (HEP) for simulating particle collisions. Setting up its runtime environment -- Pythia, Delphes, LHAPDF, ROOT, and others -- can be tricky. Once running, individual simulations are CPU-intensive, long-running, and consume large disk space.

This project packages MadGraph and its common dependencies into a Docker image and deploys it on Runpod Serverless, a platform that allows users to run containers on demand. You submit a run via an HTTP request with the same commands you'd enter in MadGraph, pay only for the compute you use, and run many simulations in parallel without managing infrastructure.

## Dependencies

```
 hepmc ────┬───▶ pythia ────┬───▶ madgraph
 2.06.09   │     8.316      │     3.5.13
           │                │
 zlib ─────┘                │
 1.3.1                      │
                            │
 root ─────────▶ delphes ───┤
 6.34.10         3.5.0      │
                            │
 emela ─────────────────────┤
 1.0.1                      │
                            │
 fastjet ───────────────────┤
 3.5.1                      │
                            │
 lhapdf ────────────────────┘
 6.5.5
```

MadGraph integrates all of these components into a single simulation pipeline -- from matrix element calculation, through parton showering and hadronization, to detector response simulation.

- [HepMC](https://hepmc.web.cern.ch/hepmc/): C++ event record library for Monte Carlo generators representing particle-level events (`.hepmc` file).
- [zlib](https://zlib.net/): General-purpose lossless data-compression library.
- [ROOT](https://root.cern/): Open-source data analysis framework used across HEP.
- [eMELA](https://github.com/gstagnit/eMELA): Library for quantum electrodynamics (QED) evolution of lepton parton distribution functions (PDFs) at next-to-leading logarithmic (NLL) accuracy.
- [FastJet](https://fastjet.fr/): Package for jet finding in $pp$ and $e^+ e^-$ collisions.
- [LHAPDF](https://lhapdf.hepforge.org/): Standard library for evaluating PDFs.
- [Pythia](https://www.pythia.org/): General-purpose Monte Carlo event generator for high-energy collisions, handling parton showers, fragmentation, and decay.
- [Delphes](https://delphes.github.io/): Fast detector response simulation, producing reconstruction-level events (`.root` file).
- [MadGraph5_aMC@NLO](https://launchpad.net/mg5amcnlo): Framework for simulating particle physics processes, producing parton-level events (`.lhe` file).

## Usage

The workers accepts only one parameter `commands`. You request body should look like:

```json
{
  "input": {
    "commands": [
      "generate p p > w+ w-, w+ > j j, w- > j j",
      "output pp2ww_w2jj_w2jj-1k-42",
      "launch",
      "shower=pythia8",
      "detector=delphes",
      "done",
      "set iseed 42",
      "set ebeam 7000",
      "set htjmin 300",
      "set htjmax 400",
      "set nevents 1000",
      "add pythia8_card Random:setSeed = on",
      "add pythia8_card Random:seed = 42",
      "add delphes_card --line_position=0 set RandomSeed 42",
      "done"
    ]
  }
}
```
