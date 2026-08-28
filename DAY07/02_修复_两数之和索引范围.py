"""DAY07 修复练习：下面的代码仍允许外层索引与内层索引相同。

进行必要修改，输出 Python 索引、两个数值和目标值。
"""

numbers = [2, 7, 11, 15]
target = 26
found = False

for first_index in range(len(numbers)):
    for second_index in range(first_index+1, len(numbers)):
        if numbers[first_index] + numbers[second_index] == target:
            found = True
            break

    if found:
        break

if found:
    print(f"第一个索引：{first_index}，第二个索引：{second_index}")
else:
    print("没有符合条件的两个数")


# 测试记录：目标9、目标26、目标14、[3, 3]与目标6。

