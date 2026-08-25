"""DAY03选做挑战：根据整除规则判断闰年。"""

year = int(input("输入年份："))

if year % 400 == 0:
    is_leap_year = True
elif year % 100 == 0:
    is_leap_year = False
elif year % 4 == 0:
    is_leap_year = True
else:
    is_leap_year = False

if is_leap_year:
    print(f"{year}是闰年")
else:
    print(f"{year}不是闰年")