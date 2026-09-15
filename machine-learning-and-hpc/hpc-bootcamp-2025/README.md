# NERSC / DOE HPC Bootcamp 2025 — Module Notebooks

Jupyter notebooks from the **Introduction to High Performance Computing Bootcamp 2025** (NERSC / U.S. Department of Energy), which the author worked through. The modules cover how computer hardware consumes power, what the TOP500 list shows about supercomputer performance and energy efficiency, and a fusion-energy project on workload and energy trade-offs at an HPC center.

The lesson text, exercise prompts, starter code and synthetic datasets are **bootcamp-provided material**. This project holds the author's executed copies. Each section below separates what a module covers from what was run in this copy, and quotes results only when they appear in the saved outputs.

---

## Contents

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| [`Module_1_NERSC_DOE_HPC_BOOTCAMP2025.ipynb`](Module_1_NERSC_DOE_HPC_BOOTCAMP2025.ipynb) | Power consumption in computers and HPC systems | Component power bar charts, donut chart, CO₂ estimate from kWh | `matplotlib` |
| [`Module_2_NERSC_DOE_HPC_BOOTCAMP2025.ipynb`](Module_2_NERSC_DOE_HPC_BOOTCAMP2025.ipynb) | TOP500 (June 2025) analysis | Robust column detection, numeric coercion, performance per kW, accelerator fraction, country and vendor aggregation | `pandas`, `matplotlib`, `seaborn` |
| [`Module_5_Project_1_NERSC_DOE_HPC_BOOTCAMP2025.Fusion_Energy_HPC_Analysis.ipynb`](Module_5_Project_1_NERSC_DOE_HPC_BOOTCAMP2025.Fusion_Energy_HPC_Analysis.ipynb) | Fusion-energy workloads: performance and energy trade-offs | Synthetic job table, pivot tables, annotated and row-normalized heatmaps, planning worksheets | `pandas`, `seaborn`, `matplotlib`, `numpy` |
| [`entrypoint.sh`](entrypoint.sh) | WireGuard VPN container entrypoint (not part of the bootcamp material) | Bash, `wg`, `wg-quick`, `iptables` | none |

---

## Module 1 — Understanding Power Consumption in Computers

### What the module covers
- How CPUs, GPUs, RAM, storage, cooling, power supplies, networking and power distribution each draw power, in personal computers and in HPC systems.
- Dynamic, static and short-circuit power in processors, and the dynamic-power relation **P = C · V² · f**.
- Energy-efficiency strategies for HPC: algorithm optimization, efficient hardware, cooling, and monitoring.
- Several optional written exercises, such as comparing a real HPC GPU like the NVIDIA A100 or AMD MI250X, or looking at how Perlmutter or Frontier handle cooling and power distribution.

### What was run in this copy
All code cells were executed. They are the interactive exercises, left at the example values in the "modify these values" placeholders:

1. **PC component power:** a bar chart of CPU 95 W, GPU 120 W, RAM 40 W, storage 10 W, motherboard 50 W, cooling 20 W and other 15 W, drawn twice (reference chart and "custom PC" exercise).
2. **Configuration comparison:** stacked bars of idle vs. full-load power for Gaming, Workstation and Energy-Efficient configurations.
3. **HPC components:** a bar chart of processors, memory, interconnects, cooling, storage and other.
4. **Typical HPC node:** a donut chart of CPU, GPU, RAM, storage, cooling and PSU shares. The section heading mentions Plotly, but the chart is drawn with `matplotlib`.
5. **Carbon footprint:** one node at 0.5 kW for 24 h, using 0.4 kg CO₂/kWh (U.S. grid average). Saved output: **"Estimated CO₂ emissions per day: 4.80 kg"**.
6. **Efficiency measures:** a bar chart of the percentage reduction from efficient cooling, power scaling, optimized algorithms and other measures.

The optional written exercises are not answered in this copy.

---

## Module 2 — Top 500 Supercomputers Analysis

### What the module covers
- Background on the TOP500 and Green500 lists.
- A reusable loader for the June 2025 TOP500 CSV with three helper functions:
  - `normalize` standardizes column-name text.
  - `find_col` finds a column whose name contains given keywords, so the code keeps working when header names change between releases.
  - `coerce_numeric` turns strings like `"1,234.5"` into floats.
- Exercises on performance per watt, accelerator adoption, geographic distribution and vendor comparisons.
- Discussion prompts, and an extension activity that repeats the analysis on the Green500 list.

### Data
- `data/TOP500_202506.csv`, the June 2025 TOP500 list from [top500.org](https://www.top500.org/). **It is not included in this project.** Download the list and save it at that path.
- Columns the loader detected in the saved run: `Name`, `Country`, `Manufacturer`, `Rmax [TFlop/s]`, `Rpeak [TFlop/s]`, `Power (kW)`, `Accelerator/Co-Processor Cores`, `Total Cores`.

### What was run in this copy
1. **Load and clean:** detect key columns, fill missing system names from the site ID, and coerce numeric columns.
2. **Accelerator fraction** (cell 8, "Your Work"):
   - `accel_frac = accelerator cores / total cores`, with a histogram of that fraction.
   - Mean `Rmax / Power(kW)` compared between accelerated (`accel_frac > 0`) and CPU-only systems.
3. **Energy efficiency** (cell 10): `efficiency_perf_per_kw = Rmax / Power`, the top-10 table, and a scatter plot of Rmax vs. power for all systems.
4. **Geography** (cell 12): horizontal bar charts of system count and total Rmax for the top 12 countries.
5. **Top 10 by Rmax** (cell 14): a standalone cell that reloads the CSV, prints the first rows, and draws a `seaborn` bar chart.
6. **Vendors** (cell 18): mean Rmax and mean efficiency per manufacturer, with a bar chart of the top-10 vendors by efficiency.

### Results in the saved outputs
- **Top systems by Rmax (TFlop/s):** El Capitan 1,742,000; Frontier 1,353,000; Aurora 1,012,000; JUPITER Booster 793,400; Eagle 561,200 (no power value).
- **Mean efficiency (Rmax TFlop/s per kW, numerically GFlops/W):** accelerated systems **35.9** vs. non-accelerated **5.32**.
- **Top 10 by Rmax per kW:**

| # | System | Rmax (TFlop/s) | Power (kW) | Rmax per kW |
|---|---|---|---|---|
| 1 | Adastra 2 | 2,529 | 36.60 | 69.10 |
| 2 | JEDI | 4,504 | 67.31 | 66.91 |
| 3 | Henri | 2,882 | 44.07 | 65.40 |
| 4 | Portage | 24,100 | 371.48 | 64.88 |
| 5 | Hunter | 31,680 | 490.00 | 64.65 |
| 6 | Isambard-AI phase 1 | 7,417 | 117.08 | 63.35 |
| 7 | HoreKa-Teal | 3,123 | 49.60 | 62.96 |
| 8 | rzAdams | 24,380 | 388.20 | 62.80 |
| 9 | Frontier TDS | 19,200 | 308.68 | 62.20 |
| 10 | Viper-GPU | 31,096 | 499.98 | 62.19 |

- **Vendors by mean Rmax** (systems with power data), mean Rmax per kW in parentheses: Intel (26.2), Nebius AI (36.7), IBM / NVIDIA / Mellanox (12.7), NRCPC (6.05), HPE (27.7), NUDT (3.32), Fujitsu (17.9), ASUSTeK (43.0), EVIDEN (19.3), Nvidia (28.6).

### Notes
- The notebook cells are slightly out of order. The accelerator-fraction code (cell 8) comes before the Exercise 3 description. The Exercise 4 description was pasted into a **code** cell (cell 15, not executed; it would raise a `SyntaxError` if run). The Exercise 5 description appears twice.
- Cell 14 was run in a separate kernel session (lower execution count) and re-imports everything it needs.
- The discussion prompts and the Green500 extension are not answered in this copy.

---

## Module 5 — Project 1: HPC Workload and Energy Analysis in Fusion Research

### What the module covers
A "thinking project" that applies Modules 1 to 4 to DOE fusion-energy computing. Participants choose one track:

- **Track A — Workflow efficiency:** match three fusion workloads (plasma simulation, diagnostics analysis, ML prediction) to CPU, GPU or hybrid architectures, and reason about scaling and performance per watt. Worksheets A1 and A2 are provided.
- **Track B — Data-center design and scheduling:** design a facility with a **12 MW** power cap that gives **40%** of compute to fusion and prices electricity at **$0.10/kWh**, then plan a weekly schedule. Worksheets B1 and B2 are provided, with sample job classes.

The notebook also gives a hypothetical workload table (runtime, nodes, kW per node, scaling efficiency), formulas for energy per job, science per kWh and cost, background on 2025 leadership systems (El Capitan, Frontier, Aurora, Perlmutter, Jupiter and others), DOE fusion strategy and facilities, AI/ML in fusion, and policy and commercialization, with references.

### What was run in this copy
1. **Synthetic dataset** (cell 12): a provided 20-row `DataFrame` of fusion jobs with `JobID`, `Project` (DIII-D, NSTX-U, NIF, SPARC, ITER Physics Support), `Facility` (Perlmutter, Frontier, El Capitan, Aurora, Jupiter, LUMI, Henri), `Cores`, `RuntimeMinutes`, `JobType` and `Energy_kWh`.
2. **Heatmaps** (cell 13):
   - `pivot_table`s of **mean runtime** and **job count** by project × facility, with columns ordered to match the 2025 systems list.
   - A `seaborn` heatmap annotated as "mean (n)".
   - A second **row-normalized** heatmap that scales each project's runtimes to 0–1 across facilities, to compare relative runtime within a project.

The Track A and B worksheet tables are **not filled in** in this copy. Cells 7 and 18 are empty.

**Related project work:** notebooks that compute energy per job, science per kWh and cost from fusion and non-fusion project CSVs, and a greedy scheduler that fits jobs under a 4.8 MW fusion cap (40% of 12 MW), are in the author's separate `data-science-notebooks` repository (`misc/CleanedmergedDataset.ipynb`, `misc/scheduler.ipynb`).

---

## `entrypoint.sh`

A standalone Bash entrypoint for a WireGuard VPN agent container. The notebooks do not use it.

1. Generates a WireGuard key pair in `/etc/wireguard/keys/` if one does not exist yet (`wg genkey | wg pubkey`, with `umask 077`).
2. Writes `/etc/wireguard/wg0.conf` from environment variables: `WG_ADDRESS`, `WG_IFACE`, `WG_SERVER_PUBLIC_KEY`, `WG_SERVER_ENDPOINT`, `WG_ALLOWED_IPS`, `WG_KEEPALIVE`. It adds NAT masquerading with `iptables` in `PostUp`/`PostDown`.
3. Prints the public key for registration, enables IPv4 forwarding, runs `wg-quick up wg0`, and keeps the container alive with `tail -f /dev/null`.

No keys are stored in the repository. The script needs root privileges or `NET_ADMIN`, plus `wireguard-tools` and `iptables`.

---

## Requirements

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

- The notebooks were saved with a Python 3.11.7 kernel, and Modules 1 and 2 carry Noteable metadata. They need no GPU or cluster resources and run on a laptop or a NERSC JupyterHub session.
- Module 2 needs `data/TOP500_202506.csv` (see [Data](#data)).

## How to run

```bash
git clone <this-repo>
cd hpc-bootcamp-2025
mkdir -p data   # put TOP500_202506.csv here for Module 2
jupyter lab
```

Open a module and run the cells from top to bottom. In Module 2, cell 14 can be run on its own.

## Related

Other HPC bootcamp projects by the author:
- [Intro-to-HPC-Modeling-Epidemic-Outbreaks](https://github.com/joserico00/Intro-to-HPC-Modeling-Epidemic-Outbreaks)
- [Intro-to-HPC-Bootcamp-Teaching-Students-to-Leverage-LLMs-for-Regulatory-Genomics-on-HPC](https://github.com/joserico00/Intro-to-HPC-Bootcamp-Teaching-Students-to-Leverage-LLMs-for-Regulatory-Genomics-on-HPC)

## Author

Jose E. Rodriguez Rios
