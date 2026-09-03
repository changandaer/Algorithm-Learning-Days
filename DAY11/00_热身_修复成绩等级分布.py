"""DAY11热身：修复成绩等级互斥判断，使用字典统计。"""

scores = [95, 64, 82, 60, 59, 101, 90, 82]

# 第一步：最小输入与预期输出：[95, 82, 60, 59, 101, 90, 82] -> A 2、B 2、C 1、D 1、Invalid 1
# 第二步：代码阶段：
# 第三步：需要保存的状态与小测试：


# 定义get_grade和count_grades，完成规定结果后停止扩展。
def get_grade(score):
    if score < 0 or score > 100:
        return "Invalid"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 60:
        return "C"
    else:
        return "D"

def count_grades(scores):
    score_level = {}
    for score in scores:
        grade = get_grade(score)
        score_level[grade] = score_level.get(grade, 0) + 1
    return score_level


score_level = count_grades(scores)
print(score_level)