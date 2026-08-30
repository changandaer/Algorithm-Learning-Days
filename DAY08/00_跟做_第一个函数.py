"""DAY08 跟做：定义 add 函数，理解参数、返回值与 assert。"""

# 函数合同
# 函数名：add
# 输入：两个数字
# 输出：两数之和
# 最小例子：1 2 -> 3


# 按课程分段手敲 add，并保存一次调用结果。
def add(first_number, second_number):
    result = first_number + second_number
    return result

answer = add(1.1,2)
print(answer)

# 写三个正确断言；故意制造一次失败后再恢复。
assert add(1,2) == 3
assert add(-1,1) == 0
assert add(2,2) == 4
