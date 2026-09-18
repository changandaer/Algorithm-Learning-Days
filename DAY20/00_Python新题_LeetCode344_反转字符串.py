"""DAY20新题：反转字符串，原地修改字符列表；要求见课程，自己写三步分析、实现和测试。"""

def rebind(items):
    items = ["new"]


def replace_first(items):
    items[0] = "new"


values = ["old", "keep"]
# rebind(values)
values = ["new"]
assert values == ["old", "keep"]
replace_first(values)
assert values == ["new", "keep"]

