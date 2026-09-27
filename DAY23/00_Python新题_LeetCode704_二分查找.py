"""DAY23新题：LeetCode 704二分查找；题意和测试见课程，三步分析、实现与测试自己写。"""


class Solution:

    def search(self, nums, target):

        left = 0
        right = len(nums) - 1

        while left < right or left == right:

            mid_index = (right + left) // 2

            if nums[mid_index] < target:
                left = mid_index + 1
                
            elif nums[mid_index] > target:
                right = mid_index - 1

            else:
                return mid_index
        
        return -1


solution = Solution()

nums = [-8, -2, 1, 4, 9, 15, 21]
target = 9
assert solution.search(nums,target) == 4

target = -8
assert solution.search(nums,target) == 0

target = 21
assert solution.search(nums,target) == 6

target = 0
assert solution.search(nums,target) == -1