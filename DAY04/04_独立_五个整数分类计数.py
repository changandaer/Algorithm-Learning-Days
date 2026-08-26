"""DAY04 独立练习：读取五个整数，统计正数、负数和零。

必须使用 for 循环，不能复制五次 input()。
"""

zero_num = 0
negative_num = 0
positive_num = 0

for i in range(1,6):

    a = int(input(f"输入第{i}个整数："))

    if a == 0:
        zero_num += 1
    elif a > 0:
        positive_num +=1
    else:
        negative_num +=1

print(f"正数{positive_num}个、负数{negative_num}个、零{zero_num}个")