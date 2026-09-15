# Miscellaneous Data Science Notebooks

A mixed collection of notebooks, grouped below by theme:

- a **power-outage and heatwave training project** (tutorial notebooks plus the author's analysis, run on NERSC Perlmutter)
- **fusion/HPC workload** data preparation and a power-capped job scheduler
- **network traffic and malware** dataset preparation
- statistics exercises (**correlation, R², t-test, K-means goodness of fit**)
- visualization work (**Gapminder bubble chart, World Happiness choropleths**)
- pandas/NumPy practice and a few quick experiments

None of the datasets these notebooks read are included in this folder (see [Data availability](#data-availability)).

---

## Contents

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| **Power outages and heatwaves project** | | | |
| [1_Exploring_Datasets](1_Exploring_Datasets.ipynb) | Guide: explore the project datasets in Google Sheets | Markdown only | none |
| [2_Python_Pandas_Intro](2_Python_Pandas_Intro.ipynb) | Tutorial: pandas on movie data and county data | `read_excel`, `loc` filters, pandas/matplotlib bar charts, `merge` on FIPS | pandas, matplotlib |
| [3_Time_Series_Data](3_Time_Series_Data.ipynb) | Tutorial: EAGLE-i outage time series | Date-range filters, up-sampling with `interp1d`, `groupby().agg`, flattening MultiIndex columns, merge | pandas, scipy, matplotlib |
| [4_CorrelationAnalysis](4_CorrelationAnalysis.ipynb) | Tutorial: correlation vs. causation | Normality check, scatter plots, Spearman rho and p-value, correlation heatmap | pandas, scipy, seaborn |
| [5_Drawing_Maps](5_Drawing_Maps.ipynb) | Tutorial: county maps | GeoDataFrame from lat/lon, `sjoin(predicate="contains")`, `explore()`, folium layers | geopandas, folium |
| [6_MPI_Intro](6_MPI_Intro.ipynb) | Pointer to the mpi4py exercises | Markdown only | none |
| [7_Big_Questions](7_Big_Questions.ipynb) | The project's research questions | Markdown only | none |
| [realwork](realwork.ipynb) | **Author's analysis** of the heatwave, outage and medically vulnerable population questions | Filtering, merges, heatwave vs. baseline means, Spearman tests, choropleth maps | pandas, scipy, geopandas, folium |
| **HPC / fusion workloads** | | | |
| [CleanedmergedDataset](CleanedmergedDataset.ipynb) | Energy and science-per-kWh metrics for fusion and non-fusion project tables | `to_numeric`, derived energy/cost columns, key normalization, dedupe, outer merge | pandas |
| [CleanedDataset](CleanedDataset.ipynb) | Near-duplicate of the above | none | pandas |
| [scheduler](scheduler.ipynb) | Greedy fusion-job scheduler under a 4.8 MW cap | Priority score, cycle-based packing, time-zone-aware timeline, Gantt and step charts, CSV export | pandas, numpy, matplotlib |
| [simpleIntroToVisualization](simpleIntroToVisualization.ipynb) | Tutorial: scientific computing and visualization with Python | NumPy arrays and linear algebra, pandas, matplotlib, seaborn, 3D plots, animation, GeoPandas choropleth | numpy, pandas, matplotlib, seaborn, geopandas |
| **Network traffic and malware** | | | |
| [1-initial-data-cleaning](1-initial-data-cleaning.ipynb) | Cleaning a labeled Zeek connection log | Header parsing, splitting a merged column, dropping ID and constant columns, NaN placeholders, dtype fixes | pandas, numpy |
| [Malwaredataset](Malwaredataset.ipynb) | Exploring a PE-header malware/legitimate dataset | `max()`, dropping an empty column, derived column, column sort, appending a row, sorting | pandas, numpy |
| **Statistics and modeling** | | | |
| [coefDet](coefDet.ipynb) | Coefficient of determination (R²) | `LinearRegression`, `score`, manual R², correlation | scikit-learn, pandas |
| [coefDet2](coefDet2.ipynb) | R² (shorter version) | `LinearRegression`, `corr` | scikit-learn, pandas |
| [data-analysis-exam](data-analysis-exam.ipynb) | Exam: grades by semester, t-test, regression reshape question | `apply` grade function, `melt`, `groupby().unstack`, `ttest_ind`, bar and pie charts | pandas, scipy, matplotlib |
| [cluster_goodOfFit](cluster_goodOfFit.ipynb) | K-means goodness of fit | Inertia/elbow method, silhouette score over k | scikit-learn, matplotlib |
| [AmazonStockSVM](AmazonStockSVM.ipynb) | Predicting AMZN closing price with support vector regression | `SVR(kernel='linear')`, `SVR(kernel='rbf')`, `train_test_split` | scikit-learn, pandas |
| **Visualization** | | | |
| [JoseHWGapminder](JoseHWGapminder.ipynb) | Recreating the Gapminder "health vs. wealth" chart (2007 and 2011) | seaborn bubble scatter, log axis, annotations, `melt` + `merge` of Gapminder tables, `k`/`M` suffix parsing | pandas, seaborn, matplotlib |
| [happyness](happyness.ipynb) | World Happiness Report 2017 choropleths | GeoPandas merge by country name, min-max normalization, per-continent maps and palettes | geopandas, pandas, matplotlib |
| [visualization](visualization.ipynb) | matplotlib subplot practice | `add_subplot`, `subplots`, shared axes | matplotlib, numpy |
| **pandas/NumPy practice and quick tests** | | | |
| [pandas data structure](pandas%20data%20structure.ipynb) | Series/DataFrame practice | Index changes, `%timeit`, `savetxt`/`loadtxt` | pandas, numpy |
| [clase de marzo 1 2023](clase%20de%20marzo%201%202023.ipynb) | In-class wrangling of an airline schedule | `skiprows`/`skipfooter`, header merge, filtering | pandas |
| [datascience](datascience.ipynb) | xlsx to csv conversion; NumPy stats | `read_excel`, `to_csv`, `np.std`, `np.mean(axis=0)` | pandas, numpy |
| [Biopython testing](Biopython%20testing.ipynb) | Quick Biopython test | `Seq`, `complement`, `reverse_complement` | biopython |
| [stockpredicate](stockpredicate.ipynb) | Streaming median of simulated prices | Timed loop, running median | numpy |
| [student-merge.R](student-merge.R) | R script merging two student CSVs | `read.table`, `merge` | base R |

---

## Power outages and heatwaves project (1_ to 7_, realwork)

A training project on the **June 2016 heatwave in the U.S. Southwest (California, Nevada, Arizona)**. Its data covers daily county average temperatures (`CtyAvTemp6XY16.csv`), power outages from **EAGLE-i** (`eaglei_outages_2016.csv`, customers without power per county in 15-minute intervals), **HHS emPOWER** counts of Medicare beneficiaries who rely on electricity-dependent medical equipment (DME) (`2016_HHSemPOWERMapHistoricalDataset.xlsx`), county population, and 2010 county demographics. Notebooks `1_` to `7_` are the project's tutorial and guide notebooks: they are narrated and their exercise cells are left blank. `realwork.ipynb` holds the author's own analysis.

### 1_Exploring_Datasets (markdown only)
Instructions for opening `CtyAvTemp62016.csv` in Google Sheets, adding a Fahrenheit column (`=1.8*(K-273)+32`), filtering to AZ/NV/CA with a filter view, and building bar charts. It ends with exercises on the emPOWER workbook. The screenshots it references in `images/` are not included. The code cell is empty.

### 2_Python_Pandas_Intro
- **Movies:** loads `data/2020-movie-data.xlsx` (19 films with studio, budget, box office, multiplier and type), filters with `loc` (`BUDGET > 15M`, combined with `&` and `|`), and makes a pandas bar chart and a sorted matplotlib bar chart with colored budget bands.
- **County data:** loads `CtyAvTemp62016.csv` (3,233 counties, temperature in Kelvin) and the emPOWER **County** sheet, then merges them with an inner join on `FIPS_Code` = `GEOID` (3,226 rows).
- The exercise cells are commented out or empty.

### 3_Time_Series_Data
- Loads `eaglei_outages_2016.csv`, **13,306,024 rows** of `fips_code, county, state, sum, run_start_time`, with times in UTC.
- Filters June 20–21 and plots Los Angeles and Pima counties. It notices that the two counties have different numbers of samples (153 vs. 66 rows).
- Up-samples both series to 15-minute steps: converts timestamps to integers, builds `scipy.interpolate.interp1d` interpolators on an `np.arange` grid, and overlays the two counties.
- Aggregates June 20 local time (UTC−7) with `groupby("fips_code").agg({"sum": ["mean", "median"]})`. Saved results: **Los Angeles mean 2,037 / median 1,815**, Orange County mean 2,446, Riverside 905, San Bernardino 606, Clark (NV) 416, and 17 more counties.
- Flattens the MultiIndex columns and merges the aggregates with the emPOWER county table.

### 4_CorrelationAnalysis
- Explains Pearson vs. Spearman correlation and p-values, using the movie data.
- Adds `GROSS PROFIT = BOX OFFICE − BUDGET`, plots a budget histogram (not normal) and scatter plots.
- **Saved results:**
  - Spearman(BUDGET, GROSS PROFIT) = **−0.164, p = 0.503**.
  - Spearman(GROSS PROFIT, MULTIPLIER) = **0.839, p = 7.3 × 10⁻⁶**.
  - A Spearman correlation matrix for the three variables with a `seaborn` heatmap.
- The "TO DO" histogram cell is empty.

### 5_Drawing_Maps
- Converts temperatures to °F and shows a plain lat/lon scatter plot.
- Builds a `GeoDataFrame` with `points_from_xy(..., crs="EPSG:4326")`.
- Downloads U.S. county polygons from the Python Graph Gallery GeoJSON on GitHub and spatially joins points to polygons with `sjoin(predicate="contains")`.
- Makes interactive `explore()` maps with a Fahrenheit layer and a state layer, switched with `folium.LayerControl`.

### 6_MPI_Intro (markdown only)
Introduces MPI and `mpi4py` for processing all years of EAGLE-i data in parallel and points to `eaglei_mpi_scripts/6_MPI_exercises.ipynb`, which is not included.

### 7_Big_Questions (markdown only)
The nine project questions: hottest counties, DME-reliant populations, outages during and outside the heatwave, DME vs. outage correlation, interactive maps, submitting jobs to Perlmutter, hourly temperature vs. outages, DME vs. asthma, and repeating the analysis for another disaster. It also describes the final presentation.

### realwork.ipynb — author's analysis
Run on NERSC Perlmutter, according to the environment paths in the saved warnings.

1. **Q1, hottest counties:**
   - For each day from June 17 to 24, loads `CtyAvTemp6XY16.csv`, adds °F, filters to state FIPS 6, 32 and 4, and plots the 10 hottest counties.
   - The saved `head()` outputs show **Yuma and La Paz (AZ) as the hottest counties on June 19–22**, peaking at **102.1 °F on June 20**. Pima, Cochise and Santa Cruz are hottest on June 23.
2. **Q2, DME-reliant population:**
   - Filters the emPOWER County sheet to the three states and merges it with 2016 county population (`county_population_by_year.csv`).
   - Sorts by June 2016 power-dependent DME counts and plots the 10 lowest and 10 highest counties.
3. **Q3, outages during vs. outside the heatwave:**
   - Merges EAGLE-i outages with the DME table.
   - Computes mean customers without power per county for **June 19–20** and for a **June 1–14** baseline.
   - Draws side-by-side bar charts of the top 10 counties.
4. **Q4, DME vs. outages:**
   - Spearman correlation between June DME counts and mean heatwave outages across the Southwest counties. Saved: **rho = 0.827, p = 6.2 × 10⁻⁷**.
5. **Q8, DME vs. adult asthma:**
   - Merges `CtyAvDemog2010.csv` with emPOWER. Saved: **rho = 0.002, p = 0.549**.
   - The merge key is the 3-digit county code (`COUNTYFP` = `County_FIPS_Code`), which is not unique across states, so this join matches counties from different states.
6. **Q7, hourly temperature vs. outages (Los Angeles, June 20):**
   - Loads a hand-built `hourlytemp2016.csv`, converts timestamps to integers, and inner-joins it with LA outage rows.
   - Saved: **Spearman rho = −0.306, p = 0.166**.
7. **Q5, maps:**
   - GeoDataFrames of June 19 temperatures, spatially joined to county polygons, shown as folium `explore()` maps with temperature and state layers.
   - The same map is built for June 19 outages merged with temperature.

**Notes:** cell 13 reads the emPOWER sheet into `calcal2016` but then displays `medical2016`, which was defined in an earlier session, so re-running from top to bottom raises a `NameError` until that name is fixed. Several charts reuse the title "61716 temperature" and the label "LA power outages".

---

## HPC / fusion workloads

These notebooks relate to the fusion-energy project in NERSC/DOE HPC Bootcamp 2025 Module 5, which has a 12 MW facility cap with a 40% fusion share.

### CleanedmergedDataset.ipynb
- **Loads** `data/fusion_workload_projects_perf.csv`, `data/fusion_workload_projects_architecture.csv`, `data/NERSCProject_nonfusion_hpc_projects.csv` and `data/NERSCProject_nonfusion_hpc_projects_architecture.csv`. The tables list synthetic projects by workload, platform, node type, bottleneck, library, framework, precision, nodes, kW per node, runtime and work units.
- **Derives, for each table:**
  - `Power_draw_kW = Nodes × Power_per_Node_kW`, and the same in MW
  - `Energy_per_job_kWh = Runtime_h × Power_draw_kW`
  - `Science_per_kWh = Work_Units / Energy_per_job_kWh`
  - `Cost_per_job_$ = 0.10 × kWh`
  - `Science_per_$`
  - For architecture tables, the node count comes from `Nodes` or `Average Nodes`.
- **Merges** each performance/architecture pair with an outer join on lowercase `Workload` + `Project_Name` keys, after de-duplicating on those keys. Saved shapes: **fusion 476 × 36**, **non-fusion 173 × 36**.
- The last cells are empty.

### CleanedDataset.ipynb
A **near-duplicate** of *CleanedmergedDataset*. It has the same cells except one extra `fusion_merged.head()` display cell that the merged version adds.

### scheduler.ipynb
1. Loads `fusion_workload_projects_architecture.csv`, derives the same power, energy, science and cost columns, and classifies each row as CPU, GPU or HYBRID from `Node_Type`/`Platform` text. Saved: **153 of 250 rows kept**, all eligible.
2. **Priority** = 0.6 × (share of total work units) + 0.4 × (`Science_per_kWh` ÷ its maximum).
3. **Greedy cycle scheduler:**
   - In each cycle, walk the unscheduled jobs by priority (then size) and place every job that still fits under a global **4.8 MW** cap.
   - The cycle lasts as long as its longest job.
   - Repeat until all jobs are placed.
4. Gives the cycles calendar times starting 2025-08-15 09:00 America/Chicago. Saved plan: **start 2025-08-15 09:00, end 2025-08-17 05:07 (UTC−5)**.
5. Writes `fusion_arch_with_schedule_4p8MW_simultaneous.csv`, `fusion_schedule_cycles_4p8MW_simultaneous.csv` and `fusion_cycle_summary_4p8MW_simultaneous.csv`. These outputs are not included.
6. Plots a timeline by bucket (hatched horizontal bars) and a step chart of MW in use against the 4.8 MW cap, saved as `my_plot.png` (not included).

### simpleIntroToVisualization.ipynb
A provided tutorial notebook, "An Introduction to Scientific Computing and Data Visualization with Python", run on a NERSC Python kernel. It covers:
- **NumPy:** array creation (`zeros`, `ones`, `full`, `arange`, `linspace`, random), reshaping, slicing and integer/boolean indexing, element-wise operations, linear algebra (rank, trace, determinant, inverse), CSV loading, statistics, sorting, `np.interp`.
- **pandas:** Series and DataFrame from lists and dicts, `concat`, derived columns and rows, `aggregate`, `drop`, bar and pie charts, a hockey player dataset (`read_excel`, lower-cased columns, duplicate removal, multi-condition filters, mean/median/mode/quantiles, Pearson correlation matrix with a styled gradient, BMI vs. weight scatter with a `polyfit` line, colors by team), and `fillna`/`dropna`/`replace`/`interpolate`.
- **matplotlib and seaborn:** line, scatter, bar, histogram and pie charts, legends, grids, subplots, error bars, annotations, 3D surface/scatter/bar plots, and a `FuncAnimation`.
- **GeoPandas:** a Natural Earth world map, and a U.S. county choropleth of 2020 unemployment built by merging a GeoJSON with a CSV.

The one exercise cell (adding a `celery` column and redrawing the pie chart) is completed. Its data (`data/numpy_data.csv`, `data/hockey_data.xlsx`, `data/unemployment-2020.csv`, `data/lat-lon-fips.csv`, `data/US-counties.geojson`) and images (`img/`) are not included.

---

## Network traffic and malware

### 1-initial-data-cleaning.ipynb
"ML Classification – Network Traffic Analysis, Part 1".
- Reads the raw `conn.log.labeled` Zeek log from `..\data\raw\` (Windows-style path), taking the column names from its commented header. Saved: **23,145 × 21**.
- Splits the last column, which holds three fields because of an unmatched delimiter, into `tunnel_parents`, `label` and `detailed_label`.
- Drops `ts`, `uid`, the constant `local_*`/`tunnel_parents` columns, the IP addresses, and `detailed_label`.
- Replaces `'-'` and `'(empty)'` with `NaN` and casts `duration`, `orig_bytes` and `resp_bytes` to float, leaving **15 columns**.
- Writes `..\data\interim\conn.log.labeled_cleaned.csv`.

The same log format is modeled with a Transformer in the author's `deep-learning-coursework` repository.

### Malwaredataset.ipynb
- Loads `kaggle-data.csv` (the file name points to Kaggle), **216,352 rows × 58 columns** of Windows PE-header and section/resource features (for example `Machine`, `SizeOfCode`, `SectionsMeanEntropy`, `ImportsNbDLL`) with a `legitimate` label.
- Shows column maxima, shifts the index to start at 1, and removes the empty trailing `Unnamed: 57` column.
- Adds `TotalSize = SizeOfCode + SizeOfImage` and sorts the columns alphabetically.
- Appends one row of random integers, then sorts by `TotalSize`.
- No modeling is done.

---

## Statistics and modeling

### coefDet.ipynb
1. **Fahrenheit→Celsius:** 10 random °F values are converted exactly to °C and fitted with `LinearRegression`. The slope is **0.5556** and the correlation is 1.0.
2. **Random target:** the same °F values against random numbers give a slope of 0.032.
3. **Buildings:** `index.txt` (tab-separated `YEAR, HEIGHT, STORIES`; not included) is regressed as height on stories. Saved: **R² = 0.9036, r = 0.9506**.
4. Four synthetic buildings are added with `DataFrame.append` and the model is refit (r = 0.9588).
5. R² is computed by hand as `1 − SS_res/SS_tot`. The print cell references `r_squared` from an earlier session, so it shows 0.90355 while `model.score` shows 0.90344.
6. A closing note in Spanish comments on how the coefficient changed.

### coefDet2.ipynb
A shorter version: the exact °F→°C fit (slope 0.5556, r = 1.0) and the buildings regression with **R² = 0.9036, r = 0.9506**. It reads `index.txt` from the notebook's folder.

### data-analysis-exam.ipynb
An exam notebook in Spanish from a data-analysis tools course.
1. **Written question:** the difference between the correlation coefficient and the coefficient of determination.
2. **Grades** (`data_B.csv`, not included, holds two semesters of numeric grades stacked in one column):
   - Splits the semesters into two columns, maps grades to letters A–F with a function, and melts the table.
   - Counts letters overall. Saved: **A 8, B 8, C 20, D 10, F 11**.
   - Counts letters per semester. Saved: **A 5/3, B 3/5, C 12/8, D 5/5, F 7/4**.
   - Compares semester means with `scipy.stats.ttest_ind`. Saved: **71.19 vs. 72.44, t = −0.291, p = 0.772**, so no significant difference.
   - Plots a grouped bar chart and one pie chart per semester.
3. **Written question:** why `df['a'].values.reshape(-1, 1)` is needed before `LinearRegression.fit`, answered with a demonstration (`x.ndim == 2`).

Cell 28 uses `grade_counts` where `grado_counts` was meant, so re-running it as saved raises a `NameError`.

### cluster_goodOfFit.ipynb
A lesson that continues the K-means introduction:
- K-means on 3 and 5 synthetic blobs.
- The **elbow method**: inertia for k = 2 to 9. Saved inertia for the 5-blob data at k = 2: 6,771.8.
- The **silhouette method**: definitions of a(j), b(j) and s(j), and `silhouette_score` for each fitted model.
- The text reads the elbow at k = 4 and the best silhouette score at k = 2, and plots the k = 4 and k = 8 clusterings.
- `make_blobs` has no `random_state`, so results vary between runs.

### AmazonStockSVM.ipynb
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

### JoseHWGapminder.ipynb
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

### happyness.ipynb
- Loads `happiness_2017.csv` (World Happiness Report 2017: 140 countries, 14 columns; not included).
- Lists the countries whose names do not match GeoPandas' Natural Earth low-resolution world map, left-merges the map with the scores, and fills in the United States score by hand (6.993).
- Min-max normalizes `HappinessScore`, sets missing values to −1, and plots a world choropleth, a 2×3 grid of per-continent maps, and one map with a different color palette per continent.
- The figures were drawn with the interactive `%matplotlib notebook` backend, so they are not saved as images. `gpd.datasets` was removed in GeoPandas 1.0.

### visualization.ipynb
Practice following the matplotlib lesson in `coursework/visualization_Part1.ipynb`: `add_subplot` histogram, scatter and line; `plt.subplots(2, 3)`; shared-axis histograms. The last cell was not executed.

---

## pandas/NumPy practice and quick tests

- **pandas data structure.ipynb:** practice following the Series/DataFrame lesson (index changes, `%timeit` of 695 µs vs. 4.6 µs, a DataFrame from a dict, `savetxt`/`loadtxt` to `jupyter/data3.csv`). The saved run has three errors: prose typed into a code cell (`SyntaxError`), `sort_values(dataF, by=...)` (`TypeError`), and a stray character (`SyntaxError`). A chained assignment `dataF2['area'] = dataF2['largo'] = dataF2['ancho']` overwrote `largo`.
- **clase de marzo 1 2023.ipynb:** in-class version of the flight-schedule cleaning (`ConfirmedFSMarch2023.csv`, not included): reads with `skiprows`/`skipfooter`, merges the headers, and filters flights from SJU. The last executed cell ends in a `SyntaxError` (mismatched brackets), and the remaining cells are empty.
- **datascience.ipynb:** prints "hello", converts `Test.xlsx` (not included) to `Test.csv`, and computes NumPy statistics on 1,000,000 uniform samples (std 0.2886) and column means of a 4×8 matrix. The cells were run out of order (pandas is used before the import cell).
- **Biopython testing.ipynb:** a quick check of `Bio.Seq.Seq("AGTACACTGGT")` with `complement()` → `TCATGTGACCA` and `reverse_complement()` → `ACCAGTGTACT`.
- **stockpredicate.ipynb:** despite the name, there is no stock prediction. It appends random transactions (price ~ U(5, 500)) for 10 seconds and prints the running median after every insert. The printed medians settle around 252–254, and the printed log is about 3 MB.
- **student-merge.R:** reads `student-mat.csv` and `student-por.csv` (semicolon-separated, not included) and merges them on 13 shared demographic attributes. A comment says the merge yields 382 students.

---

## Data availability

**No data files are included in `misc/`.** Files each notebook expects:

| Notebook(s) | Expected files |
|---|---|
| 2_, 3_, 4_, 5_, realwork | `data/2020-movie-data.xlsx`, `data/temperaturedata/CtyAvTemp6{17..24}16.csv`, `data/eaglei_outages/eaglei_outages_2016.csv` ([EAGLE-i](https://eagle-i.doe.gov/)), `data/2016_HHSemPOWERMapHistoricalDataset.xlsx` ([HHS emPOWER](https://empowerprogram.hhs.gov/)), `data/county_population_by_year.csv`, `data/CtyAvDemog2010.csv`, `data/hourlytemp2016.csv`, `images/` |
| 6_MPI_Intro | `eaglei_mpi_scripts/` |
| CleanedDataset, CleanedmergedDataset | `data/fusion_workload_projects_perf.csv`, `data/fusion_workload_projects_architecture.csv`, `data/NERSCProject_nonfusion_hpc_projects.csv`, `data/NERSCProject_nonfusion_hpc_projects_architecture.csv` |
| scheduler | `fusion_workload_projects_architecture.csv` (in the notebook's own folder) |
| simpleIntroToVisualization | `data/numpy_data.csv`, `data/hockey_data.xlsx`, `data/unemployment-2020.csv`, `data/lat-lon-fips.csv`, `data/US-counties.geojson`, `img/` |
| 1-initial-data-cleaning | `../data/raw/conn.log.labeled` |
| Malwaredataset | `kaggle-data.csv` |
| coefDet, coefDet2 | `index.txt` |
| data-analysis-exam | `data_B.csv` |
| AmazonStockSVM | `AMZN20233.csv` |
| JoseHWGapminder | `gapminder_data.csv`, `gapminder_income_all_years.csv`, `pop.csv`, `lex.csv`, `gdp_pcap.csv`, `ddf--entities--geo--country.csv` |
| happyness | `happiness_2017.csv` ([World Happiness Report](https://worldhappiness.report/)) |
| clase de marzo 1 2023 | `ConfirmedFSMarch2023.csv` |
| datascience | `Test.xlsx` |
| student-merge.R | `student-mat.csv`, `student-por.csv` |

5_Drawing_Maps and realwork download U.S. county polygons from GitHub at run time, and happyness and simpleIntroToVisualization use GeoPandas' built-in Natural Earth dataset.

## Author

Jose E. Rodriguez Rios
