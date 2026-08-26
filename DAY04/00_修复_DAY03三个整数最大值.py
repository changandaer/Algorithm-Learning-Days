"""DAY04 修复练习：从空白重写三个整数最大值。

要求：
1. 不使用 max()。
2. 每个新数字都与“目前最大值”比较。
3. 测试 3/8/5、10/1/5、-1/-5/-3、4/4/4。
"""

a = int(input("输入第一个数字："))
b = int(input("输入第二个数字："))
c = int(input("输入第三个数字："))

if b > a:
    current_max = b
else:
    current_max = a 
if c > current_max:
    current_max = c 
# else:
#     current_max = current_max
print(f"三个数中最大的是{current_max}")

# 有 if 不一定非要有 else ，可以只有 if

