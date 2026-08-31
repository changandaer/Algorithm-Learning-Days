"""DAY09修复：严格遵守成绩等级函数合同。

返回A/B/C/D或“成绩无效”，函数内部不输入、不打印。
"""

# 函数合同
# 函数名：get_grade
# 参数：score
# 返回值及类型：字符串
# 最小例子：90 -> A


# 先写六个assert，再定义函数时请暂时将assert放到函数定义之后运行。

def get_grade(score):
    if score < 0 or score > 100:
        return "成绩无效"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 60:
        return "C"
    return "D"

score_level = get_grade(90)
print(type(score_level))
print(score_level)

assert get_grade(90) == "A"
assert get_grade(80) == "B"
assert get_grade(60) == "C"
assert get_grade(40) == "D"
assert get_grade(-10) == "成绩无效"

