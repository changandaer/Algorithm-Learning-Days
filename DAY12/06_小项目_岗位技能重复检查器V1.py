"""DAY12小项目：统计岗位技能、首次索引和重复技能。"""


job_skills = [
    " Python ",
    "Linux",
    "Git",
    "python",
    "PyTorch",
    "git",
    "C++",
    "PYTHON",
]


# 固定三步法：
# 第一步：" Python "、"python"、"PYTHON"统一后都算python
# 第二步：一次遍历中更新次数和首次索引；遍历计数找重复技能
# 第三步：保存counts、first_indices、duplicates三个结果


def analyze_duplicate_skills(raw_skills):
    """返回包含counts、first_indices和duplicates的字典。"""
    # TODO：独立完成，不要复制DAY10和DAY11函数后直接拼接。
    normal_skills = []
    duplicates = []
    counts = {}
    first_indices = {}
    if raw_skills == []:
        return {
        "counts": counts,
        "first_indices": first_indices,
        "duplicates": duplicates
    }

    for skill in job_skills:
        normal_skills.append(skill.strip().lower())
    for skill in normal_skills:
        counts[skill] = counts.get(skill,0) + 1
    for index in range(len(normal_skills)):
        if normal_skills[index] not in first_indices:
            first_indices[normal_skills[index]] = index
        else:
            if normal_skills[index] not in duplicates:
                duplicates.append(normal_skills[index]) 
    
    return {
        "counts": counts,
        "first_indices": first_indices,
        "duplicates": duplicates
    }
    
    pass

normal_skills = analyze_duplicate_skills(job_skills)

# 规定结果：
# counts == {"python": 3, "linux": 1, "git": 2, "pytorch": 1, "c++": 1}
# first_indices == {"python": 0, "linux": 1, "git": 2, "pytorch": 4, "c++": 6}
# duplicates == ["python", "git"]


# 完成函数后取消注释并运行：
report = analyze_duplicate_skills(job_skills)
assert report["counts"] == {
    "python": 3,
    "linux": 1,
    "git": 2,
    "pytorch": 1,
    "c++": 1,
}
assert report["first_indices"] == {
    "python": 0,
    "linux": 1,
    "git": 2,
    "pytorch": 4,
    "c++": 6,
}
assert report["duplicates"] == ["python", "git"]
assert analyze_duplicate_skills([]) == {
    "counts": {},
    "first_indices": {},
    "duplicates": [],
}
print(report)

