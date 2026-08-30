"""DAY08 独立练习：把线性查找封装成函数。

找到返回真实索引，找不到返回 -1。
"""

# 函数合同
# 函数名：find_skill_index
# 输入：target_skill的字符串
# 输出：skill的索引数值
# 最小例子：python -> 0


# 从这里定义函数并编写四类断言。

def find_skill_index(target_skill):
    skills = ["python", "linux", "git", "pytorch", "c++", "docker"]
    normal_target_skill = target_skill.strip().lower()
    for index in range(len(skills)):
        if normal_target_skill == skills[index]:
            return index
    return -1

target_skill_index = find_skill_index("python")
print(target_skill_index)

assert find_skill_index("Linux") == 1
assert find_skill_index("Git ") == 2
assert find_skill_index("PyTorch") == 3
assert find_skill_index("java") == -1
