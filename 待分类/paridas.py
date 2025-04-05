def find_zero_pairs(arr):
    seen = set()
    result = set()

    for num in arr:
        if -num in seen:
            pair = tuple(sorted((num,-num)))
            result.add(pair)
        seen.add(num)
    return sorted(list(result))


arr = [1, 2, -2, 4, -4, 3, -3]
print(find_zero_pairs(arr))