# Algorithms Practice

A collection of Python solutions and work-in-progress attempts at classic interview and competitive-programming problems: sliding window, two pointers, hashing, binary search, selection (quickselect and median of medians), divide and conquer, dynamic programming, grid DFS, matrix puzzles, and HackerRank-style exercises. Most files are standalone scripts with hard-coded sample input; the HackerRank-style files read from standard input.

This is a practice repository, so the files are at different stages. Each section below states whether the file runs, runs with known bugs, or is unfinished, and the complexity figures are derived from the code as written.

## Contents

### Sliding window

| File | Problem | Technique | Complexity |
|---|---|---|---|
| `smallsumS.py` | Smallest contiguous subarray with sum >= S | Variable-size sliding window | O(n) time, O(1) space |
| `maximunsumarrray.py` | Maximum sum of a contiguous subarray of size k | Fixed-size sliding window | O(n) time, O(1) space |
| `arrayaveerage.py` | Average of every contiguous subarray of size k | Brute force vs. fixed-size sliding window | Brute force O(n·k) summing plus O(n) per `pop(0)`; sliding window O(n) |
| `slidingstring.py` `strinsubstring(s, k)` | Longest substring with at most k distinct characters | Sliding window + frequency hash map | O(n) time, O(k) space |
| `slidingstring.py` `fruitsplit(arr, k)` | Fruits into baskets (at most 2 kinds) | Same as above with k fixed to 2 | O(n) time, O(1) space |
| `slidingstring.py` `strinsubstring(s)` | Longest substring without repeating characters | Sliding window + frequency hash map | O(n·σ), σ = distinct characters (calls `max()` over the map) |
| `slidingstring.py` `repeatablestring(s, k)` | Longest same-letter substring after k replacements (buggy) | Sliding window | O(n) |
| `slidingstring.py` `binaires(arr, k)` | Longest run of 1s after flipping at most k zeros | Non-shrinking sliding window with a counter | O(n) time, O(1) space |
| `slidingstring.py` `permutation(s, p)` | Does `s` contain a permutation of `p` | Fixed-size window + character counts | O(n + m) time, O(m) space |
| `slidingstring.py` `matchingletters(s, p)` | Smallest window containing all characters of `p` (buggy) | Variable-size window + character counts | O(n + m) time, O(m) space |

### Two pointers, hashing and binary search

| File | Problem | Technique | Complexity |
|---|---|---|---|
| `twopointers.py` `pair_with_targetsum` (1st and 3rd) | Pair with target sum in a sorted array (buggy) | Two pointers | O(n); 3rd version adds an O(n log n) sort |
| `twopointers.py` `pair_with_targetsum` (2nd) | Pair with target sum | Hash map of complements | O(n) time, O(n) space |
| `twopointers.py` `make_squares` | Sorted squares of a sorted array | Two pointers from both ends | O(n²) as written (`insert(0, …)`) |
| `twopointers.py` `remove_duplicates` | Number of distinct values in a sorted array | Adjacent comparison | O(n) time, O(1) space |
| `2SUM.py` `bruteforce` | Does any pair sum to a target | Nested loops | O(n²) time, O(1) space |
| `4sum.py` | Does any pair sum to a target (despite the file name) | Binary search for the complement | O(n log n) comparisons, but O(n²) time and O(n) space because of slicing |

### Divide and conquer, selection and partitioning

| File | Problem | Technique | Complexity |
|---|---|---|---|
| `ALGORITHIM.ipynb` | Partition an array so even numbers come first | Lomuto partition with a parity test | O(n) time, O(1) extra space |
| `examenalgo.py` `Select25` | 25th-percentile element | Randomized select (quickselect) | Expected O(n), worst O(n²) |
| `examenalgo.py` `SELECT` / `product.py` | i-th smallest element (buggy) | Median of medians, groups of 5 | Intended worst-case O(n) |
| `mediansort.py` | Median of two sorted arrays of equal length (buggy base case) | Divide and conquer on the two medians | O(log n) levels; O(n) total with list slicing |
| `2SUM.py` `PowRec` / `Powiter` / `PowDC` / `PowDCIterFast` | Compute xⁿ | Linear recursion / loop / divide and conquer / binary exponentiation | O(n) / O(n) / O(log n) / O(log n) |

### Dynamic programming

| File | Problem | Technique | Complexity |
|---|---|---|---|
| `brute.py` `maxSubArrayProduct` | Maximum product subarray with indices | Brute force over all subarrays with a running product | O(n²) time, O(1) space |
| `brute.py` `max_product_subarray` | Maximum product subarray indices (buggy indices) | Max/min product ending here (Kadane variant) | O(n) time, O(1) space |
| `examenalgo.py` `maxSubarrayProduct(arr, n)` | Maximum product subarray value | Max/min product ending here | O(n) time, O(1) space |
| `examenalgo.py` `MaxProduct`, `maxSubAayProduct` | Maximum product subarray indices (buggy indices) | Kadane variant with a swap on negatives | O(n) time, O(1) space |
| `examenalgo.py` `MaxProductSubAaybruteforce` | Largest product of two distinct elements | Nested loops | O(n²) time |

### Graphs and matrices

| File | Problem | Technique | Complexity |
|---|---|---|---|
| `island.py` | Number of islands in a 0/1 grid | DFS flood fill (the BFS version is broken) | O(R·C) time, O(R·C) worst-case recursion depth |
| `diagonaldiffrence.py` | Absolute difference of the two diagonal sums | One pass per diagonal | O(n) time, O(1) space |
| `flipinfmatrix.py` | Flipping the Matrix (maximize the upper-left quadrant) | Greedy: best of four mirror cells | O(n²) for a 2n×2n matrix |

### Sorting, counting and string exercises (HackerRank style)

| File | Problem | Technique | Complexity |
|---|---|---|---|
| `frecquency.py` | Counting sort part 1: frequency of values 0–99 | Counting array | O(n + 100) time, O(100) space |
| `median.py` | Median of a list (broken) | Sort, then index | O(n log n) |
| `ZIGZAG.PY` | Zig Zag Sequence | Sort, swap, reverse the right half | O(n log n) time, O(1) extra space |
| `timeconversion.py` | 12-hour to 24-hour time (unfinished) | Character-list manipulation | O(1) (fixed-length input) |
| `strnvalid.py` | String validators (buggy) | Linear scans | O(n) per check intended |
| `tuple.py` | Hash of a tuple of integers | Built-in `hash` | O(n) |

### Randomized, stack and miscellaneous

| File | Problem | Technique | Complexity |
|---|---|---|---|
| `nuts.py` | Pair identical items by "shaking a bag" (buggy shuffle) | Las Vegas randomized algorithm | O(n²) per round worst case; number of rounds is random |
| `window.py` | Baseball Game score, plus an unfinished stub (does not compile) | Stack | O(n) time, O(n) space |
| `decode.py` | Decode raw bytes as UTF-16 (trivial) | n/a | n/a |
| `binarymedian.py` | Median of two sorted arrays with binary search (stub) | n/a | n/a |
| `mug.py` | Mug-color input exercise (unfinished) | n/a | n/a |
| `group.py` | Not an algorithm: the python-nmap project's example script (third-party) | n/a | n/a |

---

## Sliding window

### `smallsumS.py`: smallest subarray with a given sum

**Status:** runs. The call at the bottom doesn't print anything, because its return value is never printed.

- **Problem:** find the length of the shortest contiguous subarray whose sum is at least `S`.
- **Approach (`smallsum(array, s)`):**
  1. Move `windowend` across the array and add each element to `windowsum`.
  2. While `windowsum >= s`, record the window length if it is the smallest so far, subtract `array[windowstart]`, and move `windowstart` forward.
  3. Return `smallestlen`.
- **Input/output:** hard-coded `array = [2, 1, 5, 2, 3, 2]`, `S = 7`. The function returns `2` (the subarray `[5, 2]`).
- **Complexity:** O(n) time, because each element enters and leaves the window at most once. O(1) extra space.
- **Notes:** `smallestlen` starts at the sentinel `99`. If no window reaches `s`, the function returns `99` instead of 0 (for example, `smallsum([1, 1], 5)`), and it can never report a length above 99. The `lists` variable is unused.

### `maximunsumarrray.py`: maximum sum subarray of size k

**Status:** runs and prints `9`.

- **Problem:** find the largest sum of any `k` consecutive elements.
- **Approach (`summaxarray(array, k)`):** keep a running `windowsum`. Once the window holds `k` elements (`windowend >= k - 1`), compare it with `maxsum`, subtract the outgoing element and slide `windowstart` forward.
- **Input/output:** `array = [2, 1, 5, 1, 3, 2]`, `K = 3`. It prints `9` (from `[5, 1, 3]`).
- **Complexity:** O(n) time, O(1) space.
- **Notes:** `maxsum` starts at `0`, so an array of all negative numbers prints `0`. `result`, `aritarray` and the final `array = []` are unused.

### `arrayaveerage.py`: averages of subarrays of size K

**Status:** runs. Only the sliding-window version is called.

- **Problem:** return the average of every contiguous subarray of length `K`.
- **`bruteforce(array, K)`:** while at least `K` elements remain, append `sum(aritarray[:K]) / K` and `pop(0)` the first element. Each step costs O(K) for the sum plus O(n) for `pop(0)`, which is O(n·K + n²) in the worst case. `aritarray` is the caller's list, not a copy, so the input list gets emptied.
- **`sliding(array, K)`:** keep a running sum. Once the window is full, append `windowsum / K`, subtract the outgoing element and move the start forward. O(n) time, O(n − K) output space.
- **Output:** for `[1, 3, 2, 6, -1, 4, 1, 8, 2]` with `K = 5`, it prints `[2.2, 2.8, 2.4, 3.6, 2.8]`.

### `slidingstring.py`: sliding-window string problems

**Status:** runs and prints the output below. Several functions are buggy or unfinished, as noted in each item.

```
5
max 3
repeatareplace 2
binaries 6
binaries True
maatchingletters abdec
maatchingletters abdec
```

Most functions share the same scaffolding (`windowstart`, `hashtable`, `maxlenght`) plus unused variables left over from copying (`windowsum`, `lists`, `cureentlenght`).

- **`strinsubstring(array, k)`: longest substring with at most k distinct characters.** Add the right character's count to `hashtable`. While the map has more than `k` keys, decrement the left character and delete it when its count reaches 0. Track the largest window. The call `strinsubstring("araaci", 2)` returns `4` but isn't printed. O(n) time, O(k) space.
- **`fruitsplit(array, k)`: Fruits into Baskets.** Same algorithm, but `k` is overwritten with `2` inside the function. `['A','B','C','B','B','C']` gives `5`.
- **`strinsubstring(array)` (second definition, replaces the first): longest substring without repeating characters.** Shrinks the window while `max(hashtable.values()) >= 2`. `"abccde"` gives `3`. Because `max()` scans the whole map on every check, the cost is O(n·σ), where σ is the number of distinct characters.
- **`repeatablestring(array, k)`: longest substring of one letter after at most k replacements.** This one is buggy. Each character is counted twice (lines 96 and 98), and the result of `max(...)` on line 97 is thrown away, so the most-frequent-letter count stays `0`. The window therefore never grows past `k` characters: `("aabccbb", 2)` returns `2`, but the correct answer is `5`.
- **`binaires(array, k)`: longest subarray of 1s after replacing at most k zeros.** Count the 1s in the window. When the number of zeros (`window length − ones`) exceeds `k`, slide the start forward by one position. Since the window never shrinks, its final size is the answer. `[0,1,1,0,0,0,1,1,0,1,1]` with `k = 2` gives `6`. O(n) time, O(1) space.
- **`permutation(array, pattern)`: Permutation in a String.** Build character counts for `pattern`. When a character's count drops to 0, increment `matched`. Return `True` once every distinct pattern character is matched. After the window reaches `len(pattern)`, add the left character back before moving on. `("oidbcaf", "abc")` gives `True` (the window `"bca"`). The print label says `binaries` because it was copied from the previous function, and the final `return maxlenght` can never be reached. O(n + m) time, O(m) space.
- **`matchingletters(array, pattern)`: smallest window substring.** Decrement pattern counts and increment `matched` while a count stays at 0 or above. While `matched == len(pattern)`, record the smallest window and shrink from the left. Bug: after `windowstart += 1`, it updates `hashtable[array[windowstart]]` (the new left character) instead of `left_char`. The sample `("aabdec", "abc")` still returns `"abdec"`, but `("abdbca", "abc")` raises `KeyError: 'd'`. O(n + m) time.
- **`concatanating(array, pattern)`:** an exact copy of `matchingletters`. Its name suggests the Words Concatenation problem, which was never implemented. It is never called, and the print after it calls `matchingletters` a second time.
- **`anagram(array, words)`:** an unfinished Words Concatenation attempt: for each start index, check `word_count` word-length chunks against a word-frequency map. It would crash if called: `for word in word` raises an unbound local error, `range(...)+1` is a `TypeError`, and `word_seen = 0` replaces the dict. It is never called.

## Two pointers, hashing and binary search

### `twopointers.py`

**Status:** runs and prints the output below. The first two lines are wrong because of the index-sum bug described in the first bullet.

```
[2, 4]
[-1, -1]
[1, 3]
[0, 2]
Squares: [0, 1, 4, 4, 9]
Squares: [0, 1, 1, 4, 9]
4
2
```

- **`pair_with_targetsum(arra, target)`, first definition (two pointers):** start with pointers at both ends of a sorted array, move the right pointer left when the sum is too large and the left pointer right when it is too small. Bug: `sum = pointer1 + pointer2` adds the indices instead of `arra[pointer1] + arra[pointer2]`. For `([1, 2, 3, 4, 6], 6)` it returns `[2, 4]` (the right answer is `[1, 3]`), and for `([2, 5, 9, 11], 11)` it returns `[-1, -1]` (the right answer is `[0, 2]`). O(n) time, O(1) space.
- **Second definition (hash map):** for each element, check whether `target − arr[i]` has already been seen; otherwise store `arr[i] → i`. Returns `[1, 3]` and `[0, 2]`, both correct. O(n) time, O(n) space.
- **`make_squares(arr)`:** compare the squares at both ends of a sorted array (which may contain negatives), insert the larger one at the front of the result and move that pointer. The output is correct, but `list.insert(0, …)` is O(n) per call, so the function is O(n²).
- **`remove_duplicates(arr)`:** start the count at 1 and add 1 each time `arr[right-1] != arr[right]`. It returns the number of distinct values (`4` and `2` for the samples) without changing the array. `uniq` and `right += 1` do nothing, and an empty list returns `1`. O(n) time.
- **`pair_with_targetsum`, third definition:** sorts the list in place first, but has the same index-sum bug. It is never called.

### `2SUM.py`: pair sum and exponentiation

**Status:** **does not run.** The file ends with `def merge(A,p,q,r):` and no body, so Python raises an `IndentationError` while parsing, before any line runs. The functions are still worth reading:

- **`bruteforce(a, target)`:** checks every ordered pair `i != k`. Returns `"yes"` or, implicitly, `None`. O(n²).
- **`PowRec(x, n)`:** `x * PowRec(x, n-1)` with base cases `n == 0` and `n == 1`. O(n) time and O(n) recursion depth.
- **`Powiter(x, n)`:** multiplies `n` times. O(n) time, O(1) space. Bug: `n == 1` hits a bare `return` and gives `None`.
- **`PowDC(x, n)`:** divide and conquer. Compute `z = PowDC(x, n//2)`, then return `z*z` or `z*z*x` depending on whether `n` is even or odd. The comments write out the recurrence T(n) = T(n/2) + O(1), which solves to **O(log n)** (the header comment says O(N)). O(log n) stack.
- **`PowDCIterFast(x, n)`, first definition:** iterative binary exponentiation. While `m > 0`, multiply the result by `z` when the low bit is 1, square `z`, and halve `m`. O(log n) time, O(1) space.
- **`PowDCIterFast(x, n)`, second definition (replaces the first):** uses `m = n/2` (float division) and the built-in `pow`. It returns floats and gives wrong results for odd `n`: `PowDCIterFast(3, 5)` evaluates to `729.0` instead of `243`.
- **`merge(A, p, q, r)`:** an empty stub for merge sort.
- The sample calls `PowRec(2,6)` and the others don't print their results.

### `4sum.py`: pair sum with binary search

**Status:** runs and prints `NO`.

- **Problem:** despite the file name, this checks whether any **two** elements of a sorted array sum to `T`.
- **Approach:** `binarysearch(A, T)` is a standard iterative binary search. `sumT(A, T)` loops over each `i` and searches for `T − A[i]` in `A[i+1:]`, returning `"YES"` or `"NO"`.
- **Input/output:** `a = [1, 2, 3, 4, 7, 8, 9, 11]`, `T = 1` gives `NO` (the smallest pair sum is 3).
- **Complexity:** n binary searches take O(n log n) comparisons. But `A[i+1:]` copies up to n elements on every iteration, so the real cost is **O(n²) time and O(n) extra space**. Passing index bounds instead of slices would bring it to O(n log n).

## Divide and conquer, selection and partitioning

### `ALGORITHIM.ipynb`: quicksort-style partition by parity

**Status:** runs (it was last run on Python 3.9.13). It uses NumPy and `random`.

- **Problem:** rearrange `A[p..r]` so that even numbers come first. The notebook uses the quicksort `PARTITION` procedure with the comparison `A[j] <= x` replaced by `A[j] % 2 == 0`.
- **Approach (`partition(A, p, r)`):**
  1. Take the pivot `x = A[r]` (the last element) and set `i = p - 1`.
  2. For `j` from `p` to `r-1`, when `A[j]` is even, increment `i` and swap `A[i]` with `A[j]`.
  3. After the loop, swap the pivot into position `i+1`.
  4. Return the modified array. It is modified in place and, unlike CLRS, the function returns the array rather than the pivot index.

  The result is the even numbers from `A[p..r-1]`, then the original last element, then the odd numbers.
- **Cells:** cell 1 has a first version where the final pivot swap is indented inside the `for` loop, so it runs on every iteration and corrupts the data: `[3, 8, 5, 2, 7, 6, 4]` becomes `[8, 2, 6, 4, 7, 4, 4]`. Cell 2 moves the swap outside the loop and produces `[8, 2, 6, 4, 7, 5, 3]`. The later cells run cell 2's version on `np.random.randint(1, 1000, 1000)` and on `random.sample(range(100), 100)`. The saved output shows the evens, then the pivot `71`, then the odds. Cells 4, 5 and 11 are empty. The `if 1:` wrapper has no effect.
- **Complexity:** O(n) time, O(1) extra space. The partition is not stable.

### `examenalgo.py`: exam practice on selection and maximum product

**Status:** runs (exit code 0), but prints about 10,000 lines. Several functions are buggy or unfinished, as noted below.

The module runs in this order:
1. Builds `A = [1..100]` and `ran`, a random permutation of 0–999.
2. `MaxProductSubAaybruteforce(A)` prints every `(r, s)` index pair (10,000 lines), then the best pair.
3. `print(percent25(ran))` runs the randomized select, which prints the array at every recursion level, then prints `None` because this first `percent25` has no `return`.
4. For `A = [1, -10, 4, 3, 2, 4, -2, 5]`, it prints `MaxProduct(A)` → `(5, 7)`, then `maxSubAayProduct(A)` → `(5, 7)`, and calls `maxSubarrayProduct(A, len(A))` without printing it.
5. For `arr = [2, -3, 4, -1, -2, 1, 5, -3]`, it prints `Indices: 6 7`.
6. `print(percent25(A))`, now the median-of-medians version, prints `1`.

Functions:

- **`Select25(A, p, r, i)`, `randompartition`, `partition`: randomized select (quickselect).** Swap a random element into `A[r]`, run a Lomuto partition, and compute the pivot's rank `k = q − p + 1`. Return the pivot if `i == k`; otherwise recurse left with `i` or right with `i − k`. It gave the correct i-th smallest element in 500 of 500 random tests. **Expected O(n), worst case O(n²)** time. The first `percent25` passes `i = n * 0.25` as a float, which only matches an integer rank when `n` is a multiple of 4.
- **`MaxProductSubAaybruteforce(A)`:** despite its name, finds the two distinct indices with the largest product `A[r] * A[s]`, not a subarray. O(n²). It raises `UnboundLocalError` if no positive product exists.
- **`MaxProductSubAay(A)`:** unfinished DP with `Maxproduct[]` and `minproduct[]` arrays. It refers to an undefined `max_product` and returns nothing. Never called.
- **`MaxProduct(A)` and `maxSubAayProduct(A)`:** Kadane-style scan that swaps `currentmax` and `currentmin` when `A[i] < 0` and tries to track the start and end indices. O(n) time, O(1) space. The index tracking is wrong. On the sample, both return `(5, 7)` (product −40), but the whole array `(0, 7)` has product 9600. In random tests, about half of the returned ranges were not the maximum product.
- **`dynamicpro(A)`:** broken (`Maxi` is used before assignment, and `n` is undefined). Never called.
- **`maxSubarrayProduct(arr, n)`:** the standard max/min-product-ending-here recurrence, returning the maximum product value. It was correct on 1,000 random arrays. O(n) time, O(1) space.
- **`maxSubarrayProduct(arr)`:** a later definition with the same name that returns `(start, end)` and replaces the previous one. It is never called.
- **`SELECT(A, p, r, i)`, `PARTITION(A, p, r, x)`, `percent25(A)`: median of medians.** The comments ("Paso 1" to "Paso 5") follow CLRS:
  1. Split `A[p..r]` into groups of 5.
  2. Sort each group and take its median.
  3. Recursively `SELECT` the median of those medians, `x`.
  4. `PARTITION` finds `x` with `A.index(x)`, swaps it to `A[r]` and runs a Lomuto partition.
  5. Compare `i` with the pivot's rank `k` and recurse on one side.

  The intended bound is worst-case O(n), from T(n) ≤ T(n/5) + T(7n/10) + O(n). **Bug:** groups are sliced as `A[j:j + 5]` for `j in range(p, r + 1, 5)` without stopping at `r`, so the last group can include elements outside the current subarray, and the pivot can come from outside `[p, r]`. `A.index(x)` also searches the whole list and would pick the wrong copy when there are duplicates. In random tests, about 40% of results were wrong, and on the sample above it returns `1` where the 2nd smallest element is `-2`.

### `product.py`: median-of-medians selection

**Status:** runs. It is a near-duplicate of `examenalgo.py`, and the file name doesn't describe its contents.

- Contains exactly the `SELECT`, `PARTITION` and `percent25` functions from `examenalgo.py` (see above), so it has the same grouping bug.
- It builds `A = [1..100]` and a sample of 0–999 that is then sorted, prints both lists, and prints `percent25(ran)`. With `i = int(1000 * 0.25) = 250`, it prints `250`, while the 250th smallest value (ranks start at 1) is `249`.

### `mediansort.py`: median of two sorted arrays

**Status:** runs if NumPy is installed. The two-element base case is wrong, so results are often incorrect, and the main block uses random input, so the output changes between runs.

- **Problem:** find the median of the union of two sorted arrays `A` and `B` of the same length `n`.
- **Approach (`MedianOfTwo(A, B, n)`):**
  1. If `n == 1`, return `(A[0] + B[0]) / 2`.
  2. If `n == 2`, reduce to one element per array with `TwoArraysOfOneElement` and recurse.
  3. Otherwise compute each array's median (the average of the two middle elements when `n` is even).
  4. If the medians are equal, return that value.
  5. If `medianOfA > medianOfB`, the combined median lies in the lower part of `A` and the upper part of `B`. Keep `A[0 : mid+1]`, and `B[mid-1:]` (even `n`) or `B[mid:]` (odd `n`), so both halves stay the same length, and recurse. When `medianOfA < medianOfB`, do the mirror image.

  Helper functions `isItEven`, `minimum` and `maximum` support this, and `print` calls trace every step.
- **Input/output:** the sample `A = [1..6]`, `B = [7..12]` is replaced by `numpy.random.randint(1, 9, 6)` arrays, which are sorted and passed in. It prints the trace and the median.
- **Complexity:** each step roughly halves `n` (6 → 4 → 3 → 2 → 1), giving O(log n) recursion levels. With Python lists every slice copies, which adds up to O(n) total. NumPy slices are views, so the NumPy input stays O(log n).
- **Bug:** for `A = [i, j]` and `B = [k, l]`, the median of the four values is `(max(i, k) + min(j, l)) / 2`, but `TwoArraysOfOneElement` returns `[minimum(i, j)], [maximum(k, j)]` in one branch and `[maximum(i, j)], [minimum(k, l)]` in the other. In 1,000 random tests with lists, about 40% of results were wrong. Replacing only this base case made all 2,000 follow-up tests correct.

## Dynamic programming

### `brute.py`: maximum product subarray

**Status:** runs. The O(n) version reports wrong indices.

```
Maximum Sub Aay product is 4, starting at index 1 and ending at index 1
(0, 1)
```

- **`maxSubArrayProduct(A, n)`: brute force.** For each start `i`, extend `j` to the right while keeping a running product, and record the best product with its `(start, end)`. It was correct on 500 random arrays. O(n²) time, O(1) space.
- **`max_product_subarray(A)`: Kadane-style DP.** Track the maximum and minimum product ending at `i`, because a negative number turns the minimum into the maximum. On a zero, reset both to 1 and set `current_start = i + 1`. Returns only `(max_start, max_end)`. O(n) time, O(1) space.
  - The start index moves only at zeros, so a best subarray that begins after a sign change is reported with the wrong start. On the sample it returns `(0, 1)` (product −10), while the brute force finds `4` at `(1, 1)`.
  - A zero is never considered as the answer: `[-1, 0, -1]` returns `(0, 0)` (product −1) instead of the zero.
- The first sample array `[1, -2, -3, 0, 7, -8, 2]` is overwritten by `[-2.5, 4, 0, 3, 0.5, -8, 1]` before it is used.

## Graphs and matrices

### `island.py`: number of islands

**Status:** the DFS version runs and prints `islands 1`. The BFS version then crashes with `TypeError: deque.popleft() takes no arguments`.

- **Problem:** count groups of `1` cells connected up, down, left or right in a binary grid.
- **DFS (`dfsisland` + `visitislandDFS`):** scan every cell. When a cell is `1`, add one to the count and flood-fill from it: return on out-of-bounds or water, set the cell to `0` (which marks it visited and changes the input grid), then recurse in four directions. The sample 5×5 grid has one island.
- **BFS (`dfsisland` redefined + `visitislandBFS`):** meant to replace the recursion with a `collections.deque`. `neighbors.popleft(0)` raises `TypeError`, and the four `neighbors.extend(...)` lines are indented outside the `while` loop, so neighbors would not be queued even after fixing that call.
- **Complexity:** O(R·C) time, since each cell is visited a constant number of times. The DFS recursion can go R·C levels deep, which can exceed Python's default recursion limit (about 1000) on large islands. A working BFS would use O(R·C) queue space in the worst case instead of recursion.

### `diagonaldiffrence.py`: diagonal difference

**Status:** runs (HackerRank template).

- **Input (stdin):** `n`, then `n` rows of space-separated integers. **Output:** the result is written to the file named by the `OUTPUT_PATH` environment variable. The two diagonal sums are also printed to stdout as debug output.
- **Approach:** add up `arr[i][i]` for the main diagonal and `arr[n-1-i][i]` for the other diagonal, then return `abs(difference)`.
- **Complexity:** O(n) time, O(1) space.
- **Example:** rows `11 2 4 / 4 5 6 / 10 8 -12` give sums 4 and 19, so the result is `15`.

### `flipinfmatrix.py`: Flipping the Matrix

**Status:** **crashes** with `TypeError: 'float' object cannot be interpreted as an integer`.

- **Problem:** in a 2n×2n matrix, you may reverse any row or column any number of times. Maximize the sum of the upper-left n×n quadrant.
- **Approach:** reversals can move any of the four mirror cells `(i, j)`, `(i, 2n-1-j)`, `(2n-1-i, j)` and `(2n-1-i, 2n-1-j)` into position `(i, j)`, independently of the other positions. So the answer is the sum over the quadrant of the largest of those four values.
- **Input (stdin):** `q` queries. Each query is `n` followed by `2n` rows. The result for each query is written to `OUTPUT_PATH`.
- **Bug:** `range(size/2)` uses float division in Python 3. With integer division, the same logic returns the expected `414` on the HackerRank sample.
- **Complexity:** O(n²) time for a 2n×2n matrix, O(1) space.

## Sorting, counting and string exercises

### `frecquency.py`: counting sort, part 1

**Status:** runs (HackerRank template).

- **Approach:** create a list of 100 zeros and add 1 to `frequency[item]` for each input value. Values must be in the range 0–99: larger values raise `IndexError`, and negative values silently index from the end.
- **Input (stdin):** `n`, then the list. **Output:** 100 space-separated counts written to `OUTPUT_PATH`. For example, `1 1 3 2 1` gives `0 3 1 1 0 0 …`.
- **Complexity:** O(n + 100) time, O(100) space.

### `median.py`: find the median

**Status:** **crashes on every input.**

- **Intended approach:** sort the list and return the middle element, O(n log n).
- **Bugs:** the first line `arr=[]` throws away the input, and `arr[lenght/2]` uses a float index, which raises `TypeError`.

### `ZIGZAG.PY`: Zig Zag Sequence

**Status:** runs and gives correct output for the problem's odd-length inputs.

- **Problem:** rearrange `n` distinct integers into the lexicographically smallest sequence that increases up to the middle and then decreases. This is a HackerRank debugging challenge.
- **Approach (`findZigZagSequence(a, n)`):**
  1. Sort the list.
  2. Take `mid = int(n/2)` and swap `a[mid]` with `a[n-1]`, which puts the maximum in the middle.
  3. Reverse `a[mid+1 .. n-2]` with two pointers (`st`, `ed`).
  4. Print the sequence separated by spaces.
- **Input (stdin):** the number of test cases, then `n` and the array for each test.
- **Example:** `1 / 7 / 1 2 3 4 5 6 7` gives `1 2 3 7 6 5 4`.
- **Complexity:** O(n log n) time for the sort, O(1) extra space.

### `timeconversion.py`: 12-hour to 24-hour time

**Status:** **unfinished; crashes** with `IndexError: pop index out of range`.

- **Intended approach:** split the string (for example `07:05:45PM`) into a list of characters, pop off the `AM`/`PM` suffix, pop the hour digits, add 12 (mod 24) for PM, and join the rest back together.
- **Bugs:**
  - After the first `pop`, the list is one element shorter, so `slist.pop(max-1)` is out of range for every valid input.
  - The hour is taken from indices 1 and 2 after an earlier removal has shifted the list, so it would not be the two hour digits.
  - `12:xx AM` is not handled.
  - The function prints instead of returning, so `result + '\n'` would fail on `None`.

### `strnvalid.py`: string validators

**Status:** runs, but always prints `True`.

- **Problem:** print whether the input has any alphanumeric, alphabetic, digit, lowercase or uppercase characters, one line per check.
- **Approach:** five linear scans that `break` after the first matching character.
- **Bug:** the methods are referenced without being called (`s[i].isalnum` instead of `s[i].isalnum()`). A method object is always truthy, so each loop prints `True` at the first character and stops. Any non-empty input, even `###`, prints `True` five times. An empty string prints nothing, and `False` is never printed.

### `tuple.py`: tuples

**Status:** runs.

- **Input (stdin):** `n` (read but not used), then space-separated integers.
- **Approach:** convert the integers to a list, then to a tuple, and print `hash(tuple)`. O(n).
- **Output:** besides the hash, it prints the list, the tuple and the list again as debug output, so it prints four lines where HackerRank expects one. For input `2 / 1 2`, the last line is `-3550055125485641917` on 64-bit CPython 3.8+. Tuple hashing changed in 3.8, so older versions give a different value.

## Randomized, stack and miscellaneous

### `nuts.py`: "shake the bag" matching

**Status:** runs, but often crashes with `IndexError` (15 of 20 test runs).

- **Problem:** pair up identical items (`"a"` with `"a"` and so on) by repeatedly shaking the bag and picking out neighbors that match.
- **Approach:**
  1. `shakebag(M)`: while items remain, shuffle the list with `randomize` and remove adjacent equal pairs with `removematches`.
  2. `removematches`: scan neighbors. When `m[i] == m[i+1]`, add both to `matched`, `pop` both and step back one position.
  3. `randomize`: a Fisher–Yates shuffle from the last index down.

  It returns the items in matched pairs, for example `['b', 'b', 'a', 'a', ...]`.
- **Bug:** `randint(0, i+1)` includes `i+1`, so on the first swap `j` can equal `n`, which is out of range. A correct Fisher–Yates shuffle uses `randint(0, i)`.
- **Termination:** if any item appears an odd number of times, the leftover item can never be matched and the loop never ends.
- **Complexity:** this is a Las Vegas algorithm: when it finishes, the result is always correct, but the running time is random. Each round costs O(n) for the shuffle plus O(n²) in the worst case for `removematches`, because `list.pop(i)` is O(n). The number of rounds is random.

### `window.py`: Baseball Game (stack) and a stub

**Status:** **does not compile** (`IndentationError` at line 9).

- **`minsum(t, A)`:** an unfinished sliding-window stub. The `for r in range(len(t)):` loop has no body.
- **`Solution.calPoints(operations)`:** LeetCode's Baseball Game. An integer pushes a score, `"+"` pushes the sum of the previous two, `"D"` doubles the previous score, `"C"` removes it, and the function returns the sum of the stack. O(n) time and space. Problems:
  - `List` is not imported from `typing`.
  - `op.isdigit()` is `False` for negative scores such as `"-2"`, so they are skipped.
  - `"+"` and `"D"` use `previous` (the last integer read) instead of the top of the stack, and `"C"` doesn't update `previous`.

  Run on its own with `List` imported, `["5","2","C","D","+"]` returns `16`; the correct score is `30`.

### `decode.py`

**Status:** trivial. Crashes with `UnicodeDecodeError`.

It assigns three byte strings, of which only the last one is used, and tries `bytes.decode("utf-16")` on it. The first byte string starts with `16 03 03`, the same bytes that begin a TLS handshake record, so the script looks like a test of whether captured bytes contain text. The last one is 9 bytes long with an unpaired surrogate, so it is not valid UTF-16.

### `binarymedian.py`

**Status:** stub.

It contains only commented-out pseudocode for a recursive binary search and a commented-out `def binarymedian(a, b):` header. The code that runs prints two sample lists, but prints `a` under both labels. The divide-and-conquer version of this problem is in `mediansort.py`.

### `mug.py`

**Status:** **unfinished; crashes** with `TypeError`.

It reads all lines from stdin and keeps a list of five mug colors (`"Yellow."` has a stray period). The plan appears to be removing each color listed in the input from the list. `count = data[0]` is still a string, so `range(count)` fails, and the last line prints `data[1]` instead of a computed answer.

### `group.py`

**Status:** out of scope for this project. **Do not run it on networks you don't own or aren't authorized to scan.**

**Not the author's own work.** This isn't an algorithm exercise: it is the example script from the [python-nmap](https://pypi.org/project/python-nmap/) project, written by Alexandre Norman and licensed under GPL-3.0, with its original author and license header kept. It is included only as a reference. It shows the `nmap.PortScanner` API:
- a TCP scan of `127.0.0.1` on ports 22–443 that prints the host, protocol and port states and a CSV export
- a ping sweep of `192.168.0.0/24`
- an asynchronous scan of `192.168.0.0/30` with `PortScannerAsync` and a callback
- OS detection and MAC vendor lookup (only when run as root)
- parsing of `./nmap_output.xml`, which crashes if the file is missing
- a progressive `PortScannerYield` scan and a scan with `timeout=1`

It needs the `nmap` binary and the `python-nmap` package.

---

## Requirements

- Python 3.8 or newer (the notebook was last run on 3.9.13). Most scripts use only the standard library.
- `numpy` for `mediansort.py` and `ALGORITHIM.ipynb`
- `jupyter` (or VS Code / JupyterLab) to open `ALGORITHIM.ipynb`
- `python-nmap` and the `nmap` command-line tool, only for `group.py`

```bash
pip install numpy jupyter
```

## Usage

Scripts with hard-coded samples run directly:

```bash
python3 arrayaveerage.py      # [2.2, 2.8, 2.4, 3.6, 2.8]
python3 maximunsumarrray.py   # 9
python3 slidingstring.py
python3 twopointers.py
python3 brute.py
python3 island.py             # prints "islands 1", then the BFS version raises TypeError
python3 mediansort.py         # needs numpy; random input each run
python3 product.py
```

`ZIGZAG.PY` and `tuple.py` read stdin and print to stdout:

```bash
printf "1\n7\n1 2 3 4 5 6 7\n" | python3 ZIGZAG.PY   # 1 2 3 7 6 5 4
printf "2\n1 2\n" | python3 tuple.py
```

The HackerRank templates (`diagonaldiffrence.py`, `frecquency.py`, `flipinfmatrix.py`, `median.py`, `timeconversion.py`) write their answer to the file named by `OUTPUT_PATH`:

```bash
printf "3\n11 2 4\n4 5 6\n10 8 -12\n" | OUTPUT_PATH=/dev/stdout python3 diagonaldiffrence.py   # 15 (plus debug sums 4 and 19)
printf "5\n1 1 3 2 1\n" | OUTPUT_PATH=/dev/stdout python3 frecquency.py                        # 0 3 1 1 0 0 ...
```

Open the partition notebook with:

```bash
jupyter notebook ALGORITHIM.ipynb
```

## Author

Jose E. Rodriguez Rios
