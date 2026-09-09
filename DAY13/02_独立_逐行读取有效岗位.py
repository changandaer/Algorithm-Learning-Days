"""DAY13任务2：要求见课程文档。请自己写三步分析，再从空白完成实现和测试。"""


def load_job_lines(file_path):

    with open(file_path,"r",encoding="utf-8") as file:
        job_skills = []
        for file_line in file:
            clean_line = file_line.strip()
            if clean_line != '':
                job_skills.append(clean_line)
    return job_skills
    
job_skills = load_job_lines("DAY13/岗位技能样例.txt")
print(job_skills)
            