"""DAY10修复：核心技能为空时覆盖率返回0.0，不能执行除零。"""


def calculate_coverage(core_skills, candidate_skills):
    covered_count = 0
    for core_skill in core_skills:
        if core_skill in candidate_skills:
            covered_count += 1
    return covered_count / len(core_skills) * 100


# 先只运行第一条并观察ZeroDivisionError，再修复函数。
assert calculate_coverage([], ["python"]) == 0.0
assert calculate_coverage(["python"], []) == 0.0
assert calculate_coverage(["python", "git"], ["python", "git"]) == 100.0
assert calculate_coverage(["python", "git"], ["python"]) == 50.0

# 空核心清单的合同理由：

