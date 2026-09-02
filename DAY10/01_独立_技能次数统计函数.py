"""DAY10独立练习：标准化技能并返回出现次数的字典。"""

# 第一步：最小输入与预期输出：["python", "git", "PYTHON"] -> {'python': 2, 'git': 1}
# 第二步：代码阶段：
# 建立空列表用来存放标准化技能
# 遍历原始列表并将原始列表标准化
# 建立空字典
# 遍历标准化技能列表并将技能添加到空字典中
# 第三步：需要保存的状态与小测试：标准化列表、技能列表



# 函数合同：count_skills(raw_skills) -> dict
raw_skills = ["python", "git", "PYTHON", "linux", "GIT", ""]
# raw_skills = []
# raw_skills = ["", "", ""]

def count_skills(raw_skills):
    normal_skills = []
    for skill in raw_skills:
        normal_skill = skill.strip().lower()
        if normal_skill == '':
            pass
        else:
            normal_skills.append(normal_skill)

    skill_counts = {}
    # for skill in normal_skills:
    #     if skill in skill_counts:
    #         skill_counts[skill] += 1
    #     else:
    #         skill_counts[skill] = 1
    # print(skill_counts)
    for skill in normal_skills:
        skill_counts[skill] = skill_counts.get(skill, 0) + 1
    return skill_counts
# 从这里实现并测试普通、重复大小写、空列表、空字符串。

assert count_skills(["python", "git", "PYTHON", "linux", "GIT", ""]) == {'python': 2, 'git': 2, 'linux': 1}
assert count_skills([]) == {}
assert count_skills(["", "", ""]) == {}
