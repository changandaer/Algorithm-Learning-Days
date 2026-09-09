"""DAY13任务5：要求见课程文档。请自己写三步分析，再从空白完成实现和测试。"""


#1.输入：岗位技能样例.txt  
#  输出：job_count：岗位数量
#       skill_counts：每个技能出现在多少条岗位中
#       common_skills：至少出现在3条岗位中的技能，按首次出现顺序

#2.阶段：读取解析：逐行读取、每行进行清洗、清洗后进行归一化处理加入空字典
#       统计分析：从空字典中读取数据进行分析

def Data_Parsing(file_path):

    with open(file_path,"r",encoding="utf-8") as file:

        job_skills = []

        for line_file in file:
            clean_line = line_file.strip()

            if clean_line != '':
                normal_skills = []
                split_file = clean_line.split(',')

                for skill in split_file:
                    normal_skill = skill.strip().lower()
                    normal_skills.append(normal_skill)
                
                job_skills.append(normal_skills)
        
    return job_skills



def Statistical_Analysis(job_skills_data):

    # job_count：岗位数量
    # skill_counts：每个技能出现在多少条岗位中
    # common_skills：至少出现在3条岗位中的技能，按首次出现顺序

    job_count = len(job_skills_data)
    skill_counts = {}
    common_skills = []

    for each_job_skills in job_skills_data:
        
        for each_job_skill in each_job_skills:

            skill_counts[each_job_skill] = skill_counts.get(each_job_skill,0) + 1

    for skill,count in skill_counts.items():

        if count >= 3:
            common_skills.append(skill)

    return {
        "job_count":job_count,
        "skill_counts":skill_counts,
        "common_skills":common_skills,
    }

# === 主程序运行区 ===
# 外界（主程序）负责调度：先让A干活，把A的产出交给B
file_path_to_read = "DAY13/岗位技能样例.txt"
parsed_data = Data_Parsing(file_path_to_read)         # 第一步：拿到返回值
analysised_data = Statistical_Analysis(parsed_data)   # 第二步：把返回值传给统计函数

print(analysised_data)