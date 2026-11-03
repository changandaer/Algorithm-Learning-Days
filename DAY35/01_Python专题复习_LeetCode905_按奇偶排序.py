# DAY35：独立复习905，简述读写职责并实现测试；要求见同目录课程。
# 双指针：
#       读位置：当前正在检索的元素位置
#       写位置：下一个满足条件要写入的位置
#       读位置往前推进，写位置只有当满足条件才向前推进

class Solution:
    def sortArrayByParity(self,nums):
        write = 0
        for read in range(len(nums)):
            if nums[read] %2 == 0:
                nums[write],nums[read] = nums[read],nums[write]
                write += 1
        
        return nums

solution = Solution()
for nums,expected in [
                        ([3,1,2,4],[2,4,3,1]),
                        ([0],[0]),
                        ([1,3,5],[1,3,5]),
                        ([2,4,6],[2,4,6]),
                        ([2,1,2,1],[2,2,1,1])
]:
    nums_copy = nums.copy()
    assert nums == nums_copy # True
    results = solution.sortArrayByParity(nums_copy)
    assert results == expected

