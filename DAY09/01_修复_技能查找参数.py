"""DAY09修复：技能列表和目标技能都必须通过参数传入。"""

# 函数合同
# 函数名：find_skill_index
# 参数：skills, target_skill
# 返回值及类型：索引整数或 -1
# 最小例子：(["python", "linux", "git"], "Linux") == 1


# 定义函数，不在内部写死技能列表。
def find_skill_index(skills, target_skill):
    normal_skills = []
    for skill in skills:
        if skill.strip().lower() not in normal_skills:
            normal_skills.append(skill.strip().lower())
    
    for skill_index in range(len(normal_skills)):
        if target_skill.strip().lower() == normal_skills[skill_index]:
            return skill_index
    return -1


# 使用两套不同列表、空列表和找不到情况编写assert。

assert find_skill_index(["python", "linux", "git"], "Linux") == 1
assert find_skill_index(["python", "linux", "git"], "git ") == 2
assert find_skill_index(["python"], "java") == -1
assert find_skill_index([], "python") == -1