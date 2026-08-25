"""第002天独立任务：比较两个整数。

不要复制完整答案。完成后依次测试：(8, 3)、(2, 7)、(5, 5)、(-2, -5)。
"""

first_number = -2
second_number = -5

# TODO：使用if、elif、else覆盖“第一个更大、第二个更大、相等”三种情况。
if first_number > second_number:
    print(f"较大的数是：{first_number}")
elif first_number < second_number:
    print(f"较大的数是"{second_number})
else:
    print("两个数相等")
