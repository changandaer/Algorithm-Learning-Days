# DAY26｜字典记住“谁”，栈记住“最近谁没处理完”，模型开始更新参数

> 根据DAY25实际提交和《课后总结.md》调整。今天只有这一份课程和五份留白练习；自己写三步分析，不增加TODO或记录表。旧作业不改，不安装新工具，全部在Mac本地运行。
>
> 先说明调整：你明确表示LC20没有思路、字典有所遗忘。今天复习位换成字典综合题，LC20先讲透并给昨日完整参考，再做新题1047。LC20仍是待独立完成，不会因为看过答案就记为通过。模型先新增一个更新器，完成一次全批量更新；Trainer的组合移到DAY27与训练循环衔接，不删除阶段目标。

## 一、DAY25检查与评语

已阅读五份代码、注释和《课后总结.md》，运行已实现代码并更换输入测试。部分提交按实际证据评价，不将空白当成“算法写错”。

| 内容 | 实际结果 | 结论 |
|---|---|---|
| LC20有效括号 | 文件只有说明，没有实现 | 尚未完成；需要补“题意如何转成栈中状态”，不是再背一遍栈定义 |
| LC35搜索插入位置 | 1,143组输入通过，原列表未改变 | 二分稳定，可以继续新题，不重讲已经会的部分 |
| C++区间判断 | 无警告编译；函数858组输入通过 | 参数、bool返回、端点判断正确；你用两组输入连续调用，能工作 |
| C++范围筛选求和 | 无警告编译；函数1,573组输入通过，另测连续调用 | DAY20忽略start的问题已修正；循环、局部累计及空范围处理正确 |
| mean平均损失 | 7,380组预测/标签列表通过 | return已经移出循环，之前的核心问题已修复，不再反复扣同一个问题 |
| LossEvaluator | 4份数据×12组模型参数通过，参数不被评估修改 | 对象组合的实际代码正确；你在心得里的职责解释也正确 |
| 参数变化实验 | 实际运行的是四样本版本，数值正确 | 创建了单样本评估器，但没有调用它做试探，也没有计算单样本精确偏导数；这部分目标尚未完成 |
| 独立副本短检查 | 没有相关容器和断言实现 | 保留待验证，不因此停掉C++函数学习 |

二分测试是−3至3组成的非空升序数组、目标−4至4。C++区间测试覆盖负数、两端点及区间外；求和覆盖起点高于终点、阈值低于起点或高于终点。mean测试覆盖长度1—4、元素来自−1/0/2的预测与标签组合。教师测试不是你的闭卷独立性证据，本次不虚构总分。

**评语：已写部分的正确性比上一天更稳定。现在主要短板是“看懂一种操作之后，怎样选它来解决题目”，以及“实验实际用的是哪份数据”。这两点决定接下来的讲法，而不是变量命名或空行。**

### 1. 哪些不需要改成老师的写法

- C++的`and`是`&&`的合法替代写法，不是把Python语法误搬过来。你的编译和运行都通过。示范用&&只是常见风格。[官方说明](https://learn.microsoft.com/en-us/cpp/cpp/logical-and-operator-amp-amp?view=msvc-170)
- 求和用while没有错；你在if和else里都推进value，不会卡住。示范把共同的推进写在分支外，是减少重复，不是另一种算法。
- 区间题的main读取两组数据、输出两个判断，是可用的本地测试版本；昨天约定的标准输入是一组。示范用一组终端输入加断言检查重复调用，统一使用方式，不否定你的函数。
- LossEvaluator里保存属性叫data而非dataset都可以。直接把data.ys交给mean在当前接口中也能工作。

### 2. 模型后半段的差别不是“数算错了”

你创建了`dataset_2 = RegressionDataset([2], [5])`和`loss_evaluate_2`，但后面的循环调用的是另一个四样本evaluator。因此输出基准损失1.75、变化率接近−2与−1.5，都符合那四条数据。

DAY25要求的单样本是x=2、y=5，基准损失应为4.5，变化率接近−6与−3。**对象创建好了，不表示后面的计算已经使用它。** 今天算更新前，先明确“哪个评估器、哪份数据、哪个模型”，不靠记住某个数判断正确。

## 二、昨天理论回答的参考与补充

1. 你已经正确区分pop和[-1]。括号数量相同仍不合法的具体原因是：在`([)]`里读到`)`时，最近未配对的左括号是`[`，它不能被`)`关闭。缺的不是计数，而是未完成括号的先后顺序。下文会逐字符讲清。
2. return把结果交给调用者并结束本次调用；cout只输出显示，你答对了。求和函数每次从0开始，是因为本题要求每次独立求和，不是“所有函数的累计状态永远必须为0”。
3. 数据集取样、model预测、损失对象评分，你答对了；mean在第一轮return会提前结束整个函数，你也已通过代码修正。
4. 这一问尚未回答：单条损失`L=(wx+b−y)²/2`，令`e=wx+b−y`，对w的偏导数是e×x，对b是e。因为w改变h会让预测改变x×h，而b改变h只让预测改变h。只动w时固定b、x、y以及损失定义，才能单独衡量w方向的影响。今天在此基础上学习真正的参数更新。

## 三、先回应“栈和LC20到底有什么关系”

### 1. 从问题出发，不从容器名字出发

想象你正在阅读`([])`。读到`(`时，事情还没做完：后面必须有对应的`)`。接着读到`[`，又开了一个内层；此时不能先关外层，必须先关最近打开的`[`。

因此需要一份记录，保存“目前还没有关闭的左括号”。最晚加入这份记录的，是眼下最先要处理的。**栈就是为“最后加入、最先处理”这种顺序服务的工具。** 不是看到括号就凭记忆写stack，而是这个顺序要求自然需要它。

下面用列表从左到右表示由栈底到栈顶，右端是最近打开的括号：

| 当前字符 | 处理前未关闭的括号 | 发生了什么 | 处理后 |
|---|---|---|---|
| `(` | 空 | 新开一层 | `(` |
| `[` | `(` | 在里面再开一层 | `( [` |
| `]` | `( [` | 关闭最近的`[` | `(` |
| `)` | `(` | 关闭剩下的`(` | 空 |

对`([)]`，前两步相同，第三步读到`)`时却看到栈顶为`[`，冲突已经发生。不能跑去找栈底那个`(`来配对，否则相当于绕过了尚未关闭的内层。

还有两种失败：读到右括号但记录为空，例如`)`；整串读完记录仍有东西，例如`((`。所以“这次配对成功”不能马上返回True，后面可能还有错误；失败一旦确定却可以立即返回False。

### 2. 字典和栈各自负责什么

这里可以用一个**固定映射**保存“右括号需要哪种左括号”：`)`对应`(`，`]`对应`[`，`}`对应`{`。它回答的是**类型**。

栈保存本次扫描中尚未关闭的括号，回答的是**顺序和状态**。固定映射不随输入变化，栈会随输入变化。字典并不是本题必须使用的工具，用if/elif也能判断对应关系；所以忘记字典不等于这道题彻底无法开始。

先口述`{()}`与`{(})`哪里不同，再展开下面的完整参考。昨天你已经明确表示卡住，今天给完整讲解；看懂后仍需要关掉答案独立写，不能把阅读算作掌握。

## 四、DAY25五题完整示范答案

<details>
<summary>1．LC20：完整答案与每个判断的作用</summary>

```python
class Solution:
    def isValid(self, s):
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for char in s:
            if char in "([{":
                stack.append(char)
            else:
                if not stack:
                    return False
                if stack[-1] != pairs[char]:
                    return False
                stack.pop()
        return not stack


solution = Solution()
assert solution.isValid("()") is True
assert solution.isValid("()[]{}") is True
assert solution.isValid("{[()]}") is True
assert solution.isValid("([)]") is False
assert solution.isValid("(]") is False
assert solution.isValid("]") is False
assert solution.isValid("((") is False
assert solution.isValid("(()") is False
```

输入按题目保证只有六种括号。因此else分支一定是右括号，可以查询pairs；不必另外过滤字母。

先判断栈是否为空，再访问[-1]，防止访问不存在的元素。比较的是“最近没关闭的左括号”和“当前右括号要求的类型”；吻合后pop，表示这一层已处理完。循环结束的`not stack`才判断有没有未完成的层。

你的文件尚未实现，所以这里是参考而非对你代码挑错。时间O(n)，额外空间O(n)。DAY27复习位优先安排独立补写LC20，今天不额外增加第六份完整作业。

</details>

<details>
<summary>2．LC35：与你的算法相同，只补齐测试</summary>

```python
class Solution:
    def searchInsert(self, nums, target):
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            else:
                return mid
        return left


solution = Solution()
assert solution.searchInsert([-3, 1, 8], 8) == 2
assert solution.searchInsert([-3, 1, 8], 2) == 2
assert solution.searchInsert([-3, 1, 8], -5) == 0
assert solution.searchInsert([-3, 1, 8], 10) == 3
assert solution.searchInsert([4], 4) == 0
assert solution.searchInsert([4], 3) == 0
assert solution.searchInsert([4], 5) == 1
```

你的实现正确，原来的自测也通过。时间O(log n)，额外空间O(1)。本次无需再抄一遍二分。

</details>

<details>
<summary>3．C++区间判断：补上昨天未做的副本检查</summary>

```cpp
#include <iostream>
#include <vector>
#include <cassert>

bool in_closed_range(int value, int low, int high) {
    return value >= low && value <= high;
}

int main() {
    std::vector<int> original = {3, 7};
    std::vector<int> copy = original;
    copy[0] = 9;
    assert(original[0] == 3);
    assert(copy[0] == 9);
    assert(original.size() == 2 && copy.size() == 2);

    assert(in_closed_range(3, 3, 8));
    assert(!in_closed_range(9, 3, 8));

    int value, low, high;
    std::cin >> value >> low >> high;
    std::cout << in_closed_range(value, low, high) << "\n";
    return 0;
}
```

示范直接返回比较结果；你的if/else返回true/false同样正确。`!`是C++的逻辑取反，对应Python的not；这里第二个断言要求判断结果为false。输入`5 3 8`输出1，输入`9 3 8`输出0，各运行一次。

真正补充的是独立副本，不是把and换成&&。不要把有#include<vector>误当成已经创建了vector。

</details>

<details>
<summary>4．C++范围求和：保留你的while思路</summary>

```cpp
#include <iostream>
#include <cassert>

int sum_at_least(int start, int end, int threshold) {
    int total = 0;
    int value = start;
    while (value <= end) {
        if (value >= threshold) {
            total += value;
        }
        value += 1;
    }
    return total;
}

int main() {
    assert(sum_at_least(5, 8, 3) == 26);
    assert(sum_at_least(5, 8, 9) == 0);
    assert(sum_at_least(-2, 2, 0) == 3);
    assert(sum_at_least(8, 5, 0) == 0);
    int start, end, threshold;
    std::cin >> start >> end >> threshold;
    std::cout << sum_at_least(start, end, threshold) << "\n";
    return 0;
}
```

你的求和本身已经正确。示范只把两条分支共有的`value += 1`合并，并补连续调用验证。设范围中整数个数为m，非空时遍历时间O(m)，额外空间O(1)；空范围直接返回0。

</details>

<details>
<summary>5．模型：完整实现DAY25要求的两样本评估与单样本偏导数</summary>

```python
class LinearNeuron:
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias

    def forward(self, x):
        return self.weight * x + self.bias


class RegressionDataset:
    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys

    def size(self):
        return len(self.xs)

    def get_item(self, index):
        return self.xs[index], self.ys[index]


class SquaredLoss:
    def forward(self, prediction, target):
        return (prediction - target) ** 2 / 2

    def mean(self, predictions, targets):
        total = 0
        for i in range(len(predictions)):
            total += self.forward(predictions[i], targets[i])
        return total / len(predictions)


class LossEvaluator:
    def __init__(self, data, loss):
        self.data = data
        self.loss = loss

    def evaluate(self, model):
        predictions = []
        targets = []
        for i in range(self.data.size()):
            x, y = self.data.get_item(i)
            predictions.append(model.forward(x))
            targets.append(y)
        return self.loss.mean(predictions, targets)


loss = SquaredLoss()
data_two = RegressionDataset([0, 2], [1, 5])
eval_two = LossEvaluator(data_two, loss)
base = LinearNeuron(1, 0)
perfect = LinearNeuron(2, 1)
assert eval_two.evaluate(base) == 2.5
assert eval_two.evaluate(perfect) == 0
assert eval_two.evaluate(base) == 2.5
assert loss.mean([0, 0], [1, 3]) == 2.5

data_one = RegressionDataset([2], [5])
eval_one = LossEvaluator(data_one, loss)
base_loss = eval_one.evaluate(base)
assert base_loss == 4.5

for h in [0.1, 0.01]:
    weight_model = LinearNeuron(base.weight + h, base.bias)
    bias_model = LinearNeuron(base.weight, base.bias + h)
    weight_loss = eval_one.evaluate(weight_model)
    bias_loss = eval_one.evaluate(bias_model)
    weight_rate = (weight_loss - base_loss) / h
    bias_rate = (bias_loss - base_loss) / h
    assert abs(weight_rate - (-6 + 2 * h)) < 0.000001
    assert abs(bias_rate - (-3 + h / 2)) < 0.000001
    print("w方向", h, weight_loss, weight_rate)
    print("b方向", h, bias_loss, bias_rate)

x, y = data_one.get_item(0)
error = base.forward(x) - y
grad_weight = error * x
grad_bias = error
assert grad_weight == -6
assert grad_bias == -3
print("公式求得的偏导数", grad_weight, grad_bias)
assert (base.weight, base.bias) == (1, 0)
assert eval_two.evaluate(base) == 2.5
```

| h | w方向：新损失、变化率 | b方向：新损失、变化率 |
|---|---|---|
| 0.1 | 3.92、−5.8 | 4.205、−2.95 |
| 0.01 | 4.4402、−5.98 | 4.47005、−2.995 |

你的mean和evaluate已正确；参考额外收集targets只是接口组织选择。实质差别是试探循环使用eval_one，并从实际样本算出精确偏导数。你原来的四样本实验本身有效，不需要删除，只不能把它当成单样本任务已经完成的证据。

</details>

## 五、今天的五份任务与时间

| 时间 | 内容 | 文件 |
|---:|---|---|
| 25分钟 | 字典集中复习，一道字符统计综合题 | [01_字典综合](01_Python复习_字典统计与唯一字符.py) |
| 50分钟 | 上面的括号讲解＋新题1047 | [00_新题1047](00_Python新题_LeetCode1047_相邻重复项.py) |
| 45分钟 | 函数接收vector，两项短练 | [02_总耗时](02_C++基础_函数计算总耗时.cpp)、[03_超时计数](03_C++变式_函数统计超时项.cpp) |
| 50分钟 | 从偏导数到单样本、全批量的一步更新 | [04_模型实践](04_模型实践_梯度下降与全批量更新.py) |
| 10分钟 | 看重点评语、保存、反馈一个卡点 | 不新增必填文档 |

今天从新题与已经通过的C++模块各借5分钟给字典复习，总时长仍为180分钟。LC20不再称为“已掌握后的复习”；它的独立补写移到DAY27复习位，1047届时先作口述回访。若今天仍不能解释栈中的状态，直接反馈，不把看完参考算通过。

## 六、字典集中复习：先明确键和值各代表什么

### 1. 一个容器，不止一种用途

**字典（dictionary，dict）**保存键（key）与值（value）的对应关系。一个键只对应当前一个值，值可以更新。

| 问题 | 键代表什么 | 值代表什么 |
|---|---|---|
| 技能出现次数 | 技能名称 | 已出现的次数 |
| 两数之和 | 已经见过的数字 | 它的下标 |
| 括号类型对应 | 右括号 | 它需要的左括号 |

因此不能一看到字典就固定写“值加1”：计数才加1，记录下标保存的是位置，括号对应则是固定规则。列表按位置找，字典按键找，没有谁比谁更高级。

### 2. 把以前用过的操作重新串起来

下面是独立语法例子，不是今日字符统计的答案：

```python
counts = {}
counts["python"] = 1
counts["python"] = counts["python"] + 1
counts["git"] = 1
print(counts["python"])          # 2
print("python" in counts)        # True：检查键
print(2 in counts)               # False：不是检查值
print(counts.get("linux", 0))    # 0：临时返回默认值
print("linux" in counts)         # False：get没有插入这个键

for key in counts:
    print(key)                    # 只拿键
for key, value in counts.items():
    print(key, value)             # 一起拿键和值
```

`counts[不存在的键]`读取会报KeyError；`get(key, 默认值)`适合还不确定键是否存在的情况。计数时“读取旧次数，缺失按0处理，再把增加后的次数存回去”，是你以前`get(..., 0) + 1`那句代码的含义。只调用get不会更新字典。[Python字典教程](https://docs.python.org/3.11/tutorial/datastructures.html#dictionaries)

补一份速查：

| 写法 | 意义 |
|---|---|
| `len(counts)` | 不同键有多少个，不是所有次数相加 |
| `counts.keys()` | 用于遍历键；直接for遍历字典也可 |
| `counts.values()` | 用于遍历值，例如累计总次数 |
| `counts.items()` | 同时遍历键和值 |
| `a == b` | 键与对应值相同就相等，不要求插入顺序相同 |
| `other = counts` | 两个名字指向同一个字典，并没有复制 |
| `other = counts.copy()` | 新建浅副本；本课值是整数，给副本某个键重新赋值不会改原字典 |
| `del counts[key]` | 删除已有键值对；键不存在会报错 |
| `counts.pop(key, default)` | 删除并返回对应值；缺失返回default，与列表无参pop不是同一个接口 |

keys/values/items的结果可遍历，不要把它们误当成普通列表。字典保留插入顺序；更新已有键不改变其位置。不要在遍历同一字典的过程中增删键。本题不强制使用删除功能；这些是速查，不是要把所有API硬塞进一道题。[字典操作与顺序规则](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)

### 3. 只做一道综合题：字符统计与第一个唯一字符

文件01实现`analyze_text(s)`，返回两个值：字符计数字典，以及第一个只出现一次的字符的下标。找不到返回−1。它把你做过的[LC387](https://leetcode.cn/problems/first-unique-character-in-a-string/description/)扩展为能检查中间统计结果的本地练习，不是直接提交到平台的接口。

输入为小写英文字母字符串，本地练习也允许空串；不要用Counter或排序代替手写计数。你可以用一个或两个字典，只要能解释每个值的意义。不预填循环或三步分析。

| s | 返回的字典 | 返回的下标 |
|---|---|---:|
| `aabc` | `{'a':2,'b':1,'c':1}` | 2 |
| `abacb` | `{'a':2,'b':2,'c':1}` | 3 |
| `aabb` | `{'a':2,'b':2}` | −1 |
| `z` | `{'z':1}` | 0 |
| 空串 | `{}` | −1 |

同一文件里，对返回的字典做几个很短的检查，仍是这道题的结果检查，不另写一套函数：

- 用字典相等比较核对预期统计；用in检查一个存在和一个不存在的字符。
- 用get查询不存在的字符，得到0后确认字典没有因此多一个键。
- 用items打印字符和次数；用values遍历累计次数，结果应等于字符串长度。不同键的数量用len读。
- 创建整数计数字典的副本，只改变副本的一项，检查原字典不变；空串例子无需改不存在的项。

这覆盖此前常用的创建、增改、读取、默认值、查键、遍历、比较与副本。删除、复杂嵌套和其他API不作为今天额外负担。先实现，再核对测试；不为展示所有语法写没有用途的代码。

设字符总数n、种类数k，目标平均时间O(n)，额外空间O(k)；限定26个小写字母时k有固定上限。平均O(1)的字典查找不是保证每次绝对相同耗时，也不是从头for遍历所有键。

## 七、新题1047：删除一对之后，新的相邻关系怎么办

### 1. 从括号迁移，而不是再背一个模板

[LeetCode 1047：删除字符串中的所有相邻重复项，简单](https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/description/)。每次删除相邻且相同的两个字母，反复处理直到没有这样的相邻对，返回最终字符串。

以`abccba`为例，删掉cc后，两个b变成邻居；删掉bb后，两个a也变成邻居，最后为空。只在原字符串里找一次相邻重复是不够的；用字典算总次数也不够，因为`abab`与`aabb`次数相同，前者不能删除，后者能删空。

需要记住的是“已经读过、目前还没有被抵消的字符”。接下来读入新字符，它是否和当前结果的最右端构成一对？处理最右端后，更前面的字符会重新露出来。这仍然是栈擅长维护的顺序。

与LC20的区别：LC20栈中存未关闭的左括号，要求类型配对；1047存尚未抵消的字符，要求相邻字符相同。容器相同，**保存的状态和配对条件不同**。不要把LC20的True/False返回逻辑整段搬来。

### 2. 先教作业会用的新操作：join

最后需要字符串，不是字符列表。字符串的**连接方法（join）**把一组字符串用指定分隔符连接起来：

```python
letters = ["p", "y"]
print("".join(letters))       # py：中间不加内容
print("-".join(letters))      # p-y：中间加横线
print("".join([]))            # 空字符串
print(letters)               # ['p', 'y']：没有修改原列表
```

列表里必须是字符串。不要用`str(letters)`替代，它会得到带方括号等内容的列表表示。今天先用列表维护结果，最后连接一次，不在循环里反复重建越来越长的字符串。[join官方定义](https://docs.python.org/3.11/library/stdtypes.html#str.join)

### 3. 文件00的交付要求

实现平台入口`Solution.removeDuplicates(self, s)`，返回字符串，不只打印；用列表作为栈，暂不调用现成去重工具。输入非空且只含小写英文字母，**输出可以为空**。

| 输入 | 预期输出 |
|---|---|
| `abccba` | 空字符串 |
| `abbaca` | `ca` |
| `azxxzy` | `ay` |
| `aaa` | `a` |
| `aaaa` | 空字符串 |
| `abab` | `abab` |
| `abc` | `abc` |
| `z` | `z` |

自己写三步分析和测试。当天1047不提供完整循环或骨架。若卡住，先回答“读过的一段经过处理后，栈中还剩什么”，再向我请求提示。

一个字符至多压入、弹出各一次，加上末尾连接，时间O(n)，额外空间O(n)。不要用循环中不断全串replace的方法绕开今天的状态训练。

## 八、C++：把整组数据交给函数

### 1. 从三个整数到一个vector

昨天函数接收start、end、threshold。今天函数接收一组已经读取好的耗时，main依然负责输入输出，函数负责计算。

**按值传递（pass by value）**在本课写法中意味着：形参是一个vector副本。下面只演示“函数里改副本”，不是今天求和或计数的完整答案。

```cpp
#include <iostream>
#include <vector>

int changed_first(std::vector<int> values) {
    if (values.empty()) {
        return 0;
    }
    values[0] += 1;
    return values[0];
}

int main() {
    std::vector<int> original = {3, 7};
    std::cout << changed_first(original) << "\n";  // 4
    std::cout << original[0] << "\n";             // 仍为3
    std::vector<int> empty;
    std::cout << changed_first(empty) << "\n";    // 0
    return 0;
}
```

函数名之前的int说明返回一个整数；括号里的`std::vector<int> values`说明接收整数容器。empty()在没有元素时为true，先检查才不会访问不存在的第0项。[vector官方说明](https://learn.microsoft.com/en-us/cpp/standard-library/vector-class?view=msvc-170)

这里没有引用或指针。复制n个整数有O(n)成本，因此本课传vector的函数即使只用了几个局部整数，也不能把包含形参副本的额外空间说成O(1)。后续学引用再优化，今天先把语义写对。

### 2. 文件02：总耗时函数

自己定义`int total_duration(std::vector<int> durations)`，返回所有耗时之和，空容器返回0。函数不cin、不cout，局部累计每次重新开始。

main读取n，再读取n个整数放入vector，调用函数，输出一行总和。n为0—20，耗时为0—1000。0是合法耗时，不是结束标记。

| 终端输入 | 输出 |
|---|---:|
| `4 12 0 8 20` | 40 |
| `1 7` | 7 |
| `0` | 0 |

同一文件再用断言连续测试非空容器和空容器，确认结果不串。补昨天未完成的小检查：自己建立原容器与独立副本，修改副本一个元素后，检查原元素保持不变；只需几行，不另建题目。

### 3. 文件03：统计严格超时项

自己定义`int count_over_limit(std::vector<int> durations, int limit)`，返回**严格大于**limit的项数；等于不算超时，空容器返回0。

main读取n、n项耗时，最后读取limit，输出一行数量。n与耗时范围同上，limit为0—1000。先把输入读完整，再传给函数。

| 终端输入 | 输出 |
|---|---:|
| `4 12 0 8 20 8` | 2 |
| `3 5 5 6 5` | 1 |
| `2 0 0 0` | 0 |
| `0 10` | 0 |

同一容器分别用两个阈值调用，确认计数不会沿用前次结果。两题均不使用全局vector或全局累计值，main里保存原数据，函数里通过形参使用数据。

## 九、教材模型：从“知道方向”走到“真的改变模型”

### 1. 接回教材主线，明确今天解决的问题

参考[本地《神经网络与深度学习》](../../学习资料/AI%20agent/神经网络与深度学习%20%28邱锡鹏%29.pdf)：2.2.3的参数、超参数与梯度下降，书内30—31页/PDF45—46页；2.3及2.3.1的线性回归与平方损失，书内32—33页/PDF47—48页。已核对正文、公式和页边说明，不要求今天学习矩阵求逆。

我们已经有数据、有模型、有损失，也能评估不同参数。问题是：以前的候选参数由人挑，程序只比较，不会自行改好。导数提供局部方向，**梯度下降（gradient descent）**把这个方向变成一条实际更新规则，让模型的参数能够从数据中逐步调整。

这仍是同一个线性神经元，不是突然新增一种网络。**线性回归（linear regression）**在本课就是用`预测=w×x+b`拟合数值标签；w、b是待学习的参数。它能完成一次训练更新，不等于已经成为完整深度网络。

### 2. 先把单样本偏导数算清，再谈更新

固定x=2、y=5、w=1、b=0：预测2、误差e=−3、单条损失4.5。

为什么对w多乘x？w增加h时，预测从wx+b变为wx+b+xh，误差增加xh。代入平方损失，变化率为`e×x + x²×h/2`；h趋近0时剩e×x。b增加h时误差只增加h，变化率为`e+h/2`，极限为e。

所以本例`grad_weight=−6`、`grad_bias=−3`。这两个偏导数组成梯度。不要把昨天四样本平均损失的−2、−1.5拿来用于这个单样本：目标函数换了，梯度也会换。

这里的“梯度”是我们按公式手工计算的，不是自动求导，更不是多层网络反向传播。

### 3. 为什么是减去梯度

在当前位置，如果对w的偏导数为负，说明w往大一点的方向动，损失倾向下降；要增加w。用“减去一个负数”恰好实现增加。如果偏导数为正，则应该往减小w的方向试。

**学习率（learning rate）**控制这一步走多大，记为α，本课取0.1。更新规则是：

```text
新w = 旧w − α × 对w的偏导数
新b = 旧b − α × 对b的偏导数
```

代入本例：新w=`1−0.1×(−6)=1.6`，新b=`0−0.1×(−3)=0.3`。同一个x=2的新预测为3.5，新损失为`(3.5−5)²/2=1.125`，确实比4.5小。

两个梯度必须都来自更新前的参数。可以先算好两个数，再先后赋值w和b；不能更新w之后再用新w重算另一个梯度，假装仍是同一次标准梯度下降。

### 4. 学习率不是越大越好

若从同一基准w=1、b=0改用α=1，更新后w=7、b=3，对x=2预测17，损失72，反而更差。局部方向有用，不代表沿它走任意大的一步都安全。

α=0时参数完全不动，损失也不动。这是很好的检查：若代码在学习率0时仍改变参数，说明实现有问题。

**参数（parameter）**在这里是w、b，通过数据和更新规则调整；**超参数（hyperparameter）**在这里是学习率，控制学习过程，本次实验由我们事先设置，不由这条梯度更新规则自动学习。不要把“超参数”理解成更大的数字。

### 5. 为什么多个样本要平均梯度

只看一条样本，一次更新只关心那一条。我们的目标是整份训练数据的平均损失，所以需要在**同一组旧参数**下，算完每条样本的梯度，再平均，最后只更新一次。这叫**全批量梯度下降（batch gradient descent）**。

回到阶段固定数据，初始w=b=0：

| x | y | 预测 | e=预测−y | e×x | e |
|---:|---:|---:|---:|---:|---:|
| −1 | −1 | 0 | 1 | −1 | 1 |
| 0 | 1 | 0 | −1 | 0 | −1 |
| 1 | 3 | 0 | −3 | −3 | −3 |
| 2 | 5 | 0 | −5 | −10 | −5 |

对w的平均梯度为−14/4=−3.5，对b为−8/4=−2。初始平均损失为4.5；学习率0.1更新后w=0.35、b=0.2，重新评估得到3.021875。

“先平均再更新”不是把每个样本的参数更新轮流做一遍。后者会让后面的样本使用新参数，已经变成另一种更新过程。今天只实现一次全批量更新，不同时学习随机抽样或小批量训练。

教材2.3.1的公式(2.34)—(2.36)页边注明为简化省略了1/N；本课继续保留平均，与前面mean以及式(2.28)一致。因此损失和梯度都除以样本数，不能只平均一个、不平均另一个。

### 6. 对象怎样参与真实训练

之前LossEvaluator只计算分数，不修改模型。今天新增**更新器**GradientDescent：保存学习率，接收模型及已计算的梯度，修改这个模型的weight和bias。

它的方法里self指更新器，model指调用者传进来的神经元。要改的是model的参数，不是随手给更新器创建`self.weight`。这就是对象组合中的职责边界：数据集给样本，模型给预测，损失对象给分数，更新器改变模型参数。

Python形参model在本次调用中指向传入的那个对象；修改它的属性，外部也能看到变化。这与今天C++按值传vector得到副本不同。不要把“所有语言的函数参数”当成一种固定复制规则。[Python函数与对象传递](https://docs.python.org/3.11/tutorial/controlflow.html#defining-functions)

## 十、文件04：只新增一次更新所需的最小代码

### 1. 复用与新增的边界

复用你已写对的LinearNeuron、RegressionDataset、SquaredLoss、LossEvaluator，不重抄整个项目，不导入框架。

新增两项，由你自己实现，老师不预填方法体：

| 接口 | 接收什么 | 产生什么 |
|---|---|---|
| `GradientDescent(learning_rate)` | 一个学习率 | 用实例属性保存它 |
| `step(self, model, grad_weight, grad_bias)` | 真实模型、已经算好的两个梯度 | 按更新公式修改模型参数 |
| `batch_gradients(data, model)` | 非空数据集与当前模型 | 返回平均的两个梯度，不修改参数 |

step本课不返回新模型；没有返回表达式的Python方法返回None。因此不要写`model = optimizer.step(...)`，否则会把模型变量变成None。调用后继续用原来的模型做forward或evaluate即可。

batch_gradients使用size/get_item拿样本，用model.forward产生预测，再计算梯度。数据集非空、输入标签等长。不在这个函数里更新参数，两个累计值必须是局部变量。

### 2. A段：单样本一步更新

使用x=2、y=5，模型初始w=1、b=0。先计算预测、误差和两个精确梯度，再创建学习率0.1的更新器，调用一次step，最后用单样本评估器重新评价。

预期：梯度−6、−3；新参数1.6、0.3；预测3.5；损失4.5降到1.125。所有数字来自你的方法和公式，不把期望直接写成计算结果。

另建一份相同初始模型、学习率0，更新后仍为1、0，损失仍为4.5。两份模型应当独立，不能先把第一份更新后的模型当成第二份初始模型。

### 3. B段：同一文件中完成一次全批量更新

新建固定数据`[-1,0,1,2]`和标签`[-1,1,3,5]`，另建w=b=0的模型。调用batch_gradients时应得到−3.5、−2，而且模型仍为0、0。再交给学习率0.1的step更新一次。

预期参数0.35、0.2，平均损失从4.5降到3.021875；数据列表不变。小数用`abs(实际−预期) < 0.000001`检查。

今天没有fit循环，没有100次更新，没有Trainer外壳。DAY27再把这些已验证部件组合为Trainer并重复调用。一次损失下降只说明本次更新有效，不能保证已经拟合好，也不能证明真实任务泛化能力。

50分钟内先保证A段能解释和运行，再做B段；若卡在A，提交实际代码与结果，明确B未完成，不靠照抄凑齐。B仍是本轮需要完成的内容，DAY28验收时如实核对，必要时顺延补缺。

## 十一、运行与简短反馈

在仓库根目录使用现有解释器。你的环境若使用python，把python3替换即可：

```bash
cd /Users/chen/CCY/Algorithm-Learning-Days
python3 "DAY26/00_Python新题_LeetCode1047_相邻重复项.py"
python3 "DAY26/01_Python复习_字典统计与唯一字符.py"
python3 "DAY26/04_模型实践_梯度下降与全批量更新.py"
```

```bash
mkdir -p .build/DAY26
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY26/02_C++基础_函数计算总耗时.cpp" -o .build/DAY26/total_duration
./.build/DAY26/total_duration
```

```bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY26/03_C++变式_函数统计超时项.cpp" -o .build/DAY26/count_over_limit
./.build/DAY26/count_over_limit
```

每组C++终端输入重新运行一次；断言通过通常没有输出。当前代码文件仅有一句说明，要由你自己实现，空文件运行不报错不等于完成。

只需四个短回答，可以写在代码注释或自愿创建的课后总结里：

1. 字典中的键和值今天各代表什么？get缺失时返回0，会不会创建一个新键？
2. LC20与1047各自的栈保存什么？为什么`abab`不能按字典里的字符次数直接删空？
3. 今天C++函数内的vector与main里的vector是否同一份？复制会有什么成本？
4. 为什么梯度下降要减去梯度？全批量更新为什么要先算完同一份旧参数下的梯度，再修改参数？

加一句仍卡在哪里、有没有参考答案即可，不写长篇流水账。下次会检查实际成果再决定练习大小；LC20、副本与单样本求导等未独立完成项不会自动消失，也不会挤掉所有新内容。
