# DAY34：先学课程中的905精讲，关闭答案后从空白重写并测试；三步用自己的话简述。
# 双指针：读位置（当前检查哪一个元素）、写位置（下一符合条件的结果放在哪里）

class Solution:
    def sortArrayByParity(self, nums):
        write = 0
        for read in range(len(nums)):

            if nums[read] % 2 == 0:

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
    assert nums == nums_copy # False，因为.copy()会在内存中开辟一块全新的独立空间，把原列表里的所有元素完整复制一份放进去。
                             # solution.sortArrayByParity(nums_copy) 在原地修改的是 nums_copy 的那块新空间，而原本的 nums 空间完好无损、保持原样。
                             # 故而此时nums_copy已经被修改
    assert results == expected


