"""DAY22新题：原地整理有序数组的有效前缀并返回长度；题意与测试见课程，三步和实现自己写。"""
# 1.输入输出：[0, 0, 1, 1, 1, 2] -> [0, 1, 2],3
# 2.write依旧是保留要被替换的位置的索引和被替换掉位置长度

class Solution:
    
    def removeDuplicates(self, nums):

        write = 1

        for read in range(1,len(nums)):

            if nums[read-1] != nums[read]:

                nums[write] = nums[read]
                write += 1
            print(nums)
        
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

