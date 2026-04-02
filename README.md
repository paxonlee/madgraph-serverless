# MadGraph Serverless

[![Runpod](https://api.runpod.io/badge/paxonlee/madgraph-serverless)](https://console.runpod.io/hub/paxonlee/madgraph-serverless)

MadGraph5_aMC@NLO is a widely used tool in high energy physics (HEP) for simulating particle collisions. Setting up its runtime environment -- Pythia, Delphes, LHAPDF, ROOT, and others -- can be tricky. Once running, individual simulations are CPU-intensive, long-running, and consume large disk space.

Serverless computing is a natural fit: you submit a run with a simple HTTP request, pay only for the compute you use, and scale horizontally without managing infrastructure. This project packages MadGraph and all of its dependencies into a Docker image ready to deploy on Runpod Serverless.

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

## Usage

The workers accepts only one parameter `commands`. You request body should look like:

```json
{
  "input": {
    "commands": [
      "generate p p > w+ w-, w+ > j j, w- > j j",
      "output pp2ww_w2jj_w2jj-10k",
      "launch",
      "shower=pythia8",
      "detector=delphes",
      "done",
      "set iseed 42",
      "set ebeam 7000",
      "set htjmin 300",
      "set htjmax 400",
      "set nevents 10000",
      "add pythia8_card Random:setSeed = on",
      "add pythia8_card Random:seed = 42",
      "add delphes_card --line_position=0 set RandomSeed 42",
      "done"
    ]
  }
}
```
