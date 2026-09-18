"""DAY20新题：反转字符串，原地修改字符列表；要求见课程，自己写三步分析、实现和测试。"""

# 1.输入输出 [1,2,3] -> [3,2,1]
class Solution:

    def reverseString(self, s):

        len_s = len(s)
        i = 0
        j = len_s-1

        while i < j:

            # a = s[i]
            # b = s[j]
            # c = a
            # s[i] = b
            # s[j] = c
            s[i],s[j] = s[j],s[i]

            i += 1
            j -= 1
        
        return s

solution = Solution()
s = solution.reverseString(["c", "o", "d", "e"])
print(s)

assert solution.reverseString(["a", "b", "c", "d", "e"]) == ["e", "d", "c", "b", "a"]
assert solution.reverseString(["a", "a", "b"]) == ["b", "a", "a"]
assert solution.reverseString(["a"]) == ["a"]

