# DAY12：真正看懂时间复杂度——列表查找、哈希查找与判断重复元素

> 预计用时：3～3.5小时。今天只增加一个核心知识：复杂度。代码仍围绕你已经学过的列表、字典、循环和函数展开，不引入无关框架。

## 一、DAY11验收：86分，通过

| 检查项目 | 结果 | 判断依据 |
|---|---:|---|
| 两数之和题意与`needed` | 通过 | 能说清“还差的另一个数字”。 |
| 暴力法 | 通过 | 两层循环与索引范围正确，三组测试通过。 |
| 哈希法 | 通过 | 闭卷函数版和LeetCode版都能正确手写。 |
| 先检查、后记录 | 通过 | 能用`[3, 3]`解释为何不能使用同一个索引。 |
| 岗位技能快速索引器 | 通过 | 能建立“技能名称→首次索引”并处理重复、找不到和空列表。 |
| 时间复杂度 | 待补 | 知道两层循环较慢，但还不能准确解释字典为何平均查找快。 |
| 空间复杂度 | 待补 | 把循环次数误当成了新占用的存储空间。 |

### 评分明细

- 概念理解：21/25
- 代码正确性：27/30
- 独立分析与调试：18/20
- 测试、边界与复杂度：11/15
- Git记录与表达：9/10

### 最重要的结论

你已经掌握两数之和哈希解法，证据是`03_独立_闭卷两数之和函数.py`和`04_独立_LeetCode两数之和.py`都正确。DAY12不要求你再背一遍答案，而是解决你主动提出的疑问：

```text
if needed in seen 难道不是暗中遍历字典吗？
为什么暴力法额外空间不是O(n²)？
```

## 二、先更正我的一道题

DAY11热身数据是：

```python
[95, 64, 82, 60, 59, 101, 90, 82]
```

其中`64`和`60`都属于C，所以正确结果是：

```python
{"A": 2, "B": 2, "C": 2, "D": 1, "Invalid": 1}
```

我在DAY11课程中写成了“C 1”，这是我的题目答案写错了。你的程序输出C 2是正确的，这一项满分通过。

---

## 三、DAY11全部代码示范答案与逐题对比

### 1. 修复成绩等级分布

```python
def get_grade(score):
    if score < 0 or score > 100:
        return "Invalid"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 60:
        return "C"
    return "D"


def count_grades(scores):
    grade_counts = {}
    for score in scores:
        grade = get_grade(score)
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    return grade_counts
```

对比：你的判断顺序和统计逻辑都正确。最后一个`else`可以保留，也可以直接`return "D"`，不影响掌握结论。

### 2. 两数之和暴力法

```python
def two_sum_brute_force(nums, target):
    for first_index in range(len(nums)):
        for second_index in range(first_index + 1, len(nums)):
            if nums[first_index] + nums[second_index] == target:
                return [first_index, second_index]
    return []
```

对比：你的实现与示范相同。内层从`first_index + 1`开始，因此不会重复使用同一个位置，也不会把同一对数字正反检查两次。

### 3. 两数之和哈希跟做版

```python
def two_sum_hash(nums, target):
    seen = {}

    for index in range(len(nums)):
        number = nums[index]
        needed = target - number

        if needed in seen:
            return [seen[needed], index]

        seen[number] = index

    return []
```

对比：你在这个文件中故意把“记录”放在“检查”前，并写出`[0, 0]`来观察错误。这能帮助理解原因，但断言的职责应该是检查正确结果，不能把错误结果写成“测试通过”。正确测试应为：

```python
assert two_sum_hash([3, 2, 4], 6) == [1, 2]
assert two_sum_hash([3, 3], 6) == [0, 1]
assert two_sum_hash([3], 6) == []
```

如果想保留错误实验，可以打印错误结果并写注释，但不要用`assert 错误结果`。

### 4. 闭卷普通函数版

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

对比：你的闭卷代码正确。你的`else`可以省略，因为找到答案时函数已经`return`结束；但这只是简化建议，不是知识错误。

### 5. LeetCode格式

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}

        for index in range(len(nums)):
            needed = target - nums[index]
            if needed in seen:
                return [seen[needed], index]
            seen[nums[index]] = index

        return []
```

对比：你的核心代码完全正确。`return []`后面的`pass`永远不会执行，可以删除，但它不影响算法正确性。

### 6. 暴力法哈希对比

```python
def two_sum_brute_force(nums, target):
    for first_index in range(len(nums)):
        for second_index in range(first_index + 1, len(nums)):
            if nums[first_index] + nums[second_index] == target:
                return [first_index, second_index]
    return []


def two_sum_hash(nums, target):
    seen = {}
    for index in range(len(nums)):
        needed = target - nums[index]
        if needed in seen:
            return [seen[needed], index]
        seen[nums[index]] = index
    return []
```

对比：两个函数都正确。你的时间复杂度方向正确，但空间复杂度解释需要修正：暴力法不会保存全部数字组合，只有两个索引变量，因此额外空间是O(1)；哈希法的循环变量也是O(1)，真正增长的是`seen`字典，因此额外空间是O(n)。

### 7. 岗位技能快速索引器

```python
def build_first_index(job_skills):
    first_index = {}

    for index in range(len(job_skills)):
        skill = job_skills[index].strip().lower()
        if skill not in first_index:
            first_index[skill] = index

    return first_index


def find_skill_index_with_hash(job_skills, target_skill):
    first_index = build_first_index(job_skills)
    target = target_skill.strip().lower()
    return first_index.get(target, -1)
```

对比：你的四组测试全部正确。你先建立标准化列表再建字典，示范在一次循环中直接完成，少创建一个中间列表。两种写法都正确，示范的额外空间更少一些。

---

## 四、DAY11理论示范答案

1. `seen`的键是以前见过的数字，值是该数字的索引。
2. `needed = target - number`表示：当前数字已经选定，要凑成目标值，还缺哪个数字。
3. 先记录再检查可能让当前数字和自己配对，例如一个`3`就错误得到`[0, 0]`。
4. O(n²)表示数据扩大10倍，最坏工作量大约扩大100倍；O(n)表示工作量大约扩大10倍。
5. 哈希法最坏要把接近n个已经看过的数字和索引存进`seen`，所以额外空间是O(n)。
6. 处理第二个3时，字典中保存的是第一个3的索引0，当前索引是1，因此返回两个不同位置。
7. 现在只需知道`Solution`是LeetCode规定的类外壳，`self`代表由这个类创建的当前对象；类的完整原理以后单独学习。
8. 建空字典；逐个计算当前还缺的`needed`；先查旧记录，找到就返回，否则记录当前数字和索引。

你的第1、2、3、6、7题已经达到要求。第8题中的“目标值在字典中”应改成“还缺的数字`needed`在字典中”。第4、5题是DAY12主任务。

---

## 五、数据结构和算法到底有什么区别

### 数据结构（Data Structure）

数据结构是“怎样组织和保存数据”。

生活类比：同样是一堆工具，可以散放在桌上，也可以按种类放进有标签的抽屉。工具没变，组织方式变了，寻找速度也会变。

你已经用过的数据结构：

- 列表：按位置排成一队。
- 字典：通过键找到对应的值。
- 字符串：按顺序保存字符。

### 算法（Algorithm）

算法是“为解决一个问题而执行的步骤”。

两数之和的暴力法和哈希法是两种算法；列表和字典是这些算法使用的数据结构。

### 是否必须先学完数据结构，再开始算法

不需要，也不应该先把所有数据结构学完才做题。对初学者更合适的顺序是：

```text
遇到一个小问题
→ 学解决它所必需的数据结构
→ 立刻写算法解决问题
→ 在后面的题目中再次使用
```

因此当前安排是列表、字典配合数组与哈希题；以后遇到“后进先出”问题再学栈，遇到层层相连的数据再学链表和树。这样既有基础，又不会同时塞进所有知识。

---

## 六、时间复杂度：衡量输入变大后，工作量怎样增长

### 1. n是什么

`n`通常代表输入规模。对于两数之和，`n = len(nums)`。

大O不是精确秒表，也不是数代码有几行。它关心的是：当n越来越大，执行步骤增长得有多快。

### 2. 今天掌握三个级别

| 复杂度 | 人话 | n从10变成100时的大致变化 |
|---|---|---:|
| O(1) | 输入再多，完成这一步的平均工作量基本不跟着增长 | 基本不变 |
| O(n) | 每个元素大致处理一次 | 约10倍 |
| O(n²) | 每个元素又和许多元素配对检查 | 约100倍 |

### 3. 为什么两个连续循环仍是O(n)

```python
for number in nums:
    print(number)

for number in nums:
    print(number)
```

步骤大约是`n + n = 2n`。大O关注增长最快的部分并忽略固定倍数，所以是O(n)，不是O(n²)。

### 4. 为什么嵌套循环常常是O(n²)

```python
for first in nums:
    for second in nums:
        print(first, second)
```

外层每走一次，内层都要走n次，总量约为`n × n`，所以是O(n²)。

暴力两数之和实际最多检查：

```text
(n - 1) + (n - 2) + ... + 1 = n(n - 1) / 2
```

虽然不是精确的`n²`，但n变大后增长速度仍由平方项决定，所以记作O(n²)。

---

## 七、为什么`needed in seen`平均不是遍历整个字典

### 列表查找：逐个问

`target in numbers`面对普通列表时，Python通常要从头逐个比较，直到找到或走到末尾。因此平均/最坏工作量会随列表长度增长，最坏是O(n)。

### 字典查找：先计算储物柜编号

字典底层主要使用哈希表（hash table）。可以把它想成一排储物柜：

1. 哈希函数（hash function）根据键计算一个编号。
2. Python直接去对应位置附近寻找。
3. 通常只需检查很少几个位置，不需要从第一个键一路问到最后一个键。

因此，对于两数之和中的整数键，面试分析通常把`needed in seen`看成平均O(1)。它不是特殊的Python层`for`循环。

### 为什么只说“平均”O(1)

不同键有时会计算到相同或相近位置，这叫哈希冲突（hash collision）。Python需要继续寻找其他位置。如果冲突非常严重，最坏可能退化到O(n)；但正常使用下，字典会调整容量，让查找平均接近O(1)。

你现在不需要背Python哈希表的具体内存布局。需要能讲清：

```text
列表查找通常逐个比较；字典先通过键计算位置，所以平均不必扫描全部键。
```

---

## 八、空间复杂度：算法另外开了多少储物空间

空间复杂度关注输入之外，算法额外使用的存储空间怎样随n增长。

### 暴力两数之和

```python
first_index
second_index
```

不管列表有10个还是100万个元素，算法始终只保存少量索引变量，没有保存全部组合，所以额外空间是O(1)。循环执行很多次，不等于同时占用很多份空间。

### 哈希两数之和

```python
seen[number] = index
```

最坏情况下会保存接近n个键值对，输入扩大10倍，字典所需空间也约扩大10倍，所以额外空间是O(n)。

这就是“用空间换时间”：多用一个字典，把时间从O(n²)降到平均O(n)。

---

## 九、DAY12代码任务

所有题继续只使用固定三步法：

1. 用最小数据说清输入和输出。
2. 把任务拆成几个代码阶段。
3. 边写边用小数据测试，并记录必要状态。

### 任务0：修复哈希跟做文件（15分钟）

文件：`00_热身_修复两数之和哈希跟做.py`

先检查`needed`，再记录当前数字；把三组断言改成真正的正确结果。

### 任务1：亲手数操作次数（25分钟）

文件：`01_跟做_复杂度操作计数.py`

分别完成单层循环和双层循环计数。运行n=10、100、1000，观察n增大10倍时次数怎样增长。n=1000的双层循环是一百万次，在本机CPU即可完成，不需要GPU。

### 任务2：判断重复元素——暴力法（25分钟）

文件：`02_独立_判断重复元素暴力法.py`

给定整数列表，只要存在两个不同位置的值相同就返回`True`，否则返回`False`。先用两层循环，写出O(n²)时间、O(1)额外空间版本。

### 任务3：判断重复元素——哈希法（25分钟）

文件：`03_独立_判断重复元素哈希法.py`

用字典记录已经见过的数字，写出平均O(n)时间、O(n)额外空间版本。不要复制两数之和代码，要根据新题意重新组织条件。

### 任务4：两数之和操作计数（30分钟）

文件：`04_独立_两数之和操作次数.py`

让暴力法和哈希法除了返回索引，还返回主要检查次数。比较列表长度20、100、500时的数据。正确性比计时更重要。

### 任务5：列表与字典查找计时（20分钟）

文件：`05_实验_列表与字典查找速度.py`

使用`time.perf_counter()`分别测量“不存在的数字”在列表和字典中的查找时间。计时会受电脑状态影响，所以只观察总体趋势，不把一次结果当成数学证明。

### 任务6：岗位技能重复检查器V1（45分钟）

文件：`06_小项目_岗位技能重复检查器V1.py`

输入一份岗位技能列表，统一大小写和首尾空格后，输出：

- 每个技能出现次数；
- 每个技能第一次出现的原始索引；
- 重复出现的技能列表。

这是DAY10频率统计和DAY11快速索引器的组合，也是把两个小功能合成一个工作型功能。

---

## 十、DAY12理论作业

请在你自己新建的`课后总结.md`中回答：

1. 数据结构和算法有什么区别？是否必须先学完所有数据结构才能刷题？
2. 大O为什么不等于程序实际运行了多少秒？
3. 两个前后相接的n次循环为什么是O(n)，两个嵌套的n次循环为什么是O(n²)？
4. `target in 列表`和`target in 字典`大致怎样寻找目标？
5. 为什么字典查找只能说平均O(1)，而不保证永远O(1)？
6. 暴力两数之和为什么是O(1)额外空间，而哈希法是O(n)？
7. 用自己的话解释“哈希法用空间换时间”。
8. 不看代码，口述“判断重复元素”的哈希解法。

只记录真实理解和疑问，不需要写学习流水账。

## 十一、DAY12通过标准

- 能判断单层循环、连续循环和两层嵌套循环的复杂度。
- 能解释字典平均O(1)不是暗中扫描整个字典。
- 能分清“运行次数多”和“同时占用空间多”。
- 能独立写出判断重复元素的暴力法与哈希法。
- 能说明两种算法的时间和空间取舍。
- 岗位技能小项目的规定输出正确。

核心达到以上标准就进入DAY13。变量名称或输出排版等小问题只作为建议，不会掩盖核心掌握判断。

## 十二、本日参考范围

本日只参考《Python数据结构与算法分析（第2版）》第2章“算法分析”中大O记法、列表操作和字典操作的相关内容。教材用于核对原理；完成课程不要求你通读整章，也不要求背表格。
