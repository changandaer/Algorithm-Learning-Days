"""DAY12独立：记录两数之和两种算法的主要检查次数。"""


def two_sum_brute_force_with_count(nums, target):
    """返回字典：{"indices": 两个索引或空列表, "checks": 加法比较次数}。"""
    check_count = 0

    # TODO：完成暴力法；每比较一对数字前，把check_count加1。
    for first_index in range(len(nums)):
        for second_index in range(first_index+1,len(nums)):
            check_count += 1
            if nums[first_index] + nums[second_index] == target:
                return {"indices": [first_index,second_index],"checks": check_count}
            

    return {"indices": [], "checks": check_count}


def two_sum_hash_with_count(nums, target):
    """返回字典：{"indices": 两个索引或空列表, "checks": 字典包含检查次数}。"""
    seen = {}
    check_count = 0

    # TODO：完成哈希法；每执行一次“needed是否在seen”前，把check_count加1。
    for index in range(len(nums)):
        needed = target - nums[index]
        check_count += 1
        if needed in seen:
            return {"indices": [seen[needed],index], "checks": check_count}
        seen[nums[index]] = index

    return {"indices": [], "checks": check_count}


# 让答案位于最后两个位置，观察接近最坏情况的检查次数。
for input_size in [20, 100, 500]:
    numbers = list(range(input_size))
    target_value = numbers[-2] + numbers[-1]

    # TODO：分别调用两个函数并打印input_size、indices和checks。
    two_sum_brute_force = two_sum_brute_force_with_count(numbers,target_value)
    two_sum_hash = two_sum_hash_with_count(numbers,target_value)

    print(f"数据量 n={input_size}:")
    print(f"  暴力法 -> 索引: {two_sum_brute_force['indices']}, 检查次数: {two_sum_brute_force['checks']}")
    print(f"  哈希法 -> 索引: {two_sum_hash['indices']}, 检查次数: {two_sum_hash['checks']}")
    print("-" * 40)



# TODO：写出n从100变成500时，两种检查次数的大致变化。

