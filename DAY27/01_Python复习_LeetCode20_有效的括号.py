"""DAY27：关闭参考答案，独立补写LeetCode20并测试；要求见当天课程。"""

class Solution:

    def isValid(self, s):

        left_bracket = []
        bracket_pairs = {')':'(',']':'[','}':'{'}

        for bracket in s:

            if bracket in '([{':
                left_bracket.append(bracket)
            else:
                if not left_bracket:
                    return False
                if left_bracket[-1] == bracket_pairs[bracket]:
                    left_bracket.pop()
                else:
                    return False
        
        return not left_bracket


solution = Solution()
assert solution.isValid("()") is True
assert solution.isValid("()[]{}") is True
assert solution.isValid("{[()]}") is True
assert solution.isValid("([)]") is False
assert solution.isValid("(]") is False
assert solution.isValid("]") is False
assert solution.isValid("((") is False
assert solution.isValid("(()") is False