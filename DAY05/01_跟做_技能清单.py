"""DAY05 跟做练习：建立、更新并展示技能列表。

请按课程 Markdown 分三段手敲，随后关闭课程并从空白重写。
"""

# TODO 1：建立已有技能列表，读取并标准化一项新技能。

# TODO 2：分别处理空输入、重复技能和新技能。

# TODO 3：带编号输出所有技能，再输出技能总数。

# TODO 4：分别测试 Git、PYTHON 和三个空格。

skills = [ "python", "Linux" ]
new_skill = input("输入一项新技能：").strip().lower()

if new_skill == "":
    print("输入技能为空")
elif new_skill in skills:
    print("该技能已经存在")
else:
    skills.append(new_skill)

for index in range(len(skills)):

    print(f"第{index+1}项技能是{skills[index]}")

print(f"一共有{len(skills)}项技能")

# Git、PYTHON 和三个空格 都已经测试通过
# 但是由于lower()的存在，必须让 skills 列表中的技能都是小写字母。
