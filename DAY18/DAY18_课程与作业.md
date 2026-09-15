# DAY18：开始C++简单算法题——从一个总和到一组累计结果

> 今天仍只读这一份课程，约180分钟。前半部分包含DAY17全部示范答案、代码对比和理论反馈；后半部分是DAY18理论与三份作业。旧目录不改，新代码文件不预填实现、三步分析或断言。
>
> 今天的主线是C++返回vector，并解决LC1480；Python复习LC1；神经网络只用已学的计算，不同时加入多输入数学、继承或PyTorch。全部在Mac本地运行。

## 一、DAY17评语：87/100，已经可以开始C++简单题

最重要的结论：你的C++函数不是只对某个样例有效。它接收本次参数、在函数里建立累计值、遍历并返回结果，换输入仍然正确。Python的387也正确；神经元的列表预测能正确逐项调用forward。

我读了三份代码、全部代码注释、`课后总结.md`及本地Git记录，实际执行了原程序和补充测试。没有修改你的DAY17答案。

| 内容 | 实际检查结果 | 怎么评价 |
|---|---|---|
| LC387 | 原6条断言通过；补测9,841组短字符串及3组长串/全字母案例通过 | 两个字典的解法正确，不要求改成老师同款 |
| C++求和 | 原程序输出50，4条断言通过；C++17编译无警告；补测106组连续调用及输入不变均通过 | 函数参数、局部累计和返回值已在代码中正确使用 |
| 神经元 | 原3条断言通过；补测90组模型/样本列表组合和A→B→A调用通过 | 方法版计算正确；普通函数接收模型对象的写法尚未在提交中体现 |
| 理论与反馈 | 已能指出辅助字典、说出三次单输入预测；形参/实参回答不完整，空间分析及sample对应关系待补清 | 用具体变量补齐，不因此重学整天函数 |

教学估分：概念20/25，代码30/30，分析与调试17/20，测试与复杂度11/15，Git记录与表达9/10，共87分。核心计算正确性给满分；代码组织不同不直接当成计算错误。

没有看到本次LC387用时和提示使用情况，不能据此断言已经通过限时闭卷验收。分析与调试项按现有代码和回答估计，不代表我看到了你的完整编写过程。老师的补充测试也不算作你已经独立写过的测试。

需要补强的不是空行和命名，而是两点：能把解释对应到正在运行的具体值；能自己保留关键测试。你已经开始用断言验证神经元，这是相较DAY16的进步。

## 二、DAY17全部示范答案与逐题对比

示范用于对照昨天的题，不要求机械重抄。DAY18的新题答案不提前放在作答文件中。

### 00：LC387，第一个唯一字符

```python
class Solution:
    def firstUniqChar(self, s):
        counts = {}
        for letter in s:
            counts[letter] = counts.get(letter, 0) + 1

        for index in range(len(s)):
            if counts[s[index]] == 1:
                return index
        return -1


solution = Solution()
assert solution.firstUniqChar("leetcode") == 0
assert solution.firstUniqChar("loveleetcode") == 2
assert solution.firstUniqChar("aabb") == -1
assert solution.firstUniqChar("aabc") == 2
assert solution.firstUniqChar("z") == 0
assert solution.firstUniqChar("") == -1
assert solution.firstUniqChar("abacbd") == 3
```

你的`seen`保存次数，`word`保存每个字符最后出现的索引。虽然重复字符的索引被更新，但最后只查询次数为1的字符；这种字符只有一次出现，所以它的最后位置也就是唯一位置，没有错误。

你按照`seen.items()`顺序找到第一个次数为1的字符，这在当前Python中也正确：字典保持键首次插入的顺序，更新已有键的值不会把键挪到最后。由于你从左到右插入字符，筛出的第一个唯一字符就是最靠左的唯一字符。不能误判成“字典无序，所以你的算法不成立”。[Python字典顺序规则](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)

示范只保留计数字典，第二遍直接走原字符串，因此不需要保存索引的第二个字典，也不依赖读者理解字典遍历顺序。它的优点是少保存一份状态，不是你的答案必须推倒重写。

你完成了课程列出的6组测试，未见自行增加的第7组；示范补了一个“前面有重复字符、中间出现唯一字符”的输入。缺少自选测试不等于算法会算错。

### 01：C++，把耗时求和写成函数

```cpp
#include <vector>
#include <cassert>

int total_time_ms(std::vector<int> times_ms) {
    int total = 0;
    for (int time : times_ms) {
        total += time;
    }
    return total;
}

int main() {
    std::vector<int> training_times{15, 25, 10};
    assert(total_time_ms({7}) == 7);
    assert(total_time_ms(training_times) == 50);
    assert(total_time_ms({}) == 0);
    assert(total_time_ms({12, 8}) == 20);
    assert(total_time_ms(training_times) == 50);
    assert(total_time_ms({0, 0}) == 0);

    assert(training_times.size() == 3);
    assert(training_times[0] == 15);
    assert(training_times[1] == 25);
    assert(training_times[2] == 10);
    return 0;
}
```

你的计算函数与示范实质相同，不需要为了格式或变量名修改。

你的main已经包含空容器、单元素、全零和普通数组的断言；50这一组只打印，没有断言，未保留A→其他输入→A及原数组内容检查。我补测后确认这些情形都能通过，所以评价为“实现正确，测试记录还可以更完整”，不是“函数不通用”。

你在main和函数里都使用`total`这个名字是合法的，它们属于各自的作用域，不是共享一个全局变量。

今天仍保留值传参，没有偷偷把形参换成`const ... &`。对于一个已有的vector实参，当前版本会复制容器，计入副本后额外空间O(n)；求和循环自己的累计变量只占O(1)。以后再解释怎样省掉这份复制。

### 02：神经元，给模型传入一组样本

先给出昨天要求的“普通函数版”完整示范：

```python
class SingleNeuron:
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias

    def forward(self, x):
        z = self.weight * x + self.bias
        if z > 0:
            return z
        return 0


def predict_samples(model, samples):
    outputs = []
    for sample in samples:
        outputs.append(model.forward(sample))
    return outputs


neuron_a = SingleNeuron(2, 1)
neuron_b = SingleNeuron(-1, 3)
samples = [-1, 0, 2]
assert predict_samples(neuron_a, samples) == [0, 1, 5]
assert predict_samples(neuron_b, samples) == [4, 3, 1]
assert predict_samples(neuron_a, samples) == [0, 1, 5]
assert predict_samples(neuron_a, []) == []
assert predict_samples(neuron_a, [4]) == [9]
assert predict_samples(neuron_b, [5]) == [0]
assert samples == [-1, 0, 2]
assert neuron_a.weight == 2
assert neuron_a.bias == 1
assert neuron_b.weight == -1
assert neuron_b.bias == 3
```

你写的是`SingleNeuron`里面的`predict_samples(self, samples)`，也就是方法版；它使用`self.forward(sample)`。这种设计本身合理，而且计算正确。

| 对比 | 你的方法版 | 昨天要求的普通函数版 |
|---|---|---|
| 在哪里定义 | 类里面 | 类外面，与类并列 |
| 怎样调用 | `neuron_a.predict_samples(samples)` | `predict_samples(neuron_a, samples)` |
| 怎样选模型 | 点号前的对象自动成为self | 第一个实参显式交给model |
| 怎样处理单条数据 | `self.forward(sample)` | `model.forward(sample)` |

这不是“方法比函数差”，也不是“把缩进挪出来就更高级”。昨天特意安排普通函数，是要验证你能否把一个已有对象作为数据交给另一个函数使用；这一点不能仅凭方法版就认定已验收。

你保留了A的普通、空列表和单样本3条断言，但未见B、输入不变及参数不变的测试。老师补测了B和更多模型，结果正确。DAY18不要求回去重抄整题，而是用一个很小的新统计功能验证“显式接收模型对象”。

## 三、DAY17五道理论题：参考回答与反馈

### 1. 辅助数据与复杂度

你指出`seen`和`word`两个字典，正确；时间O(n)也正确。需要补充的是：空间取决于存了多少不同字符，不直接等于遍历了多少次。

假设s有1000个a：循环会访问1000次，但两个字典各只有一个键。换成100000个a，访问次数变多，键数仍然各为1。

用k表示不同字符数，两个字典合计最多2k项，额外空间O(k)。本题限定26个小写字母，k最多26，因此常见机试口径是额外空间O(1)。如果不限制字符种类，最坏可以有n种字符，才会写O(n)。你的O(n)可作为较宽上界，但没有说明固定字母表下更准确的结论。

本课程按通常算法题的固定大小数值单位分析；暂不额外讨论超大整数的位数。你只需要问：“这份容器最多存多少项？”不用背一串空间结论。

### 2. 返回类型、形参、实参

你说“两边不必同名”是对的，但还没有指出实际位置。

用你的代码：定义`int total_time_ms(std::vector<int> times_ms)`时，第一个int是返回类型，times_ms是接收数据的形参；main调用`total_time_ms(arr)`时，arr是这次提供数据的实参。`int total = ...`中的total是调用方接住结果的变量，不是函数的形参。

### 3. 局部变量与返回值

你的回答抓住了重点：函数内部的累计值不能被main直接按名字读取，但返回的整数可以交给main使用。

补一个准确区分即可：作用域（scope）讨论名字在哪些代码中可见；生命周期（lifetime）讨论对象从何时存在到何时结束。它们不是同一个概念。当前普通局部int让两件事看起来接近，但不用在今天深入地址、栈或内存布局。

你可以简单解释成：“函数算完把50交回来，main的total接住50；main不是继续借用函数内部那个total。”说“放在某个地址里”不是今天证明理解所必需的。

### 4. model、self、sample和x

你的代码在这部分是对的：循环取出的sample确实被逐个交给了forward。文字中“sample代表列表数据”与当前代码不对应；整张列表的名字是samples，多了一个s。

这不是要求背单词单复数。变量完全可以叫别的名字，关键是认出它此刻的值。对于你的A和`[-1,0,2]`：

| 名字或位置 | 第一轮实际对应 |
|---|---|
| `samples` | 整张列表`[-1,0,2]` |
| `sample` | 从列表取出的一个数`-1` |
| `self` | 当前神经元A，保存weight=2、bias=1 |
| `self.forward(sample)`里的实参 | `-1` |
| forward中的`x` | 收到同一个数`-1` |
| 神经元计算结果 | 2×(-1)+1=-1，经过ReLU变成0 |

在普通函数版中，model也是A；它与forward中的self指向同一个神经元。下一轮sample、x都是0，再下一轮都是2。不会在某一轮把整张列表自动拆进x。

### 5. 三条样本与多个输入特征

你回答“三次单输入预测”正确；提出用不同实例、不同参数测试，也正确。现在只差把你想到的B测试写进实际断言，便能用代码证明这段理解。

当前每次计算仍是`z = weight * x + bias`再经过ReLU，并没有把三个数同时当成一个样本的三个特征，也没有开始训练权重。

## 四、DAY18主线理论：函数不只能返回一个整数

### 1. 为什么今天适合开始C++算法题

昨天输入`{15,25,10}`，返回50。训练日志除了关心总共用了多久，还可能需要知道：完成第一步用了15毫秒，完成第二步累计40毫秒，完成第三步累计50毫秒。

输入仍是一组耗时；但输出从“最后一个总数”变成“一组阶段累计值”。这与[LC1480一维数组的动态和](https://leetcode.com/problems/running-sum-of-1d-array/)的数学含义一致。它是简单题，今天只练顺序遍历和返回容器，不另开一整套算法章节。

“动态和”这个题名不等于要求你现在学习动态规划。它指走到每个位置时，前面这一段的总和，也称前缀和（prefix sum）；前缀就是“从开头截取的一段”。

先手算一份不同于作业的样本：

| 位置 | 当前这项 | 从开头到当前位置的和 |
|---:|---:|---:|
| 0 | 6 | 6 |
| 1 | 2 | 6+2=8 |
| 2 | 5 | 6+2+5=13 |

所以`{6,2,5}`对应`{6,8,13}`，不是只返回13。输入每个位置都对应一个输出位置。

这张表解释题意，不替你写三步分析或循环。你已经会求一个总和；今天由你决定，怎样把需要交付的各个阶段结果保留下来。

### 2. 先理解返回容器，不直接看整道题的答案

返回类型（return type）描述函数把什么交给调用者。昨天是int，今天可以是`std::vector<int>`：不是交回一个整数，而是交回一组整数。

先看一个只把两个数装进容器的小示例。它不是动态和的实现：

```cpp
#include <vector>
#include <cassert>

std::vector<int> pack_two(int first, int second) {
    std::vector<int> result;
    result.push_back(first);
    result.push_back(second);
    return result;
}

int main() {
    std::vector<int> output = pack_two(3, 8);
    assert(output.size() == 2);
    assert(output[0] == 3);
    assert(output[1] == 8);

    std::vector<int> another = pack_two(-2, 0);
    assert(another[0] == -2);
    assert(another[1] == 0);
    return 0;
}
```

逐段理解，不要求把示例当作第四份作业：

- 开头的`std::vector<int>`是返回类型，pack_two是函数名，括号里是两个整数形参。
- `std::vector<int> result;`建立一个空容器；还没有元素，因此此时不能访问result[0]。
- 两次push_back分别在末尾添加元素。这里保存的是3和8，不是3+8。
- `return result;`交回这份容器的值，不是把容器打印出来，也不是只交回最后一项。
- main用`std::vector<int> output`接住容器，之后正常使用size和索引。

按值返回局部vector是正常、安全的做法。函数结束后，调用方收到的容器不会随局部变量一起“失效”。编译器可以省略复制或转移内部资源；今天不需要为此学习移动语义，更不需要写指针或返回局部变量的引用。[C++函数与返回值](https://learn.microsoft.com/en-us/cpp/cpp/functions-cpp?view=msvc-170)

### 3. push_back、索引和return各管什么

push_back是“在末尾增加一个元素”，不是“覆盖当前位置”。例如空容器先加入4，再加入7，内容是`{4,7}`，长度从0变1再变2。要创建结果时可以使用它。[vector操作参考](https://learn.microsoft.com/en-us/cpp/standard-library/vector-class?view=msvc-170)

索引读写则使用已经存在的位置。空vector没有第0项，不能指望`result[0] = 4`自动帮你增加一个元素；这种访问越界可能崩溃，也可能产生难以察觉的错误。

return会结束本次函数调用。处理整个输入以后才有完整结果；如果过早交回容器，后续输入不会再处理。要保留一个阶段值和要结束函数，是两件不同的事。具体放在哪里，自己依据题意决定。

本地练习继续按值接收vector，所以不改动调用方的输入。今天不要求原地优化，也不引入引用、const和下标循环的新写法；使用你已经会的范围for即可。

### 4. 怎样判断“一组结果”是否算对

不仅要看最后一项，还要检查结果长度和每个位置；只知道最后总数对，不能说明前面的阶段结果也对。

C++的两个`vector<int>`可以用`==`比较：长度相同、对应位置元素都相同才为true。它不是比较两个变量名是否相同，也不是只比较长度。

```cpp
#include <vector>
#include <cassert>

int main() {
    std::vector<int> actual{4, 7};
    std::vector<int> expected{4, 7};
    assert(actual == expected);

    expected[1] = 9;
    assert((actual == expected) == false);
    return 0;
}
```

测试时先建立expected，再比较结果；不需要为此学习测试框架。也可以沿用逐项断言，没有强制写法。

当expected很长，比较它也要逐项检查；分析解法复杂度时，把算法本身与main里的验证代码分开，不把老师准备了几条断言也算成算法步骤。

### 5. 怎样解释空间，不把“循环次数”和“容器项数”混在一起

回看你已经完成的两个程序：

| 程序 | 工作容器最多存什么 | 通常怎样描述 |
|---|---|---|
| LC387，小写字母 | 两个字典，各最多26个键 | 额外空间O(1)，时间随串长增加 |
| C++总耗时，按值接收已有vector | n项形参副本，外加一个累计整数 | 计入副本后额外空间O(n) |

DAY18若构造n项返回容器，输出存储本身是O(n)。当前还会按值复制输入，因此即使不计返回容器，计入形参副本后也仍是O(n)额外空间。不要只看到一个累计整数，就把整个当前实现说成O(1)。

不需要今天消除所有复制。先能明确“哪一份数据在增长”，以后才知道为什么学习引用有用。

## 五、C++题目入口：本地函数与LeetCode外壳

先在本地写普通函数并通过测试，再适配平台入口。今天只增加最小外壳，不同时学习C++完整面向对象体系。

下面沿用很小的“装两个数”示例，展示外壳语法；不是LC1480题解：

```cpp
#include <vector>
#include <cassert>

class Solution {
public:
    std::vector<int> packTwo(int first, int second) {
        std::vector<int> result;
        result.push_back(first);
        result.push_back(second);
        return result;
    }
};

int main() {
    Solution solution;
    std::vector<int> output = solution.packTwo(3, 8);
    assert(output[0] == 3);
    assert(output[1] == 8);
    return 0;
}
```

- `class Solution { ... };`把方法放进Solution类型；末尾的分号不能遗漏。
- `public:`表示这下面的方法可以由类外部调用。C++的class成员默认不是public，所以不能照搬Python缩进后就省略这行。[C++访问控制](https://learn.microsoft.com/en-us/cpp/cpp/member-access-control-cpp?view=msvc-170)
- `Solution solution;`创建一个对象，`solution.packTwo(...)`调用它的方法。这个例子不需要自己写构造函数，也不用把Python的self照搬进参数表。
- 本地由main调用；LeetCode由平台测试程序创建对象、调用指定方法。提交时不要附带自己的main或断言。

LC1480的方法名称是`runningSum`。本课先用值传参签名`std::vector<int> runningSum(std::vector<int> nums)`，沿用已学知识；平台用一个vector调用时，这种签名也可接收。

若页面默认签名带`&`，本课可以先改成上面的值传参版本；不是要求你盲抄未学语法。引用会在后续用同一段代码单独讲。平台最终是否通过，以你的实际提交结果为准；本地测试不能冒充线上提交记录。

你可以直接把独立写好的计算放入方法，也可以由方法调用同文件中已经定义好的普通函数。不要求为了形式手写两遍相同循环。若保留普通函数，平台提交也需包含其定义，并放在调用它的类之前。

## 六、神经网络小支线：模型作为普通函数的一个输入

今天不增加神经元数学。现有模型仍然把一个数x乘weight，加bias，再用ReLU把负值变成0。复用你自己已写正确的SingleNeuron即可。

为什么需要一个类外部的函数？例如同一套统计规则要分别用于A和B。统计者只需要收到“选哪一个模型”和“这一批有哪些样本”，不用写死某个全局neuron，也不用把所有统计功能塞进模型类里。

昨天的示范已经展示`predict_samples(model, samples)`；今天用不同输出要求练习迁移，不要求原样抄一遍。要统计的是：有多少条样本的forward结果严格大于0。

这里有两个特别容易混的判断：

- 统计的是模型输出，不是原始输入正不正。B的weight=-1、bias=3，输入-1时输出4，所以负输入也可能产生正输出。
- 输出0只表示当前神经元经过ReLU后输出0，不代表这条样本“预测错误”；我们没有真实标签，不能由此计算准确率。

普通函数定义中的model不需要新语法，它接住的是已有对象。调用`model.forward(sample)`时，model自动成为该方法里的self，sample这个数交给x。两者不是同一种东西，但同一次调用同时需要它们。

本题只用你已经学过的函数、循环、判断和整数计数。支线代码由你独立写；今天不再增加模型参数、多输入向量或训练步骤。

## 七、DAY18三份独立作业

### 时间安排

| 时长 | 内容 |
|---:|---|
| 15分钟 | DAY17反馈，示范按需对照 |
| 20分钟 | Python闭卷复习LC1 |
| 45分钟 | C++题意、返回vector与测试理论 |
| 50分钟 | 独立实现并测试LC1480本地版本 |
| 15分钟 | 理解最小平台外壳并适配自己的代码 |
| 25分钟 | 神经元小支线：讲解约8分钟、实践约17分钟 |
| 10分钟 | 简短回答、保存结果和Git提交 |

共180分钟。若C++首次编写超过预算，优先把本地算法写对、解释清楚；支线可以顺延。不把两道LeetCode都当成今天首次接触的新算法，Python题是到期复习。

### 任务0：Python闭卷复习LC1两数之和

文件：`00_Python复习_LeetCode1_两数之和.py`。

[LC1官方题目](https://leetcode.com/problems/two-sum/)。沿用`Solution.twoSum(self, nums, target)`。输入保证恰有一对合法答案，返回两个不同位置的索引，顺序不限。本次不扩展“无答案”“多组答案”或去重要求。

| nums | target | 预期索引，反序也对 |
|---|---:|---|
| `[2,7,11,15]` | 9 | `[0,1]` |
| `[3,2,4]` | 6 | `[1,2]` |
| `[3,3]` | 6 | `[0,1]` |
| `[-3,4,3,90]` | 0 | `[0,2]` |

写自己的三步分析、实现与断言，补一组自己设计的合法输入。索引反序时可用已学的or接受两种顺序，不要求为测试安装库。目标是独立写出熟悉的字典解法；若只想起双循环，先完成正确版，反馈卡点，不先翻旧答案。

只记录真实用时和是否获得提示。今天不提前提供这道复习题答案。

### 任务1：C++的第一道vector累计题——LC1480

文件：`01_C++算法_LeetCode1480_一维数组的动态和.cpp`。

先自己实现普通函数，接口是`std::vector<int> running_sum(std::vector<int> nums)`。要求返回每个位置从开头累计到该位置的和；不打印代替返回，不修改调用方输入。算法阶段不调用未教过的库算法。

课程练习使用空容器作本地扩展；官方题目输入长度至少1。官方长度最多1000，单项在正负100万以内，本机32位int足以容纳这些累计结果；这里不额外布置大整数处理。

| 输入 | 预期返回 |
|---|---|
| `{1,2,3,4}` | `{1,3,6,10}` |
| `{3,1,2,10,1}` | `{3,4,6,16,17}` |
| `{7}` | `{7}` |
| `{0,0,0}` | `{0,0,0}` |
| `{2,-3,4}` | `{2,-1,3}` |
| `{}` | `{}`，本地扩展 |

main由你写，用断言检查整组结果；可使用本课教过的vector比较或逐项检查。先用一组输入，再用另一组，然后再调用第一组，确认没有残留上次结果；检查原输入内容不变。自己再加一组合法输入。

只有本地版通过后，再适配`Solution.runningSum`平台方法。保持在同一个文件中即可，不增加一份重复答案文件。最后运行至少一次方法入口的本地断言；能登录LeetCode时再提交，并保留真实结果。

验收重点：返回完整序列、负数和单元素正确、每次调用独立，以及你能解释代码中的核心状态。若做成重复从头求和，先认可正确性，再与你一起分析重复工作；不要求一开始就背最优模板。

岗位小迁移，不新增代码文件：把训练三步耗时`{15,25,10}`交给同一个函数，预期`{15,40,50}`。用一句话解释返回数组第1项的40代表什么。它将是日志分析器里的累计时间数据，不宣称现在已经完成整个日志项目。

### 任务2：普通函数统计正输出样本数量

文件：`02_神经网络支线_统计正输出样本.py`。

可以复制自己已经理解的SingleNeuron类到这份文件，不要求机械重敲相同类。新增普通函数`count_positive_predictions(model, samples)`，定义在类外面，返回模型对这些样本逐项计算后，输出严格大于0的个数。

输入保证是现有SingleNeuron对象和数字列表，不需处理非法类型。返回一个整数，不返回输出列表，不打印代替返回。不改模型weight/bias，也不改samples，不使用固定全局模型。

| 模型 | samples | 预期数量 |
|---|---|---:|
| A：weight=2，bias=1 | `[-1,0,2]` | 2 |
| B：weight=-1，bias=3 | `[-1,0,2]` | 3 |
| A | `[]` | 0 |
| B | `[3,4]` | 0 |
| A | `[-2]` | 0 |

自己先手算至少一条，然后写三步分析、函数和断言。A→B→A再次调用，验证同一个统计函数确实使用传入的模型；检查原样本与两个模型参数不变。不用额外保存或提交一张测试表。

若卡住，请发已有代码和具体疑问，先给引导问题；不会直接把循环与判断写进你的练习文件。

## 八、运行命令与最少反馈

仍在仓库根目录、当前Python环境运行，不安装任何新依赖：

```bash
cd /Users/chen/CCY/Algorithm-Learning-Days
python3 DAY18/00_Python复习_LeetCode1_两数之和.py
python3 DAY18/02_神经网络支线_统计正输出样本.py
```

C++先编译：

```bash
mkdir -p .build/DAY18
clang++ -std=c++17 -Wall -Wextra -pedantic DAY18/01_C++算法_LeetCode1480_一维数组的动态和.cpp -o .build/DAY18/running_sum
```

确认编译成功再运行，不拿旧可执行文件验证新代码：

```bash
./.build/DAY18/running_sum
```

断言全部通过时可能没有输出，这是正常的；前提是你真的调用了被测函数。`.build`已在根目录忽略规则中，不提交可执行文件，不新增重复的公共文件夹。

今天只需回答下面四点，写在此处或自己的课后总结中，二选一：

1. 用自己的LC1变量解释字典存什么，为什么不会把同一个位置用两次；说时间与额外空间。
2. C++返回int与返回vector有什么区别？自己程序中的输入、累计状态、结果容器分别存什么？用一组数字讲。
3. 为什么LC387固定小写字母时字典空间可视为O(1)，而今天n项输出需要O(n)存储？当前C++值传参又增加了哪份存储？
4. 对自己的一次`count_positive_predictions(neuron_b, [-1,0,2])`，第一轮的model、sample、self和x分别是什么？只说具体对象和数值，并解释负输入为什么也可能被计入。

不要求新的流程名称、TODO或额外学习报告。三步分析仍是你思考的工具，不按字数评分。用一行补充：LC1用时、C++用时、提示/答案使用情况、最卡的一处。

### 我的回答

1.

2.

3.

4.

用时与提示情况：

## 九、下一课如何根据你的结果调整

若LC1480能自己解释并通过测试，DAY19先用Python重写同一思路，C++再以已完成的函数解释“引用与只读参数为什么能避免复制”；不同时增加陌生算法和C++完整类体系。若平台外壳还卡住，就只补外壳，Python每日题照常。

LC1480后续安排DAY19、DAY21、DAY25、DAY39回访；DAY19用Python重写，后续结合需要用C++复现。原有DAY19 LC217、DAY20 LC242、DAY21 LC387的复习保留：当日另有主要编码题时，旧题先口述关键变量，遗忘再重写，不强制每天堆三道完整机试。DAY32～35的LC1/217/242/387回访仍保留。

神经网络支线待对象传参和逐项计算验证稳定后，再进入多输入特征与权重列表；不会因为这次数学没升级就把它误认为原地踏步。它正在练之后训练和评估函数实际需要的对象调用能力。

开源项目仍按总约定在自己完成后按小模块对照。今天不增加整仓阅读或环境搭建任务，把时间留给首次C++算法题；本课没有搬用第三方项目实现。
