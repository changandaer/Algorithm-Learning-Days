"""DAY08 挑战：返回训练损失第一次反弹的当前索引。

找到返回索引，没有反弹返回 -1。
"""

# 函数合同
# 函数名：find_first_rebound_index
# 输入：losses = [1.0, 1.0, 1.0, 0.8, 0.6, 0.7, 0.5]
# 输出：5
# 最小例子：


# 从这里定义函数，并测试反弹、下降、立即反弹、空列表和单元素。
def find_first_rebound_index(losses):
    if losses == [] or losses == '':
        return("损失为空，需要重新输入")
    else:
        for loss_index in range(len(losses)-1):
            if losses[loss_index+1] > losses[loss_index]:
                return loss_index+1
                print("判断return是否能让函数停止")
        return -1


losses = [1.0, 1.0, 1.1, 0.8, 0.6, 0.7, 0.5]

rebound_index = find_first_rebound_index(losses)
print(rebound_index)

assert find_first_rebound_index([1.0, 1.0, 0.8]) == -1
assert find_first_rebound_index([]) == "损失为空，需要重新输入"
assert find_first_rebound_index([1.0]) == -1