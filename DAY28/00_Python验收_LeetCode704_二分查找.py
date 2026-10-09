"""DAY28：闭卷完成704及换输入测试，自己写三步分析；题意和验收要求见当天课程。"""
# [-8,-2,1,6,11,19],6 -> 3

class Solution:
    
    def search(self, nums, target):

        left_index = 0
        right_index = len(nums)-1
        
        while right_index>=left_index:

            middle_index = (left_index + right_index)//2

            if nums[middle_index] > target:
                right_index = middle_index - 1
            elif nums[middle_index] < target:
                left_index = middle_index + 1
            else:
                return middle_index
            
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
