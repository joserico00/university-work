# Data Science Notebooks

A collection of Jupyter notebooks from data science courses, training projects and personal practice. They cover **data cleaning and wrangling with pandas**, **exploratory and geographic visualization** (matplotlib, seaborn, Plotly, GeoPandas/folium), **statistics** (confidence intervals, correlation, R², t-tests), **clustering** (K-means with elbow and silhouette methods), small **machine learning** experiments (support vector regression), and HPC-related work (a power-outage/heatwave analysis run on NERSC Perlmutter and a power-capped fusion-workload scheduler). Many course notebooks have **Spanish** narration and comments.

Each folder has its own README with detailed notes for every notebook:

| Folder | What's inside | Details |
|---|---|---|
| [`coursework/`](coursework/) | pandas data structures, cleaning and wrangling (including an airline-connection search), matplotlib/seaborn/Plotly visualization, the Matplotlib plot-types gallery, a notebook-merging utility | [coursework/README.md](coursework/README.md) |
| [`confidence-intervals-clustering/`](confidence-intervals-clustering/) | 95% CI for a difference of means (Titanic ages), K-means introduction, silhouette scores | [confidence-intervals-clustering/README.md](confidence-intervals-clustering/README.md) |
| [`misc/`](misc/) | Heatwave, power-outage and medically vulnerable population project; fusion/HPC workload metrics and scheduler; network-traffic and malware data prep; regression, correlation and exam notebooks; Gapminder and World Happiness visualizations; quick tests | [misc/README.md](misc/README.md) |

---

## Notebook index

### `coursework/`

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| [Pandas Data Structures - A](coursework/Pandas%20Data%20Structures%20-%20A.ipynb) | Series/DataFrame basics | Indexing, `%timeit`, NumPy vs. pandas file I/O, add columns/rows | pandas, numpy |
| [Pandas Data Structures - B](coursework/Pandas%20Data%20Structures%20-%20B.ipynb) | Stats and filtering on a 140-country happiness table | `mean`, `sum(axis)`, `idxmin`, boolean `loc` | pandas |
| [dataCleaningandWrang](coursework/dataCleaningandWrang.ipynb) | Missing values, duplicates, replacement | `dropna`, `fillna`, `drop_duplicates`, `replace` | pandas, numpy |
| [dataCleaningandWrang2](coursework/dataCleaningandWrang2.ipynb%20) | Exact duplicate of the above (the file name ends in a space) | none | none |
| [dataWrang-Asignacion](coursework/dataWrang-Asignacion.ipynb) | Airline schedule cleaning; SJU→TUS one-stop search | `skiprows`/`skipfooter`, header merge, `isin`, `merge` | pandas |
| [dataWrang-Cont](coursework/dataWrang-Cont.ipynb) | Connection search with time parsing | `to_datetime`, set intersection, min connection time, cross merge | pandas |
| [dataWrang_Final](coursework/dataWrang_Final.ipynb) | Group-by, pivot, join | `map`, `groupby`, `pivot`, `join` | pandas |
| [covid dataframe](coursework/covid%20dataframe.ipynb) | U.S. county COVID-19 tables, 2020–2021 | `fillna`, `merge`, `join`, `pivot_table` | pandas |
| [datascience project](coursework/datascience%20project.ipynb) | CDC suicide data + EM-DAT disasters (project start) | `read_csv`, `read_excel`, xlsx to csv | pandas |
| [visualization_Part1](coursework/visualization_Part1.ipynb) | matplotlib fundamentals | Subplots, styles, ticks, legends | matplotlib |
| [Viz3](coursework/Viz3.ipynb) | Color by group, seaborn, Plotly choropleths | `hue`, `px.choropleth`, derived prison-fraction column | seaborn, plotly |
| [plot_types_jupyter/](coursework/plot_types_jupyter/) | 33 Matplotlib gallery notebooks | basic, arrays, stats, unstructured, 3D | matplotlib |
| [union](coursework/union.ipynb) / [unionlibrary.py](coursework/unionlibrary.py) | Concatenate notebooks in a folder | `nbformat` | nbformat |
| [merged_notebook](coursework/merged_notebook.ipynb), [merged_notebookpart1](coursework/merged_notebookpart1.ipynb) | Auto-generated concatenations of the notebooks above | none | none |

### `confidence-intervals-clustering/`

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| [confInt _ and_Cluster](confidence-intervals-clustering/confInt%20_%20and_Cluster.ipynb) | CI for difference of mean ages; K-means intro | z-interval, `make_blobs`, `KMeans` | scipy, scikit-learn |
| [silkmeans](confidence-intervals-clustering/silkmeans.ipynb) | Silhouette score (errored in the saved run) | `KMeans`, `silhouette_score` | scikit-learn |
| [silkmeans-Copy1](confidence-intervals-clustering/silkmeans-Copy1.ipynb) | Silhouette on uniform random data (different code, not a copy) | `KMeans`, `silhouette_score` | scikit-learn |
| [silkmeansresults](confidence-intervals-clustering/silkmeansresults.ipynb) | Silhouette score over k = 2 to 9 | `KMeans`, `silhouette_score` | scikit-learn |

### `misc/`

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| [1_Exploring_Datasets](misc/1_Exploring_Datasets.ipynb) | Heatwave project: Google Sheets guide | Markdown only | none |
| [2_Python_Pandas_Intro](misc/2_Python_Pandas_Intro.ipynb) | Heatwave project: pandas tutorial | `loc`, plots, FIPS `merge` | pandas |
| [3_Time_Series_Data](misc/3_Time_Series_Data.ipynb) | Heatwave project: EAGLE-i outage time series | Up-sampling with `interp1d`, `groupby().agg` | pandas, scipy |
| [4_CorrelationAnalysis](misc/4_CorrelationAnalysis.ipynb) | Heatwave project: correlation tutorial | Spearman, p-values, correlation heatmap | scipy, seaborn |
| [5_Drawing_Maps](misc/5_Drawing_Maps.ipynb) | Heatwave project: county maps | `sjoin`, `explore()` | geopandas, folium |
| [6_MPI_Intro](misc/6_MPI_Intro.ipynb) | Heatwave project: pointer to mpi4py exercises | Markdown only | none |
| [7_Big_Questions](misc/7_Big_Questions.ipynb) | Heatwave project: research questions | Markdown only | none |
| [realwork](misc/realwork.ipynb) | **Author's heatwave, outage and DME analysis** (NERSC Perlmutter) | Heatwave vs. baseline, Spearman tests, maps | pandas, scipy, geopandas |
| [CleanedmergedDataset](misc/CleanedmergedDataset.ipynb) | Fusion/non-fusion project energy metrics | Derived kWh/science/cost, key-based outer merge | pandas |
| [CleanedDataset](misc/CleanedDataset.ipynb) | Near-duplicate of CleanedmergedDataset | none | pandas |
| [scheduler](misc/scheduler.ipynb) | Greedy fusion-job scheduler under a 4.8 MW cap | Priority score, cycle packing, timeline charts | pandas, matplotlib |
| [simpleIntroToVisualization](misc/simpleIntroToVisualization.ipynb) | Scientific computing and visualization tutorial | NumPy, pandas, matplotlib, 3D, animation, GeoPandas | numpy, pandas, matplotlib |
| [1-initial-data-cleaning](misc/1-initial-data-cleaning.ipynb) | Cleaning a labeled Zeek connection log | Column split, drop IDs/constants, NaN placeholders | pandas |
| [Malwaredataset](misc/Malwaredataset.ipynb) | PE-header malware dataset exploration | Derived column, sorting | pandas |
| [coefDet](misc/coefDet.ipynb) / [coefDet2](misc/coefDet2.ipynb) | Coefficient of determination | `LinearRegression`, manual R² | scikit-learn |
| [data-analysis-exam](misc/data-analysis-exam.ipynb) | Exam: letter grades, t-test | `melt`, `unstack`, `ttest_ind` | pandas, scipy |
| [cluster_goodOfFit](misc/cluster_goodOfFit.ipynb) | K-means elbow and silhouette methods | Inertia, `silhouette_score` | scikit-learn |
| [AmazonStockSVM](misc/AmazonStockSVM.ipynb) | AMZN close-price SVR (April 2022) | Linear and RBF `SVR` | scikit-learn |
| [JoseHWGapminder](misc/JoseHWGapminder.ipynb) | Gapminder bubble chart, 2007 and 2011 | seaborn, `melt`/`merge`, annotations | seaborn, pandas |
| [happyness](misc/happyness.ipynb) | World Happiness Report 2017 choropleths | GeoPandas merge, normalization | geopandas |
| [visualization](misc/visualization.ipynb) | matplotlib subplot practice | `add_subplot`, `subplots` | matplotlib |
| [pandas data structure](misc/pandas%20data%20structure.ipynb) | Series/DataFrame practice | Indexing, file I/O | pandas |
| [clase de marzo 1 2023](misc/clase%20de%20marzo%201%202023.ipynb) | In-class airline schedule wrangling | `skiprows`/`skipfooter`, filtering | pandas |
| [datascience](misc/datascience.ipynb) | xlsx to csv; NumPy stats | `read_excel`, `np.std` | pandas, numpy |
| [Biopython testing](misc/Biopython%20testing.ipynb) | Quick Biopython test | `Seq.complement` | biopython |
| [stockpredicate](misc/stockpredicate.ipynb) | Running median of simulated prices (no prediction) | Timed loop | numpy |
| [student-merge.R](misc/student-merge.R) | Merge two student CSVs in R | `merge` | base R |

---

## Selected results (from saved outputs)

- **Titanic ages:** 95% CI for survivors minus non-survivors = **[−4.47, −0.10]** years (survivor mean 28.34 vs. 30.63).
- **Heatwave project (`realwork`):** Spearman rho between June 2016 DME-reliant population and mean outages during June 19–20 across Southwest counties = **0.827 (p = 6.2 × 10⁻⁷)**. Hottest county temperature was **102.1 °F** (Yuma and La Paz, AZ, June 20).
- **Movies tutorial:** Spearman(gross profit, box-office multiplier) = **0.839 (p = 7.3 × 10⁻⁶)**. Spearman(budget, gross profit) = −0.164 (p = 0.50).
- **Buildings regression (`coefDet`):** height vs. stories, **R² = 0.904**, r = 0.951.
- **Exam t-test:** semester grade means 71.19 vs. 72.44, **p = 0.772**.
- **K-means silhouette:** 0.558 (3 blobs, k = 3), 0.378 (uniform data, k = 3).
- **Fusion scheduler:** 153 CPU/GPU/HYBRID jobs packed under 4.8 MW, from 2025-08-15 09:00 to 2025-08-17 05:07 (UTC−5).

---

## Data availability

**Included**

| File | Description |
|---|---|
| `coursework/suicides.csv` | U.S. suicide deaths by state, 2001–2020, from the CDC National Center for Injury Prevention and Control ([WISQARS](https://wisqars.cdc.gov/)) |
| `coursework/disasters.xlsx`, `coursework/Test.csv` | [EM-DAT](https://www.emdat.be/) export of U.S. and Puerto Rico disasters, 1960–2023, with its CSV conversion |
| `coursework/datasets/iris.csv` | Iris dataset (150 rows) |
| `coursework/datasets/2012_Election_Data.csv` | 2012 U.S. turnout and eligibility by state (51 rows) |
| `confidence-intervals-clustering/titanic_data.csv` | Titanic passengers with recorded age (714 rows) |

**Referenced but not included.** The full per-notebook list is in each folder's README. Main examples:
- the heatwave project `data/` folder: EAGLE-i outages, county temperatures, HHS emPOWER workbook, population, demographics
- fusion/NERSC project CSVs
- `conn.log.labeled`, `kaggle-data.csv`, `AMZN20233.csv`
- the Gapminder CSVs, `happiness_2017.csv`
- `ConfirmedFSMarch2023.csv`, `us-counties-2020.csv` / `us-counties-2021.csv`, `index.txt`, `data_B.csv`

Where a notebook names its source, the folder README links to it.

---

## Requirements

```bash
pip install jupyter pandas numpy scipy matplotlib seaborn scikit-learn plotly \
            openpyxl geopandas folium nbformat biopython
```

For `misc/student-merge.R`, base R is enough.

**Version notes**
- `DataFrame.append` (in `coursework/Pandas Data Structures - A` and `misc/coefDet`) was removed in **pandas 2.0**. Use pandas < 2 or replace it with `pd.concat`.
- `gpd.datasets.get_path('naturalearth_lowres')` (in `misc/happyness` and `misc/simpleIntroToVisualization`) was removed in **GeoPandas 1.0**. Use geopandas < 1 or load Natural Earth separately.
- `KMeans(n_init='auto')` needs scikit-learn ≥ 1.2.
- `fillna(method=...)` is deprecated in recent pandas.
- No GPU is needed. `misc/JoseHWGapminder` and `misc/AmazonStockSVM` carry Colab metadata but do not mount Google Drive. `misc/realwork` was run on NERSC Perlmutter, but it runs on any machine with the data.

## How to run

```bash
git clone <this-repo>
cd data-science-notebooks
jupyter lab
```

1. Open a notebook from the folder it lives in, because relative paths such as `suicides.csv` or `data/...` assume that working directory.
2. Put any missing data files at the paths listed in that folder's README.
3. Data paths in the notebooks are relative (for example `datasets/iris.csv`, `ranDat.csv`, `index.txt`), so they resolve against the notebook's own folder.
4. Several notebooks have saved errors or cells that were executed out of order. These are noted per notebook in the folder READMEs.

## Related

- The fusion-workload notebooks in `misc/` go with Module 5 of the author's `hpc-bootcamp-2025` repository.
- `misc/1-initial-data-cleaning.ipynb` prepares the same connection-log format that is modeled with a Transformer in the author's `deep-learning-coursework` repository.

## Author

Jose E. Rodriguez Rios
