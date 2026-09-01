"""DAY10修复：normalize_skill只处理一个字符串，查找保持原始索引。"""


def normalize_skill(raw_skill):
    normalized_skills = []
    for skill in raw_skill:
        normalized_skills.append(skill.strip().lower())
    return normalized_skills


def find_skill_index(skills, target_skill):
    normalized_skills = normalize_skill(skills)
    for index in range(len(skills)):
        if normalized_skills[index] == normalize_skill(target_skill):
            return index
    return -1


# 预置合同测试。不得改测试迁就实现。
assert normalize_skill(" Python ") == "python"
assert normalize_skill("   ") == ""
assert find_skill_index(["python", "python", "git"], "git") == 2
assert find_skill_index(["python", "python"], "java") == -1
assert find_skill_index([], "python") == -1

