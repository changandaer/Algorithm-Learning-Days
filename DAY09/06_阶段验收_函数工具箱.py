"""DAY09闭卷阶段验收，限时60分钟，关闭其他课程与AI。

完成normalize_skill、find_skill_index、find_two_sum三个函数。
每个函数写合同和至少三个assert。到时保留真实现场。
"""

# 函数一合同与实现：normalize_skill(raw_skill)
def normalize_skill(raw_skill):
    normalize_skill = []
    for skill in raw_skill:
        if skill.strip().lower() not in normalize_skill:
            normalize_skill.append(skill.strip().lower())
    return normalize_skill

# 函数一assert：
assert normalize_skill([" Python ", "Git", "linux", "PYTHON"]) == ["python", "git", "linux"]
assert normalize_skill([]) == []

# 函数二合同与实现：find_skill_index(skills, target_skill)
def find_skill_index(skills,target_skill):
    normalize_skill = []
    for skill in skills:
        if skill.strip().lower() not in normalize_skill:
            normalize_skill.append(skill.strip().lower())
    for skill_index in range(len(skills)):
        if normalize_skill[skill_index] == target_skill.strip().lower():
            return skill_index
    return -1


# 函数二assert：
assert find_skill_index([" Python ", "Git", "linux", "PYTHON"],"git") == 1
assert find_skill_index([" Python ", "Git", "linux", "PYTHON"],"GIT") == 1
assert find_skill_index(["python", "linux", "git"], "Linux") == 1
assert find_skill_index(["python", "linux", "git"], "git ") == 2
assert find_skill_index(["python"], "java") == -1
assert find_skill_index([], "python") == -1

# 函数三合同与实现：find_two_sum(numbers, target)
def find_two_sum(numbers,target):
    target_index = []
    for first_index in range(len(numbers)):
        for second_index in range(first_index+1,len(numbers)):
            if numbers[first_index] + numbers[second_index] == target:
                target_index.append(first_index)
                target_index.append(second_index)
    return target_index


# 函数三assert：
assert find_two_sum([2, 7, 11, 15], 9) == [0, 1]
assert find_two_sum([2, 7, 11, 15], 26) == [2, 3]
assert find_two_sum([2, 7, 11, 15], 14) == []
assert find_two_sum([3, 3], 6) == [0, 1]
assert find_two_sum([], 9) == []
