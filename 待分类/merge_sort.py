def merge(nums:list[int], left: int, mid : int, right:int):
    '''合并左子数组和右子数组'''
    # 左子数组区间为[left,mid],右子数组区间为[mid+1, right]
    # 创建一个临时数组tmp, 用于存放合并后的结果
    tmp = [0] * (right - left + 1)

    #初始化左子数组和右子数组的起始索引
    i, j, k = left,mid + 1, 0

    # 当左右子数组都还有元素时，进行比较并将较小的元素复制到临时数组中
    while i <= mid and j <= right:
        if nums[i] <= nums[j]:
            tmp[k] = nums[i]
            i += 1
        else:
            tmp[k] = num[j]
            j += 1
        k += 1

    # 将左子数组和右子数组的剩余元素复制到临时数组中
    while i <= mid:
        tmp[k] = nums[i]
        i += 1
        k += 1
    while j <= right:
        tmp[k] = nums[j]
        j += 1
        k += 1
    #将临时数组tmp中的元素复制回原数组nums的对应区间
    for k in range(0, len(tmp)):
        nums[left + k] = tmp[k]

def merge_sort(nums: list[int], left: int, right: int):
    '''归并排序'''
    #终止条件
    if left >= right:
        return
    
    mid = (left + right) // 2
    merge_sort(nums, left, mid)
    merge_sort(nums, mid + 1, right)
    merge(nums, left, mid, right)
    
