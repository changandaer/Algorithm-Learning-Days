"""DAY24复习：闭卷完成LeetCode 704，验证单元素与查找失败；自己分析、实现和测试。"""
# 1.输入输出：[-8, -2, 1, 4, 9, 15, 21],9 -> 4

class Solution:
    
    def search(self, nums, target):

        left_index = 0
        right_index = len(nums) - 1
        

        while right_index >= left_index:

            mid_index = (left_index + right_index) // 2

            if nums[mid_index] > target:
                right_index = mid_index - 1
            elif nums[mid_index] < target:
                left_index = mid_index + 1
            elif nums[mid_index] == target:
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
