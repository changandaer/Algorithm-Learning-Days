"""DAY03必做一：读取分数，检查范围并输出等级。"""

# TODO 1：使用input()读取分数，并用int()转换成整数。
score = int(input("输入分数："))

# TODO 2：先用or判断分数是否小于0或大于100。
is_not_valid = score < 0 or score > 100

# TODO 3：使用elif从高到低判断优秀、良好、及格和不及格。
if not is_not_valid:
    if score >= 90:
        print("优秀")
    elif score >=80:
        print("良好")
    elif score >=60:
        print("及格")
    else:
        print("不及格")
else:
    print("分数不合法")
# TODO 4：用指定的8个分数逐一测试。

