"""DAY08 独立练习：把 O(n²) 两数之和封装成函数。

找到返回两个索引组成的列表，找不到返回空列表。
"""

# 函数合同
# 函数名：find_two_sum
# 输入：目标数字
# 输出：索引列表
# 最小例子：numbers = [2, 7, 11, 15] target = 26 -> [2,3]

# 从这里定义函数。找到后直接 return 两个索引。

def find_two_sum(target):
    numbers = [2, 7, 11, 15]
    target_index = []
    for first_number_index in range(len(numbers)):
        for second_number_index in  range(first_number_index+1,len(numbers)):
            if numbers[first_number_index] + numbers[second_number_index] == target:
                target_index.append(first_number_index)
                target_index.append(second_number_index)
    return target_index
                

# 覆盖目标9、26、14、相同数不同索引和空列表。
target_index = find_two_sum(26)
print(target_index)

assert find_two_sum(6) == []
assert find_two_sum(9) == [0,1]
assert find_two_sum(14) == []