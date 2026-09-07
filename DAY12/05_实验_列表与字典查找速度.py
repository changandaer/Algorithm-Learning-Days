"""DAY12实验：观察列表包含与字典包含随数据规模增长的总体趋势。"""

import time


def measure_list_lookup(numbers, missing_number, repeat_count):
    start_time = time.perf_counter()

    for _ in range(repeat_count):
        # TODO：检查missing_number是否在numbers中。
        pass

    return time.perf_counter() - start_time


def measure_dict_lookup(number_index, missing_number, repeat_count):
    start_time = time.perf_counter()

    for _ in range(repeat_count):
        # TODO：检查missing_number是否在number_index中。
        pass

    return time.perf_counter() - start_time


for input_size in [1000, 5000, 10000]:
    numbers = list(range(input_size))
    number_index = {}

    # TODO：把numbers中的数字作为字典的键，索引作为值。

    missing_number = -1
    repeat_count = 1000

    list_seconds = measure_list_lookup(numbers, missing_number, repeat_count)
    dict_seconds = measure_dict_lookup(number_index, missing_number, repeat_count)

    print(input_size, list_seconds, dict_seconds)


# TODO：写出总体趋势，并说明为什么一次计时不能当成数学证明。

