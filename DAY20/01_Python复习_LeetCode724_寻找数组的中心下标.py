"""DAY20复习：闭卷重写中心下标；要求见课程，自己写三步分析、实现和测试。"""
# 1.输入输出：[2, 4, 1, 6] -> 2
# 2.工作阶段：右侧 = 左侧 = 总值 - 右侧 - 自己

class Solution:

    def pivotIndex(self, nums):

        total = sum(nums)
        right_side = 0

        for index in range(len(nums)):

            if right_side == total - right_side - nums[index]:

                return index
            
            right_side += nums[index]
        
        return -1

solution = Solution()
assert solution.pivotIndex([2, 4, 1, 6]) == 2
assert solution.pivotIndex([1, 2]) == -1
assert solution.pivotIndex([0, 0]) == 0
assert solution.pivotIndex([2]) == 0


