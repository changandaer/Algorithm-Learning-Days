"""DAY07 独立练习：依次统计每一种技能的出现次数。

要求 skill_counts 与 unique_skills 的相同索引表示同一种技能。
"""

all_skills = [
    "python", "linux", "git", "pytorch",
    "python", "c++", "linux", "git",
    "python", "pytorch", "linux", "docker",
]
unique_skills = ["python", "linux", "git", "pytorch", "c++", "docker"]

# 最小样例：先只统计 python。
# 处理阶段：双重遍历 unique_skills 与 all_skills，分别统计 unique_skills 中每个元素出现的次数
# 必须记住的状态：每个技能出现的次数count以及skills_counts这个计数列表


# 从这里开始实现，最终建立 skill_counts 并逐项输出。
count = 0
skill_counts = []

for unique_skill in unique_skills:
    for all_skill in all_skills:
        if unique_skill == all_skill:
            count += 1
    skill_counts.append(count)
    count = 0
print(skill_counts)