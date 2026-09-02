"""DAY10跟做：使用字典统计技能次数。"""

skills = ["python", "git", "python", "linux", "git", "python"]

# 第一步：最小输入与预期输出：skills = ["python", "git", "python"]  -> python2 git1
# 第二步：代码阶段：
# 建立空统计表
# 逐项读取技能
# 更新对应次数
# 输出统计表
# 第三步：需要保存的状态与小测试：


# 先手敲“判断键是否存在”的写法。

skills = ["python", "git", "python", "linux", "git", "python"]
skill_counts = {}
# for skill in skills:
#     if skill in skill_counts:
#         skill_counts[skill] += 1
#     else:
#         skill_counts[skill] = 1

# for skill,count in skill_counts.items():
#     print(f"{skill}:{count}",end=',')

# 再清空结果，使用get()写法重写。

for skill in skills:
    skill_counts[skill] = skill_counts.get(skill,0) + 1
print(skill_counts)
for skill,count in skill_counts.items():
    print(f"{skill}:{count}",end=',')
print()