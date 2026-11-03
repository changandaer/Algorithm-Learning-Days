# DAY35：先学922精讲，关闭示范后重写与测试；理论题在同目录课后总结.md。

class Solution:
    def sortArrayByParityII(self, nums):

        even = 0
        odd = 1

        while even < len(nums) and odd < len(nums):
            if nums[even] % 2 == 0:
                even += 2
            elif nums[odd] % 2 == 1:
                odd += 2
            else:
                nums[even],nums[odd] = nums[odd],nums[even]
                even += 2
                odd += 2
        return nums

solution = Solution()
for nums,expected in [([4,2,5,7],[4,5,2,7]),
             ([2,3],[2,3]),
             ([3,2],[2,3]),
             ([0,1,2,3],[0,1,2,3]),
             ([2,0,3,1],[2,3,0,1]),
             ([2,2,1,1],[2,1,2,1])
]:
    nums_copy = nums.copy()
    results = solution.sortArrayByParityII(nums_copy)
    assert results == expected
