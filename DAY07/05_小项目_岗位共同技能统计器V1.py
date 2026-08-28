"""DAY07 小项目：分阶段完成岗位共同技能统计器 V1。

阶段一摊平并标准化；阶段二去重；阶段三计数并寻找共同技能。
"""

job_skill_lists = [
    ["Python", "Linux", "Git", "PyTorch"],
    ["python", "C++", "linux", "git"],
    ["PYTHON", "PyTorch", "Linux", "Docker"],
]

# 手算最小样例：
# 三个处理阶段：
# 每个阶段必须记住什么：摊平并标准化之后的列表、不重复技能列表、次数、次数列表、共同技能列表


# 阶段一：摊平并标准化。完成后先打印检查。
normal_lists = []
for first_skill in job_skill_lists:
    for second_skill in first_skill:
        normal_lists.append(second_skill.lower())
print(normal_lists)
# 阶段二：建立不重复技能列表。完成后先打印检查。
unique_skills = []
for unique_skill in normal_lists:
    if unique_skill in unique_skills:
        pass
    else:
        unique_skills.append(unique_skill)
print(unique_skills)

# 阶段三：统计次数并找出所有岗位共同技能。
count = 0
skill_counts = []
common_skills = []
for unique_skill in unique_skills:
    for skill in normal_lists:
        if skill == unique_skill:
            count += 1
    if count == len(job_skill_lists):
        common_skills.append(unique_skill)
    skill_counts.append(count)
    count = 0
print(skill_counts)
print(common_skills)

for index in range(len(skill_counts)):
    print(f"{unique_skills[index]}{skill_counts[index]}",end=',')


print(f'共同技能为{common_skills}')
    

