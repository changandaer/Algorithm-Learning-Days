months = int(input("可实习月数："))
weekly_hours = int(input("周可实习时长："))
answer_python = input("是否会python(Y/N)：")

know_python = answer_python == "Y"
print(type(answer_python))
print(type(know_python))

is_eligible = months > 3 and weekly_hours > 40 and know_python

if is_eligible:
    print("基本满足申请资格")

else:
    if months < 3 or months == 3:
        print("不满足申请资格，实习月数不够")
    
    if weekly_hours < 40 or weekly_hours == 40:
        print("不满足申请资格，周实习时长不够")
    
    if not know_python:
        print("不满足申请资格，不会python")


