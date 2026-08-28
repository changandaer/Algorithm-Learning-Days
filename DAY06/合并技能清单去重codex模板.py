# 1.使用两个数据手算 first_skills = ["Python"] second_skills = ["python"]
# 2.把工作切成几个阶段
# 3.每个阶段程序必须要记住什么
# 直接分别遍历这两个列表 -> 遍历列表的每个元素
# 判断每个列表小写后的元素是否在合并列表中 -> 合并列表


first_skills = ["Python", "Linux", "Git"]
second_skills = ["python", "PyTorch", "Docker", "git"]
merged_skills = []

for first_element in first_skills:
    if first_element.lower() in merged_skills:
        pass
    else:
        merged_skills.append(first_element.lower())

for second_element in second_skills:
    if second_element.lower() in merged_skills:
        pass
    else:
        merged_skills.append(second_element.lower())

print(f"合并去重之后的技能清单共有{len(merged_skills)}项，分别是{merged_skills}")