"""DAY10独立练习：使用函数和字典统计成绩等级分布。"""

scores = [95, 82, 60, 59, 101, 90, 82]

# 第一步：最小输入与预期输出：
# 第二步：代码阶段：
# 第三步：需要保存的状态与小测试：


# 定义get_grade，再统计每个返回等级出现的次数。
def get_grade(scores):
    score_level = {}
    for score in scores:
        if score < 0 or score > 100:
            pass
        else:
            if score >= 90:
                score_level["A"] = score_level.get("A",0) + 1
            if score >= 80:
                score_level["B"] = score_level.get("B",0) + 1
            if score >= 60:
                score_level["C"] = score_level.get("C",0) + 1
            else:
                score_level["D"] = score_level.get("D",0) + 1
    return score_level

score_level = get_grade(scores)
print(score_level)


