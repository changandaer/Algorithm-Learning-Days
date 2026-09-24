"""DAY22复习：把已有的非零筛选思路改成原地移动零；自己检查原列表、写三步、实现与测试。"""
# 1.输入输出：[0, 5, 0, -2, 5] -> [5, -2, 5, 0, 0]
# 2.任务步骤：write保存下一个非零数的位置，也保存非零数的数量

class Solution:
    
    def moveZeroes(self, nums):

        write = 0

        for read in range(len(nums)):

            if nums[read] != 0:

                nums[write] = nums[read]

                write += 1
        
        for index in range(write,len(nums)):

            nums[index] = 0

        

solution = Solution()
nums = [0, 5, 0, -2, 5]
result = solution.moveZeroes(nums)
assert nums == [5, -2, 5, 0, 0]
assert result is None
nums = [0]
solution.moveZeroes(nums)
assert nums == [0]
nums = [0, 0, 0]
solution.moveZeroes(nums)
assert nums == [0, 0, 0]
nums = [4, -1, 4]
solution.moveZeroes(nums)
assert nums == [4, -1, 4]
nums = [7, 0]
solution.moveZeroes(nums)
assert nums == [7, 0]
nums = [0, 7]
solution.moveZeroes(nums)
assert nums == [7, 0]
nums = [1, 0, 0, 2, 0, 3]
solution.moveZeroes(nums)
assert nums == [1, 2, 3, 0, 0, 0]

