"""DAY18 Python新题：一维数组的动态和；要求见当天课程，自己写三步分析、实现与测试。"""
# 1.输入输出：[1, 2, 3, 4] -> [1, 3, 6, 10]

class Solution:
    
    def runningSum(self, nums):

        runningsum = []
        sum = 0

        for index in range(len(nums)):

            sum = sum + nums[index]

            runningsum.append(sum)
        
        return runningsum

solution = Solution()
runningsum = solution.runningSum([1, 2, 3, 4])
print(runningsum)

assert solution.runningSum([1, 2, 3, 4]) == [1, 3, 6, 10]
assert solution.runningSum([3, 1, 2, 10, 1]) == [3, 4, 6, 16, 17]
assert solution.runningSum([7]) == [7]
assert solution.runningSum([0, 0]) == [0, 0]
assert solution.runningSum([2, -3, 4]) == [2, -1, 3]