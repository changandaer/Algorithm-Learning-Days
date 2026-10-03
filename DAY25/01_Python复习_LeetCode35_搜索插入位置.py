"""DAY25复习：闭卷完成LeetCode 35搜索插入位置；自己分析、实现与测试，不修改输入列表。"""


class Solution:
    
    def searchInsert(self, nums, target):

        left_index = 0
        right_index = len(nums) - 1

        while right_index>=left_index:

            mid_index = (left_index + right_index)//2

            if nums[mid_index] > target:
                right_index = mid_index - 1
            elif nums[mid_index] < target:
                left_index = mid_index + 1
            else:
                return mid_index
        
        return left_index

solution = Solution()

nums = [2, 5, 9, 14]
target = 9
assert solution.searchInsert(nums,target) == 2

target = 7
assert solution.searchInsert(nums,target) == 2

target = 1
assert solution.searchInsert(nums,target) == 0

nums = [6]
target = 6
assert solution.searchInsert(nums,target) == 0

target = 4
assert solution.searchInsert(nums,target) == 0

target = 8
assert solution.searchInsert(nums,target) == 1

nums = [-5, -1, 3]
target = 0
assert solution.searchInsert(nums,target) == 2