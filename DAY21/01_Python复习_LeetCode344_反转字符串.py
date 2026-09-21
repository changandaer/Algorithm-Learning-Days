"""DAY21复习：闭卷反转字符列表，检查调用方的原列表；三步、实现和测试自己写。"""
# 1.输入输出：["p", "y", "t", "h", "o", "n"] -> ["n", "o", "h", "t", "y", "p"]


class Solution:
    
    def reverseString(self, s):

        i = 0
        j = len(s) - 1

        while i<j:

            s[i],s[j] = s[j],s[i]

            i += 1
            j -= 1
        
        return s

solution  = Solution()
# assert solution.reverseString(["p", "y", "t", "h", "o", "n"]) == ["n", "o", "h", "t", "y", "p"]
print(solution.reverseString(["p", "y", "t", "h", "o", "n"]))

