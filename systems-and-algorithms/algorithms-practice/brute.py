def maxSubArrayProduct(A, n):
    maxproduct = A[0]
    start, end = 0, 0

    for i in range(n):
        product = 1
        for j in range(i, n):
            product *= A[j]
            if product > maxproduct:
                maxproduct = product
                start, end = i, j

    return maxproduct, start, end

A = [1, -2, -3, 0, 7, -8, 2]
A = [-2.5, 4, 0, 3, 0.5, -8, 1]

n = len(A)
maxproduct, start_index, end_index = maxSubArrayProduct(A, n)
print(f"Maximum Sub Aay product is {maxproduct}, starting at index {start_index} and ending at index {end_index}")



def max_product_subarray(A):
    n = len(A)
    max_so_far = max_ending_here = min_ending_here = A[0]
    max_start = max_end = current_start = 0
    for i in range(1, n):
        if A[i] == 0:
            current_start = i + 1
            max_ending_here = min_ending_here = 1
        else:
            tmp_max = max_ending_here
            max_ending_here = max(A[i], max_ending_here * A[i], min_ending_here * A[i])
            min_ending_here = min(A[i], tmp_max * A[i], min_ending_here * A[i])
            if max_ending_here > max_so_far:
                max_so_far = max_ending_here
                max_start = current_start
                max_end = i
    return (max_start, max_end)


n = len(A)
print(max_product_subarray(A))


