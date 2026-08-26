"""DAY04 独立练习：输出 1～30 的 FizzBuzz。

15 和 30 必须输出 FizzBuzz，而不是 Fizz 或 Buzz。
"""


for i in range(1, 31):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")




