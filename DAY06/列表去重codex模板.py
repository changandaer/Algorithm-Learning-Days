# 首先是按照 3 步
# 1.拿两个小数据手算 输入 python Linux
# 2.把工作分为几个阶段
# 3.每个阶段程序必须记住什么 
#   首先是将输入的带空格的字符串全部小写后放在一个空列表中 -> 记住这个放了输入的列表
#   其次是遍历这个列表的元素判断是否已经在去重之后的列表中 -> 记住放了输入的列表每次遍历的元素，去重之后的列表

user_skills = input("请输入你的技能，用空格间隔：").strip().lower().split()
unique_skills = []

for skills in user_skills:
    if skills in unique_skills:
        pass
    else:
        unique_skills.append(skills)
    
print(f"去重之后的技能有{len(unique_skills)}项，分别是：{unique_skills}")