"""DAY19复习：闭卷重写一维数组的动态和；要求见课程，自己写三步分析、实现和测试。"""

# 1.输入输出：[4, 1, -2, 3] -> [4, 5, 3, 6]
class Solution:
    
    def runningSum(self, nums):

        add = []
        adding = 0

        for index in range(len(nums)):

            adding += nums[index]
            add.append(adding)
        
        return add

solution = Solution()
assert solution.runningSum([4, 1, -2, 3]) == [4, 5, 3, 6]
assert solution.runningSum([-2, -3]) == [-2, -5]
assert solution.runningSum([0]) == [0]

