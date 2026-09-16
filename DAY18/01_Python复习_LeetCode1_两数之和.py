"""DAY18 Python复习：闭卷重写两数之和；要求见当天课程，自己写三步分析、实现与测试。"""

class Solution:

    def twoSum(self, nums, target):

        seen = {}

        for index in range(len(nums)):

            needed = target - nums[index]

            if needed in seen:
                
                return [seen[needed],index]
            
            seen[nums[index]] = index
        
        return []

solution = Solution()
assert solution.twoSum([2, 7, 11, 15],9) == [0, 1]
assert solution.twoSum([3, 2, 4],6) == [1, 2]
assert solution.twoSum([3, 3],6) == [0, 1]
assert solution.twoSum([-3, 4, 3, 90],0) == [0, 2]
assert solution.twoSum([],0) == []
