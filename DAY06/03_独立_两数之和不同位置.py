"""DAY06 独立修复：寻找和为目标值的两个不同索引。

要求输出索引和数值；每种位置组合最多检查一次；找到后停止两层循环。
"""

numbers = [2, 7, 11, 15]
target = 100

# 我的拆题
# 输入：容器为列表，元素为正整数
# 输出：索引、数值
# 最小样例的手算过程：numbers = [2, 2]，index=0
# 必须记住的状态：是否存在这两个数，存在的话在那个位置数值是多少
# 重复动作与控制结构：
# 普通测试、边界测试、反例：
# 中文伪代码：
# 双重循环遍历列表
#   判断是否有两个数相加等于目标值
#   如果有跳出循环
#   如果没有输出没有

# 从这里开始独立实现。不要照抄课程中的示范答案。

is_equal = False

for i in range(len(numbers)):
    for j in range(1,len(numbers)):
        if numbers[i] + numbers[j] == target:
            is_equal = True
            break
        else:
            pass
    if is_equal:
        break
if is_equal:
    print(f"第{i+1}个数字与第{j+1}个数字之和等于目标数字{target}")
else:
    print(f"没找到两个数字之和等于目标数字{target}")
        