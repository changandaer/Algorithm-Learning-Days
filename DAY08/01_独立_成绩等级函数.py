"""DAY08 独立练习：把成绩判断封装成返回等级的函数。

函数内部不使用 input() 和 print()。
"""

# 函数合同
# 函数名：get_grade
# 输入：整数分数
# 输出：字符串格式等级
# 最小例子：90 -> A


# 从这里定义函数。
def get_grade(score):
    if score<0 or score>100:
        return("成绩不合法，重新输入")
    else:
        if score >= 90:
            return "A"
            # print("A")
        elif score >= 80:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "D"

# 在这里编写至少六个 assert，再调用一次并打印返回结果。
score_level = get_grade(101)
print(score_level)

assert get_grade(90) == "A"
assert get_grade(80) == "B"
assert get_grade(60) == "C"
assert get_grade(40) == "D"
assert get_grade(-10) == "成绩不合法，重新输入"
