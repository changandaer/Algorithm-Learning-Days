"""DAY11跟做：使用两层循环完成两数之和。"""

# 第一步：最小输入与预期输出：[2,7,11,15]/9 -> [0, 1]
# 第二步：代码阶段：
# 第三步：需要保存的状态与小测试：


# 函数合同：two_sum_brute_force(nums, target) -> list


# 测试：[2,7,11,15]/9，[3,2,4]/6，[3,3]/6。

def two_sum_brute_force(nums, target):

    for first_index in range(len(nums)):
        for second_index in range(first_index+1,len(nums)):
            if nums[first_index] + nums[second_index] == target:
                return [first_index,second_index]
    
    return []


assert two_sum_brute_force([2,11,15,7],9) == [0,3]
assert two_sum_brute_force([3,2,4],6) == [1, 2]
assert two_sum_brute_force([3,3],6) == [0,1]
