"""DAY10修复：存在多组答案时只返回遍历遇到的第一组。"""


def find_two_sum(numbers, target):
    target_indices = []
    for first_index in range(len(numbers)):
        for second_index in range(first_index + 1, len(numbers)):
            if numbers[first_index] + numbers[second_index] == target:
                target_indices.append(first_index)
                target_indices.append(second_index)
    return target_indices


# 先运行，第一条应失败。不得修改预期结果。
assert find_two_sum([1, 4, 2, 3], 5) == [0, 1]
assert find_two_sum([3, 3], 6) == [0, 1]
assert find_two_sum([2, 7], 100) == []
assert find_two_sum([], 9) == []

# 为什么不再需要append：

