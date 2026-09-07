# DAY13：读取真实文件，并完成每日LeetCode 242

> 预计用时：3.5小时左右。今天只有一条新理论主线：读取本地文本文件。每日LeetCode继续使用已经学过的字符串、循环和字典，不加入GPU、深度学习、异常处理、CSV或JSON。

## 一、先回应你对DAY12的批评

你的四点批评成立，我从DAY13开始按以下规则执行：

1. 新建的Python练习文件只保留任务名称和空白作答区，不预写函数、变量、循环、TODO和断言。
2. 每道题的三步法由你自己写；不再要求另外写TODO清单。我只在课程文档中提供题目、输入输出、功能合同和验收数据。
3. 任何必做练习里出现的新语法，都必须先在理论部分解释，并用与作业不同的小例子演示。
4. 理论不再只给结论。要依次解释：解决什么问题、代码每部分是什么、数据怎样变化、容易错在哪里、与岗位有什么关系。
5. 每天仍只沿Python/C++与AI Infra求职主线推进，不同时塞入多个方向。

DAY12的`05_实验_列表与字典查找速度.py`违反了第3条。你没有完成它是合理选择，本次评分不扣这道题的分。

---

## 二、DAY12验收：86分，通过并带一项修复

复杂度、哈希和两种查重算法已经掌握，可以进入少量新内容；但函数参数问题必须在DAY13第一题修复。

| 检查项目 | 结果 | 依据 |
|---|---:|---|
| 两数之和检查顺序 | 通过 | 四组断言全部正确。 |
| 单层与嵌套循环次数 | 通过 | n=10、100、1000时分别得到n和n²。 |
| 判断重复元素暴力法 | 通过 | 五组测试通过，循环边界正确。 |
| 判断重复元素哈希法 | 通过 | 五组测试通过，能迁移字典查找思路。 |
| 两数之和操作计数 | 通过 | 暴力法190/4950/124750次，哈希法20/100/500次。 |
| 列表与字典实际计时 | 不计分 | 题目包含未讲知识，是我的课程设计错误。 |
| 岗位技能小项目 | 需修复 | 规定样例通过，但函数忽略`raw_skills`，错误读取全局`job_skills`。 |
| 理论回答 | 通过 | 8题均已回答；主要概念正确，大O与最坏情况的关系还需校准。 |

### 评分明细

- 概念理解：22/25
- 代码正确性：26/30
- 独立分析与调试：15/20
- 测试、边界与复杂度：14/15
- Git记录与表达：9/10

### 为什么全局变量问题是核心问题

你的函数写成：

```python
def analyze_duplicate_skills(raw_skills):
    ...
    for skill in job_skills:
        ...
```

函数门口收到了`raw_skills`，内部却去读取门外的`job_skills`。规定测试传入的刚好也是`job_skills`，所以没有暴露问题。

我增加了这组测试：

```text
输入：['Docker', 'docker', 'Linux']
正确：docker 2次、linux 1次
实际：仍然返回原来的python、git、pytorch等结果
```

这不是变量命名风格问题，而是函数没有处理调用者交给它的数据。真实训练、评估和日志处理代码都依赖正确的数据流，因此必须修复。

### DAY12其实已经完成了一道LeetCode

`02_独立_判断重复元素暴力法.py`和`03_独立_判断重复元素哈希法.py`对应的就是[LeetCode 217 存在重复元素](https://leetcode.cn/problems/contains-duplicate/)的核心问题。你已经分别写出了O(n²)暴力解法和平均O(n)哈希解法。

我没有在DAY12写清题号、难度和题目链接，导致代码练习看起来像普通自编题。这是课程标注问题。以后正式LeetCode任务都会明确写出题号、难度、链接和它训练的算法能力。

---

## 三、DAY12全部示范答案与逐题对比

### 1. 修复两数之和哈希跟做

示范答案：

```python
def two_sum_hash(nums, target):
    seen = {}

    for index in range(len(nums)):
        needed = target - nums[index]
        if needed in seen:
            return [seen[needed], index]
        seen[nums[index]] = index

    return []
```

你的代码：核心实现和四组结果全部正确。`return []`后面的`pass`不会执行，删除即可；不影响核心评价。

### 2. 复杂度操作计数

示范答案：

```python
def count_one_loop(n):
    operation_count = 0
    for _ in range(n):
        operation_count += 1
    return operation_count


def count_two_nested_loops(n):
    operation_count = 0
    for _ in range(n):
        for _ in range(n):
            operation_count += 1
    return operation_count
```

你的代码：实现正确，运行结果是：

```text
n=10：10和100
n=100：100和10000
n=1000：1000和1000000
```

这说明n扩大10倍时，单层循环次数扩大10倍，双层嵌套循环次数扩大100倍。你没有写最后一句观察结论，但代码和输出已经证明你会实现。

### 3. 判断重复元素暴力法

示范答案：

```python
def contains_duplicate_brute_force(nums):
    for first_index in range(len(nums)):
        for second_index in range(first_index + 1, len(nums)):
            if nums[first_index] == nums[second_index]:
                return True
    return False
```

你的代码与示范核心一致，五组测试全部通过。

- 时间复杂度：O(n²)。最坏要检查大量数字对。
- 额外空间复杂度：O(1)。只使用两个索引，没有保存随n增长的新容器。

### 4. 判断重复元素哈希法

示范答案：

```python
def contains_duplicate_hash(nums):
    seen = {}

    for number in nums:
        if number in seen:
            return True
        seen[number] = True

    return False
```

你的代码使用`数字→索引`，示范使用`数字→True`。这道题只关心数字是否见过，两种方式都正确。你的五组测试全部通过。

- 平均时间复杂度：O(n)。每个数字检查一次，字典包含检查平均O(1)。
- 额外空间复杂度：O(n)。没有重复时，字典最多保存n个数字。

### 5. 两数之和操作次数

示范答案：

```python
def two_sum_brute_force_with_count(nums, target):
    check_count = 0

    for first_index in range(len(nums)):
        for second_index in range(first_index + 1, len(nums)):
            check_count += 1
            if nums[first_index] + nums[second_index] == target:
                return {
                    "indices": [first_index, second_index],
                    "checks": check_count,
                }

    return {"indices": [], "checks": check_count}


def two_sum_hash_with_count(nums, target):
    seen = {}
    check_count = 0

    for index in range(len(nums)):
        needed = target - nums[index]
        check_count += 1

        if needed in seen:
            return {
                "indices": [seen[needed], index],
                "checks": check_count,
            }

        seen[nums[index]] = index

    return {"indices": [], "checks": check_count}
```

你的两个函数和输出都正确。n从100变成500，也就是扩大5倍：

- 暴力法从4950次变成124750次，约扩大25倍，对应平方增长。
- 哈希法从100次变成500次，扩大5倍，对应线性增长。

### 6. 列表与字典查找计时

这道题不参与评分。下面只用于补齐示范答案，并解释我之前没有先教的语法。

```python
import time


def measure_list_lookup(numbers, missing_number, repeat_count):
    start_time = time.perf_counter()

    for _ in range(repeat_count):
        missing_number in numbers

    end_time = time.perf_counter()
    return end_time - start_time


def measure_dict_lookup(number_index, missing_number, repeat_count):
    start_time = time.perf_counter()

    for _ in range(repeat_count):
        missing_number in number_index

    end_time = time.perf_counter()
    return end_time - start_time
```

你当时缺少的理论：

- `import time`：把Python标准库里的时间工具加载进当前程序。
- `time.perf_counter()`：读取一个适合测量短时间间隔的高精度计时值。
- 开始值和结束值本身不是耗时；`结束值 - 开始值`才是这段代码使用的时间。
- 一次测量可能受其他程序、CPU状态影响，所以实验看总体趋势，复杂度分析看工作量增长。

我不应该在讲解这些内容之前把它设成必做题。

### 7. 岗位技能重复检查器

示范答案：

```python
def analyze_duplicate_skills(raw_skills):
    counts = {}
    first_indices = {}
    duplicates = []

    for index in range(len(raw_skills)):
        skill = raw_skills[index].strip().lower()

        counts[skill] = counts.get(skill, 0) + 1

        if skill not in first_indices:
            first_indices[skill] = index

        if counts[skill] == 2:
            duplicates.append(skill)

    return {
        "counts": counts,
        "first_indices": first_indices,
        "duplicates": duplicates,
    }
```

与你代码的关键区别：

- 示范始终遍历参数`raw_skills`；你的代码遍历全局`job_skills`。
- 示范用一次主循环完成标准化、计数和首次索引；你的代码创建中间列表后分三次遍历。多次遍历仍是O(n)，不是错误，只是可以进一步合并。
- 示范在次数第一次达到2时加入`duplicates`，因此同一个技能不会重复添加。

必须补上的测试：

```python
custom_report = analyze_duplicate_skills(["Docker", "docker", "Linux"])

assert custom_report == {
    "counts": {"docker": 2, "linux": 1},
    "first_indices": {"docker": 0, "linux": 2},
    "duplicates": ["docker"],
}
```

这组输入与全局样例不同，才能检查函数有没有真的使用参数。

---

## 四、DAY12理论题完整示范回答

### 1. 数据结构和算法有什么区别

数据结构是数据如何组织和保存，例如列表按位置保存，字典按键和值保存。算法是处理这些数据、解决问题的步骤，例如两数之和的暴力法和哈希法。

不需要先学完所有数据结构再刷题。合理顺序是：遇到问题，学习它所需的一个数据结构，立即写题和项目，再在后面重复使用。

### 2. 大O为什么不等于实际秒数

实际秒数受电脑速度、Python版本、后台程序和输入内容影响。大O描述的是输入规模n增大时，算法工作量的增长趋势，因此便于比较算法本身。

需要修正你回答中的一句：大O是“渐进上界”，但它不天然等于“最坏情况”。我们经常用大O表达最坏情况，所以两者容易混在一起；也可以描述某个算法平均情况的上界，例如字典查找平均O(1)。面试时必须说明分析的是平均还是最坏情况。

### 3. 连续循环与嵌套循环

两个连续n次循环的工作量是`n+n=2n`，忽略固定倍数后为O(n)。两个各走n次的嵌套循环是`n×n=n²`，所以为O(n²)。你的回答正确。

### 4. 列表包含与字典包含怎样寻找

列表通常从前向后逐个比较，最坏查n个元素；字典通过键的哈希值计算可能的存储位置，平均只检查少量位置，不需要扫描全部键。你的“门牌号”解释正确。

### 5. 为什么字典只说平均O(1)

不同键可能计算到相同或相近的位置，这叫哈希冲突。冲突时需要额外寻找；正常情况下冲突受到控制，所以平均O(1)，极端情况下可能退化。

### 6. 暴力与哈希的额外空间

暴力两数之和反复使用少数索引，没有保存所有数字对，额外空间O(1)。哈希法最坏要在字典里保存接近n个数字及其索引，额外空间O(n)。

### 7. 什么叫用空间换时间

哈希法多使用一个字典记住过去的数字，付出了更多内存，但避免重复扫描旧数字，把平均时间从O(n²)降到O(n)。

### 8. 判断重复元素的哈希解法

建立空字典；逐个读取数字；如果数字已经在字典中就返回`True`，否则记录它；遍历结束仍未发现重复就返回`False`。

你的书面回答写成了“返回索引”，但这道题的函数结果应是布尔值`True`或`False`。你的实际代码返回值正确，因此判断为代码已掌握、口述需要更精确。

---

## 五、岗位方向复核：今天为什么学习文件读取

我重新查看了`岗位介绍`文件夹的六份岗位：

- 反复出现的共同基础：Python/C++、算法与数据结构、Linux、代码规范、数据处理、调试、逻辑分析和解决问题。
- AI Infra主线：PyTorch、模型训练/评估、性能优化、并行训练、分布式系统。
- 公司或岗位专项：昇腾、Alcore、NoC、MindSpeed、vLLM、SGLang、TensorRT-LLM、Kubernetes等。

当前阶段继续打共同基础，不提前学习专项框架。

文件读取与岗位的关系不是“为了学语法而学语法”：

- 评估开发要读取回归数据和指标结果。
- AI Infra要读取训练配置、数据和日志。
- 软件开发要处理输入文件、配置文件和运行结果。
- 后续C++训练日志分析器的第一步也是打开并逐行读取日志。

所以DAY13把内存中的固定列表改成磁盘上的岗位数据，是从练习题走向项目输入的必要一步。

---

## 六、文件到底是什么

### 1. 变量与文件的区别

你以前写：

```python
skills = ["python", "linux", "git"]
```

这份数据在程序运行时进入内存。程序结束后，变量消失；如果想换数据，通常还要修改代码。

文本文件是磁盘上的持久数据。程序可以保持不变，只更换输入文件。

生活类比：

- 变量像摆在工作台上的材料，工作结束后会被收走。
- 文件像仓库中的纸质清单，下次运行程序仍能重新取出。

### 2. 文本文件

DAY13使用`.txt`纯文本文件。里面仍然是字符，只是保存在磁盘上。`岗位技能样例.txt`中一行代表一个匿名岗位，每行技能用英文逗号隔开。

示例：

```text
Python,C++,Linux,Git
Python,PyTorch,Linux,Git
```

程序读到的每一行首先是一个字符串，不会自动变成列表，也不会自动知道`Python`是技能。拆分和标准化要由你的代码完成。

---

## 七、`open()`：让程序打开文件

### 1. 最小语法示范

下面只是语法示范，不是DAY13作业答案：

```python
file = open("学习计划.txt", "r", encoding="utf-8")
content = file.read()
file.close()
```

逐项解释：

- `open(...)`：请求操作系统打开一个文件。
- 第一个参数是文件路径。
- `"r"`表示read，只读模式。今天不学习写文件。
- `encoding="utf-8"`告诉Python怎样把磁盘字节解释成中文、英文等字符。
- `read()`读取内容。
- `close()`释放文件资源。

### 2. 为什么推荐`with open`

实际更推荐：

```python
with open("学习计划.txt", "r", encoding="utf-8") as file:
    content = file.read()

print(content)
```

`with`可以理解成“在这段缩进代码中借用文件”。离开缩进后，Python会负责关闭文件，即使读取过程中出错，也更不容易忘记释放资源。

`as file`表示给打开的文件对象取名为`file`。它不是文件内容本身，而是程序与磁盘文件之间的操作入口。

### 3. 为什么指定UTF-8

同一串磁盘字节需要按某种编码规则解释。不同系统默认编码可能不同；明确写`encoding="utf-8"`能减少中文乱码和跨平台差异。

Python官方文档给出的`open`核心形式也是“文件名、模式、编码”，并说明文本文件通常应明确编码。

---

## 八、三种读取方式，只选择适合当前任务的一种

### 1. `read()`：一次读取全部内容

```python
with open("学习计划.txt", "r", encoding="utf-8") as file:
    content = file.read()
```

返回一个大字符串。小文件很方便；特别大的训练日志一次全部放进内存可能占用很多空间。

### 2. `readline()`：每次主动读取一行

```python
with open("学习计划.txt", "r", encoding="utf-8") as file:
    first_line = file.readline()
```

今天知道它存在即可，不作为主写法。

### 3. `for line in file`：逐行处理

```python
with open("学习计划.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line)
```

这最适合DAY13和未来训练日志：一次处理一行，思路清晰，也不必一次把大文件全部塞进内存。

---

## 九、为什么读出的每行末尾经常有`\n`

文本文件用换行符表示“这一行结束”。当文件中显示：

```text
Python,C++
Linux,Git
```

第一行读到的字符串通常类似：

```python
"Python,C++\n"
```

`\n`是一个换行字符。它显示时让光标换行，但在字符串中确实占有位置。

你已经用过的`strip()`可以删除字符串首尾空白，包括空格和换行：

```python
clean_line = line.strip()
```

注意：`strip()`不会修改原字符串，而是返回一个新字符串，所以要用变量接住结果。

空白行经过`strip()`后会变成`""`，可以据此跳过。

---

## 十、`split(",")`：把一行拆成多个技能

语法示范：

```python
line = "Python,C++,Linux"
parts = line.split(",")
```

结果：

```python
["Python", "C++", "Linux"]
```

`split(",")`表示遇到英文逗号就切开，并返回列表。

如果原文是：

```python
" Python, C++, Linux "
```

仅仅`split(",")`会保留每一部分周围的空格。因此每个技能仍要分别`strip()`和`lower()`。

数据变化顺序应能口述：

```text
磁盘中的一行
→ Python字符串
→ 删除行首尾空白
→ 按逗号拆成字符串列表
→ 每个技能分别标准化
→ 得到一条岗位的技能列表
```

---

## 十一、文件路径：程序究竟去哪里找文件

### 1. 相对路径

`"DAY13/岗位技能样例.txt"`是相对路径。它的起点通常是终端当前所在目录，而不是Python文件肉眼所在的位置。

如果终端提示符位于仓库根目录：

```text
Algorithm-Learning-Days %
```

那么路径应写：

```text
DAY13/岗位技能样例.txt
```

如果终端已经进入DAY13：

```text
DAY13 %
```

那么路径可以写：

```text
岗位技能样例.txt
```

### 2. 用`pwd`确认起点

在终端运行：

```bash
pwd
```

它会显示当前工作目录。路径错误时先看`pwd`，再检查文件名，不要盲目反复改代码。

### 3. 今天出现`FileNotFoundError`怎么办

它的人话含义是“Python按照你给的路径没有找到文件”。今天只需要会检查：

1. 当前目录是不是预期位置；
2. 路径是否包含`DAY13/`；
3. 中文文件名与大小写是否完全一致。

如何用代码捕获异常留到DAY14，今天不同时引入第二条新主线。

---

## 十二、函数参数必须成为唯一输入来源

正确的数据流：

```text
调用者传入file_path
→ 函数使用file_path打开文件
→ 函数返回读取结果
```

错误的数据流：

```text
调用者传入file_path
→ 函数忽略file_path
→ 函数偷偷使用外部固定路径或全局列表
```

为什么岗位代码强调这一点：

- 训练函数必须能接收不同数据集。
- 评估函数必须能接收不同检查点和评测集。
- 日志分析函数必须能接收不同日志文件。
- 单元测试需要传入很小的测试数据，而不是被全局数据绑死。

验证函数是否真正使用参数的最简单办法：连续传入两份明显不同的数据，看结果是否跟着改变。

---

## 十三、从文件到结果的完整工程流水线

真实数据处理通常不是一个巨大函数，而是几个职责清楚的步骤：

```text
文件路径
   ↓
读取有效行
   ↓
解析每一行
   ↓
标准化技能
   ↓
统计共同技能
   ↓
输出结果
```

人话解释：

- 读取函数只负责把磁盘内容带进程序。
- 解析函数只负责把一行文字变成结构化列表。
- 分析函数只处理列表和字典，不关心文件怎样打开。
- 主程序把它们按顺序连接起来。

这种拆分不是为了“看起来专业”，而是为了定位错误：

- 文件打不开，检查读取函数；
- 逗号拆错，检查解析函数；
- 次数不对，检查分析函数。

这正是岗位要求中的调试能力和代码规范。

---

## 十四、复杂度怎样应用到文件项目

假设文件中总共有n个技能词：

- 逐个读取并标准化：每个技能处理一次，约O(n)。
- 使用字典计数：每个技能进行一次平均O(1)更新，总体平均O(n)。
- 保存计数字典：最坏有n个不同技能，额外空间O(n)。

如果对每个技能都重新从列表头查找旧技能，最坏可能接近O(n²)。因此前两天的字典和复杂度并没有脱离工作项目，今天会直接使用。

---

## 十五、每日LeetCode：242 有效的字母异位词

题目难度：简单。题目页面：[LeetCode 242 有效的字母异位词](https://leetcode.cn/problems/valid-anagram/)

### 1. 什么是字母异位词

如果两个字符串使用的字符种类完全相同，并且每个字符出现次数也完全相同，只是排列顺序可能不同，那么它们互为字母异位词。

```text
"anagram" 与 "nagaram" → True
"rat" 与 "car" → False
"aab" 与 "abb" → False
```

最后一组很重要：两个字符串都有`a`和`b`，但次数不同。因此只检查“字符是否出现过”不够，还必须检查每个字符的数量。

### 2. 先检查长度有什么意义

如果两个字符串长度不同，它们不可能由完全相同的一批字符重新排列得到，可以立即返回`False`。这叫提前结束：已经足以确定答案时，不继续做无意义工作。

提前结束通常能让某些输入更快，但最坏情况下仍要检查全部字符，所以不会把总体O(n)变成O(1)。

### 3. 字符频率表是什么

字符频率表就是：

```text
字符 → 出现次数
```

例如`"aab"`的频率表是：

```python
{"a": 2, "b": 1}
```

这和岗位技能频率统计使用的是同一个思想。数据从“技能字符串”变成了“单个字符”，算法没有换。

### 4. 两种可行思路

方法一是分别统计两个字符串的字符次数，再比较两个字典是否相同。方法二是统计第一个字符串，再用第二个字符串逐个抵消次数。两种都能正确完成。

今天建议先独立实现“两个频率字典”的版本，因为它最直观。通过后再思考能否只使用一个字典；不要求一次写出最短代码。

### 5. 复杂度怎样说

设两个字符串长度分别是n和m：

- 遍历两个字符串，时间复杂度是O(n+m)。题目中长度必须相等才可能成功，也常简写为O(n)。
- 字典保存不同字符的次数，额外空间是O(k)，k是不同字符的数量；一般情况下最坏可到O(n)。
- 如果严格限定只有26个小写英文字母，k最多为26，是固定上限，也可以把额外空间说成O(1)。

面试时不要只背一个答案，要先说明自己采用的输入假设。

### 6. 今天必须自己考虑的测试

```text
"anagram", "nagaram" → True
"rat", "car" → False
"aab", "abb" → False
"", "" → True（本地扩展测试）
"a", "aa" → False
```

你需要自己写三步分析、普通函数、断言和LeetCode的`class Solution`版本。课程不提供实现代码。

---

## 十六、GitHub参考项目怎样使用

本阶段只借鉴两个层次，不复制代码：

1. 入门结构参考`Python-Word-Frequency`公开README中的任务流程：读取文本、标准化、使用字典计数、输出报告。DAY13把“英文单词频率”改造成“岗位技能频率”。该仓库页面没有清晰展示许可证，因此不复制其代码或文本数据。
2. 长期方向参考MIT许可的`dreamjobs-tech/skill-extractor`：真实岗位技能提取器会把原始职位文本转成规范化技能，并用独立测试样例验证一致性。它涉及词表、MiniLM、ONNX和分类器，明显超出当前水平；现在只学习它的“输入→标准化输出→测试”工程思路。

当前不克隆、不安装、不运行这两个仓库。等你完成自己的基础版本后，再阅读与当前能力匹配的局部代码，避免整仓照抄。

---

## 十七、DAY13代码规则

DAY13的七个Python文件都只有任务说明，没有预写实现。每题开始后，你亲自写：

1. 三步法；
2. 函数定义、变量、循环和返回值；
3. 规定断言；
4. 至少一组你自己补充的测试。

不再要求写TODO清单。三步分析写在代码注释中即可，其作用是帮助你想清楚程序，不按字数评分。

卡住时按固定顺序求助：先告诉我你的三步分析和实际报错，我先给引导问题；仍不会再给伪代码；最后才给局部骨架。

---

## 十八、DAY13代码任务

时间安排建议：任务0、1、2、3、6是当日核心，约2小时20分钟；阅读理论与口述约1小时。任务4、5是连续项目的进阶部分，如果当天超过3.5小时，可以在DAY14验收前继续完成，不因合理顺延判为不掌握。

### 任务0：修复函数参数问题（25分钟）

文件：`00_修复_函数必须使用传入参数.py`

从空白重新实现：

```text
analyze_duplicate_skills(raw_skills) -> dict
```

功能与DAY12小项目相同，但不允许读取函数外的`job_skills`。

必须自己手写两组断言：

```text
输入A：["Python", "python", "Git"]
counts：python 2、git 1
first_indices：python 0、git 2
duplicates：python

输入B：["Docker", "docker", "Linux"]
counts：docker 2、linux 1
first_indices：docker 0、linux 2
duplicates：docker
```

验收关键：连续调用A和B，结果必须各自对应自己的输入。

### 任务1：读取整个文本文件（20分钟）

文件：`01_独立_读取整个文本文件.py`

函数合同：

```text
read_text(file_path) -> str
```

要求：

- 使用`with open`、只读模式和UTF-8；
- 返回整个文件字符串，不在函数内部写死路径；
- 调用时读取`DAY13/岗位技能样例.txt`；
- 测试返回值是字符串，并且其中包含`Python`与`Linux`。

### 任务2：逐行读取有效岗位（25分钟）

文件：`02_独立_逐行读取有效岗位.py`

函数合同：

```text
load_job_lines(file_path) -> list
```

要求：

- 逐行读取，不使用一次性`read()`；
- 对每行使用`strip()`；
- 空白行不加入结果；
- 对样例文件应返回6条有效岗位字符串；
- 自己测试第一条内容和列表长度。

### 任务3：解析一行技能（25分钟）

文件：`03_独立_解析一行岗位技能.py`

函数合同：

```text
parse_skill_line(line) -> list
```

规定测试：

```text
输入：" Python, C++, Linux, Git "
输出：["python", "c++", "linux", "git"]
```

要求每个技能都删除首尾空格并转成小写。再自行增加一组只有一个技能的测试。

### 任务4：读取并解析整个岗位文件（30分钟）

文件：`04_独立_读取并解析岗位文件.py`

函数合同：

```text
load_job_skills(file_path) -> list
```

返回嵌套列表：外层每个元素代表一条岗位，内层是该岗位的技能列表。

规定结果的前两项：

```python
[
    ["python", "c++", "linux", "git"],
    ["python", "pytorch", "linux", "git"],
]
```

完整结果外层长度应为6。你可以调用自己写的解析函数，但需要自己决定怎样组织文件。

### 任务5：岗位共同技能分析器V1（50～60分钟）

文件：`05_小项目_岗位共同技能分析器V1.py`

输入：`岗位技能样例.txt`。

输出字典必须包含：

```text
job_count：岗位数量
skill_counts：每个技能出现在多少条岗位中
common_skills：至少出现在3条岗位中的技能，按首次出现顺序
```

样例正确结果：

```python
{
    "job_count": 6,
    "skill_counts": {
        "python": 4,
        "c++": 4,
        "linux": 6,
        "git": 4,
        "pytorch": 3,
        "数据结构": 1,
        "transformer": 1,
        "算法": 1,
    },
    "common_skills": ["python", "c++", "linux", "git", "pytorch"],
}
```

样例保证同一条岗位内没有重复技能，因此今天不需要引入集合`set`。要求至少拆成“读取解析”和“统计分析”两个函数，函数内部不得使用固定的全局岗位列表。

### 任务6：LeetCode 242 有效的字母异位词（35～45分钟）

文件：`06_LeetCode242_有效的字母异位词.py`

先从空白完成普通函数：

```text
is_anagram(s, t) -> bool
```

普通函数通过规定测试后，再改写为LeetCode外壳：

```text
class Solution:
    isAnagram(self, s, t) -> bool
```

自己写至少五组断言，并在代码末尾说明时间复杂度和额外空间复杂度。不得使用`sorted()`或`collections.Counter`，本日目标是亲手使用字典频率统计。

---

## 十九、DAY13理论作业

请自己新建`课后总结.md`，只回答以下问题和真实疑问：

1. 变量中的列表与磁盘文件有什么区别？
2. `open`的文件路径、`"r"`、`encoding="utf-8"`分别表示什么？
3. 为什么推荐`with open`，离开缩进后发生了什么？
4. `read()`和逐行`for line in file`有什么差别？训练日志很大时更适合哪种？
5. 为什么读取一行后通常要调用`strip()`？
6. `split(",")`的输入和输出分别是什么？
7. 相对路径从哪里开始？怎样用终端确认？
8. 为什么函数接收`file_path`后不能偷偷使用外部固定路径？
9. 口述岗位文件从磁盘变成统计报告的完整数据流。
10. DAY12项目为什么通过了规定测试，却没通过另一份非空输入？以后怎样设计测试避免它？
11. 判断字母异位词时，为什么只检查字符种类还不够？
12. LeetCode 242使用字典计数时，时间和额外空间复杂度分别是什么？你的结论依赖什么输入条件？

不要求背诵术语。每题目标是你能脱离原文向面试官解释。

---

## 二十、DAY13通过标准

- 七个Python文件的三步分析、实现和测试都是你自己写的，不要求TODO清单。
- 能解释文件、变量、路径、编码和关闭文件各自解决什么问题。
- 能从函数参数指定的路径读取文件，而不是写死数据。
- 能逐行清洗并解析成嵌套列表。
- 岗位共同技能分析器规定结果正确。
- 使用完全不同的输入时，函数输出会随参数改变。
- 能独立完成LeetCode 242普通函数和`class Solution`版本，并解释复杂度。

未完成的功能会影响掌握判断；变量名、空行数量或输出排版不会被当成核心错误。

---

## 二十一、本日资料范围

- Python 3.11官方教程“读写文件”：核对`open`、读取模式、UTF-8和`with`用法。
- Python 3.11官方内置类型文档：核对`strip()`与`split()`行为。
- LeetCode 242题目：确认题意、难度和输入约束。
- GitHub入门参考：[amanda-mcmullin/Python-Word-Frequency](https://github.com/amanda-mcmullin/Python-Word-Frequency)，只借鉴“文件→标准化→频率报告”的任务结构。
- GitHub长期方向：[dreamjobs-tech/skill-extractor](https://github.com/dreamjobs-tech/skill-extractor)，只观察输入输出、规范化与测试思路，不学习其模型与依赖。
