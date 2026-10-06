"""DAY25新题：LeetCode 20有效的括号；自己写三步分析、实现与测试，要求见当天课程。"""

class Solution:
    def isValid(self, s):

        brackets = []

        for bracket in s:
            
            # if bracket == '(' or '[' or '{': 
            # 这在python中的逻辑相当于 (bracket == '(') or ('[') or ('{') 
            # 由于('[')这个非空字符串，在布尔判断里永远是 `True`
            # 所以这个if分支永远执行
            # 正确写法是：
            # if bracket in '([{':
            # if bracket == '(' or bracket == '[' or bracket == '{':

            if bracket in '([{':
                brackets.append(bracket)
            else:
                if not brackets:
                    return False
                if bracket == ')':
                    if brackets[-1] == '(':
                        brackets.pop()
                    else:
                        return False
                elif bracket == ']':
                    if brackets[-1] == '[':
                        brackets.pop()
                    else:
                        return False
                elif bracket == '}':
                    if brackets[-1] == '{':
                        brackets.pop()
                    else:
                        return False
        # return True 循环走完之后，不能直接 `return True`，必须判断栈为空
        return len(brackets) == 0

solution = Solution()
assert solution.isValid("()") is True
assert solution.isValid("()[]{}") is True
assert solution.isValid("{[()]}") is True
assert solution.isValid("([)]") is False
assert solution.isValid("(]") is False
assert solution.isValid("]") is False
assert solution.isValid("((") is False
assert solution.isValid("(()") is False
