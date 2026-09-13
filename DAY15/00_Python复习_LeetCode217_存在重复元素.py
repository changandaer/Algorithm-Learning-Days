"""DAY15任务0：LC217闭卷复习；题意、输入输出和测试要求见课程。自己写三步分析、实现和测试。"""

# 整数列表中只要某个数出现至少两次，返回`True`，否则返回`False`
# 1.输入输出：[1,2,3,1]→True、[1,2,3,4]→False、[-2,0,-2]→True、[7]→False
# 2.工作阶段：建立空字典，遍历输出的列表，如果已经存在就立刻返回true，不存在就加入字典

class Solution:
    
    def containsDuplicate(self, nums):
        
        seen = {}

        for num in nums:

            if num in seen:
                return True
            
            seen[num] = seen.get(num,0) + 1
        
        return False

solution = Solution()
assert solution.containsDuplicate([1,2,3,1]) == True
assert solution.containsDuplicate([1,2,3,4]) == False
assert solution.containsDuplicate([-2,0,-2]) == True
assert solution.containsDuplicate([7]) == False


