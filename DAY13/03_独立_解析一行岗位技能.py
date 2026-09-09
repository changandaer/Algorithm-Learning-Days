"""DAY13任务3：要求见课程文档。请自己写三步分析，再从空白完成实现和测试。"""



def parse_skill_line(line):

    normal_skills = []

    job_skills = line.split(',')

    for job_skill in job_skills:
        normal_skill = job_skill.strip().lower()

        normal_skills.append(normal_skill)

    return normal_skills


normal_skills = parse_skill_line(" Python, C++, Linux, Git ")
print(normal_skills)


assert parse_skill_line("PYTHON") == ["python"]