"""DAY06 独立练习：合并两份技能清单，统一小写并保持首次出现顺序。

限制：不使用 set，不在遍历时删除原列表元素。
"""

first_skills = ["Python", "Linux", "Git"]
# second_skills = ["python", "PyTorch", "Docker", "git"]
second_skills = ["python", "Linux", "git"]

# 我的拆题
# 输入：容器为列表，元素为字符串
# 输出：合并之后的字符串
# 最小样例的手算过程：
# 必须记住的状态：是否存在新技能
# 重复动作与控制结构：
# 普通测试、边界测试、反例：
# 中文伪代码：


# 从这里开始独立实现。

is_has = False
lower_first_skills = []
lower_second_skills = []
len_first_skills = len(first_skills)
len_second_skills = len(second_skills)

for i in range(len(first_skills)):
    lower_first_skills.append(first_skills[i].lower())
for j in range(len(second_skills)):
    lower_second_skills.append(second_skills[j].lower() ) 

for index in range(len(lower_second_skills)):
    if lower_second_skills[index] in lower_first_skills:
        pass
    else:
        lower_first_skills.append(lower_second_skills[index])
        is_has = True

if is_has:
    print(f"去重前总项数是{len_first_skills+len_second_skills}项，去重之后的项数是{len(lower_first_skills)}，技能有{lower_first_skills}")
else:
    print(f"没有新加入的技能，依旧只有{lower_first_skills}这{len(lower_first_skills)}项技能")
        

