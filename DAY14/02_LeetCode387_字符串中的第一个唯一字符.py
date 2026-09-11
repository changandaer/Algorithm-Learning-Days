"""DAY14任务2：LeetCode 387。请从空白完成三步分析、实现和测试。"""

# 1.输入输出："leetcode" -> 0  "aabb" -> -1

# 2.阶段：建立空字典，查看需要数字是否存在字典中，存在就返回，不存在就加入字典

class Solution:
    
    def firstUniqChar(self, s):

        letters = {}
        word = {}

        for index in range(len(s)):

            letters[s[index]] = letters.get(s[index],0) + 1
            word[s[index]] = index

        for letter,count in letters.items():

            if count == 1:

                return word[letter]
        
        return -1

solution = Solution()

index = solution.firstUniqChar("leetcode")
print(index)

assert solution.firstUniqChar("aabb") == -1
assert solution.firstUniqChar("") == -1
assert solution.firstUniqChar("z") == 0

# 时间复杂度是 O(len(s))，输入字符串越长，时间复杂度越高，也就是O(n)
# 额外空间复杂度是两个字典的长度，输入字符越长，种类越多，额外空间复杂度也越高，也是O(n)