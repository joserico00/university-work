# Pa11y Accessibility Audit: agricultura.pr

This project holds an automated accessibility audit of 18 public pages on the Puerto Rico Department of Agriculture website (`https://www.agricultura.pr`), run with [pa11y](https://pa11y.org/). A small Bash script runs pa11y on every URL in `urls.txt` and saves one report per page, both as machine-readable JSON and as human-readable text. The results were captured in October 2023. The [findings summary](#findings-summary) below is computed from those JSON files, and the goal is to point out concrete, fixable barriers that would make the site easier to use for people with disabilities.

---

## Table of contents

- [What is pa11y?](#what-is-pa11y)
- [How it works](#how-it-works)
  - [run_pally.sh, step by step](#run_pallysh-step-by-step)
  - [The text/ variant](#the-text-variant)
  - [Output file naming](#output-file-naming)
- [File-by-file reference](#file-by-file-reference)
- [JSON result schema](#json-result-schema)
- [Findings summary](#findings-summary)
- [Requirements](#requirements)
- [How to reproduce](#how-to-reproduce)
- [Author](#author)

---

## What is pa11y?

pa11y is an open-source Node.js command-line tool for **automated web accessibility testing**. For each URL it:

1. Opens the page in headless Chromium (through Puppeteer), so JavaScript-rendered content is tested as a browser displays it.
2. Runs a set of automated accessibility rules against the rendered DOM. The default rule engine ("runner") is **HTML_CodeSniffer** (`htmlcs`), and **axe** is available as an alternative.
3. Checks the page against the **WCAG 2 Level AA** standard (`WCAG2AA`) by default. WCAG (Web Content Accessibility Guidelines) is the W3C standard that most accessibility laws and policies reference.
4. Reports each problem with a rule code, a message, the CSS selector of the offending element, and an HTML snippet.

Issues come in three types: **error** (a detected failure), **warning** (likely a problem, needs human review), and **notice** (something to check manually). By default, pa11y reports **errors only**. Warnings and notices appear only when `--include-warnings` or `--include-notices` is passed.

Automated tools catch only part of all accessibility barriers. Keyboard navigation, screen-reader behavior, and content clarity still need manual testing.

---

## How it works

### `run_pally.sh`, step by step

```bash
#!/bin/bash

while IFS= read -r url; do
    filename=$(echo "$url" | sed 's/[^a-zA-Z0-9]/_/g').json
    pa11y "$url" --reporter json > "$filename"
done < urls.txt
```

1. **Read the URL list.** `done < urls.txt` feeds `urls.txt` (from the current directory) into the loop. `while IFS= read -r url` reads one full line per iteration: `IFS=` keeps leading and trailing whitespace, and `-r` stops backslashes from being treated as escapes.
2. **Build a filename.** `sed 's/[^a-zA-Z0-9]/_/g'` replaces every character that is not a letter or digit (`:`, `/`, `.`, `-`) with `_`, and `.json` is appended. For example, `https://www.agricultura.pr/autoridad-tierras` becomes `https___www_agricultura_pr_autoridad_tierras.json`.
3. **Run pa11y.** `pa11y "$url" --reporter json` audits the page. The script passes only the reporter flag, so pa11y uses its defaults:
   - Standard: `WCAG2AA`. Every result code starts with `WCAG2AA.`.
   - Runner: `htmlcs`. Every result has `"runner": "htmlcs"`.
   - Issue types: errors only. There are no `--include-warnings` or `--include-notices` flags.
4. **Save the report.** Standard output (the JSON array) is redirected into the file from step 2 in the current directory, overwriting any earlier result. Standard error (for example, page-load failures) is not captured and goes to the terminal.
5. **Continue.** pa11y exits with a non-zero status when it finds issues. The script does not check exit codes, so it moves on to the next URL either way.

### The `text/` variant

`text/` contains a second copy of `urls.txt` (identical) and a variant of `run_pally.sh` with two differences:

| | Root `run_pally.sh` | `text/run_pally.sh` |
|---|---|---|
| Output extension | `.json` | `.txt` |
| Reporter | `--reporter json` | none, so pa11y's default **CLI reporter** |

The CLI reporter prints a "Welcome to Pa11y" banner, the URL being tested, and a bulleted list of issues (message, rule code, selector, and HTML context). It ends with an `N Errors` total, or `No issues found!` for a clean page. Because the script reads `urls.txt` and writes to the current directory, run it from inside `text/`. The error counts in the 18 text reports match the JSON results exactly.

### Output file naming

| Audited URL | JSON result | Text report |
|---|---|---|
| `https://www.agricultura.pr/` | `https___www_agricultura_pr_.json` | `text/https___www_agricultura_pr_.txt` |
| `https://www.agricultura.pr/nosotros` | `https___www_agricultura_pr_nosotros.json` | `text/https___www_agricultura_pr_nosotros.txt` |
| `https://www.agricultura.pr/autoridad-tierras` | `https___www_agricultura_pr_autoridad_tierras.json` | `text/…_autoridad_tierras.txt` |
| `https://www.agricultura.pr/copy-of-laboratorio-veterinario` | `https___www_agricultura_pr_copy_of_laboratorio_veterinario.json` | `text/…_copy_of_laboratorio_veterinario.txt` |
| `https://www.agricultura.pr/fida` | `https___www_agricultura_pr_fida.json` | `text/…_fida.txt` |
| `https://www.agricultura.pr/csa` | `https___www_agricultura_pr_csa.json` | `text/…_csa.txt` |
| `https://www.agricultura.pr/ordenes-administrativas` | `https___www_agricultura_pr_ordenes_administrativas.json` | `text/…_ordenes_administrativas.txt` |
| `https://www.agricultura.pr/solicitudes` | `https___www_agricultura_pr_solicitudes.json` | `text/…_solicitudes.txt` |
| `https://www.agricultura.pr/olicpr` | `https___www_agricultura_pr_olicpr.json` | `text/…_olicpr.txt` |
| `https://www.agricultura.pr/pequenos-rumiantes` | `https___www_agricultura_pr_pequenos_rumiantes.json` | `text/…_pequenos_rumiantes.txt` |
| `https://www.agricultura.pr/documentos` | `https___www_agricultura_pr_documentos.json` | `text/…_documentos.txt` |
| `https://www.agricultura.pr/noticias` | `https___www_agricultura_pr_noticias.json` | `text/…_noticias.txt` |
| `https://www.agricultura.pr/comu` | `https___www_agricultura_pr_comu.json` | `text/…_comu.txt` |
| `https://www.agricultura.pr/about-3` | `https___www_agricultura_pr_about_3.json` | `text/…_about_3.txt` |
| `https://www.agricultura.pr/calendario-mercados` | `https___www_agricultura_pr_calendario_mercados.json` | `text/…_calendario_mercados.txt` |
| `https://www.agricultura.pr/noticias/categories/oportunidades-de-empleo` | `https___www_agricultura_pr_noticias_categories_oportunidades_de_empleo.json` | `text/…_noticias_categories_oportunidades_de_empleo.txt` |
| `https://www.agricultura.pr/blank-1` | `https___www_agricultura_pr_blank_1.json` | `text/…_blank_1.txt` |
| `https://www.agricultura.pr/contactanos` | `https___www_agricultura_pr_contactanos.json` | `text/…_contactanos.txt` |

Because every non-alphanumeric character becomes `_`, two URLs that differ only in punctuation (for example `/about-3` and `/about_3`) would write to the same file. No such collision exists in the current list.

---

## File-by-file reference

| Path | Description |
|---|---|
| `run_pally.sh` | Runs pa11y with the JSON reporter on each URL in `urls.txt` and writes `<sanitized-url>.json`. |
| `urls.txt` | The 18 page URLs to audit, one per line. |
| `https___www_agricultura_pr_*.json` (18 files) | pa11y JSON results, one per page. A page with no errors has an empty array (`[]`). |
| `text/run_pally.sh` | Same loop, using the default CLI reporter, writing `<sanitized-url>.txt`. |
| `text/urls.txt` | Identical copy of `urls.txt` so the text script can run from inside `text/`. |
| `text/https___www_agricultura_pr_*.txt` (18 files) | Human-readable pa11y CLI reports for the same pages. |
| `.gitignore` | Ignores OS files, Python caches, `.env`, `node_modules/`, `vendor/`, and `*.key`. |

---

## JSON result schema

Each JSON file is an **array of issue objects**, one per detected issue:

| Field | Type | Description |
|---|---|---|
| `code` | string | Rule identifier in the form `Standard.Principle.Guideline.SuccessCriterion.Technique[.Variant]`, e.g. `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail` → WCAG 2 AA, Principle 1 (Perceivable), Guideline 1.4, Success Criterion **1.4.3**, technique **G18**. |
| `type` | string | `"error"`, `"warning"`, or `"notice"` |
| `typeCode` | number | Numeric type: `1` = error, `2` = warning, `3` = notice |
| `message` | string | Explanation of the problem, sometimes with a fix recommendation |
| `context` | string | Truncated HTML snippet of the offending element |
| `selector` | string | CSS selector that locates the element in the page |
| `runner` | string | Rule engine that produced the issue (`"htmlcs"` in all results here) |
| `runnerExtras` | object | Runner-specific extra data (empty `{}` for htmlcs) |

Example record, from `https___www_agricultura_pr_calendario_mercados.json`:

```json
{
  "code": "WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail",
  "type": "error",
  "typeCode": 1,
  "message": "This element has insufficient contrast at this conformance level. Expected a contrast ratio of at least 4.5:1, but text in this element has a contrast ratio of 2.73:1. Recommendation:  change background to #00829b.",
  "context": "<span class=\"StylableButton2545352419__label wixui-button__label\" data-testid=\"stylablebutton-label\">Calendario Mercado Familiar Mes...</span>",
  "selector": "#comp-leesjn00 > a > div > span:nth-child(1)",
  "runner": "htmlcs",
  "runnerExtras": {}
}
```

---

## Findings summary

All figures below come from the 18 JSON result files (standard `WCAG2AA`, runner `htmlcs`, errors only).

### Headline numbers

| Metric | Value |
|---|---|
| Pages audited | **18** |
| Total issues | **47** |
| Errors | **47** |
| Warnings | 0 (not collected: `--include-warnings` was not used) |
| Notices | 0 (not collected: `--include-notices` was not used) |
| Pages with at least one error | 10 of 18 (56%) |
| Pages with no detected errors | 8 of 18 (44%) |
| Distinct rule codes triggered | 6 |
| Errors per page | mean 2.6, median 1 |
| Share of all errors on the home page | 27 of 47 (57%) |

**By WCAG principle:** Robust (4.1): 34 errors (72%) · Perceivable (1.3, 1.4): 10 errors (21%) · Operable (2.4): 3 errors (6%).

### Most frequent rule codes

Only **6 distinct rules** were triggered across the audit, so this list covers all of them. The request was for a top 10.

| # | Rule code | WCAG success criterion | Count | Pages |
|---|---|---|---|---|
| 1 | `WCAG2AA.Principle4.Guideline4_1.4_1_2.H91.Div.Name` | 4.1.2 Name, Role, Value | 19 (40%) | 3 |
| 2 | `WCAG2AA.Principle4.Guideline4_1.4_1_1.F77` | 4.1.1 Parsing | 13 (28%) | 1 |
| 3 | `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail` | 1.4.3 Contrast (Minimum) | 8 (17%) | 2 |
| 4 | `WCAG2AA.Principle2.Guideline2_4.2_4_1.H64.1` | 2.4.1 Bypass Blocks (frame titles) | 3 (6%) | 3 |
| 5 | `WCAG2AA.Principle4.Guideline4_1.4_1_2.H91.InputText.Name` | 4.1.2 Name, Role, Value | 2 (4%) | 2 |
| 6 | `WCAG2AA.Principle1.Guideline1_3.1_3_1.F68` | 1.3.1 Info and Relationships | 2 (4%) | 2 |

#### What each rule means

1. **Button without an accessible name** (`H91.Div.Name`, 19). Elements marked `role="button"` (17 clickable image-gallery items and image-zoom controls, plus 2 other clickable page elements) expose no text, `aria-label`, or `aria-labelledby`. A screen reader announces only "button" and never says what it does. *Fix:* give each control a descriptive `aria-label` (for example, "Enlarge image: …") or visible text. Found on the home page (14), `copy-of-laboratorio-veterinario` (4), and `pequenos-rumiantes` (1).
2. **Duplicate `id` attribute** (`F77`, 13). On the home page, 13 image elements share the same `id` value (`img_undefined`). IDs must be unique. Duplicates can break ARIA references, label associations, and in-page links for assistive technology. *Fix:* give each image a unique `id`, or remove the attribute when nothing references it. WCAG 2.2 retired SC 4.1.1 as a separate criterion, but unique IDs still matter whenever other markup references them.
3. **Insufficient color contrast** (`G18.Fail`, 8). Button label text fails the 4.5:1 minimum contrast ratio for normal-size text. Measured ratios were **2.73:1** on `calendario-mercados` (5 buttons) and **2.23:1** on `blank-1` (3 buttons). Low contrast makes text hard to read for people with low vision or color-vision deficiencies, and on screens in bright light. *Fix:* the tool suggests darker backgrounds of `#00829b` and `#4a8074` respectively; any color pair reaching at least 4.5:1 would work.
4. **Iframe without a title** (`H64.1`, 3). An embedded `<iframe>` (the same "Honeycomb" gallery widget on each page) has no `title` attribute. Screen-reader users hear an unlabeled frame and cannot tell what it contains or whether to skip it. *Fix:* add a short, descriptive `title`. Found once each on `nosotros`, `contactanos`, and `solicitudes`.
5. **Text input without an accessible name** (`H91.InputText.Name`, 2). The blog search box has only `placeholder="Search"`, which is not a reliable accessible name. *Fix:* add a `<label>` (it can be visually hidden) or `aria-label="Search"`. Found on `noticias` and `noticias/categories/oportunidades-de-empleo`.
6. **Form field not labelled** (`F68`, 2). The same search box, reported under the general form-labelling rule: no `<label>`, `title`, `aria-label`, or `aria-labelledby`. The fix for rule 5 also resolves this one. Same two pages.

### Errors by page

| Rank | Page | Errors | Breakdown |
|---|---|---|---|
| 1 | `/` (home) | **27** | 14 unnamed buttons, 13 duplicate IDs |
| 2 | `/calendario-mercados` | **5** | 5 low-contrast button labels |
| 3 | `/copy-of-laboratorio-veterinario` | **4** | 4 unnamed buttons |
| 4 | `/blank-1` | **3** | 3 low-contrast button labels |
| 5 | `/noticias` | 2 | Search input: no accessible name + no label |
| 5 | `/noticias/categories/oportunidades-de-empleo` | 2 | Search input: no accessible name + no label |
| 7 | `/nosotros` | 1 | Untitled iframe |
| 7 | `/contactanos` | 1 | Untitled iframe |
| 7 | `/solicitudes` | 1 | Untitled iframe |
| 7 | `/pequenos-rumiantes` | 1 | Unnamed button |
| – | `/about-3`, `/autoridad-tierras`, `/comu`, `/csa`, `/documentos`, `/fida`, `/olicpr`, `/ordenes-administrativas` | 0 | No errors detected |

### Observations

- **Errors cluster in shared components.** The page markup (for example `wixui-button__label` classes and gallery widgets loaded from the Wix static host) shows the site is built with a hosted site builder. All six rules point to reused components: image galleries, styled buttons, an embedded gallery iframe, and the blog search box. Fixing each component or its settings once (alt text and labels, button colors) would likely clear errors on every page that uses it.
- **The home page has the most impact.** It accounts for 57% of all errors, and every visitor passes through it. Naming the gallery controls and removing the duplicate IDs there would cut the total error count by more than half.
- **Eight pages passed the automated checks.** That is a good baseline, but a clean automated result does not prove a page is fully accessible, and warnings and notices were not collected in this run.
- **Point-in-time snapshot.** These results reflect the site as of October 2023 and may not match the current live site.

---

## Requirements

- **Node.js** and **npm**. Recent pa11y releases require a current LTS version of Node.js; check the pa11y README for the version your release supports.
- **pa11y**, installed globally. It installs Puppeteer, which downloads a compatible headless Chromium on first install.
- **Bash** (macOS, Linux, or WSL on Windows).
- Optional: **Python 3**, to recompute the summary statistics.

---

## How to reproduce

```bash
# 1. Install pa11y globally
npm install -g pa11y

# 2. JSON results (run from the repository root; overwrites the existing .json files)
./run_pally.sh

# 3. Human-readable text reports (must be run from inside text/)
cd text
./run_pally.sh
cd ..
```

If the scripts are not executable after cloning, run `chmod +x run_pally.sh text/run_pally.sh`.

**Recompute the findings summary** from the JSON files:

```bash
python3 - <<'EOF'
import json, glob, collections
types, codes, pages = collections.Counter(), collections.Counter(), {}
for f in sorted(glob.glob("https___*.json")):
    issues = json.load(open(f))
    pages[f] = len(issues)
    types.update(i["type"] for i in issues)
    codes.update(i["code"] for i in issues)
print("Pages audited:", len(pages))
print("Issues by type:", dict(types))
for code, n in codes.most_common(10):
    print(f"{n:4}  {code}")
for f, n in sorted(pages.items(), key=lambda kv: -kv[1]):
    print(f"{n:4}  {f}")
EOF
```

**Going further.** The same commands accept extra pa11y options for a broader audit, for example `--include-warnings --include-notices` (review-needed items), `--standard WCAG2AAA` (stricter level), or `--runner axe` (a different rule engine). Results will differ between pa11y versions, and as the live site changes.

---

## Author

Jose E. Rodriguez Rios
