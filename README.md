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

## Quickstart

### 1. Create the endpoint

> **Shortcut:** Click the **Deploy on Runpod** badge at the top of this page to pre-fill the deployment form -- then skip ahead to [step 2](#2-wait-for-workers).

From the Runpod console, go to **Serverless** and click **New endpoint**. Select **Custom deployment**, then **Deploy from Docker registry**.

![](assets/1-home.png)
![](assets/2-serverless.png)
![](assets/3-new-endpoint.png)
![](assets/4-custom-deployment.png)
![](assets/5-deploy-from-docker-registry.png)

Enter the Docker image `startown/madgraph-serverless:0.1.12`. Name your endpoint, set the worker type to **CPU**, and choose a CPU configuration. Set the container disk to at least **200 GB** -- MadGraph simulations generate large intermediate files.

![](assets/6-enter-docker-image.png)
![](assets/7-configure-endpoint.png)
![](assets/8-configure-container.png)

Add the following environment variables for storing output files to S3-compatible storage (e.g. Cloudflare R2):

- `ENDPOINT` -- your storage endpoint URL
- `ACCESS_KEY_ID` -- your access key
- `SECRET_ACCESS_KEY` -- your secret key
- `BUCKET` -- the bucket name

Click **Create endpoint**.

![](assets/9-set-environment-variables.png)
![](assets/10-create-endpoints.png)

### 2. Wait for workers

Workers will initialize and pull the Docker image. Once the status shows **Ready**, the endpoint is live.

![](assets/11-workers-initializing.png)
![](assets/12-workers-ready.png)

### 3. Configure auto-scaling (optional)

Click **Manage > Edit endpoint** to adjust the auto-scaling strategy. **Request count** with 1 request per worker works well for MadGraph since each simulation fully occupies a worker.

![](assets/13-edit-endpoint.png)
![](assets/14-request-count.png)
![](assets/15-save-endpoint.png)

### 4. Submit a run

**Via the console:** Go to the **Requests** tab, paste your request body, and click **Run**. The request enters the queue and is picked up by an available worker.

![](assets/16-requests.png)
![](assets/17-request-body.png)
![](assets/18-run.png)
![](assets/19-new-request.png)

**Via the API:** You can submit runs programmatically using the Runpod REST API. Replace `{endpoint_id}` and `{api_key}` with your values from the Runpod console.

```bash
curl -X POST "https://api.runpod.io/v2/{endpoint_id}/run" \
  -H "Authorization: Bearer {api_key}" \
  -H "Content-Type: application/json" \
  -d '{
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
        "set nevents 1000",
        "done"
      ]
    }
  }'
```

You can submit multiple requests at once -- each one runs on a separate worker in parallel. When doing so, give each request a unique output name to avoid collisions in your storage bucket. For example, append `-1`, `-2`, `-3` to the output name:

```
"output pp2ww_w2jj_w2jj-1k-42-1"   # request 1
"output pp2ww_w2jj_w2jj-1k-42-2"   # request 2
"output pp2ww_w2jj_w2jj-1k-42-3"   # request 3
```

![](assets/20-3-runs.png)

### 5. Get your results

When a run completes, the response includes the output path. The simulation output is uploaded as a `.tar.gz` file to your configured storage bucket.

![](assets/21-output.png)
![](assets/22-storage.png)

## Usage

The worker accepts a single parameter `commands`: a list of strings that maps directly to what you would type into MadGraph's interactive CLI, in order. The flow has four phases:

**1. Define the process**

```
"generate [process]"   # hard process in MadGraph syntax
"output [name]"        # name of the output directory and output .tar.gz
```

**2. Configure the run**

```
"launch"
"shower=pythia8"       # optional: enable parton shower (pythia8)
"detector=delphes"     # optional: enable detector simulation (delphes)
"done"                 # confirm component selection
```

**3. Set run card parameters**

```
"set iseed 42"         # random seed for the matrix element generator
"set ebeam 7000"       # beam energy in GeV (per beam)
"set nevents 1000"     # number of events to generate
"set htjmin 300"       # example kinematic cut (min HT of jets in GeV)
```

Any parameter accepted by MadGraph's `run_card.dat` can be set here.

**4. Inject card settings**

```
"add pythia8_card [setting]"                          # append a line to the Pythia8 card
"add delphes_card [--line_position=N] [setting]"      # append a line to the Delphes card
"done"                                                # start the run
```

Use `--line_position=0` to prepend instead of append.

**Full example**

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
