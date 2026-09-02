"""DAY10挑战：使用字典保存以前出现的数字与索引。"""

numbers = [2, 7, 11, 15]
target = 9

# 第一步：最小输入与预期输出：[2, 7, 11, 15] 9 ->[0, 1]
# 第二步：代码阶段：
# 第三步：需要保存的状态与小测试：


# 函数合同：find_two_sum_with_hash(numbers, target) -> list
def find_two_sum_with_hash(numbers, target):
    seen = {}
    for index in range(len(numbers)): 
        needed = target - numbers[]
        # 我不理解这句话怎么转为代码：如果needed已经是seen的键，返回旧索引和当前索引


# 卡住时只看课程中的一级提示。挑战题不作为当天通过硬门槛。

