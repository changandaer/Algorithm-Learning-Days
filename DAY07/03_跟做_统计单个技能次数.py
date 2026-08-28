"""DAY07 跟做练习：统计一个目标技能在列表中的出现次数。"""

all_skills = [
    "python", "linux", "git", "pytorch",
    "python", "c++", "linux", "git",
    "python", "pytorch", "linux", "docker",
]
target_skill = "python"

# 先手算 target_skill 的预期次数：3
# 程序必须记住的状态：次数


# 从这里开始实现。只需要一层循环和一个计数器。
count = 0
for skill in all_skills:
    if skill == target_skill:
        count += 1

print(f"目标技能{target_skill}出现了{count}次")