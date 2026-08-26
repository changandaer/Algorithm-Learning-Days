"""DAY05 挑战：使用两层循环完成两数之和暴力搜索。

今天故意不使用字典。后续将对比更快的哈希表解法。
"""

numbers = [2, 7, 11, 15]
target = 26

is_find = False
finish_find = False 

while not finish_find:
    for i in range(len(numbers)):
        for j in range(len(numbers)):
        
            if int(numbers[i]) + int(numbers[j]) == target:
                a,b = i,j
                is_find = True
                finish_find = True  # 在第一次找到之后如何立刻结束寻找是我没有搞懂的地方，所以我只能想出来这个笨办法？
                break
    finish_find = True        

if is_find:
    print(f"找到了两个数满足两数之和等于{target}，分别是{numbers[a]}和{numbers[b]}")
else:
    print("没有符合条件的两个数")
