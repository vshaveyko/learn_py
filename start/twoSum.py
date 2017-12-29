arr = [67, 12, 3, 4, 172]

def twoSum(array, sum):
    h = {}

    for index, val in enumerate(array):
        if h.has_key(sum - val):
            return True

        h[val] = True

    return False

print(twoSum(arr, 7))
print(twoSum(arr, 8))
