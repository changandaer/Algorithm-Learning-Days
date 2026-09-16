"""DAY19新题：寻找数组的中心下标；要求见课程，自己写三步分析、实现和测试。"""

# 1.输入输出：[1, 7, 3, 6, 5, 6] -> 3 
# 2.工作阶段：sum求出输入和，然后索引遍历输入，判断右侧和=总和-当前索引数字-左侧和是否=左侧和
class Solution:
    
    def pivotIndex(self, nums):

        total = sum(nums)

        adding = 0

        for index in range(len(nums)):
    
            if adding == total - nums[index] -adding:
                return index
            adding += nums[index]
        
        return -1


solution = Solution()
pivot = solution.pivotIndex([1, 7, 3, 6, 5, 6])
print(pivot)

assert solution.pivotIndex([1, 2, 3]) == -1
assert solution.pivotIndex([2, 1, -1]) == 0
assert solution.pivotIndex([0, 0, 0]) == 0
assert solution.pivotIndex([8]) == 0
assert solution.pivotIndex([1, -1, 4]) == 2
assert solution.pivotIndex([-1, -1, 0, 1, 1, 0]) == 5