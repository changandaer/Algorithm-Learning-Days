"""DAY05 独立练习：拆分、标准化并按首次出现顺序去重。

限制：今天不使用 set。
"""

# 测试 split() 函数的用法

# text = "python  linux      git"
# skills = text.split()
# print(skills)

# text = "python，    linux，git"
# skills = text.split()
# print(skills)

# text = "python,linux,git"
# skills = text.split()
# print(skills)

skills = input("输入你的技能：").strip().lower().split()
# skills = input("输入你的技能：").split().strip().lower()会报错
# 因为split()提前将字符串转换为了列表
# 在 Python 中 strip() 和 lower() 这两个方法基本上只能作用于字符串对象而不能是列表

deduplicate_skills = []
num = 0
for index in range(len(skills)):
    if skills[index] in deduplicate_skills: 
        print(f"{skills[index]}技能已经存在")
    else:
        deduplicate_skills.append(skills[index])
        num += 1

print(f"去重之后有{num}项技能，分别是{deduplicate_skills}")






