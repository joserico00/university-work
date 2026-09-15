# Coursework — pandas, Data Wrangling and Visualization

Notebooks from a data-analysis tools course, mostly with **Spanish** narration and comments. They move from pandas/NumPy data structures, through cleaning and wrangling (missing values, duplicates, merges, pivots, joins) and a flight-connection search on a real airline schedule, to visualization with matplotlib, pandas, seaborn and Plotly. The folder also has a copy of the Matplotlib "plot types" gallery notebooks, a small utility that concatenates notebooks, and the two merged notebooks it produced.

Several notebooks are narrated lesson walkthroughs. Data paths are relative to this folder (for example `datasets/iris.csv` and `ranDat.csv`), so run the notebooks from here.

---

## Contents

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| [Pandas Data Structures - A](Pandas%20Data%20Structures%20-%20A.ipynb) | Series and DataFrame basics | Indexing, `RangeIndex`, `%timeit` (Python `sum` vs `np.sum`), dict to DataFrame, `savetxt`/`loadtxt` vs `read_csv`, adding columns/rows, sorting | pandas, numpy |
| [Pandas Data Structures - B](Pandas%20Data%20Structures%20-%20B.ipynb) | Math, statistics and filtering | `mean`/`sum` by axis, `idxmin`, boolean masks, `loc` with conditions | pandas |
| [dataCleaningandWrang](dataCleaningandWrang.ipynb) | Missing data, duplicates, replacement | `isna`, `dropna(how, thresh)`, `fillna` (value/dict/ffill/bfill/mean), `duplicated`, `drop_duplicates(subset, keep)`, `replace` | pandas, numpy |
| [dataCleaningandWrang2](dataCleaningandWrang2.ipynb%20) | Duplicate of the above | none | none |
| [dataWrang-Asignacion](dataWrang-Asignacion.ipynb) | Airline schedule cleaning and SJU→TUS connection assignment | `skiprows`/`nrows`/`skipfooter`, header merge, `isin`, `~`, `concat`, `merge` | pandas |
| [dataWrang-Cont](dataWrang-Cont.ipynb) | Continuation: time parsing and connection filtering | `to_datetime`, set intersection, minimum connection time, `merge(how='cross'/'left'/'right')` | pandas |
| [dataWrang_Final](dataWrang_Final.ipynb) | Group-by, pivot and join | `map`, `groupby().sum()`, `pivot`, `join` (index and `on=`), `set_index` | pandas |
| [covid dataframe](covid%20dataframe.ipynb) | U.S. county COVID-19 cases/deaths, 2020 and 2021 | Null checks, `fillna`, `merge`, `join`, `pivot_table`, `groupby` | pandas |
| [datascience project](datascience%20project.ipynb) | Start of a project: CDC suicide data and EM-DAT disasters | `read_csv`, `read_excel`, xlsx to csv conversion | pandas, openpyxl |
| [visualization_Part1](visualization_Part1.ipynb) | matplotlib fundamentals | Implicit vs. explicit API, subplots, styles, ticks, labels, legends | matplotlib, numpy |
| [Viz3](Viz3.ipynb) | Coloring by group, seaborn, Plotly choropleths, pandas bar charts | Color dicts, `hue`, `px.choropleth` (USA-states), derived ratio columns | pandas, matplotlib, seaborn, plotly |
| [plot_types_jupyter/](plot_types_jupyter/) | 33 Matplotlib "plot types" gallery notebooks | basic, arrays, stats, unstructured, 3D | matplotlib, numpy |
| [union](union.ipynb) + [unionlibrary.py](unionlibrary.py) | Concatenate all notebooks in the folder into one | `nbformat` | nbformat, glob |
| [merged_notebook](merged_notebook.ipynb) | Auto-generated concatenation (311 cells) | none | none |
| [merged_notebookpart1](merged_notebookpart1.ipynb) | Auto-generated concatenation (622 cells) | none | none |

### Data files in this folder

| File | Contents | Used by |
|---|---|---|
| [`suicides.csv`](suicides.csv) | U.S. suicide deaths by state and year, **2001–2020**: deaths, population, crude and age-adjusted rates, years of potential life lost. The footer says it was produced by the CDC National Center for Injury Prevention and Control ([WISQARS](https://wisqars.cdc.gov/)). | datascience project |
| [`disasters.xlsx`](disasters.xlsx) | [EM-DAT](https://www.emdat.be/) custom export (version 2023-05-08): 1,364 disaster records for the United States and Puerto Rico, 1960–2023 | datascience project |
| [`Test.csv`](Test.csv) | CSV conversion of `disasters.xlsx`, written by *datascience project* | datascience project |
| [`datasets/iris.csv`](datasets/iris.csv) | Iris flower measurements (150 rows, 3 species) | Viz3 |
| [`datasets/2012_Election_Data.csv`](datasets/2012_Election_Data.csv) | 2012 U.S. turnout by state: VEP/VAP, ballots, non-citizen %, prison/probation/parole counts | Viz3 |

**Referenced but not included:** `ConfirmedFSMarch2023.csv` (airline schedule for March 1–31, 2023; used by *Pandas B* and *dataWrang-Asignacion*, and read from `datasets/ConfirmedFSMarch2023.csv` by *dataWrang-Cont*), `us-counties-2020.csv` and `us-counties-2021.csv` (*covid dataframe*), the happiness table shown in *Pandas B*'s saved outputs, and `ranDat.csv` (written and then read back by *Pandas A*).

---

## Pandas Data Structures - A

**Goal:** a lesson on pandas `Series` and `DataFrame`.

**Steps**
1. Builds a mixed-type `Series`, inspects and changes its index (`index += 1`, `pd.RangeIndex(start=4, stop=24, step=4)`, string labels).
2. Times Python `sum` against `np.sum` on 10,000 random numbers. Saved run: **606 µs vs. 5.51 µs** per loop.
3. Builds a DataFrame from a dictionary of sample records.
4. Saves a random 5×8 matrix with `np.savetxt` and reads it back three ways:
   - `np.loadtxt` works.
   - `pd.read_csv` puts everything in one column, because the file is space-delimited.
   - `sep=' '` turns the first row into headers, and passing new column names then produces all-`NaN` rows.
   The lesson concludes that purely numeric files should be read with NumPy.
5. Adds a derived `area` column, reorders columns, and appends a row with `DataFrame.append` (removed in pandas 2.0).

**Notes:** the last two cells (`sort_values`, `iloc`) failed with `NameError` in the saved run because the kernel had been restarted. The matrix is written to and read from `ranDat.csv` in this folder.

## Pandas Data Structures - B

**Goal:** basic math, statistics and conditional selection.

**Data:** the saved outputs show a **140-country happiness table**: `Country`, `Region`, `Rank`, `HappinessScore`, `Life Ladder`, `Log GDP per capita`, `Social support`, `Healthy life expectancy at birth` and others. The load cell was later edited to read `ConfirmedFSMarch2023.csv` and re-run, so its output no longer matches the cells after it. Neither file is included.

**Steps and saved results**
- Mean `HappinessScore` computed three ways (`sum/len`, `.mean()`, built-in `sum`): **5.399**.
- `df.sum()` by column and by row, `dtypes`/`info()`, and row slices with `iloc`.
- `idxmin` of `HappinessScore`: **Central African Republic, 2.693** (rank 140).
- Boolean filtering: 89 countries score above 5. With `HappinessScore > 5 & Log GDP per capita < 8` only one row remains (rank 88, Commonwealth of Independent States region).

## dataCleaningandWrang

**Goal:** a lesson on handling missing data, duplicates and sentinel values, on small synthetic Series and DataFrames.

**Steps**
- `NaN` vs. `None`. `isna`/`notna`, `dropna()` with `how="all"`, `axis=1` and `thresh`.
- `fillna` with a constant, a per-column dict, `method="ffill"`/`"bfill"`, and the mean.
- `duplicated()`, `drop_duplicates()` with `subset` and `keep="last"`.
- `replace(-999, NaN)`, replacing a list of values, and list-to-list or dict replacement.

## dataCleaningandWrang2

`dataCleaningandWrang2.ipynb ` (the file name ends in a trailing space) is an **exact duplicate** of *dataCleaningandWrang*. Every cell and output is the same; only the kernel version in the metadata differs (3.8.8 vs. 3.9.13).

## dataWrang-Asignacion

**Goal:** clean a messy airline schedule export and solve an assignment: *find all flights from San Juan (SJU) to Tucson (TUS). If there is no direct flight, find itineraries with at most one stop, and no leg may use an aircraft type in a `notAllowed` list (A319/A320/A321 variants).*

**Data:** `ConfirmedFSMarch2023.csv`, a "Confirmed FS Schedule" valid March 1–31, 2023, with origin, destination, flight number, frequency, departure and arrival times, aircraft type, subfleet, and effective/discontinue dates. **Not included.** The notebook's first code cell prints the whole raw file with a shell command, which is why the notebook is about 1 MB.

**Steps**
1. Reads the file with `skiprows=[0,1,2,3,6,7]` and `nrows=8355`, and alternatively with `skipfooter` using the Python engine.
2. Renames the duplicated `Flight.1` column and joins the two header rows into one (`df.columns + ' ' + df.iloc[0]`), for example `Origin Airport`, `Flight Frequency`.
3. Drops the header row, resets the index, and checks `info()`.
4. Filters departures from SJU, checks membership with `in df[...].values`, and uses `isin` and its complement `~isin` against `notAllowed`.
5. Assignment:
   - `dfd` holds allowed flights out of SJU and `dfa` holds allowed flights into TUS.
   - Connecting airports are the destinations in `dfd` that also appear as origins in `dfa`.
   - The first legs (`dfA`) and second legs (`dfD`) are combined with `concat` and with left merges on the connecting airport.

**Result in the saved outputs:** no direct SJU→TUS flights. The allowed one-stop options connect through **DFW** (SJU–DFW flight 2196, aircraft code 772, then DFW–TUS 0785, code 738) and **ORD** (SJU–ORD 1184/0395, then ORD–TUS 0639/0822, all code 738). The merges match on airport only and do not check dates or connection times.

**Notes:** one empty cell raised a `NameError` in the saved run.

## dataWrang-Cont

**Goal:** continue the SJU→TUS search with proper time handling.

**Steps**
1. Re-reads and cleans the schedule the same way, from `datasets/ConfirmedFSMarch2023.csv`.
2. Parses `Departure Time` and `Arrival Time` with `pd.to_datetime(format='%H:%M')`. An alternative split/timedelta parser is kept but not executed.
3. Finds the connecting airports as the intersection of TUS origins and allowed SJU destinations. Saved result: `['ORD', 'DFW']`.
4. Builds the first-leg and second-leg tables, pads the shorter one, and filters with a **2-hour minimum connection** (`pd.Timedelta(hours=2)`). The comparison is by row position.
5. Joins the legs with a cross merge filtered on matching airports, and also tries left, `Effective Date` and right merges.

**Saved result of the cross merge (5 rows):** one SJU–DFW 2196 → DFW–TUS 0785 row, and four SJU–ORD 1184 → ORD–TUS 0822 rows covering different effective-date ranges.

## dataWrang_Final

**Goal:** a lesson on `groupby`, `pivot` and `join`.

**Steps** (on a small car-model table)
- Maps models to brands with a dict and `Series.map`, then sums quantities with `groupby('brand').sum()`. Saved: nissan 16, toyota 17, and others.
- `pivot(index='brand', columns='model')`, and `drop_duplicates` followed by `pivot(index, columns, values)`.
- `join` by index, with `lsuffix`/`rsuffix`, after `set_index('brand')`, and with `on='brand'`. It shows that rows of the joined frame with no matching key are left out.

## covid dataframe

**Goal:** practice cleaning and combining two large tables, and describe possible visualizations.

**Data:** `us-counties-2020.csv` and `us-counties-2021.csv`, daily cumulative COVID-19 `cases` and `deaths` by county, with columns `date, county, state, fips, cases, deaths`. **Not included.**

**Steps and saved results**
- 2020 table: **884,737 rows**, with `fips` and `deaths` partly missing (27,027 rows with a null, for example "New York City" and "Unknown" counties). 2021 table: **1,185,373 rows**.
- `fillna(0)` on both tables.
- `merge(how='right')`: because no rows are shared, the result equals the 2021 table.
- Index-aligned `join` with suffixes.
- `pivot_table(index='date', values='deaths', aggfunc='sum')` sums the counties' cumulative deaths per date. Saved value for 2020-12-31: **346,050**.
- `groupby('date').first()`.
- Two markdown answers propose bar charts and histograms of infections and deaths.

## datascience project

**Goal:** first steps of a project combining suicide statistics with disaster records.

**Steps:** loads `suicides.csv` (1,035 rows including the footer notes) and `disasters.xlsx` with `read_excel`, writes it out as `Test.csv`, and reloads it. The EM-DAT metadata rows at the top of the sheet are still in the table (the header is not yet fixed). There is no further analysis.

## visualization_Part1

**Goal:** a lesson on matplotlib.

**Steps:** a line plot of `np.arange(10)`, titles and axis labels, `plt.figure()` with `add_subplot` (histogram, scatter, cumulative random walk), redefining the grid (2×3 on top of 2×2), the implicit `plt.subplot`/`gca` form, a bar chart, `plt.subplots(2, 3)`, shared-axis histograms with `subplots_adjust(wspace=0, hspace=0)`, color/linestyle/marker shorthands (`'gp:'`), `drawstyle="steps-post"`, legends, and custom ticks and tick labels.

## Viz3

**Goal:** color points by category, and a first look at seaborn, Plotly and pandas bar charts.

**Steps**
1. **Iris** (`datasets/iris.csv`): scatter of sepal width vs. petal length with matplotlib and with `DataFrame.plot.scatter`, then colored by species using a dict built with `zip(set(species), colors)`. A cell intentionally shows the `ValueError` raised by `c='species'` with string categories. `sns.scatterplot(hue='species')` does the same in one line.
2. **Plotly choropleths:** a demo map of the U.S. states, then `datasets/2012_Election_Data.csv`:
   - Voting-Age Population (VAP) by state.
   - A derived **Prison Fraction** = prison population ÷ VAP (after stripping thousands separators), mapped with `px.choropleth(locationmode="USA-states")`.
3. `px.data.gapminder().query("year==2023")` returns an empty frame, because the built-in data ends in 2007.
4. **pandas bar charts** of a random 6×4 table: grouped, stacked horizontal, and transposed.

## plot_types_jupyter/

The **Matplotlib "Plot types" gallery** notebooks ([matplotlib.org/stable/plot_types](https://matplotlib.org/stable/plot_types/index.html)). Each one draws a single chart type from synthetic NumPy data.

| Folder | Notebooks |
|---|---|
| `basic/` | `bar`, `fill_between`, `plot`, `scatter_plot`, `stackplot`, `stem`, `step` |
| `arrays/` | `barbs`, `contour`, `contourf`, `imshow`, `pcolormesh`, `quiver`, `streamplot` |
| `stats/` | `boxplot_plot`, `errorbar_plot`, `eventplot`, `hexbin`, `hist2d`, `hist_plot`, `pie`, `violin` |
| `unstructured/` | `tricontour`, `tricontourf`, `tripcolor`, `triplot` |
| `3D/` | `scatter3d_simple`, `surface3d_simple`, `trisurf3d_simple`, `voxels_simple`, `wire3d_simple` |

24 notebooks were executed and have saved figures. Their code does not include the `plt.style.use('_mpl-gallery')` line. The other 9 are unexecuted and still include that line: `arrays/contour`, `contourf`, `imshow`, `pcolormesh`, `quiver`, `streamplot`, and `3D/scatter3d_simple`, `surface3d_simple`, `trisurf3d_simple`. In `basic/bar.ipynb`, the axis-label lines are commented out.

## union.ipynb and unionlibrary.py

`unionlibrary.py` defines `combine_notebooks(filenames)`. It reads each `*.ipynb` in the current folder with `nbformat` and appends its cells to a new notebook, writing `merged_notebook.ipynb`. `union.ipynb` runs the same code and writes **`merged_notebookpart1.ipynb`**. Its saved output lists the input notebooks and the `nbformat` warnings about duplicate cell IDs.

## merged_notebook.ipynb and merged_notebookpart1.ipynb

These are **auto-generated concatenations with no new content**:
- `merged_notebook.ipynb` (311 cells) contains, in order, *Viz3*, *covid dataframe*, *visualization_Part1*, *datascience project*, *union*, *dataWrang-Asignacion*, *Pandas Data Structures - A*, *dataWrang_Final*, *dataCleaningandWrang*, *dataWrang-Cont* and *Pandas Data Structures - B*.
- `merged_notebookpart1.ipynb` (622 cells) was built after `merged_notebook.ipynb` existed, so it contains that notebook again.

Every non-empty cell in both files also appears in one of the notebooks above. The one exception is the cell that writes `merged_notebook.ipynb`, which is the same code as `unionlibrary.py`.

---

## Running these notebooks

- Install the requirements listed in the [top-level README](../README.md#requirements).
- Start Jupyter from this folder (or open the notebooks from here), because data paths such as `datasets/iris.csv` and `ranDat.csv` are relative.
- *Pandas Data Structures - A* uses `DataFrame.append`, which needs **pandas < 2.0**, or replace it with `pd.concat`.
- `fillna(method=...)` is deprecated in recent pandas.

## Author

Jose E. Rodriguez Rios
