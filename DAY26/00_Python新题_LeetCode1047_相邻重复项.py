"""DAY26新题：LeetCode 1047相邻重复项；自己写三步分析、实现与测试，要求见课程。"""

class Solution:
    
    def removeDuplicates(self, s):

        single = []

        for element in s:
            if not single:
                single.append(element)
            else:
                if single[-1] == element:
                    single.pop()
                else:
                    single.append(element)
        
        return (''.join(single))

solution = Solution()

assert solution.removeDuplicates("abccba") == ''
assert solution.removeDuplicates("abbaca") == 'ca'
assert solution.removeDuplicates("azxxzy") == 'ay'
assert solution.removeDuplicates("aaa") == 'a'
assert solution.removeDuplicates("aaaa") == ''
assert solution.removeDuplicates("abab") == 'abab'
assert solution.removeDuplicates("abc") == 'abc'
assert solution.removeDuplicates("z") == 'z'



