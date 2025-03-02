### 排序算法 - 冒泡排序
def bubble_sort(arr):
    arr_len = len(arr)
    swapped = False
    for i in range(arr_len - 1):
        for j in range(arr_len - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
               break   
    return arr


if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("排序前",arr)
    print("排序后", bubble_sort(arr))
    

        