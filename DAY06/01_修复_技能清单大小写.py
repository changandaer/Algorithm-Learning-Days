"""DAY06 调试练习：复现并修复技能标准化不一致。

先输入 Linux 观察错误，再进行最小修改并补充回归测试记录。
"""

skills = ["python", "linux"]
new_skill = input("请输入一项新技能：").strip().lower()

if new_skill == "":
    print("输入技能为空")
elif new_skill in skills:
    print("该技能已经存在")
else:
    skills.append(new_skill)

print(skills)


# 根因（比较两边分别是什么值）：比较两边要求都是小写

# 最小修改：将Linux改为linux

# 回归测试记录（失败输入、修改内容、修改后的结果）：
# 修改前：
# chen@CHENdeMacBook-Air Algorithm-Learning-Days % python3 DAY06/01_修复_技能清单大小写.py
# 请输入一项新技能：linux
# ['python', 'Linux', 'linux']
# 修改后：
# chen@CHENdeMacBook-Air Algorithm-Learning-Days % python3 DAY06/01_修复_技能清单大小写.py
# 请输入一项新技能：linux
# 该技能已经存在
# ['python', 'linux']