# DAY08：函数——把一段代码做成可以反复使用和测试的工具

> 预计用时：3.5～4 小时。今天只学习一个知识组：函数。不会同时加入字典、类、继承或深度学习。

## 一、DAY07 验收结果：85 分

| 评分项目 | 得分 | 说明 |
|---|---:|---|
| 概念理解 | 21 / 25 | 已正确理解哨兵值、标准化和计数器重置；对“怎样证明输出满足需求”和回归测试理解仍不完整。 |
| 代码正确性 | 26 / 30 | 去重、计数、共同技能与关键两数之和反例通过；部分输出字段遗漏；周测没有停止外层循环；空列表隐藏测试会越界。 |
| 独立分析与调试 | 19 / 20 | 成功把未完成项目拆成三阶段并独立完成，进步明显。 |
| 测试、边界与需求验收 | 10 / 15 | 关键反例通过；测试记录不完整，未覆盖空列表、多解和岗位内部重复技能。 |
| Git 与表达 | 9 / 10 | 提交过程清楚，课程总结有价值；检查时本地 `main` 比 `origin/main` 多一个总结提交，尚未推送。 |
| **总分** | **85 / 100** | **达到解锁条件，进入函数。** |

### DAY07 的关键进步

- 你已经知道 `found_index = -1` 是“没找到”的标记，而 `skills[-1]` 才是访问最后一项。
- 两数之和把内层起点修成 `first_index + 1`，目标 14 正确地找不到，`[3, 3]` 目标 6 也能找到两个不同索引。
- 你把原来卡住的岗位共同技能项目拆成“摊平—去重—计数”，并得到正确规定结果。
- 闭卷小测的核心算法由你独立写出，没有为了好看而事后伪装。

---

## 二、DAY07 全部代码示范答案与逐题评语

### 示范 1：用哨兵值完成线性查找

```python
skills = ["python", "linux", "git"]
target_skill = "docker"
found_index = -1

for index in range(len(skills)):
    if skills[index] == target_skill:
        found_index = index
        break

if found_index == -1:
    print(f"没有找到 {target_skill}")
else:
    print(f"找到 {target_skill}，索引是 {found_index}")
```

对比你的代码：

- `linux` 和 `docker` 都能给出正确结果，理论总结也正确。
- 你同时维护 `is_found` 和 `found_index`，其实一个 `found_index` 已经能表达两件事：-1 表示没找到，其他值表示找到的位置。状态越少越不容易不一致。
- `is_found` 初始为 `True` 不符合“还没开始查找”的事实。更自然的初值应为 `False`。
- 找到后应输出 `found_index`，不应依赖循环变量 `index`。
- 隐藏空列表测试会在前面的 `skills[-1]` 处越界。那两行只是概念实验，实际查找程序不需要访问最后一个元素。

### 示范 2：空输入与列表去重

```python
raw_skills = input("请输入技能，用空格分隔：").lower().split()
unique_skills = []

for skill in raw_skills:
    if skill not in unique_skills:
        unique_skills.append(skill)

print(f"去重结果：{unique_skills}")
print(f"技能数量：{len(unique_skills)}")
```

对比你的代码：

- 普通输入、空行和全部重复测试均通过。
- `split()` 会让空行直接变成 `[]`，所以不需要专门的 `if/else`；对空列表执行 `for` 会自然循环零次。
- 你只在空输入分支输出数量 0，普通输入没有输出数量。需求要求所有情况都输出结果和数量。
- `if ...: pass else: append` 可以写成 `if skill not in unique_skills: append`。

### 示范 3：两数之和索引范围

```python
numbers = [2, 7, 11, 15]
target = 26
found = False

for first_index in range(len(numbers)):
    for second_index in range(first_index + 1, len(numbers)):
        if numbers[first_index] + numbers[second_index] == target:
            found = True
            break

    if found:
        break

if found:
    print(f"第一个索引：{first_index}，数值：{numbers[first_index]}")
    print(f"第二个索引：{second_index}，数值：{numbers[second_index]}")
    print(f"目标值：{target}")
else:
    print("没有符合条件的两个数")
```

对比你的代码：

- 内层范围已正确修复，四个关键测试的查找结果全部正确。
- 题目要求“输出索引和数值”，你的程序只输出了索引。
- 你的理论回答“更换不同目标值成功输出就算完成”不能证明输出字段齐全。正确测试应明确写出：输入 `[2,7]` 和 9，预期同时看见索引 0、1以及数值 2、7。
- 空格规范：`first_index + 1`，而不是 `first_index+1`。

### 示范 4：统计单个技能

```python
all_skills = [
    "python", "linux", "git", "pytorch",
    "python", "c++", "linux", "git",
    "python", "pytorch", "linux", "docker",
]
target_skill = "python"
current_count = 0

for skill in all_skills:
    if skill == target_skill:
        current_count += 1

print(f"{target_skill} 出现了 {current_count} 次")
```

你的实现与示范逻辑一致，结果正确。`count` 可以使用；`current_count` 更能说明这是当前目标的计数器。

### 示范 5：统计多种技能

```python
all_skills = [
    "python", "linux", "git", "pytorch",
    "python", "c++", "linux", "git",
    "python", "pytorch", "linux", "docker",
]
unique_skills = ["python", "linux", "git", "pytorch", "c++", "docker"]
skill_counts = []

for target_skill in unique_skills:
    current_count = 0

    for skill in all_skills:
        if skill == target_skill:
            current_count += 1

    skill_counts.append(current_count)

for index in range(len(unique_skills)):
    print(f"{unique_skills[index]}：{skill_counts[index]} 次")
```

对比你的代码：

- 结果 `[3, 3, 2, 2, 1, 1]` 正确。
- 你正确发现每次外层循环结束后必须清零计数器。
- 示范把 `current_count = 0` 放在外层循环开头。这样代码结构直接表达“每换一种目标，开始新的计数”，不需要在末尾记得清零。
- 题目要求逐项输出技能和次数，你只打印了次数列表。

### 示范 6：岗位共同技能统计器

```python
job_skill_lists = [
    ["Python", "Linux", "Git", "PyTorch"],
    ["python", "C++", "linux", "git"],
    ["PYTHON", "PyTorch", "Linux", "Docker"],
]

normalized_job_lists = []

for raw_job_skills in job_skill_lists:
    normalized_job_skills = []

    for raw_skill in raw_job_skills:
        skill = raw_skill.lower()
        if skill not in normalized_job_skills:
            normalized_job_skills.append(skill)

    normalized_job_lists.append(normalized_job_skills)

unique_skills = []

for job_skills in normalized_job_lists:
    for skill in job_skills:
        if skill not in unique_skills:
            unique_skills.append(skill)

skill_job_counts = []

for target_skill in unique_skills:
    job_count = 0

    for job_skills in normalized_job_lists:
        if target_skill in job_skills:
            job_count += 1

    skill_job_counts.append(job_count)

common_skills = []

for index in range(len(unique_skills)):
    print(f"{unique_skills[index]}：出现在 {skill_job_counts[index]} 个岗位")

    if skill_job_counts[index] == len(job_skill_lists):
        common_skills.append(unique_skills[index])

print(f"所有岗位共同技能：{common_skills}")
```

对比你的代码：

- 规定数据结果完全正确：python 3、linux 3、git 2、pytorch 2、c++ 1、docker 1。
- 你终于完成了 DAY06 卡住的阶段，说明“先做一个计数，再扩展到多个计数”有效。
- 隐藏数据中，如果第一个岗位写了三次 Python，另外两个岗位没有 Python，你会因为总次数等于 3 而误判 Python 是所有岗位共同技能。
- 工作中的指标必须先定义清楚。这里真正想测的是“出现过该技能的岗位数量”，不是原始文本出现总次数。因此示范先对每个岗位内部去重，再按岗位计数。

### 示范 7：第一周闭卷小测

```python
raw_skills = ["Python", "Linux", "python", "Git", "git"]
unique_skills = []

for raw_skill in raw_skills:
    skill = raw_skill.lower()
    if skill not in unique_skills:
        unique_skills.append(skill)

print(unique_skills)

numbers = [4, 1, 6, 3]
target = 9
found = False

for first_index in range(len(numbers)):
    for second_index in range(first_index + 1, len(numbers)):
        if numbers[first_index] + numbers[second_index] == target:
            found = True
            break

    if found:
        break

if found:
    print(first_index, numbers[first_index])
    print(second_index, numbers[second_index])
else:
    print("没有找到")
```

对比你的闭卷结果：

- 去重完全正确。
- 两数之和能找到规定答案，说明核心嵌套范围已经能闭卷写出。
- 内层 `break` 后外层继续运行；隐藏多解 `[1,2,3,4]` 目标 5 会输出两组答案。
- 没有输出两个数值，也没有处理找不到的情况。
- 三行拆题卡为空，说明时间压力下你仍会直接编码。这不是判失败，但下一步要利用函数的“输入—输出合同”帮助拆解。

---

## 三、什么是回归测试？

**回归测试（regression test）**的专业含义是：修复一个错误以后，把当时能触发错误的输入保存下来；以后每次修改都重新运行，防止旧错误悄悄回来。

人话解释：车修好以后，把当时出故障的那段路再开一遍；以后每次保养完也走这段路，确保老毛病没有复发。

它与项目大小无关。DAY06 的 `Linux` 大小写错误已经是一个真实回归测试案例：

```text
旧错误输入：Linux
旧错误结果：列表同时出现 Linux 和 linux
修复后预期：提示已存在，只保留 linux
```

小鹏评估开发岗位强调维护高价值回归测试集，你现在写的这些小反例，正是在练同一种基础思维。

---

## 四、要不要先学完面向对象才能刷 Hot 100？

不需要。

你提到的对象、成员方法、构造方法、封装、继承、重写和多态都属于**面向对象编程（Object-Oriented Programming，OOP）**。它们对工程项目和 C++ 很重要，但不是开始数组、哈希和双指针算法的前置条件。

Hot 100 当前真正需要的是：

- 变量、条件、循环。
- 列表和字符串。
- 函数的参数与返回值。
- 字典/哈希表。
- 后续按题型学习栈、队列、链表和树。

LeetCode 会提供类似下面的外壳：

```python
class Solution:
    def twoSum(self, nums, target):
        # 你主要完成这里
```

DAY10 会先用人话解释：`Solution` 是一个工具箱，`twoSum` 是工具箱里的工具，`self` 暂时理解成“这个工具箱自己”。不要求先学完整继承和多态才能写方法内部算法。

Python 工程知识不会跳过，顺序是：

| 课次 | 内容 |
|---|---|
| DAY08 | 函数、参数、返回值、局部变量、简单自动测试 |
| DAY09 | 字典/哈希表 |
| DAY10 | 第一题正式 Hot 100，两数之和 |
| DAY11～12 | 文件、异常、模块和项目结构 |
| DAY13 | 类、对象、构造方法、成员方法与基本封装 |
| DAY14 | 第一阶段验收和项目整理 |
| C++阶段 | 类、构造/析构、引用、指针、RAII；再对比继承与多态 |

魔术方法、复杂继承体系不会为了“学高级”一次性讲完，而是在项目确实需要时选学。

---

## 五、函数到底是什么？

### 1. 函数是有名字的小机器

**函数（function）**是一段完成明确任务、可以反复调用的代码。

```python
def add(first_number, second_number):
    result = first_number + second_number
    return result
```

人话解释：我们造了一台名叫 `add` 的加法机器。它有两个投入口，把两个数字放进去，会从出口送出相加结果。

### 2. `def`、参数和调用

```python
def greet(name):
    return f"你好，{name}"

message = greet("小陈")
print(message)
```

- `def`：告诉 Python“现在定义一台新机器”。
- `name`：**参数（parameter）**，机器设计图上预留的输入位置。
- `"小陈"`：**实参（argument）**，实际调用时放进去的值。
- `greet("小陈")`：调用函数，让机器真正运行。

初学阶段不用纠结参数和实参的中文差异。记住：定义时写的是输入插槽，调用时传的是实际数据。

### 3. `return` 与 `print()` 完全不同

```python
def add_and_print(a, b):
    print(a + b)

def add_and_return(a, b):
    return a + b
```

`print()` 是把结果显示给人看；`return` 是把结果交还给调用函数的其他代码。

```python
first_result = add_and_print(2, 3)   # 屏幕显示5，但 first_result 是 None
second_result = add_and_return(2, 3) # second_result 真正保存5
```

**None** 表示“没有返回一个实际结果”。人话就是机器响了一声告诉你答案，却没有把成品放到出口。

LeetCode 会检查函数返回值，所以只 `print()` 而不 `return` 通常无法通过。

### 4. 函数遇到 `return` 就结束

```python
def find_skill_index(skills, target_skill):
    for index in range(len(skills)):
        if skills[index] == target_skill:
            return index

    return -1
```

找到后执行 `return index`，函数立即结束，因此不再需要 `found` 和两层 `break`。走完整个循环还没找到，才执行最后的 `return -1`。

### 5. 局部变量

**局部变量（local variable）**是在函数内部建立、主要由这次函数调用使用的变量。

```python
def count_skill(skills, target_skill):
    current_count = 0
    for skill in skills:
        if skill == target_skill:
            current_count += 1
    return current_count
```

每次调用都会建立新的 `current_count = 0`，所以不会把上次统计结果错误带到下一次。这正好解决 DAY07 手动清零计数器的问题。

### 6. 函数合同

工作代码和算法题都应先说明函数合同：

```text
函数名：find_skill_index
输入：技能列表、目标技能
输出：找到时返回索引，找不到返回 -1
例子：(["python", "git"], "git") -> 1
```

这比长篇拆题更适合你：先确定小机器吃什么、吐什么，再在机器内部边写边用小数据测试。

### 7. 使用 `assert` 做最小自动测试

**断言（assertion）**就是让程序自动核对“实际结果是否等于预期结果”。

```python
assert add(2, 3) == 5
assert add(-1, 1) == 0
```

结果正确时没有输出；结果错误时程序会报 `AssertionError`。

人话解释：`assert` 像自动验货员。符合订单就安静放行，不符合就拉响警报。

今天每个独立函数至少写三个断言：普通情况、边界情况、反例。

---

## 六、跟做：第一个可测试函数

在 `00_跟做_第一个函数.py` 中分段手敲：

```python
def add(first_number, second_number):
    result = first_number + second_number
    return result
```

调用并保存返回值：

```python
answer = add(2, 3)
print(answer)
```

增加自动测试：

```python
assert add(2, 3) == 5
assert add(-1, 1) == 0
assert add(0, 0) == 0

print("add 的测试全部通过")
```

然后故意把第一个预期结果改成 6，观察 `AssertionError`，再改回 5。这是今天第一次主动制造失败测试。

---

## 七、DAY08 代码任务

### 任务 0：第一个函数与断言（必做，25～30 分钟）

文件：`00_跟做_第一个函数.py`

按照上面示范分段手敲。必须亲眼观察一次失败断言，然后恢复正确测试。

### 任务 1：成绩等级函数（必做，35～45 分钟）

文件：`01_独立_成绩等级函数.py`

函数合同：

```text
函数名：get_grade
输入：一个整数成绩
输出："A"、"B"、"C"、"D" 或 "成绩无效"
```

函数内部不要使用 `input()`，也不要 `print()`。用 `return` 返回结果。在函数外调用并打印。

至少断言：90→A、89→B、60→C、59→D、101→成绩无效、-1→成绩无效。

### 任务 2：技能索引函数（必做，35～45 分钟）

文件：`02_独立_查找技能索引函数.py`

实现：

```text
find_skill_index(skills, target_skill)
找到返回真实索引，找不到返回 -1
```

函数内部统一把目标技能标准化；传入的技能列表已经是小写标准格式。

测试：找到第一项、找到最后一项、找不到、空列表。

思考：使用 `return index` 后，为什么不需要 `break`？

### 任务 3：技能标准化去重函数（必做，40～50 分钟）

文件：`03_独立_技能标准化去重函数.py`

实现：

```text
normalize_and_deduplicate(raw_skills)
输入字符串列表，输出统一小写、去首尾空格、保持首次顺序的列表
```

测试：普通重复、不同大小写、空列表、包含空字符串。空字符串清理后不要加入结果。

### 任务 4：两数之和函数（必做，45～60 分钟）

文件：`04_独立_两数之和函数.py`

实现：

```text
find_two_sum(numbers, target)
找到返回包含两个索引的列表，例如 [0, 1]
找不到返回空列表 []
```

使用 O(n²) 暴力法，今天不提前学习字典。函数找到后可以直接 `return [first_index, second_index]`，这样两层循环和整个函数一起结束。

必须测试：目标9、目标26、目标14、`[3,3]`目标6、空列表。

### 任务 5：小项目——岗位技能覆盖率评估器 V1（必做，60～75 分钟）

文件：`05_小项目_岗位技能覆盖率评估器V1.py`

给定：

```python
core_skills = ["python", "c++", "pytorch", "linux", "git"]
candidate_skills = [" Python ", "Git", "linux", "PYTHON"]
```

使用三个小函数完成：

```text
normalize_and_deduplicate(raw_skills) -> 标准化去重列表
find_missing_skills(core_skills, candidate_skills) -> 缺失技能列表
calculate_coverage(core_skills, candidate_skills) -> 覆盖率百分数
```

规定数据标准化后已有 python、git、linux，缺少 c++、pytorch，覆盖率为 60.0。

这里的**指标（metric）**是技能覆盖率：

```text
已覆盖核心技能数量 ÷ 核心技能总数 × 100
```

这与小鹏评估岗位的思维相通：先明确指标定义，再用固定输入验证计算结果。它不是完整招聘评价，只是练习函数和指标测试。

至少写四个断言：规定数据、全部覆盖、完全未覆盖、核心技能列表为空。核心列表为空时不能除以 0，请自行决定返回 0.0，并在函数合同中写明。

### 任务 6：训练损失反弹函数（挑战，30～40 分钟）

文件：`06_挑战_训练损失反弹函数.py`

实现：

```text
find_first_rebound_index(losses)
找到第一次反弹，返回发生反弹的当前索引
没有反弹返回 -1
```

测试：规定反弹、一直下降、立即反弹、空列表、只有一个元素。

---

## 八、理论回答

可以写在本文件底部，也可以继续建立自己的总结文件。

1. 函数的参数和调用时传入的实际数据有什么区别？
2. `return` 与 `print()` 的区别是什么？为什么 LeetCode 更关心 `return`？
3. 为什么函数内部的计数器每次调用都能从 0 开始？
4. `return index` 为什么可以同时代替 `found = True` 和 `break`？
5. 函数合同至少应该写清哪些内容？
6. `assert` 有什么作用？测试正确时为什么通常没有输出？
7. 为什么不需要学完继承、多态和所有魔术方法才开始 Hot 100？
8. 今天哪一个函数最像工作中可重复使用的小工具？为什么？

## 九、AI 使用规则

独立函数卡住时，优先把函数合同和失败断言交给 AI：

```text
这是函数输入、预期输出、我的代码和失败的 assert。
请只指出实际结果与合同在哪一步不一致，不给完整答案。
```

这样 AI 是测试和调试助手，而不是替你生成整份代码。

## 十、DAY08 验收标准

- 能独立定义并调用函数。
- 分清 `return` 和 `print()`。
- 至少三个函数使用断言验证普通、边界和反例。
- 两数之和函数通过所有规定测试。
- 覆盖率项目能解释三个函数各自负责什么。
- 能说明为何基本 OOP 以后会学，但不是 Hot 100 前置条件。

DAY08 达到 80 分且不存在 `return` 核心误解，DAY09 进入字典/哈希表；否则继续用更小函数补练。

## 十一、Git 提交提醒

检查时 `b2f7c21 课程总结` 尚未出现在 `origin/main`。开始 DAY08 前可以先运行：

```bash
git push
```

DAY08 建议提交：

```text
feat(day08): 完成函数与返回值练习
test(day08): 为技能函数增加边界断言
feat(day08): 完成岗位技能覆盖率评估器
```

---

## 十二、我的回答（也可写在课程总结）

### 1. 参数和实际传入的数据有什么区别？


### 2. `return` 与 `print()` 有什么区别？


### 3. 函数内的计数器为什么每次调用都从 0 开始？


### 4. `return index` 为什么可以替代状态变量和 `break`？


### 5. 函数合同至少写清什么？


### 6. `assert` 有什么作用？


### 7. 为什么不用先学完高级 OOP 才刷 Hot 100？


### 8. 哪个函数最像工作中的可复用工具？为什么？


