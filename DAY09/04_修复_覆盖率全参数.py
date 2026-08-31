"""DAY09修复：缺失技能和覆盖率函数不得偷偷读取全局核心清单。"""

# 合同一：find_missing_skills(core_skills, candidate_skills)
def find_missing_skills(core_skills, candidate_skills):
    missing_skills = []
    normal_candidate_skills = []
    for skill in candidate_skills:
        if skill.strip().lower() not in normal_candidate_skills:
            normal_candidate_skills.append(skill.strip().lower())
    for skill in core_skills:
        if skill not in normal_candidate_skills:
            missing_skills.append(skill)
    return missing_skills

# 合同二：calculate_coverage(core_skills, candidate_skills)
def calculate_coverage(core_skills, candidate_skills):
    normal_candidate_skills = []
    miss_count = 0
    for skill in candidate_skills:
        if skill.strip().lower() not in normal_candidate_skills:
            normal_candidate_skills.append(skill.strip().lower())
    for skill in core_skills:
        if skill not in normal_candidate_skills:
            miss_count += 1
    return (1-(miss_count/len(core_skills)))*100

# 分别定义函数，空核心清单覆盖率为0.0。


# 使用两套不同核心技能清单和空核心清单测试。

assert find_missing_skills(["python", "c++", "pytorch", "linux", "git"],[" Python ", "Git", "linux", "PYTHON"]) == ["c++", "pytorch"]
assert calculate_coverage(["python", "c++", "pytorch", "linux", "git"],[" Python ", "Git", "linux", "PYTHON"]) == 60

assert find_missing_skills(["python", "c++", "pytorch", "linux", "git"],[" Python ", "Git", "linux", "PYTHON", "C++", "PyTorch"]) == []
assert calculate_coverage(["python", "c++", "pytorch", "linux", "git"],[" Python ", "Git", "linux", "PYTHON", "C++", "PyTorch"]) == 100

assert find_missing_skills(["python", "c++", "pytorch", "linux", "git"],[]) == ["python", "c++", "pytorch", "linux", "git"]
assert calculate_coverage(["python", "c++", "pytorch", "linux", "git"],[]) == 0
