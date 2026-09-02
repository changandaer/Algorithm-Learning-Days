"""DAY10小项目：使用字典分析匿名化岗位技能出现频率。"""

job_skill_lists = [
    ["Python", "Linux", "Git", "PyTorch"],
    ["python", "C++", "linux", "git"],
    ["PYTHON", "PyTorch", "Linux", "Docker"],
]

# 第一步：最小输入与预期输出：
# 第二步：代码阶段：
# ​建立空统计表
# 逐项读取技能
# 更新对应次数
# 输出统计表
# 第三步：需要保存的状态与小测试：


# 使用字典统计，输出全部频率、最高频技能和至少出现2次的技能。
def find_frequently_skill(job_skill_lists):
    normal_skills = []
    frequently_skills = {}
    least_two = {}
    frequently_skill_counts = 0
    for row_skill in job_skill_lists:
        for skill in row_skill:
            normal_skills.append(skill.strip().lower())
    for skill in normal_skills:
        frequently_skills[skill] = frequently_skills.get(skill, 0) + 1
    for skill in frequently_skills:
        if frequently_skills[skill] > frequently_skill_counts:
            frequently_skill = skill
            frequently_skill_counts = frequently_skills[skill]
    for skill in frequently_skills:
        if frequently_skills[skill] >= 2:
            least_two[skill] = frequently_skills[skill]
    return  f"全部技能频率是{frequently_skills}，最高频技能是{frequently_skill}，至少出现两次以上的技能是{least_two}"

frequently_skills = find_frequently_skill(job_skill_lists)
print(frequently_skills)

