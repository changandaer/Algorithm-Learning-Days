"""DAY14任务1：LeetCode 1闭卷复习。题意与测试要求见课程文档。"""

# 1.输入输出：`[2,7,11,15],9` -> [0,1]

# 2.阶段：建立空字典，查看需要数字是否存在字典中，存在就返回，不存在就加入字典

class Solution:

    def twoSum(self, nums, target):

        seen = {}

        for index in range(len(nums)):

            needed = target - nums[index]

            if needed in seen:

                return [seen[needed],index]
            
            seen[nums[index]] = index
        return []

solution = Solution()

assert solution.twoSum([2,7,11,15],9) == [0,1]
assert solution.twoSum([3,3],6) == [0,1]
assert solution.twoSum([3],6) == []