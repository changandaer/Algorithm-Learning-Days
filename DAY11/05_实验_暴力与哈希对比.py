"""DAY11实验：让暴力法和哈希法处理相同测试，并解释复杂度。"""

test_numbers = [2, 7, 11, 15]
test_target = 9

# 固定三步法：
# 第一步：
# 第二步：
# 第三步：


# 定义暴力函数和哈希函数，调用后检查索引对应数字之和。
def two_sum_brute_force(nums, target):
    for first_index in range(len(nums)):
        for second_index in range(first_index+1, len(nums)):
            if nums[first_index] + nums[second_index] == target:
                return [first_index,second_index]
    return []

def two_sum_hash(nums, target):
    seen = {}
    for index in range(len(nums)):
        needed = target - nums[index]
        if needed in seen:
            return [seen[needed],index]
        seen[nums[index]] = index
    
    return []

# 我的复杂度解释：
# 我对复杂度还是不理解，需要你系统讲解，甚至可能涉及到计算机底层存储逻辑
# 暴力法时间：需要两个for循环，最多需要检索 len(nums)*(len(nums)-1)个
# 暴力法额外空间：最多需要 len(nums)*(len(nums)-1) 个存储空间
# 哈希法平均时间：只有一个for循环，但是我的疑问是 if needed in seen难道不也是一种特殊的for循环检索吗，检索seen这个字典中是否存在needed这个key，为什么这个时间复杂度就低呢？
# 哈希法额外空间：放一个for循环的空间len(nums)和一个字典的空间

