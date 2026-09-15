# Confidence Intervals and K-Means Clustering

A lesson notebook with two parts: a **95% confidence interval for the difference between two means**, applied to the ages of Titanic survivors and non-survivors, and an **introduction to K-means clustering** on synthetic blobs. Three shorter notebooks compute **silhouette scores** for K-means. The last of them also compares K-means and the silhouette score in a short written answer.

---

## Contents

| Notebook | Topic | Techniques | Key libraries |
|---|---|---|---|
| [confidence_intervals_and_kmeans](confidence_intervals_and_kmeans.ipynb) | CI for a difference of means; K-means intro | z-interval with sample standard deviations, `make_blobs`, `KMeans`, centroid plots | pandas, numpy, scipy, scikit-learn, matplotlib |
| [silhouette_score_first_attempt](silhouette_score_first_attempt.ipynb) | Silhouette score (first attempt) | `make_blobs`, `KMeans`, `silhouette_score` | scikit-learn |
| [silhouette_score_uniform_data](silhouette_score_uniform_data.ipynb) | Silhouette score on uniform random data | `KMeans(n_clusters=3)`, `silhouette_score`, centroid plot | scikit-learn, numpy, matplotlib |
| [silhouette_choosing_k](silhouette_choosing_k.ipynb) | Silhouette score and choosing *k* | `KMeans` for k = 2 to 9, silhouette curve | scikit-learn, matplotlib |

**Data:** [`titanic_data.csv`](titanic_data.csv) is **included**. It has 714 passengers, all with a recorded age, and the columns `PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Embarked`. The other data is generated in the notebooks with `make_blobs` or `np.random`.

---

## confidence_intervals_and_kmeans.ipynb

### Part 1 — Confidence interval for a difference of means
1. Loads `titanic_data.csv` and prints mean ages. Saved values: **all passengers 29.70**, **survivors 28.34** (n = 290), **non-survivors 30.63** (n = 424).
2. Explains the interval
   $(\bar{x}_1-\bar{x}_2) \pm z_{\alpha/2}\sqrt{s_1^2/n_1 + s_2^2/n_2}$
   and its assumptions (Central Limit Theorem, independent groups).
3. Computes the interval with `scipy.stats.norm.ppf(0.975)`.

**Saved result:** 95% CI = **[−4.47, −0.10]** years. The interval does not contain 0 and both bounds are negative, so the notebook concludes that non-survivors were on average older at the 95% level.

### Part 2 — Introduction to K-means
1. Describes the K-means algorithm: random centroids, assign each point to the nearest centroid, recompute centroids, repeat. The markdown cells embed attached figures.
2. Generates 200 two-dimensional points from 3 blobs (`cluster_std=1.5`), plots them unlabeled and then colored by true blob.
3. Fits `KMeans(n_clusters=3, n_init='auto')` and shows `labels_`, `cluster_centers_`, and a scatter plot with centroid markers.
4. Makes the problem harder with 5 blobs and `cluster_std=3`, fits K-means with k = 5 and again with k = 2, and compares the plots. It observes that k = 2 separates this overlapping data reasonably well, which motivates the goodness-of-fit metrics covered next.

`make_blobs` is called without `random_state`, so points and centroids change on every run.

## silhouette_score_first_attempt.ipynb

Generates 300 points from 4 blobs (`random_state=0`) and fits `KMeans(n_clusters=4)`. **The saved run failed at `kmeans.predict(X)`** with `AttributeError: 'NoneType' object has no attribute 'split'`. This is an environment error (a known problem with older `threadpoolctl` versions used by scikit-learn), not a bug in the notebook's code. The silhouette cells after it were never executed.

## silhouette_score_uniform_data.ipynb

A separate silhouette example with different code from *silhouette_score_first_attempt*:
- 100 uniform random 2-D points (`np.random.seed(0)`) and `KMeans(n_clusters=3, random_state=0)`.
- Computes the silhouette score and plots the clusters with their centers.

**Saved result:** silhouette score **0.378**.

## silhouette_choosing_k.ipynb

1. 200 points from 3 blobs (`cluster_std=1.5`) and `KMeans(n_clusters=3)`. **Saved result:** average silhouette score **0.558**. Scatter plot with centroids.
2. Fits K-means for k = 2 to 9 and plots the average silhouette score against the number of clusters.
3. A markdown answer in Spanish compares the two: K-means is the clustering algorithm, while the silhouette score evaluates how well points sit within their own cluster relative to other clusters.

---

## Running

```bash
pip install pandas numpy scipy scikit-learn matplotlib seaborn jupyter
```

`n_init='auto'` requires scikit-learn 1.2 or newer. If *silhouette_score_first_attempt* raises the `'NoneType' object has no attribute 'split'` error, upgrade `threadpoolctl`.

## Author

Jose E. Rodriguez Rios
