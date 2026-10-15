# DAY29：闭卷复写LeetCode26；题意、测试与要求见同目录课程，自写三步分析。

class Solution:

    def remove_duplicates(self,nums):

        count = 0
        unique_elements = []

        for num in nums:
            if num not in unique_elements:
                unique_elements.append(num)
                count += 1
        
        return count,unique_elements,nums

solution = Solution()
count,unique_elements,nums = solution.remove_duplicates([0,0,2,2,5])
print(count,unique_elements,nums)

# 要求是原地修改，但是我忘记了如何原地修改，所以新建了一个列表unique_elements
# 这种leetcode题目做一遍之后过几天还是不会做是正常的吗，应该如何融会贯通呢，还是就靠多做几遍呢？