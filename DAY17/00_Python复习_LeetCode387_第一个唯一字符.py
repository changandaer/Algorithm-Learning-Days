"""DAY17任务0：LC387闭卷复习，题意和测试要求见课程；自己写三步分析、实现和测试。"""

class Solution:
    
    def firstUniqChar(self, s):

        seen = {}
        word = {}

        for index in range(len(s)):

            seen[s[index]] = seen.get(s[index],0) + 1
            word[s[index]] = index

        for key,count in seen.items():

            if count == 1:

                return word[key]
        
        return -1

solution = Solution()
print(solution.firstUniqChar("leetcode"))
assert solution.firstUniqChar("leetcode") == 0
assert solution.firstUniqChar("loveleetcode") == 2
assert solution.firstUniqChar("aabb") == -1
assert solution.firstUniqChar("aabc") == 2
assert solution.firstUniqChar("z") == 0
assert solution.firstUniqChar("") == -1

