# Bioinformatics Motif Scripts

Two small scientific-computing scripts. `bedline.py` converts motif-scanning results from **MOODS** (CSV) into a color-coded **BED** track that can be viewed in a genome browser such as UCSC or IGV. `recursive_ftt.py` is a textbook **recursive Fast Fourier Transform** that evaluates a polynomial at the complex n-th roots of unity using divide and conquer. Both use only the Python standard library.

## Contents

| File | Description |
|---|---|
| [`bedline.py`](#bedlinepy-moods-csv-to-bed-track) | MOODS CSV hits → BED9 track with per-motif colors (`itemRgb`) |
| [`recursive_ftt.py`](#recursive_fttpy-recursive-fast-fourier-transform) | Recursive FFT over complex roots of unity. "ftt" in the file name, and `vtt` in the function name, are typos for FFT. |

---

## Background

### MOODS output

MOODS (Motif Occurrence Detection Suite) scans DNA sequences with position frequency matrices (`.pfm` files) and reports every match above a score threshold. Its command-line scanner writes one CSV line per hit. `bedline.py` reads the first six fields:

| Index | Field | Example |
|---|---|---|
| `row[0]` | Name of the scanned sequence, in `chrom:start-end` form | `chr1:1000-1200` |
| `row[1]` | Matrix (PFM) file name | `Nkx2-5Tbx5_019_monNKX_edit6bp.pfm` |
| `row[2]` | Hit position (offset inside the sequence) | `15` |
| `row[3]` | Strand | `+` or `-` |
| `row[4]` | Match score | `7.42` |
| `row[5]` | Matched DNA sequence | `TCAAGT` |

Sequence names like `chr1:1000-1200` are what `bedtools getfasta` produces when it extracts region sequences from a genome, so the script can turn offsets within a region back into genome coordinates.

### BED format

BED is a tab-separated text format for genome annotations, used by the UCSC Genome Browser, IGV, bedtools and many other tools. Coordinates are **0-based and half-open**: `chromStart` is the first base, and `chromEnd` is one past the last base. The first three columns are required; `bedline.py` writes nine (BED9):

| # | Column | What `bedline.py` writes |
|---|---|---|
| 1 | `chrom` | Chromosome from the sequence name (`chr1`) |
| 2 | `chromStart` | `hitstart` = region start + hit position |
| 3 | `chromEnd` | `hitend` = `hitstart` + motif length |
| 4 | `name` | The PFM file name |
| 5 | `score` | The MOODS score, copied unchanged |
| 6 | `strand` | `+` / `-` from MOODS |
| 7 | `thickStart` | `0` |
| 8 | `thickEnd` | `0` |
| 9 | `itemRgb` | `R,G,B` color for the motif |

A BED file can start with header lines. `browser …` lines set the UCSC view, and a `track …` line sets the track's name, description and display options.

---

## `bedline.py`: MOODS CSV to BED track

### How it works

`moods_csv_to_bed(input_csv, output_bed)`:

1. **Motif-length regex.** `pattern = r"(\d+)bp\.pfm$"` captures the number right before `bp.pfm` at the end of the matrix file name. For example, `…_seed1_edit12bp.pfm` gives `12`, the motif length in base pairs. A Spanish comment in the code asks that every PFM file name end in `<number>bp.pfm` for this reason.
2. **Color table.** A dictionary maps each of five known PFM file names to an RGB color:

   | PFM file | Label in file name | Length | RGB | Color |
   |---|---|---|---|---|
   | `Nkx2-5Tbx5_019_monNKX_edit6bp.pfm` | `monNKX` | 6 bp | `102,204,255` | light blue |
   | `Nkx2-5Tbx5_019_monTBX_edit6bp.pfm` | `monTBX` | 6 bp | `255,153,153` | light red |
   | `Nkx2-5Tbx5_019_seed1_edit12bp.pfm` | `seed1` | 12 bp | `153,51,255` | purple |
   | `Nkx2-5Tbx5_019_seed2_edit17bp.pfm` | `seed2` | 17 bp | `153,102,255` | medium purple |
   | `Nkx2-5Tbx5_019_seed3_edit19bp.pfm` | `seed3` | 19 bp | `153,153,255` | lavender |

3. **Header lines.** It opens the output file and writes:
   ```
   browser position chr1:1-1000
   track name="moods_hits2" description="MOODS hits" visibility=2 itemRgb="On"
   ```
   `visibility=2` shows the track in full mode, and `itemRgb="On"` tells the browser to color each feature using column 9.
4. **One BED line per CSV row:**
   - split `row[0]` on `:` to get the chromosome, then split the range on `-` to get the region start and end
   - `hitstart = int(region_start) + int(row[2])`
   - `hitend = hitstart + motif_length` (the length comes from the regex, not from `row[5]`)
   - look up the color with `color[name]`
   - write the tab-separated BED9 line

**Command line:** `python3 bedline.py input_csv output_bed`. Any other number of arguments prints `Usage: bedline.py input_csv output_bed` and exits with status 1.

### Coordinates

The script assumes the region start in the sequence name and the MOODS hit position are both 0-based. That is the convention for `bedtools getfasta` names, which come from BED intervals. Under that assumption, `hitstart` is the 0-based first base of the motif and `hitend` is the exclusive end, so every feature covers exactly the motif length:

```
region chr1:1000-1200, hit at offset 15, 6 bp motif
chromStart = 1000 + 15 = 1015
chromEnd   = 1015 + 6  = 1021   →  displayed in browsers as chr1:1,016-1,021
```

If your sequence names use 1-based starts, every hit will be shifted by one base.

### Example

Input (`hits.csv`):

```
chr1:1000-1200,Nkx2-5Tbx5_019_monNKX_edit6bp.pfm,15,+,7.42,TCAAGT,
chr3:50000-50400,Nkx2-5Tbx5_019_seed3_edit19bp.pfm,120,-,11.9,AGGTGTGAAGTGTTTCAAG,
```

Output (`hits.bed`, tab-separated):

```
browser position chr1:1-1000
track name="moods_hits2" description="MOODS hits" visibility=2 itemRgb="On"
chr1	1015	1021	Nkx2-5Tbx5_019_monNKX_edit6bp.pfm	7.42	+	0	0	102,204,255
chr3	50120	50139	Nkx2-5Tbx5_019_seed3_edit19bp.pfm	11.9	-	0	0	153,153,255
```

### Notes and limitations

- **Only the five hard-coded PFM names work.** Any other matrix name raises `KeyError`, and a name that doesn't end in `<number>bp.pfm` raises `AttributeError` because the regex finds no match. To add a motif, add an entry to `color`.
- **Score column.** The BED specification, and UCSC custom tracks, expect an integer score from 0 to 1000. MOODS scores are floating-point and can be negative, so UCSC may reject the file unless the scores are rounded or rescaled. IGV accepts the scores as written.
- **`thickStart`/`thickEnd` are both 0.** That falls outside every feature, so browsers draw no thick region and hits show up as thin bars. Setting these columns to `hitstart`/`hitend` would draw full-height blocks.
- The `browser position chr1:1-1000` line always opens UCSC at the start of chr1, wherever the hits are.
- The CSV must not have a header row, and blank lines will cause errors.
- `start`, `end`, `Dna`, `rgbstr` and `hitposition` are computed but not written. Four commented-out `bed_line` variants remain in the code; they would have written the region coordinates or the DNA sequence as extra columns.
- The output file is overwritten on every run.

### Loading the track in a genome browser

**UCSC Genome Browser**
1. Open the Genome Browser and go to **My Data → Custom Tracks**.
2. Pick the **same genome assembly** that the region coordinates came from (for example hg19 or hg38).
3. Upload `hits.bed`, or paste its contents, and click **Submit**, then **go to genome browser**.
4. The `track` line names the track "moods_hits2", and features are colored by motif. Round the score column first if UCSC reports a score error.

**IGV (desktop or igv.js web app)**
1. Select the matching genome.
2. Use **File → Load from File…** and choose `hits.bed`.
3. IGV reads the `track` line and uses the `itemRgb` colors. The `browser` line is UCSC-specific.

To sort the features or use them with bedtools, remove the header lines first:

```bash
grep -v -e '^browser' -e '^track' hits.bed | sort -k1,1 -k2,2n > hits.sorted.bed
```

---

## `recursive_ftt.py`: recursive Fast Fourier Transform

### Problem

Given the coefficients `a = [a₀, a₁, …, aₙ₋₁]` of a polynomial A(x) = Σ aⱼ xʲ, where `n` is a power of 2, compute the **discrete Fourier transform**

  yₖ = A(ωₙᵏ),  k = 0 … n−1,  where ωₙ = e^(2πi/n)

is the principal n-th root of unity. This converts a polynomial from coefficient form to its values at the n complex roots of unity. It is the first step of O(n log n) polynomial multiplication; the second step, the inverse transform, is not implemented here.

### Divide and conquer on even and odd coefficients

`recursive_vtt(a)` follows the classic `RECURSIVE-FFT` procedure:

1. **Base case:** if `n == 1`, return `a`, because a constant polynomial has the same value at every point.
2. **Setup:** `wn = cmath.exp(2*cmath.pi*1j/n)` (that is, ωₙ) and `w = 1`.
3. **Split by parity:** `a0 = a[0:n:2]` holds the even-index coefficients and `a1 = a[1:n:2]` the odd-index ones. They define two polynomials of half the size:

   A_even(x) = a₀ + a₂x + a₄x² + …   A_odd(x) = a₁ + a₃x + a₅x² + …

   These satisfy **A(x) = A_even(x²) + x · A_odd(x²)**.
4. **Recurse:** `y0 = recursive_vtt(a0)` and `y1 = recursive_vtt(a1)` evaluate the halves at the (n/2)-th roots of unity. The squares of the n-th roots of unity are exactly the (n/2)-th roots of unity (the halving lemma), so `y0[k]` = A_even((ωₙᵏ)²) and `y1[k]` = A_odd((ωₙᵏ)²).
5. **Combine:** for `k` in `0 … n/2−1`, with `w` = ωₙᵏ:
   - `y[k] = y0[k] + w*y1[k]`, which is A(ωₙᵏ)
   - `y[k + n/2] = y0[k] - w*y1[k]`, which is A(ωₙᵏ⁺ⁿᐟ²), because ωₙⁿᐟ² = −1 and both points have the same square
   - `w = w*wn` moves to the next root
6. Return `y`.

### Complexity

- **Time:** T(n) = 2T(n/2) + Θ(n), which gives **Θ(n log n)**, compared with Θ(n²) for evaluating A at n points one at a time with Horner's rule.
- **Space:** recursion depth log₂ n. Each call allocates Θ(n) for the two slices and the output list, so at most Θ(n) extra memory is in use at once (Θ(n log n) allocated over the whole run).

### Example

The script evaluates A(x) = 3 + 5x + 4x² + x³ (`a = [3, 5, 4, 1]`) at the 4th roots of unity (ω₄ = i):

| k | x = iᵏ | A(x) | Printed value |
|---|---|---|---|
| 0 | 1 | 13 | `(13+0j)` |
| 1 | i | −1 + 4i | `(-0.9999999999999998+4j)` |
| 2 | −1 | 1 | `(1+0j)` |
| 3 | −i | −1 − 4i | `(-1.0000000000000002-4j)` |

```
$ python3 recursive_ftt.py
[(13+0j), (-0.9999999999999998+4j), (1+0j), (-1.0000000000000002-4j)]
```

The tiny errors come from floating-point roots of unity. For an 8-coefficient polynomial, the results matched direct Horner evaluation to within 2×10⁻¹⁴.

### Limitations

- **The length must be a power of 2.** Otherwise the two halves have different lengths and some outputs are never filled in: `recursive_vtt([1, 2, 3])` returns `[(6+0j), (2+0j), 0]` instead of the values at the cube roots of unity.
- Only the forward transform is implemented. Interpolation or polynomial multiplication would also need the inverse FFT (use ωₙ⁻¹ and divide by n).
- The base case returns the input list itself, so a 1-element input comes back as integers rather than complex numbers.

---

## Requirements

- Python 3.6+ (`bedline.py` uses f-strings)
- Standard library only: `csv`, `re`, `sys`, `cmath`
- Optional, to produce the input: MOODS (`pip install MOODS-python`) and `bedtools`

## Usage

```bash
# Convert MOODS hits to a BED track
python3 bedline.py moods_hits.csv moods_hits.bed

# Run the FFT example
python3 recursive_ftt.py
```

One possible pipeline for producing `moods_hits.csv` (adjust the paths and threshold):

```bash
bedtools getfasta -fi genome.fa -bed regions.bed -fo regions.fa        # names: chrom:start-end
moods-dna.py -m Nkx2-5Tbx5_019_*bp.pfm -s regions.fa -p 0.0001 -o moods_hits.csv
python3 bedline.py moods_hits.csv moods_hits.bed
```

## Author

Jose E. Rodriguez Rios
