# DAY10：字典与哈希表——根据“名字”直接找到数据

> 预计用时：3.5～4小时。今天只学习一个知识组：Python字典及其背后的哈希查找思想。固定使用三步法，不增加新的学习流程。

## 一、DAY09重新判断：函数核心知识已通过

DAY09真正需要检查的是你是否掌握函数本身。结论是：**通过，可以进入下一知识点。**

你已经能够：

- 使用`def`定义函数。
- 用参数把数据传入函数。
- 理解局部变量与全局变量的区别。
- 使用`return`把结果交给调用者。
- 保持主要函数的返回值含义稳定。
- 使用`assert`检查普通和边界情况。
- 闭卷写出标准化、查找和两数之和函数的主体。

技能查找索引、多解两数之和等问题以后会作为算法边界继续修正，但不再阻止你学习新知识。

### 今后固定的判断口径

每天优先判断三件事：

1. 能否用自己的话解释当天核心概念。
2. 能否不照抄模板写出核心代码。
3. 能否运行核心程序并解释主要变量和结果。

不影响核心理解的命名、输出格式和少见边界会单独注明为“后续改进”，不会反复阻塞课程。

---

## 二、DAY09简洁示范答案

这些模板用于对照理解，不要求背诵，也不作为进入DAY10的额外门槛。

### 1. 成绩等级函数

```python
def get_grade(score):
    if score < 0 or score > 100:
        return "成绩无效"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 60:
        return "C"
    return "D"
```

### 2. 技能查找函数

```python
def find_skill_index(skills, target_skill):
    normalized_target = target_skill.strip().lower()

    for index in range(len(skills)):
        if skills[index].strip().lower() == normalized_target:
            return index

    return -1
```

### 3. 标准化去重函数

```python
def normalize_and_deduplicate(skills):
    result = []

    for raw_skill in skills:
        skill = raw_skill.strip().lower()
        if skill != "" and skill not in result:
            result.append(skill)

    return result
```

### 4. 两数之和函数

```python
def find_two_sum(numbers, target):
    for first_index in range(len(numbers)):
        for second_index in range(first_index + 1, len(numbers)):
            if numbers[first_index] + numbers[second_index] == target:
                return [first_index, second_index]

    return []
```

### 5. 技能覆盖率函数

```python
def calculate_coverage(core_skills, candidate_skills):
    if len(core_skills) == 0:
        return 0.0

    covered_count = 0

    for core_skill in core_skills:
        if core_skill in candidate_skills:
            covered_count += 1

    return covered_count / len(core_skills) * 100
```

### 6. 损失反弹函数

```python
def find_first_rebound_index(losses):
    for index in range(1, len(losses)):
        if losses[index] > losses[index - 1]:
            return index

    return -1
```

### 7. DAY09总体对比

| 核心能力 | 你的表现 | 判断 |
|---|---|---|
| 定义和调用函数 | 可以独立完成 | 已掌握 |
| 参数代替全局变量 | 覆盖率等函数已改为参数 | 已掌握核心 |
| `return` | 能返回等级、索引、列表和数值 | 已掌握 |
| 局部变量 | 能在函数内建立计数器和结果列表 | 已掌握 |
| 自动检查 | 多个文件能写`assert` | 已掌握基础 |
| 算法边界 | 个别复杂输入仍可改善 | 后续刷题继续练 |

---

## 三、继续固定使用三步法

每道题只做这三步，不再更换名称或增加新的必写表格。

### 第一步：最小数据的输入和输出

例如统计技能次数：

```text
输入：["python", "git", "python"]
输出：python 2次，git 1次
```

### 第二步：把代码切成几个阶段

```text
建立空统计表
逐项读取技能
更新对应次数
输出统计表
```

### 第三步：边写边用小数据检查，并记录状态

程序需要记住的状态只有“每种技能目前出现了几次”。字典正适合保存这种“名称→数据”的对应关系。

---

## 四、字典是什么？

### 1. 专业解释

**字典（dictionary，Python类型名为`dict`）**是一种保存“键—值”映射的数据结构。

- **键（key）**：用来查找数据的唯一名称。
- **值（value）**：这个名称对应的数据。

```python
skill_counts = {
    "python": 3,
    "linux": 2,
    "git": 2,
}
```

### 2. 人话解释

列表像一排按0、1、2编号的柜子；字典像一排贴着名字的柜子。

列表要说“打开第2号柜子”，字典可以直接说“打开python柜子”。

```python
print(skill_counts["python"])
```

输出3。

### 3. 为什么工作和算法都需要字典

常见场景：

- 技能名称对应出现次数。
- 实验名称对应损失值。
- 配置名称对应配置数据。
- 用户编号对应用户信息。
- 算法中某个数字对应它以前出现的位置。

---

## 五、字典的基本操作

### 1. 建立空字典

```python
skill_counts = {}
```

### 2. 新增或修改

```python
skill_counts["python"] = 1
skill_counts["python"] = 2
skill_counts["git"] = 1
```

同一个键不会同时保存两个独立值。再次赋值会更新原来的值。

### 3. 读取

```python
python_count = skill_counts["python"]
print(python_count)
```

如果键不存在，直接使用方括号会产生`KeyError`。

人话解释：你要求打开`docker`柜子，但仓库里根本没有贴这个名字的柜子。

### 4. 判断键是否存在

```python
if "python" in skill_counts:
    print("已经记录python")
```

这里的`in`默认检查字典的键。

### 5. 使用`get()`安全读取

```python
python_count = skill_counts.get("python", 0)
docker_count = skill_counts.get("docker", 0)
```

`get("docker", 0)`表示：有docker就拿现有值，没有就临时得到默认值0，不会报错。

### 6. 遍历字典

只遍历键：

```python
for skill in skill_counts:
    print(skill)
```

同时获取键和值：

```python
for skill, count in skill_counts.items():
    print(skill, count)
```

`items()`可以理解成把每个“标签和柜子内容”一起交给循环。

---

## 六、使用字典统计次数

给定：

```python
skills = ["python", "git", "python", "linux", "git", "python"]
```

### 三步法

第一步：

```text
输入6项技能
输出python 3、git 2、linux 1
```

第二步：

```text
建立空字典
逐个读取技能
让该技能的次数加1
输出字典
```

第三步：字典保存“技能→当前次数”。

### 写法一：先判断

```python
skill_counts = {}

for skill in skills:
    if skill in skill_counts:
        skill_counts[skill] += 1
    else:
        skill_counts[skill] = 1

print(skill_counts)
```

### 写法二：使用`get()`

```python
skill_counts = {}

for skill in skills:
    skill_counts[skill] = skill_counts.get(skill, 0) + 1

print(skill_counts)
```

先理解写法一，再手敲写法二。不要把`get()`当成必须背的口诀。

---

## 七、哈希表是什么？

### 1. 专业解释

Python字典的底层核心思想是**哈希表（hash table）**。它通过哈希计算把键快速定位到存储位置。

平均情况下，字典查找、插入和更新的时间复杂度接近**O(1)**。

### 2. 人话解释

列表查找像从第一排柜子开始一个个打开；哈希表像前台根据标签计算出柜子大概在哪个区域，直接过去查找。

O(1)不是说永远只做一步，而是数据从100项增加到100万项时，平均查找工作量不会跟着线性增加。

今天不学习哈希冲突和底层内存结构，只需要理解：字典适合根据唯一键快速查找。

### 3. 列表和字典怎样选择

| 需要 | 更适合 |
|---|---|
| 按顺序保存并通过位置访问 | 列表 |
| 根据名称、编号快速找到对应数据 | 字典 |
| 允许相同值重复出现 | 两者都可以 |
| 键必须唯一 | 字典 |

字典不是列表的高级替代品，而是解决不同问题的工具。

---

## 八、跟做：第一个技能计数字典

文件：`00_跟做_第一个字典.py`

分段手敲：

```python
skills = ["python", "git", "python", "linux", "git", "python"]
skill_counts = {}
```

```python
for skill in skills:
    if skill in skill_counts:
        skill_counts[skill] += 1
    else:
        skill_counts[skill] = 1
```

```python
for skill, count in skill_counts.items():
    print(f"{skill}：{count}次")
```

然后关闭课程，用`get()`写法重写计数循环。

---

## 九、DAY10代码任务

所有任务继续固定三步：最小输入输出、代码阶段、边写边测与状态。

### 任务0：第一个字典（必做，30分钟）

文件：`00_跟做_第一个字典.py`

- 分别手敲“先判断”和`get()`两种计数方式。
- 结果都应为python 3、git 2、linux 1。
- 能解释字典中哪个是键、哪个是值。

### 任务1：技能次数统计函数（必做，35～45分钟）

文件：`01_独立_技能次数统计函数.py`

实现：

```text
count_skills(raw_skills) -> 字典
```

- 技能先去首尾空格并转小写。
- 空字符串不统计。
- 返回“技能名称→出现次数”字典。
- 测试普通、大小写重复、空列表和空字符串。

### 任务2：成绩等级分布（必做，35～45分钟）

文件：`02_独立_成绩等级分布.py`

复用`get_grade(score)`，把一组成绩转换成等级统计字典。

```python
scores = [95, 82, 60, 59, 101, 90, 82]
```

预期：A 2、B 2、C 1、D 1、成绩无效1。

### 任务3：合并两个计数字典（必做，35～45分钟）

文件：`03_独立_合并技能计数.py`

给定：

```python
first_counts = {"python": 2, "git": 1}
second_counts = {"python": 1, "linux": 3}
```

输出：

```python
{"python": 3, "git": 1, "linux": 3}
```

不能修改两个原字典。可以建立新字典，并使用循环合并。

### 任务4：找出最高频技能（必做，35～45分钟）

文件：`04_独立_最高频技能.py`

实现：

```text
find_most_common_skill(skill_counts) -> 技能字符串
```

- 输入空字典返回空字符串。
- 有并列时返回遍历中最先遇到的技能。
- 不使用`max()`。

### 任务5：小项目——岗位技能频率分析器V2（必做，60～75分钟）

文件：`05_小项目_岗位技能频率分析器V2.py`

给定匿名化岗位技能清单：

```python
job_skill_lists = [
    ["Python", "Linux", "Git", "PyTorch"],
    ["python", "C++", "linux", "git"],
    ["PYTHON", "PyTorch", "Linux", "Docker"],
]
```

要求：

- 标准化所有技能。
- 使用一个字典统计出现次数。
- 输出每项技能及次数。
- 输出出现次数最多的技能。
- 输出出现次数至少2次的高频技能列表。

今天目标是掌握字典统计，不额外处理岗位内部重复等复杂规则。

### 任务6：两数之和哈希预习（挑战，45～60分钟）

文件：`06_挑战_两数之和哈希预习.py`

暴力法每次拿两个数配对。字典方法改成：遍历当前数字时，检查“还缺的那个数”以前是否出现过。

```text
当前数字number
需要的数字needed = target - number
seen保存：以前的数字 -> 以前的索引
```

规定：

```python
numbers = [2, 7, 11, 15]
target = 9
```

预期返回`[0, 1]`。课程末尾提供一级提示，不直接提供完整答案。

一级提示：

```text
建立空字典seen
遍历索引和数字
    计算needed
    如果needed已经是seen的键，返回旧索引和当前索引
    否则记录当前数字对应当前索引
```

---

## 十、理论回答

1. 字典中的键和值分别是什么？用技能次数举例。
2. 列表按什么找数据，字典按什么找数据？
3. 直接访问不存在的键会发生什么？`get()`怎样避免？
4. 为什么统计次数时字典比两个平行列表更自然？
5. `skill_counts[skill] = skill_counts.get(skill, 0) + 1`用人话是什么意思？
6. 哈希表平均O(1)查找用人话怎样解释？
7. 字典是否比列表更高级、更应该优先使用？为什么？
8. 今天哪个任务最接近岗位工作中的数据统计？

## 十一、验收标准

- 能独立建立、读取、更新和遍历字典。
- 理解键必须唯一，一个键对应一个当前值。
- 能用字典统计出现次数。
- 能解释`get(key, 0)`。
- 能说明列表与字典各自适合的问题。
- 小项目能够输出正确频率。
- 挑战题不作为是否通过字典课的硬门槛。

DAY10达到80分且字典核心无误解后，DAY11进入正式Hot 100第一题“两数之和”。

---

## 十二、我的回答（也可以写课后总结）

### 1. 字典的键和值是什么？


### 2. 列表和字典分别按什么查找？


### 3. 不存在的键与get()有什么区别？


### 4. 字典为什么适合计数？


### 5. 用人话解释get计数语句。


### 6. 用人话解释哈希表平均O(1)。


### 7. 字典是否总比列表更适合？


### 8. 哪个任务最接近岗位数据统计？


