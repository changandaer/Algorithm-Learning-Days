"""DAY04 跟做练习：计算从 1 到 n 的整数和。

请按照课程 Markdown 分三段手敲，不要复制整段答案。
手敲完成后增加 n 必须为正整数的判断。
"""

# TODO 1：读取正整数 n。
n = int(input("输入一个正整数："))

# TODO 2：如果 n 不合法，输出提示。
if n < 0 or n == 0:
    print("数据不合法，重新输入")

# TODO 3：否则使用 for、range 和累计器求和。
else:
    total = 0
    for i in range(1, n+1):
        total += i

# TODO 4：输出结果，并测试 n 为 1、5、10。
    print(f"1到n的整数和为{total}")

