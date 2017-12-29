def merge_dicts(left, right, mergef):
    for k, v in left.items():
        if k in right:
            if isinstance(v, dict):
                right[k] = merge(right[k], v, mergef)
            else:
                right[k] = mergef(right[k], v)
        else:
            right[k] = left[k]

    return right

# testing
#  dict1 = { 'a': [1,2],  'b': [3, 4] }
#  dict2 = { 'a': [0, 3], 'c': [1, 5] }
#
#  def merge_results(left, right):
#      return [left[0] + right[0], left[1] + right[1]]
#
#  print(merge_dicts(dict1, dict2, merge_results))
