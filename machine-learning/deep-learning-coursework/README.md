# Deep Learning Coursework

Deep learning coursework notebooks. The first is a PyTorch softmax-regression homework on Fashion-MNIST, built on the *Dive into Deep Learning* (`d2l`) library, that studies how the number of epochs and the learning rate affect training. The second is a TensorFlow/Keras Transformer-encoder classifier that separates **benign from malicious network connections** in a labeled Zeek-style connection log. The repo also holds a short, unfinished PyTorch script for loading an image dataset.

Both notebooks were run in Google Colab, and the Transformer notebook was run on a T4 GPU runtime.

---

## Contents

| File | Topic | Techniques | Key libraries |
|---|---|---|---|
| [`Jose_E_Rodriguez_Rios_Homework_deeplearning_1.ipynb`](Jose_E_Rodriguez_Rios_Homework_deeplearning_1.ipynb) | Fashion-MNIST image classification | Softmax regression (flatten + linear), cross-entropy, minibatch SGD, learning-rate and epoch sweeps | `torch`, `torchvision`, `d2l==1.0.3` |
| [`Transformer.ipynb`](Transformer.ipynb) | Network-traffic classification (benign vs. malicious) | Cleaning Zeek conn-log fields, IQR capping, KNN imputation, decision-tree imputation, one-hot encoding, scaling, single-block Transformer encoder, binary cross-entropy | `tensorflow`/`keras`, `scikit-learn`, `pandas`, `seaborn` |
| [`machineln.py`](machineln.py) | Image dataset loading (stub) | `torchvision.datasets.ImageFolder` | `torch`, `torchvision` |

---

## 1. Softmax regression on Fashion-MNIST

**File:** `Jose_E_Rodriguez_Rios_Homework_deeplearning_1.ipynb`

### Goal
Implement the softmax-regression classifier from the `d2l` library, then answer two questions by experiment:
1. Why might validation accuracy drop when you train for more epochs, and how can you fix it?
2. What happens as the learning rate increases, and which learning rate works best?

### Data
- **Fashion-MNIST**, downloaded automatically by `torchvision.datasets.FashionMNIST(download=True)`: 60,000 training and 10,000 validation 28×28 grayscale images in 10 clothing classes (t-shirt, trouser, pullover, dress, coat, sandal, shirt, sneaker, bag, ankle boot).
- Nothing needs to be downloaded by hand.

### What the code does
1. Installs `d2l==1.0.3` and imports `torch`, `torchvision` and `d2l`.
2. Defines a `FashionMNIST(d2l.DataModule)` that applies `Resize` and `ToTensor` and builds train/val `DataLoader`s. With `resize=(32, 32)` the saved output confirms 60,000/10,000 samples, images shaped `torch.Size([1, 32, 32])`, and batches of `[64, 1, 32, 32]`. One full pass over the training loader took 12.67 s in the saved run.
3. Adds `text_labels` and `visualize` helpers and plots one validation batch of 8 labeled images.
4. Defines the model `SoftmaxRegression(d2l.Classifier)` as `nn.Sequential(nn.Flatten(), nn.LazyLinear(10))`.
5. Overrides `Classifier.loss` with `F.cross_entropy` (mean reduction).
6. Trains with `d2l.Trainer` on `d2l.FashionMNIST(batch_size=256)`. The optimizer is `d2l.Classifier`'s default minibatch SGD, and `d2l`'s progress board plots training loss, validation loss and validation accuracy per epoch.

### Experiments in the saved notebook

| Cell | Learning rate | Epochs |
|---|---|---|
| 13 | 0.1 | 10 |
| 15 | 0.1 | 30 |
| 16 | 0.1 | 60 |
| 18 | 0.01 | 30 |
| 20 | 0.01 | 60 |
| 21 | 0.05 | 30 |
| 23 to 29 | 0.3, 0.6, 0.9, 1.0, 0.09, 0.01, 0.001 | 10 |

The results are saved only as training-curve figures (SVG). No numeric accuracy values are printed.

### Written answers (in the notebook)
- **More epochs:** the author attributes the drop in validation accuracy to overfitting and suggests lowering the learning rate or stopping early.
- **Learning rate:** the author concludes that a low rate around 0.1 converges smoothly without loss spikes, and that rates below 0.01 need more epochs.

### Notes
- The answers in cells 14, 17 and 30 are written as prose inside **code** cells, and cell 19 has an incomplete argument (`lr=)`). Running those cells as saved raises a `SyntaxError`, but their saved figures are from an earlier run. Cell 3 is empty, and `show_images` in cell 9 is a `NotImplementedError` stub that is never called (plotting uses `d2l.show_images`).
- `d2l==1.0.3` pins older versions of `numpy`, `pandas`, `matplotlib` and `scipy`. A fresh virtual environment or Colab is recommended.

---

## 2. Transformer encoder for network-traffic classification

**File:** `Transformer.ipynb`

### Goal
Train a small Transformer-encoder model that predicts whether a network connection is **Benign (0)** or **Malicious (1)** from connection-level features.

### Data
- `conn.log.labeled`: a tab-separated, Zeek-format connection log with `label` and detailed-label columns. The notebook reads it from the working directory (`./`).
- The notebook does not name a public source, and **the file is not included in this project**.
- Saved output: **23,145 rows × 23 columns**, with 21,222 Malicious and 1,923 Benign connections. The detailed labels are `C&C`, `PartOfAHorizontalPortScan`, `DDoS`, or unset.
- The notebook also mounts Google Drive (`/content/drive`), but it reads the data file from the working directory.

### What the code does
1. **Load:** reads the column names from the commented header line (`skiprows=6, nrows=1`), then reads the data with `comment="#"`.
2. **Inspect:** `shape`, `head`, `info`, unique values of `det_label`, and `nunique()` per column. `ts` and `uid` are unique on every row, while `local_orig`, `local_resp` and `tunnel_parents` carry no information.
3. **Clean:**
   - Replaces the placeholders `'-'` and `'(empty)'` with `NaN`.
   - Converts `duration`, `orig_bytes` and `resp_bytes` to numbers.
   - Drops `uid`, `ts`, the source/destination IP addresses, `local_orig`, `local_resp` and `tunnel_parents`.
   - Leaves 16 columns. Missing values remain in `service` (21,298), `duration`/`orig_bytes`/`resp_bytes` (17,824 each) and `det_label` (1,923), visualized as a `seaborn` null heatmap.
4. **Encode the target:** `LabelEncoder` maps `{'Benign': 0, 'Malicious': 1}`.
5. **Handle outliers:** caps `duration` at the IQR fences (Q1 − 1.5·IQR, Q3 + 1.5·IQR).
6. **Impute:**
   - `KNNImputer(n_neighbors=3)` fills the numeric features.
   - A `DecisionTreeClassifier` trained on the numeric features predicts the missing `service` values.
7. **Scale and encode:** `MinMaxScaler` on the numeric features, then `OneHotEncoder` on `proto`, `service`, `conn_state`, `history` and `det_label`, giving **52 features**.
8. **Split:** 70% train, 15% validation, 15% test (`random_state=42`): 16,201 / 3,472 / 3,472 rows. Features are standardized with `StandardScaler` and reshaped to `(batch, 1, 52)`, so each connection is a sequence of length 1.
9. **Model** (`build_transformer_model`):

| Layer | Output shape | Params |
|---|---|---|
| Input | (None, 1, 52) | 0 |
| MultiHeadAttention (4 heads, `key_dim=52`), self-attention | (None, 1, 52) | 43,940 |
| Add (residual) + LayerNormalization | (None, 1, 52) | 104 |
| Dense(64, ReLU) | (None, 1, 64) | 3,392 |
| Dense(52) | (None, 1, 52) | 3,380 |
| Add (residual) + LayerNormalization | (None, 1, 52) | 104 |
| Flatten | (None, 52) | 0 |
| Dense(1, sigmoid) | (None, 1) | 53 |
| **Total** | | **50,973 trainable** |

10. **Training:** Adam optimizer, binary cross-entropy loss, accuracy metric, 10 epochs, batch size 32, with the validation set passed to `fit`. Accuracy and loss curves are plotted for train and validation.
11. **Evaluation:** test accuracy, a correlation of each feature with the label, `classification_report` and `confusion_matrix`.

### Results in the saved run
- Validation accuracy was 1.0000 from epoch 1. Validation loss after epoch 10 was 2.80e-06.
- **Test accuracy: 99.97%**
- Confusion matrix on the test set (rows are true labels, columns are predictions):

|            | Pred 0 | Pred 1 |
|---|---|---|
| **True 0** | 295 | 1 |
| **True 1** | 0 | 3,176 |

### Notes for interpreting the results
- **Label leakage:** the one-hot `det_label_*` columns come from the detailed label and are kept as input features. The saved feature-to-label correlations show `det_label_nan` at **−1.0**, meaning it exactly marks the Benign rows (1,923 of each), and `proto_tcp`/`proto_udp` at ±0.97. The near-perfect score should be read with this in mind. Dropping `det_label` before encoding would give a harder, more realistic task.
- **Preprocessing before the split:** the KNN imputer, decision-tree imputer and MinMax scaler are fitted on the full dataset before the train/validation/test split.
- **Sequence length 1:** attention over a length-1 sequence always has weight 1. Keras warns about this ("softmax over axis ... of size 1"), and the attention block effectively acts as a learned linear projection.
- **Misspelled loss:** the `compile` cell as saved passes `loss='binaroy_crssentropy'`, so re-running it will likely fail until it is corrected to `'binary_crossentropy'`. The saved training log came from a run with a working loss.
- Cells 55 to 70 are empty.

---

## 3. `machineln.py`

A stub for loading an image-classification dataset with PyTorch:

- Imports `torch`, `Dataset`, `torchvision.datasets`, `ToTensor` and `matplotlib`.
- Creates `datasets.ImageFolder("malimg_paper_dataset_imgs", transform=transform)`.

The script is incomplete: `transform` is never defined, so it raises a `NameError` as written. The image folder `malimg_paper_dataset_imgs/` (one subfolder per class) is not included.

---

## Data availability

| File | Used by | In repo? |
|---|---|---|
| Fashion-MNIST | Homework notebook | Downloaded automatically by `torchvision` |
| `conn.log.labeled` | `Transformer.ipynb` | **Missing** |
| `malimg_paper_dataset_imgs/` | `machineln.py` | **Missing** |

## Requirements

```bash
# Homework notebook (a separate environment is recommended because of d2l's pins)
pip install d2l==1.0.3 torch torchvision

# Transformer notebook
pip install tensorflow pandas numpy scikit-learn matplotlib seaborn
```

- **Colab / GPU:** both notebooks were run in Google Colab. `Transformer.ipynb` was saved with a T4 GPU runtime and runs `google.colab.drive.mount`. Remove that cell to run locally.
- The saved Transformer run used TensorFlow 2.17.1 (Keras 3), pandas 2.2.2, NumPy 1.26.4 and scikit-learn 1.5.2.

## How to run

1. **Homework:** open the notebook in Colab or Jupyter and run all cells. The first cell installs `d2l`, and Fashion-MNIST downloads on first use. Fix or skip cells 14, 17, 19 and 30 (see Notes).
2. **Transformer:**
   - Put `conn.log.labeled` in the notebook's working directory. In Colab, upload it or `cd` into the Drive folder that holds it.
   - Correct the loss name in the `compile` cell.
   - Run all cells. A GPU is optional for a model this size.

## Author

Jose E. Rodriguez Rios
