"""DAY08 小项目：用三个函数计算候选人的核心技能覆盖率。

这只是函数与指标练习，不代表真实招聘决策。
"""

core_skills = ["python", "c++", "pytorch", "linux", "git"]
candidate_skills = [" Python ", "Git", "linux", "PYTHON"]
# 函数合同一：normalize_and_deduplicate
def normalize_and_deduplicate(raw_skills):
    normal_skills = []
    for skill in raw_skills:
        if skill.strip().lower() not in normal_skills:
            normal_skills.append(skill.strip().lower())
    return normal_skills


# 函数合同二：find_missing_skills
def find_missing_skills(normal_skills):
    missing_skills = []
    for skill in core_skills:
        if skill not in normal_skills:
            missing_skills.append(skill)
    return missing_skills

# 函数合同三：calculate_coverage
def calculate_coverage(normal_skills):
    miss_count = 0
    for skill in core_skills:
        if skill not in normal_skills:
            miss_count += 1
    return (1-(miss_count/len(core_skills)))*100


# 从这里分别定义三个函数。


# 调用函数，输出标准化清单、缺失技能和覆盖率。
normal_skills = normalize_and_deduplicate(candidate_skills)
missing_skills = find_missing_skills(normal_skills)
coverage = calculate_coverage(normal_skills)

print(f"规定数据标准化后已有{normal_skills}，缺少{missing_skills}，覆盖率为{coverage}")
# 至少断言：规定数据、全部覆盖、完全未覆盖、核心列表为空。

assert normalize_and_deduplicate(["python", "c++", "pytorch", "linux", "git"]) == ["python", "c++", "pytorch", "linux", "git"]
assert find_missing_skills(["python", "c++", "pytorch", "linux", "git"]) == []
assert calculate_coverage(["python", "c++", "pytorch", "linux", "git"]) == 100

assert normalize_and_deduplicate([]) == []
assert find_missing_skills([]) == ["python", "c++", "pytorch", "linux", "git"]
assert calculate_coverage([]) == 0