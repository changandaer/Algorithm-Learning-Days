"""DAY12独立：使用字典判断列表中是否有重复数字。"""


# 固定三步法：
# 第一步：最小输入与输出：[1, 2, 1] -> True；[1, 2, 3] -> False
# 第二步：建空字典；逐个检查数字是否见过；没见过就记录
# 第三步：seen只表示“以前见过的数字”；用五组边界测试


def contains_duplicate_hash(nums):
    # TODO：关闭课程中的相关答案后，独立完成哈希法。
    seen = {}
    for index in range(len(nums)):
        if nums[index] in seen:
            return True
        seen[nums[index]] = index
    return False 
    pass


# 完成函数后取消注释并运行：
assert contains_duplicate_hash([1, 2, 3, 1]) is True
assert contains_duplicate_hash([1, 2, 3, 4]) is False
assert contains_duplicate_hash([1, 1]) is True
assert contains_duplicate_hash([1]) is False
assert contains_duplicate_hash([]) is False

