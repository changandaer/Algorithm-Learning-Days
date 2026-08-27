"""DAY06 闭卷复习：读取一行技能，标准化并按首次出现顺序去重。

限制：不使用 set。编码前先填写下面的拆题纸。
"""

# 我的拆题
# 输入：一行用空格隔开的字符串
# 输出：去重小写之后的字符串
# 最小样例的手算过程：Python Linux python -> python、linux 
# 必须记住的状态：已存在技能列表，输入数据是否有效
# 重复动作与控制结构：用输入的每个元素与已存在的进行比较
# 普通测试、边界测试、反例：
# 中文伪代码：
# 输入字符串去重小写并放到列表储存
# 判读输入是否是空字符串
#   如果是空就让用户重新输入
#   如果不是空就进行遍历
#       判断是否已经存在于技能列表，如果是新的技能加入技能列表，如果是已存在技能就跳过 


skills = input("输入你的技能：").strip().lower()
list_skills = skills.split()

# print(f"输入的技能是{skills}，容器类型是{type(skills)}")
# print(f"输入的技能是{list_skills}，容器类型是{type(list_skills)}")

# 把输入的字符串放到列表中是因为方便增删查改的操作吗
collected_skills = []

if skills == '':
    is_None = True
else:
    is_None = False

while is_None:
    skills = input("重新输入你的技能：").strip().lower()
    if skills == '':
        is_None = True
    else:
        is_None = False
        list_skills = skills.split()

for index in range(len(list_skills)):
    if list_skills[index] in collected_skills:
        pass
    else:
        collected_skills.append(list_skills[index])
    
print(f"去重之后的技能是{collected_skills}")

