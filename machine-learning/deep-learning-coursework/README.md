# Deep Learning Coursework

This folder contains a PyTorch softmax-regression assignment on Fashion-MNIST. An early network-traffic Transformer and an unfinished image-loader script are preserved under [`archive/`](archive/) as coursework drafts rather than portfolio-ready implementations.

The corrected and expanded network-traffic project lives in [Deep Learning for Malicious Traffic Detection](https://github.com/joserico00/Deep-Learning-for-Malicious-Traffic-Detection). That repository uses IoT-23 capture-level splitting, train-only preprocessing, a conventional baseline, and class-sensitive evaluation.

## Fashion-MNIST assignment

[`Jose_E_Rodriguez_Rios_Homework_deeplearning_1.ipynb`](Jose_E_Rodriguez_Rios_Homework_deeplearning_1.ipynb) explores softmax regression with the *Dive into Deep Learning* library. It varies training duration and learning rate while plotting training loss, validation loss, and validation accuracy.

The notebook downloads Fashion-MNIST automatically through `torchvision`: 60,000 training images and 10,000 validation images across ten clothing categories.

### Saved experiments

| Learning rate | Epochs |
|---:|---:|
| 0.1 | 10, 30, 60 |
| 0.01 | 30, 60 |
| 0.05 | 30 |
| 0.3, 0.6, 0.9, 1.0, 0.09, 0.01, 0.001 | 10 each |

The written conclusion attributes declining validation performance during long runs to overfitting and observes that very small learning rates require more epochs.

### Reproduction notes

- The notebook pins `d2l==1.0.3`, which expects older scientific Python packages. Use a separate environment or Colab runtime.
- Several written answers were entered into code cells, and one saved cell contains an incomplete `lr=` argument. Skip or convert those cells to Markdown before running the notebook from top to bottom.
- The saved training curves document the original assignment, but the notebook does not print a final numeric accuracy table.

## Historical drafts

| File | Status |
|---|---|
| [`archive/transformer-network-traffic-draft.ipynb`](archive/transformer-network-traffic-draft.ipynb) | Early IoT-23 classifier with target leakage, preprocessing before the split, a sequence length of one, and a misspelled loss name. Its saved 99.97% test accuracy is not a credible generalization result. |
| [`archive/malimg-loader-stub.py`](archive/malimg-loader-stub.py) | Incomplete `ImageFolder` loader retained only as a draft; `transform` is undefined. |

These drafts should not be used as the primary portfolio examples. The standalone malicious-traffic repository supersedes the Transformer notebook, and the separate [Malware Image Classification](../malware-image-classification/) project supersedes the loader stub.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install d2l==1.0.3 torch torchvision
jupyter lab
```

## Author

Jose E. Rodriguez Rios
