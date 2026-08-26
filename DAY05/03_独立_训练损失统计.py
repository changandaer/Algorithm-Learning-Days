"""DAY05 独立练习：读取五个训练损失并统计。

限制：不使用 min()、max()、sum()。
"""

# TODO 1：建立空列表，使用循环读取五个小数并追加。

# TODO 2：使用列表中的真实数据初始化最低值和最高值。

# TODO 3：遍历列表，维护最低值、最高值与总和。

# TODO 4：计算平均值，输出列表和三项统计。

loss = []
sum = 0
for num in range(5):

    loss.append(input(f"输入第{num+1}个真实损失："))
    sum += float(loss[num])

current_min = float(loss[0])
current_max = float(loss[0])

for index in range(1,len(loss)):
    if float(loss[index]) > current_max:
        current_max = float(loss[index])
    elif float(loss[index]) < current_min:
        current_min = float(loss[index])

print(f"最低损失为{current_min}，最高损失为{current_max}，平均损失为{sum/len(loss)}")
    

