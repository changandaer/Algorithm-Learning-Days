# DAY30：巩固26的原地修改；独立写三步与实现，题意及测试见同目录课程。
# 1.输入输出：[1,1,2,2,3] -> [1,2,3,2,3],k=3
# 2.步骤：需要两个下标，一个辅助下标保存最后的相同元素的位置，一个查询下标去寻找后续的不同元素

class Solution:
    
    def removeDuplicates(self, nums):
        # for query in range(1,len(nums)):
        #     if nums[auxiliary] == nums[query-1]:
        #         pass
        #     else:
        #         nums[auxiliary] = nums[query]
        #         auxiliary += 1

        auxiliary = 1
        
        for query in range(1,len(nums)):

            if nums[query-1] != nums[query]:
            # 只有查询时候的相邻两数不同才会发生变动，用查询到的不同的数放到辅助下标的位置，然后辅助下标向后移一位

                nums[auxiliary] = nums[query]
                auxiliary += 1

        return auxiliary


solution = Solution()
nums = [0, 0, 1, 1, 1, 2]
result = solution.removeDuplicates(nums)
assert nums == [0, 1, 2, 1, 1, 2] 
assert result == 3

nums = [1, 2, 3]
result = solution.removeDuplicates(nums)
assert nums == [1, 2, 3] 
assert result == 3
