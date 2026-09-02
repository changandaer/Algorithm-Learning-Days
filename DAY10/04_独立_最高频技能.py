"""DAY10独立练习：不使用max()，找出字典中出现次数最高的技能。"""

# 第一步：最小输入与预期输出：{"python": 2, "git": 1} -> python
# 第二步：代码阶段：
# 第三步：需要保存的状态与小测试：


# 函数合同：find_most_common_skill(skill_counts) -> str
def find_most_common_skill(skill_counts):
    frequently_skill_counts = 0
    if skill_counts == {}:
        return ''
    else:
        for skill in skill_counts:
            if skill_counts[skill] > frequently_skill_counts:
                frequently_skill = skill
                frequently_skill_counts = skill_counts[skill]
        return frequently_skill

frequently_skill = find_most_common_skill({'python': 3, 'git': 1, 'linux': 4})
print(frequently_skill)
# 测试普通、并列和空字典。

assert find_most_common_skill({}) == ''
assert find_most_common_skill({'python': 3, 'git': 4, 'linux': 4}) == 'git'