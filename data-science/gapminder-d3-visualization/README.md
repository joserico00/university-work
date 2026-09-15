# Gapminder D3 Visualization

An interactive D3.js (v5) bubble chart of a Gapminder country subset: **fertility (children per woman) on the x-axis, life expectancy on the y-axis, bubble size by population, and bubble color by a pre-assigned country cluster**. A year selector re-joins the data for the chosen year and animates the bubbles and country labels to their new positions, and hovering a bubble shows a tooltip with the country's values. The page is a single self-contained HTML file that loads `gapminder.csv` from the same folder.

The code is based on the Observable notebook [Introduction to D3, Part 2](https://observablehq.com/@uwdata/introduction-to-d3-part-2), which is credited in a comment at the top of each HTML file.

---

## Contents

| File | What it is |
|---|---|
| [`gapminder-d3-JoseERodriguezRios.html`](gapminder-d3-JoseERodriguezRios.html) | The author's finished visualization (main file). |
| [`gapminder-d3-template.html`](gapminder-d3-template.html) | The template file. In this project it already holds the completed code and differs from the author's file by a single attribute (see [Template vs. author's file](#template-vs-authors-file)). |
| [`gapminder-d3-toolboxtest`](gapminder-d3-toolboxtest) | An intermediate version used to test the tooltip. It has no file extension. |
| [`DUPL`](DUPL) | An earlier draft, before the tooltip was implemented. It has no file extension. |
| [`gapminder.csv`](gapminder.csv) | The data the page loads (693 rows). |
| [`gapminder.json`](gapminder.json) | The same 693 records as JSON. No HTML file in the repo loads it. |

---

## The data

`gapminder.csv` has the columns `year, country, cluster, pop, life_expect, fertility`:

- **63 countries × 11 years** (1955 to 2005 in 5-year steps), 693 rows in total.
- `pop` ranges from about 54 thousand to 1.30 billion, `life_expect` from 23.6 to 82.6 years, and `fertility` from 0.94 to 8.5.
- `cluster` is an integer from 0 to 5 that is already in the data. In this file the clusters group countries roughly by region:

| Cluster | Countries in the file | Bubble color |
|---|---|---|
| 0 | Afghanistan, Bangladesh, India, Pakistan | red |
| 1 | 17 European countries plus Georgia and Turkey | yellow |
| 2 | Kenya, Nigeria, Rwanda, South Africa | blue |
| 3 | 21 countries in the Americas (Canada, United States, Latin America, Caribbean) | green |
| 4 | Australia, China, Hong Kong, Indonesia, Japan, New Zealand, North Korea, Philippines, South Korea | red |
| 5 | Egypt, Iran, Iraq, Israel, Lebanon, Saudi Arabia | red |

`gapminder.json` holds the same records as a JSON array. `pop` is stored as a number and the other fields as strings.

The data is a subset of [Gapminder](https://www.gapminder.org/data/) indicators.

---

## How the visualization works

The whole page is in `gapminder-d3-JoseERodriguezRios.html`. D3 v5 is loaded from `https://d3js.org/d3.v5.js`.

### Setup (`init()`)
- Creates a 600 × 400 px SVG inside `#my_dataviz`.
- Loads `gapminder.csv` with `d3.csv`, turns `pop` into a number, and calls `build(data)`.

### Scales and encodings (`build()`)

| Channel | Field | Scale |
|---|---|---|
| x position | `fertility` | `d3.scaleLinear()`, domain `[0, max(fertility)]`, `.nice()` |
| y position | `life_expect` | `d3.scaleLinear()`, domain `[0, max(life_expect)]`, `.nice()`, inverted range |
| bubble radius | `pop` | `d3.scaleThreshold()` with thresholds 1M, 10M, 100M, 1B mapped to radii 3, 6, 12, 24 px |
| bubble color | `cluster` | `d3.scaleOrdinal()`, domain 0 to 5, range red, yellow, blue, green, red, red |
| label font size | `pop` (through the radius) | `getTextSize()`: 4, 8, 10 or 14 px |
| opacity | none | 0.5 on the first render, 0.75 on bubbles created later |

- The x-axis (`d3.axisBottom`) is labeled **Fertility** and the y-axis (`d3.axisLeft`) **Life Expectancy**.
- A large light-gray year label (80 px) sits in the lower-left of the chart.
- Bubbles are keyed by `country` and sorted by population in descending order, so small bubbles are drawn on top of large ones.
- Each bubble has a country-name label 15 px below its center.

### Time control and animation (`setYear()`)
- A `<select id="mySelect">` dropdown is filled with the unique years. Despite the "slider" comment in the code, the control is a dropdown and does not autoplay.
- Choosing a year calls `setYear(year)`, which:
  1. Updates the big year label.
  2. Filters the data to that year and re-joins the circles with `selection.join(enter, update, exit)`, keyed by country. Existing circles move to the new `cx`/`cy` (and re-apply `fill`) over a **500 ms transition**. New circles are appended and missing ones are removed.
  3. Re-joins the text labels the same way, moving them and updating their font size over 500 ms.

### Tooltips
- `mouseover` fills the absolutely positioned `#tooltip` div with **Country, Population, Fertility, Life Expectancy** and makes it visible.
- `mousemove` places the tooltip 20 px right of and below the pointer, using `d3.mouse(this)`.
- `mouseout` hides the tooltip.

### Implementation notes (current behavior of the code)
- Bubble radius is set only when a circle is created. The year transition updates position and color but not `r`, so bubble sizes stay at their 1955 values. Label font sizes do update.
- The threshold scale has four thresholds and four output radii, so populations of 1 billion or more fall outside the defined range. In this data that affects China (1985 to 2005) and India (2000 to 2005). It only changes label sizing, which falls back to 14 px.
- Only `pop` is converted to a number. `fertility` and `life_expect` stay strings, and D3 converts them when it applies the scales. `d3.max` compares them as text, which still gives the right answer here because every value in each column has the same number of integer digits.
- Three clusters (0, 4 and 5) share the color red, and the chart has no legend.

---

## Template vs. author's file

In this project the two HTML files are nearly identical. Both contain the tooltip, the labels and the `setYear` transitions, and both still carry the original exercise comments ("Modify to add color based on cluster and radius based on population", "Complete to update circles with changed year", "Add transition from old values to new values"). A whitespace-insensitive `diff` shows one difference:

| | `gapminder-d3-template.html` | `gapminder-d3-JoseERodriguezRios.html` |
|---|---|---|
| Opacity of the first set of bubbles | `.attr('opacity', 0.75)`, set before `fill` | `.attr('opacity', 0.5)`, set after `fill` |

The two draft files show how the work got there:

- **`DUPL`** (earlier draft): the circles, labels and `setYear` transitions are already in place. Its `mouseover`/`mouseout` handlers only `console.log` the element, and `#tooltip` is a plain div with a green border, so no tooltip content is shown.
- **`gapminder-d3-toolboxtest`** (tooltip test): adds the full tooltip handlers and a styled tooltip div. The `tooltip` selection is declared with `var` inside `init()`, but the handlers that use it run in `build()`, where that variable is not in scope, so the tooltip does not work in this version. The author's final file fixes this by declaring `tooltip` inside `build()`.

Both draft files and the template use Unix line endings. The template and the author's file use Windows (CRLF) line endings.

---

## How to view locally

`d3.csv` fetches the data over HTTP, so opening the file straight from disk (`file://`) is blocked by most browsers. Serve the folder instead:

```bash
cd gapminder-d3-visualization
python3 -m http.server 8000
```

Then open <http://localhost:8000/gapminder-d3-JoseERodriguezRios.html> and pick a year from the dropdown.

- An internet connection is needed the first time, because D3 v5 is loaded from `d3js.org`.
- `DUPL` and `gapminder-d3-toolboxtest` have no `.html` extension, so `http.server` sends them as generic files and the browser will download them instead of rendering them. Open them in a text editor to read the code.

## Requirements

- A modern web browser
- Python 3, only for the local static server (any static file server works)
- No build step or npm packages

## Author

Jose E. Rodriguez Rios
