"""DAY09修复：没有反弹时始终返回-1，并删除return后的不可达代码。"""

# 函数合同
# 函数名：find_first_rebound_index
# 参数：losses列表
# 返回值及类型：索引整数
# 最小例子：[1.0, 0.8, 0.6, 0.7] -> 3


# 定义函数并覆盖反弹、下降、立即反弹、空列表和单元素。
def find_first_rebound_index(losses):
    for index in range(len(losses)-1):
        if losses[index+1] > losses[index]:
            return index+1
    return -1

assert find_first_rebound_index([1.0, 0.8, 0.6, 0.7]) == 3
assert find_first_rebound_index([1.0, 0.8, 0.6]) == -1
assert find_first_rebound_index([1.0, 1.1]) == 1
assert find_first_rebound_index([]) == -1
assert find_first_rebound_index([1.0]) == -1