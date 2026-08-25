"""DAY03必做二：不使用max()，找出三个整数中的最大值。"""

# TODO 1：分别读取三个整数。
a = int(input("输入第一个整数:"))
b = int(input("输入第二个整数:"))
c = int(input("输入第三个整数:"))
# TODO 2：先把第一个数保存为current_max（当前最大值）。
current_max = a
# TODO 3：如果第二个数更大，更新current_max。
if b>a:
    current_max = b
# TODO 4：如果第三个数更大，再更新current_max。
if c>b:
    current_max = c
# TODO 5：输出current_max，并完成课程要求的4组测试。
print(f"三个整数中最大的是：{current_max}")
