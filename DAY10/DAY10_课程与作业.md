# DAY10：用失败测试逼出真正正确的函数

> 预计用时：3.5～4小时。今天不增加字典或新算法，只使用已经学过的函数、列表、循环和`assert`。学习方式改成：先看失败证据，再做最小修复。

## 一、DAY09验收结果：78分

| 评分项目 | 得分 | 说明 |
|---|---:|---|
| 概念理解 | 20 / 25 | 已理解全局依赖、返回类型合同和不同边界；部分答案较像资料表述，需要继续用代码证明理解。 |
| 代码正确性 | 22 / 30 | 成绩、标准化和损失反弹正确；技能索引、两数之和与空核心覆盖率仍有关键漏洞。 |
| 独立实现与调试 | 18 / 20 | 所有任务和闭卷验收均完成，函数参数化明显进步。 |
| 测试与边界 | 8 / 15 | 多项普通测试通过，但明确要求的多解与空核心测试没有落实；闭卷中同类错误再次出现。 |
| Git与表达 | 10 / 10 | 仓库干净，本地与`origin/main`完全同步；提交和总结完整。 |
| **总分** | **78 / 100** | **接近通过，但关键失败必须在代码中修复。** |

### 为什么理论会了，代码仍会错

你已经能说出“数据应该由参数传入”“合同不能随便改”，但写代码时仍容易把注意力放在规定样例能否通过，而没有主动攻击自己的实现。

这叫“知道规则”和“形成习惯”之间的距离。DAY10不再要求先写很多分析，而是直接把最容易揭露错误的测试交给程序运行。红色报错会明确告诉你哪里还没满足合同。

---

## 二、DAY09全部示范答案与评语

### 示范1：成绩等级合同

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


assert get_grade(90) == "A"
assert get_grade(89) == "B"
assert get_grade(60) == "C"
assert get_grade(59) == "D"
assert get_grade(101) == "成绩无效"
assert get_grade(-1) == "成绩无效"
```

你的函数逻辑与合同完全一致，隐藏边界全部通过。任务要求六个断言，你仍只写了五个；函数正确不等于验收清单可以跳项。

### 示范2：返回原列表索引的技能查找

```python
def find_skill_index(skills, target_skill):
    normalized_target = target_skill.strip().lower()

    for index in range(len(skills)):
        normalized_skill = skills[index].strip().lower()

        if normalized_skill == normalized_target:
            return index

    return -1


assert find_skill_index(["python", "linux", "git"], "Git") == 2
assert find_skill_index(["python", "python", "git"], "git") == 2
assert find_skill_index([], "python") == -1
```

对比你的实现：

- 参数已经完整，空列表和普通查找正确。
- 你先对技能列表去重，再返回去重列表的索引。输入`["python", "python", "git"]`时，原列表中的git索引为2，去重后却变成1。
- 专业上这叫改变了**索引语义**。人话解释：题目问原教室的座位号，你先让重复姓名的人离场并重新排座位，返回的已经不是原座位号。
- 查找不需要去重，只需在比较时标准化当前元素。

### 示范3：标准化并去重

```python
def normalize_and_deduplicate(skills):
    normalized_skills = []

    for raw_skill in skills:
        skill = raw_skill.strip().lower()
        if skill != "" and skill not in normalized_skills:
            normalized_skills.append(skill)

    return normalized_skills
```

你的实现正确：空列表返回列表，空字符串被过滤，原列表没有被修改，所有隐藏测试通过。可以改进的是把重复的`skill.strip().lower()`先存进局部变量，避免同一轮计算三次。

### 示范4：只返回第一组两数之和

```python
def find_two_sum(numbers, target):
    for first_index in range(len(numbers)):
        for second_index in range(first_index + 1, len(numbers)):
            if numbers[first_index] + numbers[second_index] == target:
                return [first_index, second_index]

    return []


assert find_two_sum([2, 7, 11, 15], 9) == [0, 1]
assert find_two_sum([1, 4, 2, 3], 5) == [0, 1]
assert find_two_sum([3, 3], 6) == [0, 1]
assert find_two_sum([], 9) == []
```

对比你的实现：

- 函数已经接收`numbers`和`target`，普通、无答案、空列表测试通过。
- 找到后仍然继续循环并`append`。隐藏多解`[1,4,2,3]`、目标5会返回`[0,1,2,3]`。
- 任务明确要求“第一组立即返回”，正确动作是直接`return [first_index, second_index]`，不需要先建立`target_index`。
- 这项要求在DAY08、DAY09和闭卷验收中连续遗漏，DAY10会把它做成固定回归测试。

### 示范5：覆盖率全参数与空核心清单

```python
def find_missing_skills(core_skills, candidate_skills):
    normalized_candidates = []

    for raw_skill in candidate_skills:
        skill = raw_skill.strip().lower()
        if skill != "" and skill not in normalized_candidates:
            normalized_candidates.append(skill)

    missing_skills = []

    for core_skill in core_skills:
        if core_skill not in normalized_candidates:
            missing_skills.append(core_skill)

    return missing_skills


def calculate_coverage(core_skills, candidate_skills):
    if len(core_skills) == 0:
        return 0.0

    missing_skills = find_missing_skills(core_skills, candidate_skills)
    covered_count = len(core_skills) - len(missing_skills)
    return covered_count / len(core_skills) * 100


assert calculate_coverage(["python", "git"], ["Python"]) == 50.0
assert calculate_coverage(["docker"], ["Docker"]) == 100.0
assert calculate_coverage(["python"], []) == 0.0
assert calculate_coverage([], ["python"]) == 0.0
```

对比你的实现：

- 全局依赖已经修复，两套非空核心清单都能工作。
- 课程明确要求空核心清单返回0.0，但实现中没有`len(core_skills) == 0`保护，隐藏测试出现`ZeroDivisionError`。
- 你测试了候选技能为空，却没有测试核心技能为空。两者不是同一个边界。

### 示范6：损失反弹合同

```python
def find_first_rebound_index(losses):
    for current_index in range(1, len(losses)):
        if losses[current_index] > losses[current_index - 1]:
            return current_index

    return -1
```

你的实现与示范等价，五类测试全部通过，没有不可达代码。

### 示范7：闭卷函数工具箱

```python
def normalize_skill(raw_skill):
    return raw_skill.strip().lower()


def find_skill_index(skills, target_skill):
    normalized_target = normalize_skill(target_skill)

    for index in range(len(skills)):
        if normalize_skill(skills[index]) == normalized_target:
            return index

    return -1


def find_two_sum(numbers, target):
    for first_index in range(len(numbers)):
        for second_index in range(first_index + 1, len(numbers)):
            if numbers[first_index] + numbers[second_index] == target:
                return [first_index, second_index]

    return []
```

对比你的闭卷结果：

- 三个函数都能定义、调用并返回，说明函数基本结构已经掌握。
- 题目中的`normalize_skill(raw_skill)`是处理一个字符串，你把它写成处理整个列表。函数名、参数单复数和实际工作不一致。
- 查找函数先去重，再用原列表长度访问去重列表。输入`["python", "python"]`并查找java时会`IndexError`。
- 两数之和再次出现多解累计问题。
- 这说明你需要让测试主动覆盖“重复但找不到”和“存在多组答案”，而不是再读一遍理论。

---

## 三、你的Python进阶问题：都会不会学？

会学，但不会一次性塞在算法开始之前。

“Python基础扎实”不等于先把所有高级语法看完。我们按工作中出现的时机分三层：

| 优先层 | 内容 | 安排方式 |
|---|---|---|
| 近期必需 | 字典、集合、元组、可变与不可变、文件、异常、模块、基本类 | DAY11之后及第一阶段项目中逐步学习 |
| 工程常见坑 | 可变默认参数、深浅拷贝、`*args/**kwargs`、类型提示 | 在函数、配置和项目重构中结合真实错误学习 |
| 后期工程能力 | 生成器、装饰器、迭代协议 | DataLoader、训练流水线、日志和API阶段按使用场景学习 |
| 系统与性能 | Python对象/引用、引用计数与垃圾回收、GIL、线程与进程 | Linux、性能分析和分布式训练阶段学习，并与C++内存模型对照 |

几点需要澄清：

- GIL中文通常叫**全局解释器锁**，不是“全剧解释器锁”。
- 装饰器、生成器很有用，但不是开始LeetCode的前置条件。
- 深浅拷贝和可变默认参数会在项目真正出现数据被意外修改时学习，理解会比提前背面试答案更牢。
- 算法训练不会等全部高级Python学完；高级Python也不会被跳过，而是与项目和工程阶段交叉复现。

---

## 四、今天的新学习方式：红—绿—整理

这是测试驱动开发中常见的节奏：

### 红：先看测试失败

```python
assert find_two_sum([1, 4, 2, 3], 5) == [0, 1]
```

旧实现返回四个索引，断言变红。

### 绿：只做最小修改让它通过

把累计索引改成找到后直接`return`。先不追求漂亮，确认所有测试变绿。

### 整理：测试保护下改善代码

测试全通过后，再改变量名、空格和重复逻辑。每改一次重新运行测试。

专业叫**红—绿—重构（Red-Green-Refactor）**。人话就是：先让警报响起来，修到警报消失，再把现场整理干净。

### 回归测试不只是大项目才有

把下面三个曾经失败的输入固定保存，就是你的第一组高价值回归测试：

```python
assert find_skill_index(["python", "python", "git"], "git") == 2
assert find_two_sum([1, 4, 2, 3], 5) == [0, 1]
assert calculate_coverage([], ["python"]) == 0.0
```

以后修改函数，每次都运行它们。老错误重新出现时，测试立刻报警。

---

## 五、DAY10代码任务

### 任务0：跟做红—绿—整理（必做，25～30分钟）

文件：`00_跟做_红绿整理.py`

文件提供一个错误的分数合法性函数和两个断言。先运行看`AssertionError`，再做最小修复，最后整理命名。记录红、绿两个终端结果。

### 任务1：修复原始索引语义（必做，30～40分钟）

文件：`01_修复_技能查找原始索引.py`

- 先运行文件中预置的重复技能测试，确认旧实现失败。
- 不对列表去重，只在比较双方时标准化。
- 返回原列表真实索引。
- 增加“重复且找不到”测试，确保不越界。

### 任务2：修复两数之和第一组（必做，30～40分钟）

文件：`02_修复_两数之和第一组.py`

- 预置多解断言必须先失败。
- 找到第一组后直接返回。
- 测试多解、相同值不同索引、无答案、空列表。
- 用一句话解释为什么不再需要`target_index.append()`。

### 任务3：修复空核心覆盖率（必做，30～40分钟）

文件：`03_修复_空核心覆盖率.py`

- 先运行空核心测试，看见`ZeroDivisionError`。
- 在除法之前处理空核心清单，返回0.0。
- 分别测试候选为空、核心为空、全覆盖、部分覆盖。

### 任务4：修复闭卷工具箱边界（必做，35～45分钟）

文件：`04_修复_函数工具箱边界.py`

- `normalize_skill`只处理一个字符串并返回字符串。
- `find_skill_index`不去重、不越界。
- 两个函数不得读全局列表。
- 预置的重复、空列表和空字符串断言全部通过。

### 任务5：小项目——岗位指标回归测试集V1（必做，45～60分钟）

文件：`05_小项目_岗位指标回归测试集V1.py`

整理三个可复用函数：

```text
normalize_and_deduplicate(skills) -> 列表
find_missing_skills(core_skills, candidate_skills) -> 列表
calculate_coverage(core_skills, candidate_skills) -> 浮点数
```

建立至少六条固定回归测试：规定数据、全覆盖、候选为空、核心为空、重复候选、包含空字符串。每条断言带一条失败提示，例如：

```python
assert actual == expected, f"预期{expected}，实际{actual}"
```

这份测试集是面向小鹏评估开发和AI工程岗位的基础作品证据：不仅会写计算逻辑，还能定义边界并防止旧问题复发。

### 任务6：函数最终闸门（闭卷，45分钟）

文件：`06_阶段验收_函数最终闸门.py`

关闭DAY08～10和AI，只完成两个函数：

```text
find_skill_index(skills, target_skill) -> 原始索引或-1
find_two_sum(numbers, target) -> 第一组索引或[]
```

测试已经预置，不允许修改测试适应代码。45分钟结束时保留现场。

---

## 六、理论回答

1. 为什么查找前去重会改变“原始索引”的含义？
2. 为什么两数之和找到第一组后应直接`return`？
3. 核心技能为空为什么必须在除法前单独处理？
4. 什么是回归测试？请用`Linux`大小写错误或多解两数之和举例。
5. 红—绿—整理三个阶段分别做什么？
6. 为什么不能修改测试去适应不符合合同的实现？
7. 装饰器、生成器和GIL为什么不需要在Hot 100前一次学完？
8. 今天哪条失败测试最能帮助你理解代码问题？

## 七、解锁标准

- 所有预置失败测试由红变绿。
- 原始索引重复测试通过。
- 两数之和多解只返回第一组。
- 空核心覆盖率返回0.0。
- 闭卷闸门两函数通过，不修改预置测试。
- 能用自己的话解释回归测试。

达到80分后，DAY11进入字典/哈希表；DAY12正式开始Hot 100第一题。

---

## 八、我的回答（也可以写课后总结）

### 1. 去重为什么会改变原始索引？


### 2. 两数之和为什么直接return？


### 3. 空核心为什么在除法前处理？


### 4. 什么是回归测试？


### 5. 红—绿—整理分别是什么？


### 6. 为什么不能修改测试迁就错误实现？


### 7. 为什么高级Python不用在Hot 100前学完？


### 8. 哪条失败测试最有帮助？


