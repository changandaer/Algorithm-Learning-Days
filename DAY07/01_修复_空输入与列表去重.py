"""DAY07 修复练习：空行直接得到空列表；非空技能标准化并去重。

限制：不使用 set，不对空输入进行第二次询问。
"""

# 最小样例：python linux git
# 处理阶段：
# 判断输入是否合法
#   输入为空，直接输出空列表
#   输入不为空，进行标准化并去重
# 必须记住的状态：输入标准化后的列表，去重元素，去重列表


# 从这里开始实现，并输出结果列表和数量。


job_skills = input("输入你的技能，用空格隔开：").strip().lower().split()
# print(job_skills)

unique_skills = []
if job_skills == []:
    print("输入为空，数量为0")
else:
    for unique_skill in job_skills:
        if unique_skill in unique_skills:
            pass
        else:
            unique_skills.append(unique_skill)

print(f"{unique_skills}")