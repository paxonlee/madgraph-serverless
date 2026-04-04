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
