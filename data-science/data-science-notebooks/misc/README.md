# Miscellaneous Data Science Notebooks

A mixed collection of notebooks, grouped below by theme:

- **network traffic and malware** dataset preparation
- statistics exercises (**correlation, R², K-means goodness of fit**)
- visualization work (**Gapminder bubble chart, World Happiness choropleths**)
- pandas/NumPy practice and a few quick experiments

None of the datasets these notebooks read are included in this folder (see [Data availability](#data-availability)).

The Intro to HPC Bootcamp notebooks that used to be here now have their own repositories: [Intro-to-HPC-Bootcamp-2023-Power-Outages](https://github.com/joserico00/Intro-to-HPC-Bootcamp-2023-Power-Outages) (heatwave and power-outage project) and [Intro-to-HPC-Bootcamp-2025-Fusion-Energy-Workloads](https://github.com/joserico00/Intro-to-HPC-Bootcamp-2025-Fusion-Energy-Workloads) (fusion-workload metrics and scheduler).

---

## Contents

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| **Network traffic and malware** | | | |
| [zeek_conn_log_data_cleaning](zeek_conn_log_data_cleaning.ipynb) | Cleaning a labeled Zeek connection log | Header parsing, splitting a merged column, dropping ID and constant columns, NaN placeholders, dtype fixes | pandas, numpy |
| [malware_pe_dataset_exploration](malware_pe_dataset_exploration.ipynb) | Exploring a PE-header malware/legitimate dataset | `max()`, dropping an empty column, derived column, column sort, appending a row, sorting | pandas, numpy |
| **Statistics and modeling** | | | |
| [coefficient_of_determination](coefficient_of_determination.ipynb) | Coefficient of determination (R²) | `LinearRegression`, `score`, manual R², correlation | scikit-learn, pandas |
| [coefficient_of_determination_short](coefficient_of_determination_short.ipynb) | R² (shorter version) | `LinearRegression`, `corr` | scikit-learn, pandas |
| [kmeans_goodness_of_fit](kmeans_goodness_of_fit.ipynb) | K-means goodness of fit | Inertia/elbow method, silhouette score over k | scikit-learn, matplotlib |
| [amazon_stock_svr](amazon_stock_svr.ipynb) | Predicting AMZN closing price with support vector regression | `SVR(kernel='linear')`, `SVR(kernel='rbf')`, `train_test_split` | scikit-learn, pandas |
| **Visualization** | | | |
| [gapminder_health_vs_wealth](gapminder_health_vs_wealth.ipynb) | Recreating the Gapminder "health vs. wealth" chart (2007 and 2011) | seaborn bubble scatter, log axis, annotations, `melt` + `merge` of Gapminder tables, `k`/`M` suffix parsing | pandas, seaborn, matplotlib |
| [world_happiness_2017_maps](world_happiness_2017_maps.ipynb) | World Happiness Report 2017 choropleths | GeoPandas merge by country name, min-max normalization, per-continent maps and palettes | geopandas, pandas, matplotlib |
| [matplotlib_subplots_practice](matplotlib_subplots_practice.ipynb) | matplotlib subplot practice | `add_subplot`, `subplots`, shared axes | matplotlib, numpy |
| **pandas/NumPy practice and quick tests** | | | |
| [pandas_data_structures_practice](pandas_data_structures_practice.ipynb) | Series/DataFrame practice | Index changes, `%timeit`, `savetxt`/`loadtxt` | pandas, numpy |
| [airline_schedule_in_class](airline_schedule_in_class.ipynb) | In-class wrangling of an airline schedule | `skiprows`/`skipfooter`, header merge, filtering | pandas |
| [xlsx_to_csv_and_numpy_stats](xlsx_to_csv_and_numpy_stats.ipynb) | xlsx to csv conversion; NumPy stats | `read_excel`, `to_csv`, `np.std`, `np.mean(axis=0)` | pandas, numpy |
| [biopython_sequence_test](biopython_sequence_test.ipynb) | Quick Biopython test | `Seq`, `complement`, `reverse_complement` | biopython |
| [streaming_median_prices](streaming_median_prices.ipynb) | Streaming median of simulated prices | Timed loop, running median | numpy |
| [merge_student_data.R](merge_student_data.R) | R script merging two student CSVs | `read.table`, `merge` | base R |

---

## Network traffic and malware

### zeek_conn_log_data_cleaning.ipynb
"ML Classification – Network Traffic Analysis, Part 1".
- Reads the raw `conn.log.labeled` Zeek log from `..\data\raw\` (Windows-style path), taking the column names from its commented header. Saved: **23,145 × 21**.
- Splits the last column, which holds three fields because of an unmatched delimiter, into `tunnel_parents`, `label` and `detailed_label`.
- Drops `ts`, `uid`, the constant `local_*`/`tunnel_parents` columns, the IP addresses, and `detailed_label`.
- Replaces `'-'` and `'(empty)'` with `NaN` and casts `duration`, `orig_bytes` and `resp_bytes` to float, leaving **15 columns**.
- Writes `..\data\interim\conn.log.labeled_cleaned.csv`.

The same log format is modeled with a Transformer in the author's `deep-learning-coursework` repository.

### malware_pe_dataset_exploration.ipynb
- Loads `kaggle-data.csv` (the file name points to Kaggle), **216,352 rows × 58 columns** of Windows PE-header and section/resource features (for example `Machine`, `SizeOfCode`, `SectionsMeanEntropy`, `ImportsNbDLL`) with a `legitimate` label.
- Shows column maxima, shifts the index to start at 1, and removes the empty trailing `Unnamed: 57` column.
- Adds `TotalSize = SizeOfCode + SizeOfImage` and sorts the columns alphabetically.
- Appends one row of random integers, then sorts by `TotalSize`.
- No modeling is done.

---

## Statistics and modeling

### coefficient_of_determination.ipynb
1. **Fahrenheit→Celsius:** 10 random °F values are converted exactly to °C and fitted with `LinearRegression`. The slope is **0.5556** and the correlation is 1.0.
2. **Random target:** the same °F values against random numbers give a slope of 0.032.
3. **Buildings:** `index.txt` (tab-separated `YEAR, HEIGHT, STORIES`; not included) is regressed as height on stories. Saved: **R² = 0.9036, r = 0.9506**.
4. Four synthetic buildings are added with `DataFrame.append` and the model is refit (r = 0.9588).
5. R² is computed by hand as `1 − SS_res/SS_tot`. The print cell references `r_squared` from an earlier session, so it shows 0.90355 while `model.score` shows 0.90344.
6. A closing note in Spanish comments on how the coefficient changed.

### coefficient_of_determination_short.ipynb
A shorter version: the exact °F→°C fit (slope 0.5556, r = 1.0) and the buildings regression with **R² = 0.9036, r = 0.9506**. It reads `index.txt` from the notebook's folder.

### kmeans_goodness_of_fit.ipynb
A lesson that continues the K-means introduction:
- K-means on 3 and 5 synthetic blobs.
- The **elbow method**: inertia for k = 2 to 9. Saved inertia for the 5-blob data at k = 2: 6,771.8.
- The **silhouette method**: definitions of a(j), b(j) and s(j), and `silhouette_score` for each fitted model.
- The text reads the elbow at k = 4 and the best silhouette score at k = 2, and plots the k = 4 and k = 8 clusterings.
- `make_blobs` has no `random_state`, so results vary between runs.

### amazon_stock_svr.ipynb
- Written by Jose E Rodriguez Rios and a classmate.
- Loads `AMZN20233.csv` (daily Date/Open/High/Low/Close/Adj Close/Volume, not included) and keeps **April 2022** only: 13 trading days.
- Uses the day of the month as the only feature and the closing price as the target.
- Splits with `train_test_split` (default 75/25, no fixed seed) and fits `SVR(kernel='linear', C=1e3)` and `SVR(kernel='rbf', C=1e3, gamma=0.1)`.
- **Saved predictions on the 4 test days:**
  - Actual: `[158.12, 139.39, 146.07, 144.35]`
  - Linear SVR: `[150.01, 143.67, 144.57, 147.29]`
  - RBF SVR: `[155.41, 115.66, 99.88, 136.37]`
- Plots both models against the test points.

---

## Visualization

### gapminder_health_vs_wealth.ipynb
Homework that recreates the Gapminder "World Development" bubble chart ([Gapminder data](https://www.gapminder.org/data/)). Run in Colab.

1. **2007 chart:**
   - `gapminder_data.csv` (142 countries, 2007): scatter of GDP per capita vs. life expectancy, first plain and then sized by population.
   - A `seaborn` version colored by continent and sized by population on a log x-axis with $1k to $128k ticks.
   - A 20×18 in version with country names scaled by population and "HEALTH / SICK / HEALTHY" and "INCOME / POOR / RICH" axis annotations.
   - A version with population bucketed into "1 / 10 / 100 / 1000 Million" size categories.
2. **2011 chart:**
   - The combined `gapminder_income_all_years.csv` has no 2011 rows (the saved output is empty), so the notebook rebuilds the data from the wide Gapminder tables `pop.csv`, `lex.csv` and `gdp_pcap.csv`.
   - It reshapes them with `pd.melt`, merges them with `ddf--entities--geo--country.csv` (`world_4region` → continent), filters 2011 (195 countries), and converts values like `11.1k` and `29.2M` to numbers with regex replacement and `pd.eval`.
   - The final chart adds dashed lines for income levels 1–4 and a legend.

None of the CSV files are included.

### world_happiness_2017_maps.ipynb
- Loads `happiness_2017.csv` (World Happiness Report 2017: 140 countries, 14 columns; not included).
- Lists the countries whose names do not match GeoPandas' Natural Earth low-resolution world map, left-merges the map with the scores, and fills in the United States score by hand (6.993).
- Min-max normalizes `HappinessScore`, sets missing values to −1, and plots a world choropleth, a 2×3 grid of per-continent maps, and one map with a different color palette per continent.
- The figures were drawn with the interactive `%matplotlib notebook` backend, so they are not saved as images. `gpd.datasets` was removed in GeoPandas 1.0.

### matplotlib_subplots_practice.ipynb
Practice following the matplotlib lesson in `coursework/matplotlib_fundamentals.ipynb`: `add_subplot` histogram, scatter and line; `plt.subplots(2, 3)`; shared-axis histograms. The last cell was not executed.

---

## pandas/NumPy practice and quick tests

- **pandas_data_structures_practice.ipynb:** practice following the Series/DataFrame lesson (index changes, `%timeit` of 695 µs vs. 4.6 µs, a DataFrame from a dict, `savetxt`/`loadtxt` to `jupyter/data3.csv`). The saved run has three errors: prose typed into a code cell (`SyntaxError`), `sort_values(dataF, by=...)` (`TypeError`), and a stray character (`SyntaxError`). A chained assignment `dataF2['area'] = dataF2['largo'] = dataF2['ancho']` overwrote `largo`.
- **airline_schedule_in_class.ipynb:** in-class version of the flight-schedule cleaning (`ConfirmedFSMarch2023.csv`, not included): reads with `skiprows`/`skipfooter`, merges the headers, and filters flights from SJU. The last executed cell ends in a `SyntaxError` (mismatched brackets), and the remaining cells are empty.
- **xlsx_to_csv_and_numpy_stats.ipynb:** prints "hello", converts `Test.xlsx` (not included) to `Test.csv`, and computes NumPy statistics on 1,000,000 uniform samples (std 0.2886) and column means of a 4×8 matrix. The cells were run out of order (pandas is used before the import cell).
- **biopython_sequence_test.ipynb:** a quick check of `Bio.Seq.Seq("AGTACACTGGT")` with `complement()` → `TCATGTGACCA` and `reverse_complement()` → `ACCAGTGTACT`.
- **streaming_median_prices.ipynb:** appends random transactions (price ~ U(5, 500)) for 10 seconds and prints the running median after every insert. The printed medians settle around 252–254, and the printed log is about 3 MB.
- **merge_student_data.R:** reads `student-mat.csv` and `student-por.csv` (semicolon-separated, not included) and merges them on 13 shared demographic attributes. A comment says the merge yields 382 students.

---

## Data availability

**No data files are included in `misc/`.** Files each notebook expects:

| Notebook(s) | Expected files |
|---|---|
| zeek_conn_log_data_cleaning | `../data/raw/conn.log.labeled` |
| malware_pe_dataset_exploration | `kaggle-data.csv` |
| coefficient_of_determination, coefficient_of_determination_short | `index.txt` |
| amazon_stock_svr | `AMZN20233.csv` |
| gapminder_health_vs_wealth | `gapminder_data.csv`, `gapminder_income_all_years.csv`, `pop.csv`, `lex.csv`, `gdp_pcap.csv`, `ddf--entities--geo--country.csv` |
| world_happiness_2017_maps | `happiness_2017.csv` ([World Happiness Report](https://worldhappiness.report/)) |
| airline_schedule_in_class | `ConfirmedFSMarch2023.csv` |
| xlsx_to_csv_and_numpy_stats | `Test.xlsx` |
| merge_student_data.R | `student-mat.csv`, `student-por.csv` |

world_happiness_2017_maps uses GeoPandas' built-in Natural Earth dataset.

## Author

Jose E. Rodriguez Rios
