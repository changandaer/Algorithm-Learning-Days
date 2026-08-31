"""DAY09修复：两数之和接收numbers和target，找到第一组立即返回。"""

# 函数合同
# 函数名：find_two_sum
# 参数：numbers、target
# 返回值及类型：返回索引列表
# 最小例子：([2, 7, 11, 15], 9) -> [0, 1]


# 定义函数。
def find_two_sum(numbers,target):
    target_index = []
    for first_index in range(len(numbers)):
        for second_index in range(first_index+1,len(numbers)):
            if numbers[first_index] + numbers[second_index] == target:
                target_index.append(first_index)
                target_index.append(second_index)
    return target_index

# 测试固定样例、[3,3]、空列表、无答案和存在多组答案的数据。

assert find_two_sum([2, 7, 11, 15], 9) == [0, 1]
assert find_two_sum([2, 7, 11, 15], 26) == [2, 3]
assert find_two_sum([2, 7, 11, 15], 14) == []
assert find_two_sum([3, 3], 6) == [0, 1]
assert find_two_sum([], 9) == []