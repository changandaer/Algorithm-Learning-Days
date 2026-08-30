# DAY09：函数巩固——参数要完整，返回值要守合同

> 预计用时：3.5～4 小时。今天不加入字典、类或新算法，只修复函数最重要的工程习惯。函数掌握牢固后，字典和Hot 100会更容易。

## 一、DAY08 验收结果：75 分

| 评分项目 | 得分 | 说明 |
|---|---:|---|
| 概念理解 | 18 / 25 | 理解形参/实参、局部计数器和 `return` 终止函数；对“返回结果”和“函数所需数据必须来自参数”仍有误解。 |
| 代码正确性 | 22 / 30 | 所有文件语法正确，主要规定结果能运行；多个函数签名与合同不符，空输入返回类型错误，覆盖率空核心清单除零。 |
| 独立实现与调试 | 18 / 20 | 完成所有必做和挑战题，能够独立使用 `def`、调用、返回和断言。 |
| 测试、边界与合同验收 | 9 / 15 | 已写断言，但部分断言是在证明自己修改后的错误合同；缺少自定义列表、空核心清单、多个答案等关键测试。 |
| Git 与表达 | 8 / 10 | 每项任务有提交，课后总结准确；检查时本地比 `origin/main` 多3个提交，尚未完全推送。 |
| **总分** | **75 / 100** | **函数语法已会，函数设计需要补练。** |

### 为什么今天不直接进入字典

字典和Hot 100都会大量使用函数。如果函数把数据写死、偷偷读取全局变量，算法即使在一个样例上通过，换输入就会失败。

这不是拖延进度，而是在修复一个会反复出现的根问题。DAY09达到80分后：

- DAY10学习字典/哈希表。
- DAY11正式完成Hot 100第一题“两数之和”。

---

## 二、DAY08全部示范答案与逐题对比

### 示范1：第一个函数

```python
def add(first_number, second_number):
    return first_number + second_number


assert add(1, 2) == 3
assert add(-1, 1) == 0
assert add(1.5, 2.5) == 4.0

print("add测试全部通过")
```

你的实现正确，浮点数隐藏测试也通过。注意逗号后留空格：`add(1.1, 2)`。

### 示范2：成绩等级函数

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

对比你的实现：

- 等级边界判断正确，函数内没有 `input()` 和 `print()`。
- 合同规定无效时返回 `"成绩无效"`，你改成了 `"成绩不合法，重新输入"`。文字本身没有绝对好坏，但函数实现和测试必须服从事先约定的合同，不能悄悄改需求后用断言证明自己正确。
- `return` 后函数已经结束，因此不需要最外层 `else`，可以减少缩进。
- 任务要求至少6个断言，你实际写了5个。

### 示范3：技能索引函数

```python
def find_skill_index(skills, target_skill):
    normalized_target = target_skill.strip().lower()

    for index in range(len(skills)):
        if skills[index] == normalized_target:
            return index

    return -1


assert find_skill_index(["python", "linux", "git"], "Linux") == 1
assert find_skill_index(["python", "linux", "git"], "git ") == 2
assert find_skill_index(["python"], "java") == -1
assert find_skill_index([], "python") == -1
```

对比你的实现：

- 固定技能列表中的查找结果正确，`return index` 使用正确。
- 合同要求两个输入：`skills`和`target_skill`。你的函数只有一个参数，并把列表写死在内部。
- 隐藏测试调用 `find_skill_index([], "python")` 时会报 `TypeError`，因为函数不接受两个参数。
- 人话解释：你造的不是“任何技能清单都能用的查找器”，而是“只能查你写死那一个清单的查找器”。

### 示范4：技能标准化去重函数

```python
def normalize_and_deduplicate(raw_skills):
    normalized_skills = []

    for raw_skill in raw_skills:
        skill = raw_skill.strip().lower()

        if skill != "" and skill not in normalized_skills:
            normalized_skills.append(skill)

    return normalized_skills


assert normalize_and_deduplicate(["Python", "PYTHON", " Git "]) == ["python", "git"]
assert normalize_and_deduplicate([]) == []
assert normalize_and_deduplicate(["", "   "]) == []
assert normalize_and_deduplicate([" Linux "]) == ["linux"]
```

对比你的实现：

- 普通大小写去重正确。
- 合同说“输入列表，输出列表”。你的空列表却返回字符串 `"输入为空，重新输入"`，导致同一函数有时吐列表、有时吐字符串。
- 隐藏输入 `[" Python ", "   ", "PYTHON"]` 会得到 `["python", ""]`，空字符串没有被过滤。
- 不需要判断 `raw_skills == ""`，因为合同已经规定输入是列表。若调用者传错类型，以后会学习异常处理；今天先守住合同。

### 示范5：两数之和函数

```python
def find_two_sum(numbers, target):
    for first_index in range(len(numbers)):
        for second_index in range(first_index + 1, len(numbers)):
            if numbers[first_index] + numbers[second_index] == target:
                return [first_index, second_index]

    return []


assert find_two_sum([2, 7, 11, 15], 9) == [0, 1]
assert find_two_sum([2, 7, 11, 15], 26) == [2, 3]
assert find_two_sum([2, 7, 11, 15], 14) == []
assert find_two_sum([3, 3], 6) == [0, 1]
assert find_two_sum([], 9) == []
```

对比你的实现：

- 固定列表的目标9、26、14结果正确。
- 合同要求 `numbers`和`target`两个参数，你只传目标，把列表写死。
- 因此无法测试 `[3, 3]`和空列表，隐藏调用会报 `TypeError`。
- 找到后你继续遍历并不断 `append`。如果固定列表中有两组答案，可能返回四个索引。示范直接 `return [first_index, second_index]`，第一组找到后整个函数立刻结束。

### 示范6：岗位技能覆盖率评估器

```python
def normalize_and_deduplicate(raw_skills):
    normalized_skills = []

    for raw_skill in raw_skills:
        skill = raw_skill.strip().lower()
        if skill != "" and skill not in normalized_skills:
            normalized_skills.append(skill)

    return normalized_skills


def find_missing_skills(core_skills, candidate_skills):
    missing_skills = []

    for core_skill in core_skills:
        if core_skill not in candidate_skills:
            missing_skills.append(core_skill)

    return missing_skills


def calculate_coverage(core_skills, candidate_skills):
    if len(core_skills) == 0:
        return 0.0

    covered_count = 0

    for core_skill in core_skills:
        if core_skill in candidate_skills:
            covered_count += 1

    return covered_count / len(core_skills) * 100


core = ["python", "c++", "pytorch", "linux", "git"]
candidate = normalize_and_deduplicate([" Python ", "Git", "linux", "PYTHON"])

assert find_missing_skills(core, candidate) == ["c++", "pytorch"]
assert calculate_coverage(core, candidate) == 60.0
assert calculate_coverage(core, core) == 100.0
assert calculate_coverage(core, []) == 0.0
assert calculate_coverage([], candidate) == 0.0
```

对比你的实现：

- 规定数据、全覆盖和完全未覆盖的结果正确。
- `find_missing_skills()`与`calculate_coverage()`没有接收`core_skills`参数，而是偷偷使用函数外的全局变量。
- 你测试的是“候选人技能为空”，不是“核心技能列表为空”。隐藏测试把核心列表设为空时出现`ZeroDivisionError`。
- 工作函数应把需要的原料都列在参数上。调用者看到函数名和参数，就知道它依赖什么，不需要翻到文件顶部寻找隐藏变量。

### 示范7：损失反弹函数

```python
def find_first_rebound_index(losses):
    for current_index in range(1, len(losses)):
        if losses[current_index] > losses[current_index - 1]:
            return current_index

    return -1


assert find_first_rebound_index([1.0, 0.8, 0.6, 0.7]) == 3
assert find_first_rebound_index([1.0, 0.8, 0.6]) == -1
assert find_first_rebound_index([1.0, 1.1]) == 1
assert find_first_rebound_index([]) == -1
assert find_first_rebound_index([1.0]) == -1
```

对比你的实现：

- 能正确返回第一次反弹索引，下降与单元素测试正确。
- 合同明确“没有反弹返回-1”，空列表也属于没有反弹。你却返回提示字符串，使返回类型不一致。
- `return`后面的`print()`永远执行不到，叫作**不可达代码（unreachable code）**。人话就是机器已经关机并把结果送出，后面的指令没人再执行。

---

## 三、理论回答中的两个小修正

### 1. `return`不是“把结果赋值给参数”

更准确的说法是：`return`把结果交还给调用者。调用者可以选择把它赋值给变量：

```python
result = add(2, 3)
```

这里是调用者把返回的5保存到`result`，不是函数把5赋给参数。

### 2. `assert`通过时不是“返回空值”

断言为真时，它只是安静地继续执行；为假时抛出`AssertionError`。它不是用来产生返回值的函数。

你关于Hot 100与OOP的回答内容正确。不过今后尽量再用自己的两三句话复述一次，确保不是只记住一段很完整的表述。

---

## 四、今天必须掌握的三个函数规则

### 规则1：所有原料都放进参数

专业说法：减少**隐式依赖（implicit dependency）**。

人话解释：做菜前把配料清单写在门口。不要做到一半，突然从别人冰箱里拿一个全局变量。

不推荐：

```python
core_skills = ["python", "git"]

def calculate_coverage(candidate_skills):
    # 偷偷依赖外面的core_skills
    ...
```

推荐：

```python
def calculate_coverage(core_skills, candidate_skills):
    ...
```

### 规则2：同一个函数始终返回同一种含义和类型

专业说法：保持**返回类型一致（consistent return type）**。

人话解释：自动售货机不能有时吐饮料，有时吐一张写着“没饮料”的纸。调用者会不知道接下来该喝还是该读。

```python
def normalize_skills(raw_skills):
    if raw_skills == []:
        return []
    return ["python"]
```

无论有无数据，都返回列表。

### 规则3：测试合同，不要为现有代码改合同

如果合同写“找不到返回-1”，代码返回字符串，正确动作是修代码，不是把断言改成期待字符串。

先写预期：

```python
assert find_first_rebound_index([]) == -1
```

再让实现通过。这种方式以后叫**测试驱动开发（Test-Driven Development，TDD）**的一部分。今天只理解思想，不要求背流程。

---

## 五、DAY09代码任务

### 任务0：修复成绩等级合同（必做，25～30分钟）

文件：`00_修复_成绩等级合同.py`

- `get_grade(score)`必须严格返回A/B/C/D或`"成绩无效"`。
- 函数内不输入、不打印。
- 先写六个规定断言，再写函数，让测试通过。

### 任务1：修复技能查找参数（必做，30～40分钟）

文件：`01_修复_技能查找参数.py`

- 函数签名必须是`find_skill_index(skills, target_skill)`。
- 不准在函数内部写死技能列表。
- 测试两个完全不同的技能列表、空列表、找不到。

### 任务2：修复标准化返回类型（必做，35～45分钟）

文件：`02_修复_标准化返回类型.py`

- 输入始终按字符串列表处理。
- 输出始终是列表。
- 空列表返回`[]`。
- 清理后为空的字符串不加入。
- 不修改传入的原列表。

### 任务3：修复两数之和参数与立即返回（必做，40～50分钟）

文件：`03_修复_两数之和参数.py`

- 签名`find_two_sum(numbers, target)`。
- 找到第一组立即返回两个索引。
- 找不到返回`[]`。
- 测试多个不同列表，其中一组数据要存在两个答案，确认只返回第一组。

### 任务4：修复覆盖率的全局依赖（必做，45～60分钟）

文件：`04_修复_覆盖率全参数.py`

- `find_missing_skills(core_skills, candidate_skills)`。
- `calculate_coverage(core_skills, candidate_skills)`。
- 函数内部不得读取同名全局列表。
- 空核心清单返回0.0。
- 用两套完全不同的核心技能清单测试，证明函数不是只对固定数据有效。

### 任务5：修复损失反弹合同（必做，25～35分钟）

文件：`05_修复_损失反弹合同.py`

- 所有没有反弹的情况都返回-1，包括空列表和单元素。
- 删除`return`后的不可达代码。
- 覆盖五个规定断言。

### 任务6：阶段验收——函数工具箱（必做，50～60分钟）

文件：`06_阶段验收_函数工具箱.py`

闭卷完成三个小函数：

```text
normalize_skill(raw_skill) -> 标准化后的字符串
find_skill_index(skills, target_skill) -> 索引或-1
find_two_sum(numbers, target) -> 两个索引列表或空列表
```

每个函数先写四行合同，再写至少三个断言。不得读取其他DAY09答案，不使用AI生成代码。到时保留真实结果。

---

## 六、理论回答

1. 为什么`find_two_sum`必须同时接收`numbers`和`target`？
2. 函数读取全局变量有什么问题？用做菜类比解释。
3. 为什么标准化函数不能有时返回列表、有时返回提示字符串？
4. 合同规定空列表返回-1时，能否把测试改成期待提示字符串？为什么？
5. `return`后面的代码为什么执行不到？
6. “候选技能为空”和“核心技能为空”是同一个边界吗？分别预期什么覆盖率？
7. 你会怎样证明一个函数可以处理两套不同数据，而不是只对写死样例有效？

## 七、DAY09解锁标准

- 总分达到80。
- 所有函数需要的数据都通过参数传入。
- 每个函数各条路径返回类型一致。
- 两数之和能更换列表并通过多解、空列表测试。
- 覆盖率能处理空核心技能列表。
- 闭卷函数工具箱保留真实结果。

达到后DAY10学习字典/哈希表，DAY11正式开始Hot 100；未达到则继续缩小练习，不把核心误解带入下一阶段。

## 八、Git提醒

当前本地分支比GitHub多3个提交。完成同步前运行：

```bash
git push
```

DAY09建议提交：

```text
fix(day09): 让函数通过参数接收全部数据
test(day09): 增加返回类型与空输入测试
review(day09): 完成函数工具箱闭卷验收
```

---

## 九、我的回答（也可以写入课后总结）

### 1. 为什么两数之和必须接收numbers和target？


### 2. 函数读取全局变量有什么问题？


### 3. 为什么返回类型必须一致？


### 4. 能否为现有错误代码修改合同？为什么？


### 5. return后的代码为什么执行不到？


### 6. 候选技能为空和核心技能为空分别意味着什么？


### 7. 怎样证明函数没有写死数据？


