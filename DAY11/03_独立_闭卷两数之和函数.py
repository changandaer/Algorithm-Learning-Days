"""DAY11闭卷：关闭课程，从空白手写普通函数版哈希解法。"""

# 固定三步法：
# 第一步：小数据测试输入输出 [2, 7, 11, 15], 9  -> [0, 1]
# 第二步：工作阶段：建立空字典，遍历输入，在字典查找是否有需要的数字
# 第三步：


# 在这里定义two_sum_hash(nums, target)。
def two_sum_hash(nums, target):
    seen = {}
    for index in range(len(nums)):
        needed = target - nums[index]
        if needed in seen:
            return [seen[needed],index]
        else:
            seen[nums[index]] = index

    return []

# 完成后打开注释中的测试并运行：
assert two_sum_hash([2, 7, 11, 15], 9) == [0, 1]
assert two_sum_hash([3, 2, 4], 6) == [1, 2]
assert two_sum_hash([3, 3], 6) == [0, 1]

