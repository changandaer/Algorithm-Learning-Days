"""DAY07 概念实验：区分哨兵值 -1 与列表负索引 -1。"""

skills = ["python", "linux", "git"]
found_index = -1

print("found_index 保存的普通数字：", found_index)
print("skills[-1] 访问的列表元素：", skills[-1])

# 分别把目标改成 linux 和 docker，手写线性查找。
target_skill = "linux"

# 最小样例：
# 处理阶段：
# 必须记住的状态：


# 从这里开始实现。找到时保存真实索引，找不到时保留 -1。

