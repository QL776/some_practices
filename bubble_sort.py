def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):  # 外层循环控制排序的轮数，总共需要 n-1 轮
        # 设置一个标志位，用于优化算法，如果某一轮没有发生交换，则说明数组已经有序
        swapped = False
        for j in range(n - 1 - i):  # 内层循环控制每轮的比较次数，每轮比较 n-i-1 次
            # 比较相邻元素，如果左边大于右边，则交换它们
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # 如果某一轮没有发生交换，则提前结束排序
        if not swapped:
            break
    return arr

if __name__ == '__main__':
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("排序前：", arr)
    sorted_arr = bubble_sort(arr)
    print("排序后：", sorted_arr)
    print("排序后：", sorted_arr)