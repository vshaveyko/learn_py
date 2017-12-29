arr = [67, 12, 3, 4, 172]

def merge(left, right):
    aux = left + right

    left_index  = 0
    right_index = 0

    aux_index   = -1

    while aux_index < len(aux) - 1:
        aux_index += 1

        try:
            right_elem = right[right_index]
        except IndexError:
            aux[aux_index] = left[left_index]
            left_index     += 1

            continue

        try:
            left_elem = left[left_index]
        except IndexError:
            aux[aux_index] = right[right_index]
            right_index    += 1

            continue

        if left_elem > right_elem:
            aux[aux_index] = right_elem
            right_index    += 1
        else:
            aux[aux_index] = left_elem
            left_index     += 1

    return aux

def mergeSort(array):
    if len(array) > 1:
        half = len(array) / 2

        return merge(mergeSort(array[:half]), mergeSort(array[half:]))
    else:
        return array

print(mergeSort(arr))
