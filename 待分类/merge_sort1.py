def merge_sort(nums:list[int],left:int,right:int):

    if left >= right:
        return 

    mid = (left + right) // 2  
    merge_sort(nums, left, mid)
    merge_sort(nums, mid+1, right)
    merge(nums, left, right, mid)
    
def merge(nums:list[int], left:int,right:int, mid :int):
    tmp = [0] * (right - left + 1)

    i, j, k = left, mid + 1, 0

    while i <= mid and j <= right:
        if nums[i] <= nums[j]:
            tmp[k] = nums[i]
            i += 1
        else:
            tmp[k] = nums[j]
            j += 1
        k += 1

    while i <= mid:
        tmp[k] = nums[i]
        i += 1
        k += 1
    
    while j <= right:
        tmp[k] = nums[j]
        j += 1
        k += 1

    for k in range(0, len(tmp)):
        nums[left + k] = tmp[k]

def test_merge_sort():
    # 测试用例 1：空数组
    nums = []
    merge_sort(nums, 0, len(nums) - 1)
    assert nums == [], "测试用例 1 失败"

    # 测试用例 2：单个元素
    nums = [5]
    merge_sort(nums, 0, len(nums) - 1)
    assert nums == [5], "测试用例 2 失败"

    # 测试用例 3：完全无序的数组
    nums = [3, 1, 4, 2]
    merge_sort(nums, 0, len(nums) - 1)
    assert nums == [1, 2, 3, 4], "测试用例 3 失败"

    # 测试用例 4：部分有序的数组
    nums = [1, 3, 2, 4, 6, 5]
    merge_sort(nums, 0, len(nums) - 1)
    assert nums == [1, 2, 3, 4, 5, 6], "测试用例 4 失败"

    # 测试用例 5：包含重复元素的数组
    nums = [3, 1, 2, 3, 1]
    merge_sort(nums, 0, len(nums) - 1)
    assert nums == [1, 1, 2, 3, 3], "测试用例 5 失败"

    # 测试用例 6：大数组
    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    merge_sort(nums, 0, len(nums) - 1)
    assert nums == [1, 2, 3, 4, 5, 6, 7, 8, 9], "测试用例 6 失败"

    print("所有测试用例通过！")

# 运行测试
test_merge_sort()
