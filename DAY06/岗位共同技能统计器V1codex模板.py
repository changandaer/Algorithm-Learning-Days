# 1.拿 2 个数据手算 
# job_skill_lists = [
#     ["Python"],
#     ["python"],
# ]
# 2.把工作分为几个阶段
# 3.每个阶段程序都应该记住什么
# 把所有技能小写放到一个列表中 -> 小写列表
# 去重后放到去重的列表中 -> 去重列表
# 统计去重列表中每个技能在小写列表中出现的次数 -> 次数列表


job_skill_lists = [
    ["Python", "Linux", "Git", "PyTorch"],
    ["python", "C++", "linux", "git"],
    ["PYTHON", "PyTorch", "Linux", "Docker"],
]

lower_skills = []
unique_skills = []
count_skills = []
common_skills = []
count = 0

for first_skill in job_skill_lists:
    for second_skill in first_skill:
        lower_skills.append(second_skill.strip().lower())
# print(lower_skills)

for skill in lower_skills:
    if skill in unique_skills:
        pass
    else:
        unique_skills.append(skill)
# print(unique_skills)

for unique_skill in unique_skills:
    for lower_skill in lower_skills:
        if unique_skill == lower_skill:
            count += 1
    
    if count == len(job_skill_lists):
        common_skills.append(unique_skill)

    count_skills.append(count)
    count = 0
# print(count_skills)
# print(common_skills)


for index in range(len(unique_skills)):
    print(f"技能{unique_skills[index]}出现的次数是{count_skills[index]}",end="，")
print(f"共同技能是{common_skills}")