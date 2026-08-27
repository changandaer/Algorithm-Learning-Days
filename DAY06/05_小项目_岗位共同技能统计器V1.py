"""DAY06 小项目：统计匿名化岗位清单中的技能出现次数与共同技能。

限制：不使用字典和集合。请先拆成多个阶段，不要尝试在一层循环里全部完成。
"""

job_skill_lists = [
    ["Python", "Linux", "Git", "PyTorch"],
    ["python", "C++", "linux", "git"],
    ["PYTHON", "PyTorch", "Linux", "Docker"],
]

# 我的拆题
# 输入：双层列表，内层3个列表，每个列表的元素是字符串
# 输出：重复出现的技能以及次数以及共同拥有的技能
# 最小样例的手算过程：
# 必须记住的状态：
# 重复动作与控制结构：
# 普通测试、边界测试、反例：
# 中文伪代码：
# 将双层列表拆成 3 个单独的列表
# 将列表元素全部转为 小写
# 统计重复出现的技能以及次数


# 从这里开始独立实现。卡住 30 分钟后再看课程中的第一级提示。

rows = len(job_skill_lists)
cols = len(job_skill_lists[0])
collected_skills = []
unique_skills = []
count_skills = []

for i in range(rows):
    for j in range(cols):
        collected_skills.append(job_skill_lists[i][j].strip().lower())

print(collected_skills)

for k in range(len(collected_skills)):

    if collected_skills[k] not in unique_skills:
        unique_skills.append(collected_skills[k])

print(unique_skills)

for m in range(len(unique_skills)):
    for n in range(len(collected_skills)):
        if unique_skills[m] == collected_skills[n]:

