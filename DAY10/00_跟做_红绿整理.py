"""DAY10跟做：先运行看失败，再修复，最后整理代码。"""


def is_valid_score(score):
    """分数在0到100之间时返回True，否则返回False。"""
    return score > 0 and score < 100


# 第一步不要修改测试，先运行并观察失败。
assert is_valid_score(0) is True, "0分应当是合法边界"
assert is_valid_score(100) is True, "100分应当是合法边界"
assert is_valid_score(-1) is False
assert is_valid_score(101) is False

# 修复后记录：
# 红色失败证据：
# 绿色通过证据：
# 最后做了什么整理：

