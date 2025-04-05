def two_sum(arr):
    arr.sort()
    left = 0
    right = len(arr) - 1
    result = []
    while left < right:
        sum = arr[left] + arr[right]
        if sum == 0:
            result.append((arr[left], arr[right]))
            while left < right and arr[left] == arr[left + 1]:
                left += 1
            while left < right and arr[right] == arr[right - 1]:
                right -= 1
            left += 1
            right -= 1
        elif sum < 0:
            left += 1
        else:
            right -= 1
    return result

# 示例数组
arr = [1, -5, 6, 5, 0, 2, -1, 9, 6, 7]
pairs = two_sum(arr)

print("所有满足a + b = 0的二元组为：")
for pair in pairs:
    print(pair)