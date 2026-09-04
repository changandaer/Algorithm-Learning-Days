"""DAY11跟做：使用两层循环完成两数之和。"""

# 第一步：最小输入与预期输出：[2,7,11,15]/9 -> [0, 1]
# 第二步：代码阶段：
# 第三步：需要保存的状态与小测试：


# 函数合同：two_sum_brute_force(nums, target) -> list


# 测试：[2,7,11,15]/9，[3,2,4]/6，[3,3]/6。

def two_sum_brute_force(nums, target):

    seen = {}
    for index in range(len(nums)):
        needed = target - nums[index]
        if needed in seen:
            # if needed in seen难道不也是一种特殊的for循环检索吗，检索seen这个字典中是否存在needed这个key，为什么这个时间复杂度就低呢？
            return [seen[needed],index]
        seen[nums[index]] = index
    return []

assert two_sum_brute_force([2,11,15,7],9) == [0,3]
assert two_sum_brute_force([3,2,4],6) == [1, 2]
assert two_sum_brute_force([3,3],6) == [0,1]
