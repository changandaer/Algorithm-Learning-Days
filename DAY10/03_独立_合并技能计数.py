"""DAY10独立练习：合并两个技能计数字典，不修改原字典。"""

first_counts = {"python": 2, "git": 1}
second_counts = {"python": 1, "linux": 3}

# 第一步：最小输入与预期输出：{"python": 2, "git": 1} + {"python": 1, "linux": 3} -> {"python": 3, "git": 1,"linux": 3}
# 第二步：代码阶段：
# 创立新字典
# 遍历两个小字典，将小字典内容逐个加入新字典中
# 第三步：需要保存的状态与小测试：


# 建立新字典并完成合并。
merge_counts = first_counts

for skill in second_counts:
        merge_counts[skill] = merge_counts.get(skill, 0) + second_counts[skill]
print(merge_counts)
        
     
