"""DAY05 独立练习：不使用现成查找方法，手写线性查找。

限制：不使用 in、index()、count()。
"""

skills = ["python", "c++", "pytorch", "linux", "git"]

# TODO 1：读取并标准化目标技能。

# TODO 2：建立“是否找到”和“找到位置”的状态。

# TODO 3：逐项比较，找到后记录位置并停止查找。

# TODO 4：分别输出第几项或“暂未收录”。

target_skill = input("输入你想要查询的技能：")
norm_target_skill = target_skill.strip().lower()
find = False
# index_skill = 1 为什么 index_skill不用 提前定义 也可以运行成功呢？而 find 必须要提前定义呢？
# 我的猜测是因为如果 print 要用到 index_skill，就意味着 find 为 True，也意味着已经在 for 循环中定义过了
# 而 print 用到 find ，却可以不用经过 for 循环的定义直接到后续的判断

for index in range(len(skills)):
    if skills[index] == norm_target_skill:
        find = True
        index_skill = index + 1 
   
if find:
    print(f"你想要找的{target_skill}是第{index_skill}技能")
else:
    print(f"{target_skill}暂未收录。")