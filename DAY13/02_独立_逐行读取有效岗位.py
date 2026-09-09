"""DAY13任务2：要求见课程文档。请自己写三步分析，再从空白完成实现和测试。"""

with open("DAY13/岗位技能样例.txt","r",encoding="utf-8") as file:
    for file_line in file:
        clean_line = file_line.strip()
        print(clean_line)