"""DAY07 概念实验：区分哨兵值 -1 与列表负索引 -1。"""

skills = ["python", "linux", "git"]
found_index = -1

print("found_index 保存的普通数字：", found_index)
print("skills[-1] 访问的列表元素：", skills[-1])

# 分别把目标改成 linux 和 docker，手写线性查找。
target_skill = "docker"

# 最小样例：skills = ["python"]
# 处理阶段：遍历skills列表
# 必须记住的状态：列表元素 skill 以及对应的索引 index，是否找到 is_found


# 从这里开始实现。找到时保存真实索引，找不到时保留 -1。
is_found = True

for index in range(len(skills)):
    if target_skill == skills[index]:
        is_found = True
        found_index = index
        break
    else:
        is_found = False

if is_found:
    print(f"找到目标技能{target_skill}，索引是{index}")
else:
    print(f"没有找到目标技能{target_skill}")

