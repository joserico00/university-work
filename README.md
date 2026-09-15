# University Work

Coursework, labs, training and research prototypes from my computer science studies, from undergraduate through graduate school. The focus areas are **cybersecurity**, **data science**, **machine learning** and **high performance computing**.

Each project is self-contained in its own folder, with a README explaining what the code does, how to run it, and its current state. Much of this is learning work, so some files are early drafts or experiments; the READMEs say so where that applies.

## Contents

### Cybersecurity

| Project | Description | Tech |
|---|---|---|
| [Network Scanner Prototypes](cybersecurity/network-scanner-prototypes/) | Prototypes that led to my graduate project [NVSRCO](https://github.com/joserico00/NVSRCO). The progression runs from single-file nmap scanners to timestamped scan history, Plotly Dash dashboards, local CVE lookups and an OpenVAS (GVM) automation pipeline. | Python, python-nmap, OpenVAS/GMP, NVD API, Dash, Docker |
| [Python Network Tools](cybersecurity/python-network-tools/) | Low-level networking scripts: subnet detection, ARP/ICMP/TCP host discovery, SYN port scanning, packet sniffing, nmap automation and NVD lookups. | Python, Scapy, raw sockets, python-nmap |
| [Ghidra Decompilation Analysis](cybersecurity/reverse-engineering/decompiler-analysis/) | Spanish-language analysis of where decompiled C differs from source, with an English project summary and browser-friendly PDF. | Ghidra, C, x86 assembly, reverse engineering |

### Data Science

| Project | Description | Tech |
|---|---|---|
| [Data Science Notebooks](data-science/data-science-notebooks/) | Data cleaning and wrangling, exploratory and geographic visualization, statistics (confidence intervals, correlation, t-tests), K-means clustering and small machine learning models. | pandas, matplotlib, seaborn, Plotly, GeoPandas, scikit-learn |
| [Mental Health & the Economy](data-science/mental-health-suicide-analysis/) | My individual analysis in a group project. It relates U.S. suicide data to inflation and natural disasters, with correlation analysis and a regression model. | pandas, seaborn, SciPy, scikit-learn |
| [Gapminder D3 Visualization](data-science/gapminder-d3-visualization/) | Interactive bubble chart of fertility vs. life expectancy by country, with population-sized bubbles, a year selector and tooltips. | D3.js, HTML/CSS |

### Machine Learning

| Project | Description | Tech |
|---|---|---|
| [Deep Learning Coursework](machine-learning/deep-learning-coursework/) | Softmax regression on Fashion-MNIST, plus a Transformer-encoder classifier that separates benign from malicious network connections. | PyTorch, d2l, TensorFlow/Keras |
| [Malware Image Classification](machine-learning/malware-image-classification/) | Final machine-learning course project using CNNs to classify Malimg and Microsoft BIG 2015 malware-family images, with archived results and cleaned reproducible notebooks. | TensorFlow/Keras, scikit-learn, Jupyter |

My high performance computing bootcamp projects have their own repositories. See [Related repositories](#related-repositories).

### Systems & Algorithms

| Project | Description | Tech |
|---|---|---|
| [Systems Programming in Python](systems-and-algorithms/systems-programming-in-python/) | Operating system concepts: page replacement simulators (FIFO, Optimal, WSClock), a Shortest Job First scheduler, a CPU task queue and a distributed file storage system. | Python, threads, semaphores, sockets, SQLite |
| [Algorithms Practice](systems-and-algorithms/algorithms-practice/) | Interview and competitive-programming problems: sliding window, two pointers, selection algorithms, divide and conquer, dynamic programming and grid DFS, with complexity analysis. | Python |
| [Pyret Expression Interpreter](systems-and-algorithms/pyret-interpreter/) | A small interpreter with S-expression parsing, desugaring, typed values, lexical environments, closures and multi-argument functions. | Pyret, interpreters, functional programming |

### Software Development

| Project | Description | Tech |
|---|---|---|
| [Weblogs](software-development/weblogs/) | Flask web app where users upload Apache access logs and explore an interactive dashboard of traffic, status codes, 404s and suspicious activity. | Flask, SQLAlchemy, Flask-Login, ECharts |
| [Blockchain in Python](software-development/blockchain-python/) | Minimal proof-of-work blockchain node with mining, transactions, peer registration and longest-chain consensus, plus notes on blockchain cryptography. | Python, Flask, SHA-256 |
| [Pa11y Accessibility Audit](software-development/pa11y-accessibility-audit/) | Automated WCAG accessibility audit of 18 pages of a public government website, with a summary of the findings. | pa11y, Bash, WCAG 2 AA |
| [Python GUI Apps](software-development/python-gui-apps/) | Desktop GUI programs: a flight reservation form, a kilometers-to-miles converter, a geometry calculator, multi-window demos and SQLite schema scripts. | PySimpleGUI, SQLite |
| [Java Rummy Card Game](software-development/java-rummy-card-game/) | Two-player Swing card game with custom deck, hand, set and stack abstractions; original course-framework attribution and GPL license preserved. | Java, Swing, object-oriented design |

### Bioinformatics

| Project | Description | Tech |
|---|---|---|
| [Motif Scripts](bioinformatics/bioinformatics-motif-scripts/) | Converts MOODS motif-scan results into color-coded BED tracks for genome browsers, plus a recursive Fast Fourier Transform. | Python |

## Group projects

These team projects live in private class organization repositories, so they aren't copied here.

- **PICC Website:** a Laravel web application for a community organization, built by a student team.
- **Mental Health and Its Relationship With The Economy:** a team data science project. My individual part is in [data-science/mental-health-suicide-analysis](data-science/mental-health-suicide-analysis/).

## Related repositories

- [NVSRCO](https://github.com/joserico00/NVSRCO): Network Vulnerability Scanner for Resource-Constrained Organizations (graduate project)
- [Deep Learning for Malicious Traffic Detection](https://github.com/joserico00/Deep-Learning-for-Malicious-Traffic-Detection)
- [Intro to HPC Bootcamp 2023: Power Outages](https://github.com/joserico00/Intro-to-HPC-Bootcamp-2023-Power-Outages): how the June 2016 Southwest heatwave and power outages affected people who rely on electricity-dependent medical equipment, analyzed on NERSC Perlmutter
- [Intro to HPC Bootcamp 2025: Fusion Energy Workloads](https://github.com/joserico00/Intro-to-HPC-Bootcamp-2025-Fusion-Energy-Workloads): power consumption, TOP500 energy efficiency, and fusion workload energy metrics with a 4.8 MW job scheduler
- [Seniory](https://github.com/joserico00/Seniory): elder care desktop app built for a hackathon

## Notes

- **Security tools:** the scanners and sniffers are for networks you own or are authorized to test.
- **Credentials:** API keys and passwords are read from environment variables. See each project's README.
- **Data:** large datasets and scan results from real networks are not included. Each README lists what's needed.

## Author

Jose E. Rodriguez Rios · [github.com/joserico00](https://github.com/joserico00)
