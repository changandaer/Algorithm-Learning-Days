# DAY30：继续完成27；独立写三步与实现，题意及测试见同目录课程。
# 1.输入输出：[4,1,4,2,1]，排除4 -> k=3,nums=[1,2,1,4,4]
#            [4,4,4,2,1]，排除4 -> k=2,nums=[2,1,4,4,4]
#            [1,4,4,2,1]，排除4 -> k=3,nums=[1,2,1,4,4]
# 2.需要两个下标，辅助下标存储目标值的最小的下标，查询下标去寻找非目标值与目标值进行替换
#   nums = [1, 2, 3],val = 4的时候辅助下标与查询下标一起加1
#   nums[auxiliary],nums[query] = nums[query],nums[auxiliary]
#   query与auxiliary此时是相等的
#   只有nums[query] == val的时候只有查询下标向后查询，辅助下标保存与目标值相等的值的最小下标
class Solution:
    def removeElement(self, nums, val):
        auxiliary = 0
        for query in range(len(nums)):
            if nums[query] == val:
                pass
            else:
                nums[auxiliary],nums[query] = nums[query],nums[auxiliary]
                auxiliary += 1

        return auxiliary,nums

solution = Solution()
nums = [4,1,4,2,1]
result = solution.removeElement(nums,4)
assert result == (3,[1, 2, 1, 4, 4])

nums = [1, 2, 3]
result = solution.removeElement(nums,4)
assert result == (3,[1, 2, 3])  

nums = [4,4,4,2,1]
result = solution.removeElement(nums,4)
assert result == (2,[2,1,4,4,4])

nums = [4,4]
result = solution.removeElement(nums,4)
assert result == (0,[4,4])

nums = [5]
result = solution.removeElement(nums,5)
assert result == (0,[5])

nums = [5]
result = solution.removeElement(nums,0)
assert result == (1,[5])