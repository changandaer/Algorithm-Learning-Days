"""DAY03跟做任务。

请根据课程Markdown中的代码块逐行手敲，不要复制粘贴。
完成后删除下面的TODO注释也可以。
"""

# TODO 1：接收可实习月数、每周小时数和是否学过Python。
month = int(input("可实习月数："))
hour = int(input("每周可实习小时数："))
know_python = input("是否学过python：")

# TODO 2：把Y/N回答转换成布尔值。
if month > 3:
    month = True
else:
    month = False

if hour > 40:
    hour = True
else:
    hour = False

if know_python == "是":
    know_python = True
elif know_python == "否":
    know_python = False
else:
    know_python = False
    print("请重新回答是否学过python")

# TODO 3：使用and得到是否满足申请条件。
# TODO 4：输出结果；不满足时分别输出所有真实原因。
if month and hour and know_python:
    print("满足申请条件")
else:
    print("不满足申请条件")

    if not month:
        print("实习月数不满足")
    if not hour:
        print("每周可实习小时数不满足")
    if not know_python:
        print("不会python")



