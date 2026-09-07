"""DAY12独立：使用两层循环判断列表中是否有重复数字。"""


# 固定三步法：
# 第一步：最小输入与输出：[1, 2, 1] -> True；[1, 2, 3] -> False
# 第二步：选择第一个位置；选择后面的第二个位置；比较两个数字
# 第三步：只需保存两个索引；用重复、不重复、空列表测试


def contains_duplicate_brute_force(nums):
    # TODO：独立完成暴力法。
    
    for first_index in range(len(nums)):
        for second_index in range(first_index+1, len(nums)):
            
            if nums[first_index] == nums[second_index]:
                return True
    return False
    pass 


# 完成函数后取消注释并运行：
assert contains_duplicate_brute_force([1, 2, 3, 1]) is True
assert contains_duplicate_brute_force([1, 2, 3, 4]) is False
assert contains_duplicate_brute_force([1, 1]) is True
assert contains_duplicate_brute_force([1]) is False
assert contains_duplicate_brute_force([]) is False

