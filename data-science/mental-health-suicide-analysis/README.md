# Mental Health and the Economy: Suicide vs. Inflation Analysis

My individual analysis for a group data science project, *"Mental Health and Its Relationship With The Economy"* (2023). My variable was **mental health**, measured through suicide data, compared against economic indicators and natural disasters.

## Questions explored

1. How have reported suicide cases changed year by year?
2. Is there a relationship between inflation and the number of suicides?
3. Do natural disasters affect people emotionally and financially?

## What the analysis does

- Cleans and groups CDC WONDER suicide data by year
- Joins it with the Bureau of Labor Statistics Consumer Price Index (inflation)
- Uses scatter plots and correlation to measure the relationship between suicide and inflation
- Trains a scikit-learn linear regression model to predict suicide counts from inflation
- Explores disaster data from EM-DAT and OpenFEMA alongside CDC anxiety/depression indicators

**Finding:** the data showed suicides rising over the years and a significant positive correlation with inflation, which suggests a link between mental health and economic conditions.

## Project structure

```
notebooks/
├── finalJose.ipynb             # Final analysis: suicide vs. inflation, regression model, conclusions
├── datascience project.ipynb   # Exploratory work: suicides, disasters, inflation, anxiety/depression
├── Questions.ipynb             # Research questions
├── union.ipynb                 # Tool that merges the team's notebooks into one
├── unionlibrary.py             # Script version of the notebook merger
├── CPI.csv, Test.csv           # Working copies of data used by the exploratory notebook
data/
├── suicide/                    # CDC WONDER suicide data, CDC suicide report
├── inflation/                  # BLS Consumer Price Index
├── cdc_mental_health/          # CDC anxiety/depression symptom indicators
└── disasters/                  # EM-DAT disasters, OpenFEMA disaster declarations
```

## Running it

```bash
pip install numpy pandas matplotlib seaborn scipy scikit-learn openpyxl jupyter
cd notebooks
jupyter notebook finalJose.ipynb
```

## Data sources

- [CDC WONDER](https://wonder.cdc.gov/)
- [U.S. Bureau of Labor Statistics CPI](https://www.bls.gov/cpi/data.htm)
- [CDC: Indicators of Anxiety or Depression](https://data.cdc.gov/)
- [EM-DAT International Disaster Database](https://www.emdat.be/)
- [OpenFEMA Disaster Declarations Summaries](https://www.fema.gov/openfema)

## Author

Jose E. Rodriguez Rios
