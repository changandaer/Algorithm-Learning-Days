"""DAY05 小项目：岗位技能采集器 V1。

使用列表、循环、条件和字符串标准化收集岗位技能，
最后展示技能清单并找出尚未覆盖的共同核心技能。
"""

core_skills = ["python", "c++", "pytorch", "linux", "git"]

collected_skills = []
no_skills = []
num_skills = 0

is_end = True

while is_end:

    skill = input("请输入你的技能：").strip().lower()

    if skill == '':
        print("输入为空，请重新输入")
    elif skill in collected_skills:
        print("该技能已存在，请重新输入")
    elif skill == '结束':
        is_end = False
    else:
        collected_skills.append(skill)
        num_skills += 1
        print(f"这是第{num_skills}项技能")

for index in range(len(core_skills)):
    if core_skills[index] in collected_skills:
        pass
    else:
        no_skills.append(core_skills[index])

for index in range(len(collected_skills)):
    print(f"这是第{index+1}项技能{collected_skills[index]}")

print(f"目前你一共有{num_skills}项技能，但是还没有收集到{no_skills}这些核心技能")



