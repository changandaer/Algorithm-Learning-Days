"""DAY13任务4：要求见课程文档。请自己写三步分析，再从空白完成实现和测试。"""

# 固定三步法：
# 第一步：最小输入与输出：
# Python,C++,Linux,Git
# Python,PyTorch,Linux,Git

# [
#     ["python", "c++", "linux", "git"],
#     ["python", "pytorch", "linux", "git"],
# ]

# 第二步：逐行遍历，独立解析一行，解析完一行就加入到外层空列表中

# 第三步：


def load_job_skills(file_path):


    with open(file_path,"r",encoding="utf-8") as file:

        file_skills = []

        for line_file in file:

            clean_line = line_file.strip()
            # 使用 with open(...) 并通过 for line_file in file: 逐行遍历时，Python 会原封不动地保留文件里的原始格式。
            # 在文本文件中，换行的本质就是一个看不见的换行符（\n）。
            # 因此，除了文件的最后一行（如果没有敲回车的话），读取出来的每一行末尾都会自带一个 \n。
            # 所以在处理读取到的文本时，第一步永远是顺手写一个 .strip()，用来把这些隐藏的换行符和首尾空格剥离掉。

            if clean_line != '' :

                split_file = clean_line.split(",")
                normal_skills = []

                for skill in split_file:

                    normal_skill = skill.strip().lower()
                    normal_skills.append(normal_skill)

                file_skills.append(normal_skills)
                if len(file_skills) == 2:
                    return file_skills
    

line_file = load_job_skills("DAY13/岗位技能样例.txt")
print(line_file)