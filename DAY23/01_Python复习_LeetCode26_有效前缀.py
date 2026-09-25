"""DAY23复习：闭卷完成LeetCode 26，检查返回长度与原列表有效前缀；自己分析、实现和测试。"""
# 1.输入输出：[0, 0, 1, 1, 1, 2] -> [0, 1, 2],3
# 2.write是保留下一个可写位置和已保留的不同值的数量

class Solution:
    
    def removeDuplicates(self, nums):

        write = 1

        for read in range(1,len(nums)):

            if nums[read] != nums[read-1]:

                nums[write] = nums[read]
                write += 1
        
        return write

solution = Solution()
nums = [0, 0, 1, 1, 1, 2]
result = solution.removeDuplicates(nums)
assert nums == [0, 1, 2, 1, 1, 2] 
assert result == 3

nums = [1, 2, 3]
result = solution.removeDuplicates(nums)
assert nums == [1, 2, 3] 
assert result == 3

nums = [0, 0, 1, 1, 1, 2]
k = solution.removeDuplicates(nums)
assert k == 3
assert nums[:k] == [0, 1, 2]