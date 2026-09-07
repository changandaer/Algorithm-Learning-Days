"""DAY12跟做：不用猜速度，亲手统计单层与双层循环的执行次数。"""


def count_one_loop(n):
    """返回循环体执行次数，应当等于n。"""
    operation_count = 0

    # TODO：写一个执行n次的循环，每次把operation_count加1。
    for i in range(n):
        operation_count += 1

    return operation_count


def count_two_nested_loops(n):
    """返回两层循环内部执行次数，应当等于n*n。"""
    operation_count = 0

    # TODO：写两层都执行n次的循环，在最内层把operation_count加1。
    for i in range(n):
        for j in range(n):
            operation_count += 1

    return operation_count


for input_size in [10, 100, 1000]:
    one_loop_count = count_one_loop(input_size)
    two_loop_count = count_two_nested_loops(input_size)
    print(input_size, one_loop_count, two_loop_count)


# TODO：在下方写出观察结果：n扩大10倍时，两种次数分别扩大多少倍？

