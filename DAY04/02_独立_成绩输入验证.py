"""DAY04 独立练习：反复读取成绩，直到输入合法，再输出等级。

限制：使用 while 的条件自然结束，不使用 break。
"""

# TODO 1：第一次读取成绩。
score = int(input("输入你的成绩："))

# TODO 2：成绩不在 0～100 时，使用 while 反复读取。
while score < 0 or score > 100:
    score = int(input("成绩不合法，重新输入你的成绩："))

# TODO 3：合法后，使用 if/elif/else 输出 A、B、C 或 D。
if score >= 90:
    print("A")
elif score >=80:
    print("B")
elif score >=60:
    print("C")
else:
    print("D")

