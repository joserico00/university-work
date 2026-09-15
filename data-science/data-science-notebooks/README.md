# Data Science Notebooks

A collection of Jupyter notebooks from data science courses, training projects and personal practice. They cover **data cleaning and wrangling with pandas**, **exploratory and geographic visualization** (matplotlib, seaborn, Plotly, GeoPandas), **statistics** (confidence intervals, correlation, R²), **clustering** (K-means with elbow and silhouette methods), small **machine learning** experiments (support vector regression), and network-traffic and malware data preparation. Many course notebooks have **Spanish** narration and comments.

Each folder has its own README with detailed notes for every notebook:

| Folder | What's inside | Details |
|---|---|---|
| [`coursework/`](coursework/) | pandas data structures, cleaning and wrangling (including an airline-connection search), matplotlib/seaborn/Plotly visualization, the Matplotlib plot-types gallery, a notebook-merging utility | [coursework/README.md](coursework/README.md) |
| [`confidence-intervals-clustering/`](confidence-intervals-clustering/) | 95% CI for a difference of means (Titanic ages), K-means introduction, silhouette scores | [confidence-intervals-clustering/README.md](confidence-intervals-clustering/README.md) |
| [`misc/`](misc/) | Network-traffic and malware data prep; regression, correlation and exam notebooks; Gapminder and World Happiness visualizations; quick tests | [misc/README.md](misc/README.md) |

---

## Notebook index

### `coursework/`

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| [pandas_series_and_dataframes](coursework/pandas_series_and_dataframes.ipynb) | Series/DataFrame basics | Indexing, `%timeit`, NumPy vs. pandas file I/O, add columns/rows | pandas, numpy |
| [pandas_statistics_and_filtering](coursework/pandas_statistics_and_filtering.ipynb) | Stats and filtering on a 140-country happiness table | `mean`, `sum(axis)`, `idxmin`, boolean `loc` | pandas |
| [data_cleaning_missing_values_duplicates](coursework/data_cleaning_missing_values_duplicates.ipynb) | Missing values, duplicates, replacement | `dropna`, `fillna`, `drop_duplicates`, `replace` | pandas, numpy |
| [airline_schedule_wrangling_assignment](coursework/airline_schedule_wrangling_assignment.ipynb) | Airline schedule cleaning; SJU→TUS one-stop search | `skiprows`/`skipfooter`, header merge, `isin`, `merge` | pandas |
| [airline_connections_wrangling](coursework/airline_connections_wrangling.ipynb) | Connection search with time parsing | `to_datetime`, set intersection, min connection time, cross merge | pandas |
| [groupby_pivot_join](coursework/groupby_pivot_join.ipynb) | Group-by, pivot, join | `map`, `groupby`, `pivot`, `join` | pandas |
| [covid_county_cases](coursework/covid_county_cases.ipynb) | U.S. county COVID-19 tables, 2020–2021 | `fillna`, `merge`, `join`, `pivot_table` | pandas |
| [suicide_disasters_project_start](coursework/suicide_disasters_project_start.ipynb) | CDC suicide data + EM-DAT disasters (project start) | `read_csv`, `read_excel`, xlsx to csv | pandas |
| [matplotlib_fundamentals](coursework/matplotlib_fundamentals.ipynb) | matplotlib fundamentals | Subplots, styles, ticks, legends | matplotlib |
| [seaborn_plotly_choropleths](coursework/seaborn_plotly_choropleths.ipynb) | Color by group, seaborn, Plotly choropleths | `hue`, `px.choropleth`, derived prison-fraction column | seaborn, plotly |
| [matplotlib_plot_types/](coursework/matplotlib_plot_types/) | 31 Matplotlib gallery notebooks | basic, arrays, stats, unstructured, 3D | matplotlib |
| [merge_notebooks](coursework/merge_notebooks.ipynb) / [merge_notebooks.py](coursework/merge_notebooks.py) | Concatenate notebooks in a folder | `nbformat` | nbformat |
| [merged_notebook](coursework/merged_notebook.ipynb), [merged_notebookpart1](coursework/merged_notebookpart1.ipynb) | Auto-generated concatenations of the notebooks above | none | none |

### `confidence-intervals-clustering/`

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| [confidence_intervals_and_kmeans](confidence-intervals-clustering/confidence_intervals_and_kmeans.ipynb) | CI for difference of mean ages; K-means intro | z-interval, `make_blobs`, `KMeans` | scipy, scikit-learn |
| [silhouette_score_first_attempt](confidence-intervals-clustering/silhouette_score_first_attempt.ipynb) | Silhouette score (errored in the saved run) | `KMeans`, `silhouette_score` | scikit-learn |
| [silhouette_score_uniform_data](confidence-intervals-clustering/silhouette_score_uniform_data.ipynb) | Silhouette on uniform random data | `KMeans`, `silhouette_score` | scikit-learn |
| [silhouette_choosing_k](confidence-intervals-clustering/silhouette_choosing_k.ipynb) | Silhouette score over k = 2 to 9 | `KMeans`, `silhouette_score` | scikit-learn |

### `misc/`

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| [zeek_conn_log_data_cleaning](misc/zeek_conn_log_data_cleaning.ipynb) | Cleaning a labeled Zeek connection log | Column split, drop IDs/constants, NaN placeholders | pandas |
| [malware_pe_dataset_exploration](misc/malware_pe_dataset_exploration.ipynb) | PE-header malware dataset exploration | Derived column, sorting | pandas |
| [coefficient_of_determination](misc/coefficient_of_determination.ipynb) / [coefficient_of_determination_short](misc/coefficient_of_determination_short.ipynb) | Coefficient of determination | `LinearRegression`, manual R² | scikit-learn |
| [kmeans_goodness_of_fit](misc/kmeans_goodness_of_fit.ipynb) | K-means elbow and silhouette methods | Inertia, `silhouette_score` | scikit-learn |
| [amazon_stock_svr](misc/amazon_stock_svr.ipynb) | AMZN close-price SVR (April 2022) | Linear and RBF `SVR` | scikit-learn |
| [gapminder_health_vs_wealth](misc/gapminder_health_vs_wealth.ipynb) | Gapminder bubble chart, 2007 and 2011 | seaborn, `melt`/`merge`, annotations | seaborn, pandas |
| [world_happiness_2017_maps](misc/world_happiness_2017_maps.ipynb) | World Happiness Report 2017 choropleths | GeoPandas merge, normalization | geopandas |
| [matplotlib_subplots_practice](misc/matplotlib_subplots_practice.ipynb) | matplotlib subplot practice | `add_subplot`, `subplots` | matplotlib |
| [pandas_data_structures_practice](misc/pandas_data_structures_practice.ipynb) | Series/DataFrame practice | Indexing, file I/O | pandas |
| [airline_schedule_in_class](misc/airline_schedule_in_class.ipynb) | In-class airline schedule wrangling | `skiprows`/`skipfooter`, filtering | pandas |
| [xlsx_to_csv_and_numpy_stats](misc/xlsx_to_csv_and_numpy_stats.ipynb) | xlsx to csv; NumPy stats | `read_excel`, `np.std` | pandas, numpy |
| [biopython_sequence_test](misc/biopython_sequence_test.ipynb) | Quick Biopython test | `Seq.complement` | biopython |
| [streaming_median_prices](misc/streaming_median_prices.ipynb) | Running median of simulated prices | Timed loop | numpy |
| [merge_student_data.R](misc/merge_student_data.R) | Merge two student CSVs in R | `merge` | base R |

---

## Selected results (from saved outputs)

- **Titanic ages:** 95% CI for survivors minus non-survivors = **[−4.47, −0.10]** years (survivor mean 28.34 vs. 30.63).
- **Buildings regression (`coefficient_of_determination`):** height vs. stories, **R² = 0.904**, r = 0.951.
- **K-means silhouette:** 0.558 (3 blobs, k = 3), 0.378 (uniform data, k = 3).

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
- `conn.log.labeled`, `kaggle-data.csv`, `AMZN20233.csv`
- the Gapminder CSVs, `happiness_2017.csv`
- `ConfirmedFSMarch2023.csv`, `us-counties-2020.csv` / `us-counties-2021.csv`, `index.txt`

Where a notebook names its source, the folder README links to it.

---

## Requirements

```bash
pip install jupyter pandas numpy scipy matplotlib seaborn scikit-learn plotly \
            openpyxl geopandas nbformat biopython
```

For `misc/merge_student_data.R`, base R is enough.

**Version notes**
- `DataFrame.append` (in `coursework/pandas_series_and_dataframes` and `misc/coefficient_of_determination`) was removed in **pandas 2.0**. Use pandas < 2 or replace it with `pd.concat`.
- `gpd.datasets.get_path('naturalearth_lowres')` (in `misc/world_happiness_2017_maps`) was removed in **GeoPandas 1.0**. Use geopandas < 1 or load Natural Earth separately.
- `KMeans(n_init='auto')` needs scikit-learn ≥ 1.2.
- `fillna(method=...)` is deprecated in recent pandas.
- No GPU is needed. `misc/gapminder_health_vs_wealth` and `misc/amazon_stock_svr` carry Colab metadata but do not mount Google Drive.

## How to run

```bash
git clone <this-repo>
cd data-science-notebooks
jupyter lab
```

1. Open a notebook from the folder it lives in, because relative paths such as `suicides.csv` or `index.txt` assume that working directory.
2. Put any missing data files at the paths listed in that folder's README.
3. Data paths in the notebooks are relative (for example `datasets/iris.csv`, `ranDat.csv`, `index.txt`), so they resolve against the notebook's own folder.
4. Several notebooks have saved errors or cells that were executed out of order. These are noted per notebook in the folder READMEs.

## Related repositories

The Intro to HPC Bootcamp notebooks that used to be in `misc/` now have their own repositories:
- [Intro-to-HPC-Bootcamp-2023-Power-Outages](https://github.com/joserico00/Intro-to-HPC-Bootcamp-2023-Power-Outages): the author's project from the 2023 bootcamp (ORNL "Power Outages and Socioeconomics" track): heatwave, power-outage and medically vulnerable population tutorials and analysis.
- [Intro-to-HPC-Bootcamp-2025-Fusion-Energy-Workloads](https://github.com/joserico00/Intro-to-HPC-Bootcamp-2025-Fusion-Energy-Workloads): fusion-workload energy metrics and a power-capped job scheduler from the 2025 bootcamp.

In addition, `misc/zeek_conn_log_data_cleaning.ipynb` prepares the same connection-log format that is modeled with a Transformer in the author's `deep-learning-coursework` repository.

## Author

Jose E. Rodriguez Rios
