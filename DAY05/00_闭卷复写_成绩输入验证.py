"""DAY05 间隔复习：闭卷重写成绩输入验证。

请先关闭 DAY04 和 DAY05 中的参考模板，再从空白完成。
完成后在文件底部写一条与模板不同或曾经遗漏的地方。
"""

score = int(input("输入你的成绩："))

while score < 0 or score > 100:

    score = int(input("非法成绩，重新输入你的成绩："))

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >=60:
    print("C")
else:
    print("D")

# 刚开始将 判断输出 写在了 while 里面，导致了死循环，也是第一次遇到，给自己一个警示