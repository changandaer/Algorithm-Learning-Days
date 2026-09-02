# DAY11：Hot 100第一题——两数之和

> 预计用时：3.5～4小时。今天只围绕一道题学习：LeetCode 1“两数之和”。目标不是背答案，而是能解释暴力法为什么慢、哈希法为什么快，并能关闭答案后手写。

## 一、DAY10核心验收：84分，通过

| 检查项目 | 结果 | 说明 |
|---|---|---|
| 字典的键和值 | 通过 | 能正确解释并读写键值。 |
| 字典计数 | 通过 | `get(skill, 0) + 1`使用正确。 |
| 字典遍历 | 通过 | 能使用普通遍历和`items()`。 |
| 技能统计函数 | 通过 | 普通、大小写、空输入结果正确。 |
| 岗位频率项目 | 通过 | 正确得到python/linux 3次、git/pytorch 2次等结果。 |
| 列表与字典的选择 | 需补充 | 字典不是更高级；通过位置访问用列表，通过键映射数据用字典。 |
| 哈希两数之和 | 尚未完成 | 是选做挑战，不影响字典核心通过，DAY11正式学习。 |

### 主要评语

你已经能用字典解决“名称对应次数”的问题，而不是只会写字典语法。小项目是最有力的掌握证据，因此进入Hot 100。

需要保留的改进：

- 成绩分布使用多个独立`if`，导致95分同时计入A、B、C。互斥等级要用`if/elif/elif/else`。
- 合并字典时`merge_counts = first_counts`只是让两个名字指向同一个字典，因此原字典被修改。复制问题会在后续“可变对象”课程中详细学习。
- 挑战文件中的`numbers[]`缺少索引，存在语法错误。DAY11会把这句话拆成完整代码。

这些问题会继续修正，但不改变“字典核心已掌握”的结论。

---

## 二、DAY10示范答案

### 1. 字典统计次数

```python
skills = ["python", "git", "python", "linux", "git", "python"]
skill_counts = {}

for skill in skills:
    skill_counts[skill] = skill_counts.get(skill, 0) + 1

print(skill_counts)
```

你的实现与示范一致，结果完全正确。

### 2. 技能次数统计函数

```python
def count_skills(raw_skills):
    skill_counts = {}

    for raw_skill in raw_skills:
        skill = raw_skill.strip().lower()
        if skill != "":
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    return skill_counts
```

你的结果正确。你先建立标准化列表再计数；示范边标准化边计数，少保存一个中间列表。两种方法都能体现字典核心。

### 3. 成绩等级分布

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


def count_grades(scores):
    grade_counts = {}

    for score in scores:
        grade = get_grade(score)
        grade_counts[grade] = grade_counts.get(grade, 0) + 1

    return grade_counts
```

你的字典更新写法没有问题，错误来自等级判断没有互斥。规定输入的实际结果是A 2、B 4、C 5、D 1，而且无效成绩被跳过；预期是A 2、B 2、C 1、D 1、无效1。

### 4. 合并两个计数字典

```python
def merge_counts(first_counts, second_counts):
    merged_counts = {}

    for skill, count in first_counts.items():
        merged_counts[skill] = count

    for skill, count in second_counts.items():
        merged_counts[skill] = merged_counts.get(skill, 0) + count

    return merged_counts
```

你的合并结果正确，但`merge_counts = first_counts`会同时修改`first_counts`。示范建立真正的新字典，保持两个输入不变。

### 5. 最高频技能

```python
def find_most_common_skill(skill_counts):
    if skill_counts == {}:
        return ""

    most_common_skill = ""
    highest_count = -1

    for skill, count in skill_counts.items():
        if count > highest_count:
            most_common_skill = skill
            highest_count = count

    return most_common_skill
```

你的普通、并列和空字典结果正确，已掌握“遍历字典并保存目前冠军”的思路。

### 6. 岗位技能频率分析器

```python
def analyze_job_skills(job_skill_lists):
    skill_counts = {}

    for job_skills in job_skill_lists:
        for raw_skill in job_skills:
            skill = raw_skill.strip().lower()
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    most_common_skill = find_most_common_skill(skill_counts)
    frequent_skills = []

    for skill, count in skill_counts.items():
        if count >= 2:
            frequent_skills.append(skill)

    return skill_counts, most_common_skill, frequent_skills
```

你的规定结果全部正确。你把多个结果拼成一个字符串，当前可以运行；以后学习元组后，会像示范一样返回多个结构化结果，方便其他代码继续使用。

### 7. 两数之和哈希解法

```python
def find_two_sum_with_hash(numbers, target):
    seen = {}

    for index in range(len(numbers)):
        number = numbers[index]
        needed = target - number

        if needed in seen:
            return [seen[needed], index]

        seen[number] = index

    return []
```

你卡住的`numbers[]`应该写成`numbers[index]`：当前循环走到哪个位置，就用当前索引取出那个数字。

---

## 三、DAY10理论题示范回答

1. `{"python": 2}`中，`"python"`是键，2是对应的值。
2. 列表主要根据索引访问，字典主要根据键访问。
3. 方括号访问不存在的键会出现`KeyError`；`get(key, default)`在键不存在时返回默认值。
4. 字典把技能和次数直接绑在一起，不需要维护两个位置必须永远对齐的列表。
5. `get(skill, 0) + 1`表示：以前有记录就拿旧次数加1，没有记录就从0加到1。
6. 平均O(1)表示数据数量大幅增加时，通过键查找的平均步骤不会按数据量同比增加。
7. 字典不是总比列表更好。需要顺序和索引时用列表，需要键值映射时用字典。
8. 岗位技能频率分析器最接近工作中的数据统计，因为它把多份输入标准化、汇总并输出指标。

---

## 四、Git push报错的实际原因

这次不只是网络波动。当前状态是：

- 本地`main`比远程多6个提交。
- 远程`origin/main`多一个`Delete .gitignore`提交。
- 本地还有尚未提交的`DAY10/课后总结.md`修改。

这种状态叫分支发生了分叉。普通`git push`会被拒绝，因为Git不愿直接覆盖远程提交。

先决定GitHub上删除`.gitignore`是不是你故意做的。

### 如果删除是故意的

先提交当前修改，然后：

```bash
git pull --rebase origin main
git push origin main
```

### 如果删除是误操作，希望保留`.gitignore`

先提交当前修改，然后：

```bash
git pull --rebase origin main
git restore --source=f1b72df -- .gitignore
git add .gitignore
git commit -m "chore: 恢复gitignore"
git push origin main
```

不要使用`git push --force`。如果执行`pull --rebase`出现冲突，保留终端原文并让我检查，不要随意删除文件。

---

## 五、今天的题目：两数之和

### 题意

给一个整数列表`nums`和目标值`target`，找出两个不同位置，使对应数字相加等于目标值，返回两个索引。

例如：

```text
nums = [2, 7, 11, 15]
target = 9
输出 = [0, 1]
```

题目通常保证只有一组答案，并且同一元素不能使用两次。

---

## 六、固定三步法分析

### 第一步：最小输入和输出

```text
输入：[2, 7]，目标9
输出：[0, 1]
```

### 第二步：切成代码阶段

暴力法：

```text
选择第一个位置
选择它后面的第二个位置
检查两数之和
找到就返回
```

哈希法：

```text
建立空字典seen
逐个查看数字
计算当前还需要哪个数
查看需要的数以前是否出现
出现就返回两个索引
没出现就记录当前数字和索引
```

### 第三步：边写边用小数据检查

哈希法需要保存的状态：

```text
seen = 以前出现的数字 -> 它的索引
```

---

## 七、暴力解法

```python
def two_sum_brute_force(nums, target):
    for first_index in range(len(nums)):
        for second_index in range(first_index + 1, len(nums)):
            if nums[first_index] + nums[second_index] == target:
                return [first_index, second_index]

    return []
```

如果有n个数字，最坏情况下大约要进行n×n级别的检查，时间复杂度是O(n²)。

人话解释：每个人都要和后面几乎所有人握一次手。人数翻十倍，握手次数可能接近翻一百倍。

---

## 八、哈希解法逐轮跟踪

```python
nums = [2, 7, 11, 15]
target = 9
```

| 当前索引 | 当前数字 | 还需要`target-number` | 检查前的`seen` | 动作 |
|---:|---:|---:|---|---|
| 0 | 2 | 7 | `{}` | 7没出现，记录`2: 0` |
| 1 | 7 | 2 | `{2: 0}` | 2出现过，返回`[0, 1]` |

完整代码：

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

### 为什么先检查，再记录当前数字

对`[3, 3]`、目标6：

- 第一个3没有找到旧3，记录`3: 0`。
- 第二个3发现旧3，返回`[0, 1]`。

如果先记录当前3，再检查，第一次就可能错误返回`[0, 0]`，相当于同一个位置使用两次。

### 复杂度

- 时间复杂度：平均O(n)。列表只遍历一遍，每次字典查找平均接近O(1)。
- 空间复杂度：O(n)。最坏情况下字典要保存接近n个数字。

人话解释：速度变快的代价是多准备一个字典来记住以前见过的数字。

---

## 九、LeetCode的`class Solution`是什么

平台会给出：

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}

        for index in range(len(nums)):
            number = nums[index]
            needed = target - number

            if needed in seen:
                return [seen[needed], index]

            seen[number] = index

        return []
```

今天只需要这样理解：

- `Solution`是平台准备的工具箱。
- `twoSum`是工具箱中的一个函数，正式名称叫方法。
- `self`表示当前这个工具箱对象，平台会自动处理。
- 你今天真正需要掌握的是`twoSum`内部算法。

完整的类、对象和构造方法会按原计划单独学习。

本地测试：

```python
solution = Solution()
assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]
assert solution.twoSum([3, 2, 4], 6) == [1, 2]
assert solution.twoSum([3, 3], 6) == [0, 1]
```

---

## 十、DAY11代码任务

所有任务继续只用固定三步法。

### 任务0：修复成绩等级分布（热身，20～25分钟）

文件：`00_热身_修复成绩等级分布.py`

把等级判断改为互斥结果，规定输入必须得到A 2、B 2、C 1、D 1、成绩无效1。完成后不继续扩展。

### 任务1：暴力解法跟做（必做，30～40分钟）

文件：`01_跟做_两数之和暴力法.py`

分段手敲暴力法，测试三组规定数据，并解释为什么内层从`first_index + 1`开始。

### 任务2：哈希解法逐轮记录（必做，35～45分钟）

文件：`02_跟做_两数之和哈希法.py`

手敲哈希解法。暂时增加调试输出：

```python
print(index, number, needed, seen)
```

观察字典每轮怎样变化，理解后再删除调试输出。

### 任务3：闭卷手写普通函数（必做，35分钟）

文件：`03_独立_闭卷两数之和函数.py`

关闭DAY11课程，从空白实现`two_sum_hash(nums, target)`。不得查看答案。规定测试已写在文件注释中。

### 任务4：LeetCode格式手写（必做，30～40分钟）

文件：`04_独立_LeetCode两数之和.py`

使用`class Solution`格式实现并本地运行三个断言。完成后可以将方法内容手敲到LeetCode提交。

### 任务5：暴力与哈希对比（必做，30～40分钟）

文件：`05_实验_暴力与哈希对比.py`

两个函数都处理同一批测试，确认返回索引对应的数字之和确实等于目标。用自己的话写出时间和空间差别。

### 任务6：岗位技能快速索引器（独立，45～60分钟）

文件：`06_小项目_岗位技能快速索引器V1.py`

给定岗位技能列表，建立：

```text
技能名称 -> 第一次出现的原始索引
```

提供`find_skill_index_with_hash(skills, target_skill)`，使用字典快速返回索引或-1。测试大小写、重复技能、找不到和空列表。

---

## 十一、理论回答

1. 两数之和的`seen`字典中，键和值分别保存什么？
2. `needed = target - number`用人话是什么意思？
3. 为什么要先检查`needed`，再把当前数字放入`seen`？
4. 暴力法O(n²)与哈希法平均O(n)的差别是什么？
5. 哈希法为什么需要O(n)额外空间？
6. `[3, 3]`、目标6为什么能正确返回两个不同索引？
7. `class Solution`和`self`今天需要理解到什么程度？
8. 不看代码，口述哈希解法的三个阶段。

## 十二、DAY11通过标准

- 能手动跟踪`seen`的变化。
- 能解释`needed`。
- 能闭卷写出普通函数版哈希解法。
- 能使用LeetCode的`class Solution`外壳。
- 三组核心测试正确。
- 能解释时间换空间的取舍。

代码格式或额外边界仍会给建议，但不会掩盖以上核心判断。

---

## 十三、我的回答（也可以写课后总结）

### 1. seen的键和值是什么？


### 2. needed是什么意思？


### 3. 为什么先检查再记录？


### 4. O(n²)和平均O(n)有什么区别？


### 5. 为什么需要O(n)额外空间？


### 6. 两个3为什么不会使用同一索引？


### 7. class Solution和self需要理解什么？


### 8. 口述哈希解法三个阶段。


