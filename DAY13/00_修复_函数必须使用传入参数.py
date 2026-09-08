"""DAY13任务0：要求见课程文档。请自己写三步分析，再从空白完成实现和测试。"""

# 固定三步法：
# 第一步：" Python "、"python"、"PYTHON"统一后都算python
# 第二步：一次遍历中更新次数和首次索引；遍历计数找重复技能
# 第三步：保存counts、first_indices、duplicates三个结果

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

def analyze_duplicate_skills(raw_skills):

    duplicates = []
    counts = {}
    first_indices = {}

    for index in range(len(raw_skills)):

        skill = raw_skills[index].strip().lower()

        counts[skill] = counts.get(skill,0) + 1

        if skill not in first_indices:
            first_indices[skill] = index
        
        if counts[skill] == 2:
            duplicates.append(skill)
    
    return {
            "counts":counts,
            "first_indices":first_indices,
            "duplicates":duplicates
            }
            
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