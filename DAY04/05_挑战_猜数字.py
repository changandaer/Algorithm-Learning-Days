"""DAY04 挑战练习：猜固定数字并统计尝试次数。

测试输入：20、50、37。最后应显示共尝试 3 次。
"""

secret_number = 37

guess_num = int(input("请猜测固定数字是多少："))
num_guesses = 1


while guess_num != secret_number:

    if guess_num > secret_number:
        guess_num = int(input("太大，继续猜测固定数字是多少："))
        num_guesses += 1
    else:
        guess_num = int(input("太小，继续猜测固定数字是多少："))
        num_guesses += 1

print(f"猜中了，共尝试{num_guesses}次")
