"""DAY08 独立练习：标准化字符串列表并按首次顺序去重。

空字符串清理后不加入结果。
"""

# 函数合同
# 函数名：normalize_and_deduplicate
# 输入：skills = ["Python", "Linux", "Git","python", "Linux", "git"]
# 输出：skills = ["python", "linux", "git"]
# 最小例子：


# 从这里定义函数并覆盖普通、大小写、空列表和空字符串测试。
def normalize_and_deduplicate(skills):
    normal_skills = []
    if skills == [] or skills == '':
        return "输入为空，重新输入"
    else:
        for skill in skills:
            if skill.strip().lower() not in normal_skills:
                normal_skills.append(skill.strip().lower())
        return normal_skills


normal_skills = normalize_and_deduplicate(["Python", "Linux", "Git","python", "Linux", "git"])
print(normal_skills)

assert normalize_and_deduplicate([]) == "输入为空，重新输入"
assert normalize_and_deduplicate('') == "输入为空，重新输入"

