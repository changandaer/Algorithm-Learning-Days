"""DAY13任务1：要求见课程文档。请自己写三步分析，再从空白完成实现和测试。"""
# UTF-8 的全称是 8-bit Unicode Transformation Format（8位元统一码转换格式）。

# Unicode（统一码/万国码）：这是一个庞大的字符集标准，致力于收录世界上所有语言的文字和符号（包括中文、日文、阿拉伯文，甚至 Emoji 表情）。

# TF（Transformation Format/转换格式）：计算机底层只认识 0 和 1，TF 规定了如何将 Unicode 中的文字“翻译”成计算机能存储和传输的二进制数据。

# 8（8-bit/8位元）：意味着它处理数据的最小基础单位是 8 个比特（即 1 个字节）。


def read_text(file_path):

    with open(file_path,"r",encoding="utf-8") as file:
        content = file.read()
    return content

job_skills = read_text("DAY13/岗位技能样例.txt")
print(job_skills)