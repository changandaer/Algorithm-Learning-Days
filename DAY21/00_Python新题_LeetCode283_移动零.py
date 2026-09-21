"""DAY21新题：原地移动零并保持非零元素顺序；具体输入输出见课程，三步、实现和测试自己写。"""
# 1.输入输出：[0, 5, 0, -2, 5] -> [5, -2, 5, 0, 0]
# 2.任务步骤：

class Solution:
    
    def moveZeroes(self, nums):

        prefix_nmus = []
        num_zero = 0

        for index in range(len(nums)):

            if nums[index] != 0:
                prefix_nmus.append(nums[index])
            else:
                num_zero += 1
        for i in range(num_zero):
            prefix_nmus.append(0)
        
        return prefix_nmus

solution = Solution()
assert solution.moveZeroes([0, 5, 0, -2, 5]) == [5, -2, 5, 0, 0]
assert solution.moveZeroes([1, 0, 0, 2, 0, 3]) == [1, 2, 3, 0, 0, 0]
assert solution.moveZeroes([4, -1, 4]) == [4, -1, 4]



        

