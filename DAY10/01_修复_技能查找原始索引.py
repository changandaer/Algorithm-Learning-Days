"""DAY10修复：返回原列表索引，不能先去重改变座位号。"""


def find_skill_index(skills, target_skill):
    normalized_skills = []
    for skill in skills:
        if skill.strip().lower() not in normalized_skills:
            normalized_skills.append(skill.strip().lower())

    for index in range(len(normalized_skills)):
        if normalized_skills[index] == target_skill.strip().lower():
            return index
    return -1


# 先运行，第二条应当失败。不得修改预期结果。
assert find_skill_index(["python", "linux", "git"], "git") == 2
assert find_skill_index(["python", "python", "git"], "git") == 2
assert find_skill_index(["python", "python"], "java") == -1
assert find_skill_index([], "python") == -1

# 失败根因：
# 最小修复：

