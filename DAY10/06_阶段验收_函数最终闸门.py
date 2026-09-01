"""DAY10函数最终闭卷闸门，限时45分钟，关闭DAY08～10与AI。

只补全两个函数，不得修改预置测试。到时保留真实现场。
"""


def find_skill_index(skills, target_skill):
    # 在这里独立实现：返回原始索引或-1。
    pass


def find_two_sum(numbers, target):
    # 在这里独立实现：返回第一组索引或[]。
    pass


# 测试一：技能查找
assert find_skill_index(["Python", "python", "Git"], "git") == 2
assert find_skill_index(["python", "python"], "java") == -1
assert find_skill_index([], "python") == -1

# 测试二：两数之和
assert find_two_sum([1, 4, 2, 3], 5) == [0, 1]
assert find_two_sum([3, 3], 6) == [0, 1]
assert find_two_sum([2, 7], 100) == []
assert find_two_sum([], 9) == []

