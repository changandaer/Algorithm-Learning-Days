"""DAY16任务0：LC242闭卷复习。输入输出和平台入口见课程；请自己写三步分析、实现和测试。"""

# 1.输入输出：("anagram","nagaram") == True
# 2.工作阶段：建立两个字典，如果输入两个字符串长度相等，将字符串的字符加入两个字典，判断两个字典是否相同即可，字典相同意味着键值对都相同
# 3.代码用时：7分钟

class Solution:
    
    def isAnagram(self, s, t):

        s_dict = {}
        t_dict = {}

        if len(s) == len(t):

            for char_s in s:
                s_dict[char_s] = s_dict.get(char_s,0) + 1
            for char_t in t:
                t_dict[char_t] = t_dict.get(char_t,0) + 1
            
            if s_dict == t_dict:
                return True
        
        return False

solution = Solution()

assert solution.isAnagram("anagram","nagaram") == True
assert solution.isAnagram("aab","aba") == True
assert solution.isAnagram("","") == True
assert solution.isAnagram("rat","car") == False
assert solution.isAnagram("aab","abb") == False
assert solution.isAnagram("a","aa") == False



