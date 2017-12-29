arr = [67, 12, 3, 4, 172]

def swap(array, right, left):
    a            = array[right]
    array[right] = array[left]
    array[left]  = a

def partition(array, lo, hi):
    pivot = array[lo + 1]
    i     = lo
    j     = hi

    while i < j:
        while array[i] < pivot:
            i += 1
        while array[j] > pivot:
            j -= 1

        swap(array, right=i, left=j)

    return j

def quickSort(array, lo, hi):
    if lo < hi:
        p = partition(array, lo, hi)
        quickSort(array, lo, p - 1)
        quickSort(array, p, hi)

    return array

print(quickSort(arr, 0, len(arr) - 1))
