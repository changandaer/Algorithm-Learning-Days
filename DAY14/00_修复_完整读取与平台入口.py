"""DAY14任务0：要求见课程文档。请自己完成三步分析、函数和测试。"""

# 固定三步法：
# 第一步：最小输入与输出：
# Python,C++,Linux,Git
# Python,PyTorch,Linux,Git

# [
#     ["python", "c++", "linux", "git"],
#     ["python", "pytorch", "linux", "git"],
# ]

# 第二步：逐行遍历，独立解析一行，解析完一行就加入到外层空列表中

def load_job_skills(file_path):

    with open(file_path,"r",encoding="utf-8") as file:

        job_skills = []

        for line_file in file:

            clean_line = line_file.strip()
            split_line = clean_line.split(',')

            normal_skills = []

            for skill in split_line:
                normal_skill = skill.strip().lower()
                normal_skills.append(normal_skill)

            if normal_skills != ['']:

                job_skills.append(normal_skills)

    return job_skills   


skills = load_job_skills("DAY13/岗位技能样例.txt")
print(skills)

skills_A = load_job_skills("DAY14/岗位样例A_三条岗位.txt")
print(skills_A)

skills_B = load_job_skills("DAY14/岗位样例B_一条岗位.txt")
print(skills_B)

skills_C = load_job_skills("DAY14/岗位样例C_仅空白行.txt")
print(skills_C)

