"""DAY11独立：使用LeetCode提供的class Solution格式完成两数之和。"""


class Solution:
    def twoSum(self, nums, target):
        # 在这里独立完成哈希解法。
        seen = {}
        for index in range(len(nums)):
            needed = target - nums[index]
            if needed in seen:
            # if needed in seen难道不也是一种特殊的for循环检索吗，检索seen这个字典中是否存在needed这个key，为什么这个时间复杂度就低呢？
                return [seen[needed],index]
            
            seen[nums[index]] = index

        return []
        pass


# 本地测试，完成后取消注释：
solution = Solution()
assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]
assert solution.twoSum([3, 2, 4], 6) == [1, 2]
assert solution.twoSum([3, 3], 6) == [0, 1]

