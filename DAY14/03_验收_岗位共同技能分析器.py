"""DAY14任务3：独立完成能更换文件与阈值的岗位分析器；要求见课程文档。"""

# {
#     "job_count": 3,
#     "skill_counts": {
#         "python": 2, "linux": 3, "git": 2, "c++": 1, "pytorch": 1
#     },
#     "common_skills": ["python", "linux", "git"]
# }

def load_job_skills(file_path):

    with open(file_path,"r",encoding="utf-8") as file:

        job_skills = []

        for file_line in file:

            normal_skills = []
            clean_line = file_line.strip()

            if clean_line != '':

                split_line = clean_line.split(',')

                for skill in split_line:
                    normal_skills.append(skill.strip().lower())

                job_skills.append(normal_skills)
    
    return job_skills


def analyze_jobs(job_skills, min_jobs):

    job_count = len(job_skills)
    skill_counts = {}
    common_skills = []

    for job in job_skills:
        for skill_index in range(len(job)):
            skill_counts[job[skill_index]] = skill_counts.get(job[skill_index],0) + 1

    for skill,count in skill_counts.items():
        if count >= min_jobs:
            common_skills.append(skill)

    return { 
        "job_count": job_count,
        "skill_counts": skill_counts,
        "common_skills": common_skills
        }

def run_report(file_path, min_jobs):

    job_skills = load_job_skills(file_path)

    analyze_results = analyze_jobs(job_skills,min_jobs)

    return analyze_results


analyze_results = run_report("DAY13/岗位技能样例.txt",3)
analyze_results_A = run_report("DAY14/岗位样例A_三条岗位.txt",2)
analyze_results_B = run_report("DAY14/岗位样例B_一条岗位.txt",1)
analyze_results_C = run_report("DAY14/岗位样例C_仅空白行.txt",1)

print(analyze_results)
print(analyze_results_A)
print(analyze_results_B)
print(analyze_results_C)
# skills = load_job_skills("DAY13/岗位技能样例.txt")
# print(skills)
# analyze_skills = analyze_jobs(skills,3)
# print(analyze_skills)

# skills_A = load_job_skills("DAY14/岗位样例A_三条岗位.txt")
# print(skills_A)
# analyze_skills_A = analyze_jobs(skills_A,2)
# print(analyze_skills_A)

# skills_B = load_job_skills("DAY14/岗位样例B_一条岗位.txt")
# print(skills_B)
# analyze_skills_B = analyze_jobs(skills_B,1)
# print(analyze_skills_B)

# skills_C = load_job_skills("DAY14/岗位样例C_仅空白行.txt")
# print(skills_C)
# analyze_skills_C = analyze_jobs(skills_C,1)
# print(analyze_skills_C)
