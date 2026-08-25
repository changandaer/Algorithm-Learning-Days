"""第002天独立任务：比较两个整数。

不要复制完整答案。完成后依次测试：(8, 3)、(2, 7)、(5, 5)、(-2, -5)。
"""

first_number = -2
second_number = -5

# TODO：使用if、elif、else覆盖“第一个更大、第二个更大、相等”三种情况。
if first_number > second_number:
    print(f"较大的数是：{first_number}")
elif first_number < second_number:
    print(f"较大的数是：{second_number}")
else:
    print("两个数相等")

# 1. = 和 == 的区别：……
#   =是将数值赋值给变量 和 ==是询问变量是否等于变量，返回 True或False
# 2. elif 在什么情况下检查：
#   elif在情况多于两种的时候，if，else只能表示两种判断关系
# 3. 为什么必须测试 5 和 5：
#   因为数值相等这种可能性是存在的