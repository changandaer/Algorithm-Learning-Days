"""DAY11小项目：使用字典建立技能名称到首次原始索引的映射。"""

job_skills = ["Python", "Linux", "Git", "python", "PyTorch"]

# 第一步：最小输入与预期输出：["Python", "Linux", "Git", "python", "PyTorch"],python -> 0
# 第二步：代码阶段：
# 第三步：需要保存的状态与小测试：


# 函数合同：build_first_index(job_skills) -> dict
def build_first_index(job_skills):
    normal_job_skills = []
    job_index = {}
    for skill in job_skills:
        normal_job_skills.append(skill.strip().lower())
    for index in range(len(normal_job_skills)):
        if normal_job_skills[index] not in job_index:
            job_index[normal_job_skills[index]] = index
    
    return job_index



# 函数合同：find_skill_index_with_hash(job_skills, target_skill) -> int
def find_skill_index_with_hash(job_skills, target_skill):
    normal_target_skill = target_skill.lower()
    job_index = build_first_index(job_skills)
    if normal_target_skill in job_index:
        return job_index[normal_target_skill]
    
    return -1

# 测试Python应返回0、PyTorch返回4、Docker返回-1、空列表返回-1。

assert find_skill_index_with_hash(["Python", "Linux", "Git", "python", "PyTorch"],"Python") == 0
assert find_skill_index_with_hash(["Python", "Linux", "Git", "python", "PyTorch"],"PyTorch") == 4
assert find_skill_index_with_hash(["Python", "Linux", "Git", "python", "PyTorch"],"Docker") == -1
assert find_skill_index_with_hash([],"Python") == -1