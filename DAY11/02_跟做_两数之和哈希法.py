"""DAY11跟做：使用seen字典完成两数之和并观察每轮变化。"""

# 第一步：最小输入与预期输出：
# 第二步：代码阶段：
# 第三步：需要保存的状态与小测试：


# 函数合同：two_sum_hash(nums, target) -> list
def two_sum_hash(nums, target):

    seen = {}
    for index in range(len(nums)):
        needed = target - nums[index]
        if needed in seen:
        # if needed in seen难道不也是一种特殊的for循环检索吗，检索seen这个字典中是否存在needed这个key，为什么这个时间复杂度就低呢？
            return [seen[needed],index]
        
        seen[nums[index]] = index
    
    return []

# 第一次运行保留每轮print，理解seen后删除调试输出。

assert two_sum_hash([2,11,15,7],9) == [0,3]
assert two_sum_hash([3,2,4],6) == [1, 2]
assert two_sum_hash([3,3],6) == [0,1]
assert two_sum_hash([3],6) == []