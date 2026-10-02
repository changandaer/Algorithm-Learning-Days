# DAY25｜用栈处理括号，用函数组织程序，把对象组合与偏导数连起来

> 今天仍为约180分钟、五份练习、这一份课程。三步分析由你自己写，没有预填TODO、实现或测试。昨天的示范答案只供对照，不要求全部重抄。
>
> 根据你在DAY24《课后总结.md》中的反馈，今天模型部分先讲透评估器怎样使用数据、模型和损失对象，再完成偏导数实验。原定的梯度下降一步更新移到DAY26，与平均梯度衔接；没有删除这个阶段目标。Python新题和C++新内容照常推进。

## 一、DAY24评语：算法可以前进，模型先找准真正卡住的地方

已阅读全部五份代码、代码注释及《课后总结.md》，运行原代码并补测。这里分别评价计算、练习目标和独立性，不因一个模块卡住就让所有内容原地重复。

| 内容 | 验证结果 | 评语 |
|---|---|---|
| 35搜索插入位置 | 1,143组数组与目标组合通过，输入未改变 | 找到返回mid、找不到返回left都正确，可以继续新题 |
| 704二分复习 | 同样1,143组通过，输入未改变 | 闭区间的收缩与结束条件稳定；不需要再花一天重讲二分 |
| C++修改耗时 | 无警告编译，204组输入输出通过 | 读取、追加、下标修改、长度与遍历输出均正确；昨天漏长度的问题已修正 |
| C++副本 | 无警告编译，204组打印结果都符合预期，但代码没有创建第二个vector | 你实现的是先打印旧值，再修改同一份数据，不是保留独立副本 |
| 单条平方损失 | 81组预测/标签组合通过 | `(预测−标签)²/2`正确 |
| 数据集与评估器 | size和get_item实际调用通过，评估器也确实保存了传入的对象 | 之前get_item的错误已修复；并非所有“对象连接”都没写对 |
| 平均损失 | 四条样本、w=1、b=0时实际输出0，应为1.75 | mean中的return在循环内，第一条算完就离开整个方法 |
| 偏导数实践 | 尚无h=0.1、0.01的变化率实现 | 这是未完成项，不假定你已掌握；今天结合你要求的对象组合讲解补齐 |

二分补测使用−3至3的所有非空升序子集，目标为−4至4。C++补测覆盖长度1—3、元素0/5/10、每个合法下标和两个替换值。教师补测证明这些输入下的实现表现，不代替你的限时闭卷、提示使用与独立调试证据，所以本次不编造综合分数。

**总体判断：Python主线推进顺利；C++会使用vector，但“输出过旧数据”和“仍保存旧数据”还需要一次实际区分；模型的首要问题是函数何时结束，而不是要重新学所有类。**

### 1. 先定位平均损失，不把问题归咎于“类太复杂”

你的`SquaredLoss.mean`中，`return total / len(predictions)`与累加语句一起缩进在for里面。return的意思是“结束这一次函数/方法调用，把结果交回去”，不是“结束这一轮循环”。

用你自己的四条数据，模型w=1、b=0：

| 样本 | 预测 | 标签 | 单条损失 |
|---|---:|---:|---:|
| x=−1 | −1 | −1 | 0 |
| x=0 | 0 | 1 | 0.5 |
| x=1 | 1 | 3 | 2 |
| x=2 | 2 | 5 | 4.5 |

正确平均是`(0 + 0.5 + 2 + 4.5) / 4 = 1.75`。你的方法只算第一行，就返回`0 / 4`；后三行根本没有机会进入累计。这不是“小数误差”，也不是把1/2乘错。

教师还保持你的evaluate逻辑不变，仅在测试中换入正确的损失对象，便得到1.75和0。这说明你评估器的主要连接已经成立，问题能定位到mean。只测一条样本会掩盖这种错误，因此今天先测两条，再做单样本求导。

### 2. 副本题为什么“输出对了，目标仍没完成”

你先把values打印出来，随后执行`values[index] = new_value`，最后再打印。终端留下了旧数据的“照片”，但程序里仍只有一份values，原来的那个元素已经变了。

真正的复制是在修改之后，程序仍能分别读取原容器和副本。昨天要求的`vector<int>`按值复制会保存独立的整数元素；修改副本不会改原容器。这里不把“深复制”推广成所有C++对象都一样的规则。

今天只用一个很小的检查确认这点，然后继续函数，不加一整道副本作业。

### 3. 不属于核心错误的写法

- 二分最后写`elif nums[mid] == target`没有错，示范改成else只是少写一次比较条件。
- `while right_index >= left_index`与`while left_index <= right_index`完全等价。
- C++输出n而不是values.size()，在你已按n正确读入数据的前提下结果正确。
- evaluate里的single_loss算出后没有被使用，删掉会更清楚；它不是这次0.0结果的原因。
- 你直接把`self.dataset.ys`交给mean在当前类设计中可以工作。示范通过get_item同时收集预测与标签，是为了只依赖已约定的数据集接口，不把你的写法说成一定错误。

## 二、DAY24理论回答的完整参考

1. **35为何能返回len(nums)，704为何不能用它表示找到？** 假设数组为`[2,5,9]`，插入位置可以是0、1、2或末尾位置3，一共有四个空隙。返回3是“告诉调用方放在末尾”，并没有读取数组。已有元素下标只有0、1、2，读取nums[3]才越界。704要找的是已经存在的元素，找不到按题意返回−1。你已写对“返回合法、读取越界”，这里补上原因。
2. **C++复制与长度？** 对本题的`std::vector<int>`，建立独立副本后只改副本，原容器不变。替换已有元素长度不变；push_back追加一个元素，长度增加1。你的理论方向正确，代码还差真正复制这一步。
3. **标签[2,2]、预测[0,4]？** 带符号平均误差是0，MSE是4，本课平均损失是2，你这次三项都算对了。每条损失内部除以2来自公式约定；把两条损失相加后再除以2，后一个2才来自样本数量。你用“标签−预测”算第一项，本例仍为0；后续求导统一把误差定义为“预测−标签”，保持方向一致即可，不为这个写法重做旧题。
4. **x=2、y=5、w=1、b=0？** 预测是2，误差是−3，单条损失是4.5；对w的偏导数为`(预测−标签)×x = −6`，对b为`预测−标签 = −3`。单独改变w时固定b，是为了只测w这一方向的影响。邻近参数试探只是比较不同配置，还没有自动训练。你用这一问表达了实际卡点，没有交偏导数答案；今天会把推导与现有代码接起来，而不是要求背这两个数。

## 三、DAY24五份代码的示范答案与对比

以下都是昨天的完整参考，不是今天作业的预填代码。已经会的两道二分题快速对比即可；模型优先看mean的返回位置和对象间的调用。

<details>
<summary>展开：1．LeetCode 35 搜索插入位置</summary>

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
assert solution.searchInsert([2, 5, 9, 14], 9) == 2
assert solution.searchInsert([2, 5, 9, 14], 7) == 2
assert solution.searchInsert([2, 5, 9, 14], 1) == 0
assert solution.searchInsert([2, 5, 9, 14], 20) == 4
assert solution.searchInsert([6], 6) == 0
assert solution.searchInsert([6], 4) == 0
assert solution.searchInsert([6], 8) == 1
assert solution.searchInsert([-5, -1, 3], 0) == 2
```

与你的算法相同，变量名缩短不是能力差距。时间O(log n)，额外空间O(1)。示范增加末尾插入测试，你的实现本身已经能处理。

</details>

<details>
<summary>展开：2．LeetCode 704 二分查找</summary>

```python
class Solution:
    def search(self, nums, target):
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

        return -1


solution = Solution()
assert solution.search([-8, -2, 1, 4, 9, 15, 21], 9) == 4
assert solution.search([-8, -2, 1, 4, 9, 15, 21], -8) == 0
assert solution.search([-8, -2, 1, 4, 9, 15, 21], 21) == 6
assert solution.search([-8, -2, 1, 4, 9, 15, 21], 0) == -1
assert solution.search([4], 4) == 0
assert solution.search([4], 3) == -1
assert solution.search([4], 5) == -1
```

你与示范都在找不到时返回−1，正确。补测单元素用于确认最后一个候选也被检查，不是换一种解题方法。时间O(log n)，额外空间O(1)。

</details>

<details>
<summary>展开：3．C++ 修改指定耗时</summary>

```cpp
#include <iostream>
#include <vector>

int main() {
    int n;
    std::cin >> n;
    std::vector<int> values;

    for (int i = 0; i < n; i += 1) {
        int value;
        std::cin >> value;
        values.push_back(value);
    }

    int index;
    int new_value;
    std::cin >> index >> new_value;
    values[index] = new_value;

    std::cout << values.size() << "\n";
    for (int value : values) {
        std::cout << value << "\n";
    }
    return 0;
}
```

输入`3 12 0 25 1 8`，依次输出3、12、8、25，每项一行。你用while读入同样正确，示范不要求你为了统一风格改成for。题目保证n至少为1、下标合法，不把未要求的异常输入额外算错。

</details>

<details>
<summary>展开：4．C++ 真正保留原容器与副本</summary>

```cpp
#include <iostream>
#include <vector>

int main() {
    int n;
    std::cin >> n;
    std::vector<int> original;

    for (int i = 0; i < n; i += 1) {
        int value;
        std::cin >> value;
        original.push_back(value);
    }

    int index;
    int new_value;
    std::cin >> index >> new_value;

    std::vector<int> copy = original;
    copy[index] = new_value;

    std::cout << original.size() << "\n";
    for (int value : original) {
        std::cout << value << "\n";
    }

    std::cout << copy.size() << "\n";
    for (int value : copy) {
        std::cout << value << "\n";
    }
    return 0;
}
```

同样输入`3 12 0 25 1 8`，输出3、12、0、25、3、12、8、25。关键不是打印顺序，而是**修改之后仍然有两份容器可以读取**。你的程序和这份参考在此输入下打印一样，但内部保存的数据不同。

复制所有n个整数需要O(n)时间及O(n)额外空间；修改一个已有元素只涉及一个位置。今天不讨论包含指针等复杂元素的复制规则。

</details>

<details>
<summary>展开：5．模型评估、平均损失与DAY24完整变化率实验</summary>

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
    def __init__(self, dataset, loss):
        self.dataset = dataset
        self.loss = loss

    def evaluate(self, model):
        predictions = []
        targets = []
        for i in range(self.dataset.size()):
            x, y = self.dataset.get_item(i)
            predictions.append(model.forward(x))
            targets.append(y)
        return self.loss.mean(predictions, targets)


loss = SquaredLoss()
assert loss.mean([0, 2], [1, 1]) == 0.5
assert loss.mean([0, 0], [1, 3]) == 2.5

data = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
assert data.size() == 4
assert data.get_item(0) == (-1, -1)
assert data.get_item(3) == (2, 5)

evaluator = LossEvaluator(data, loss)
base = LinearNeuron(1, 0)
perfect = LinearNeuron(2, 1)
base_loss = evaluator.evaluate(base)
assert base_loss == 1.75
assert evaluator.evaluate(perfect) == 0
assert evaluator.evaluate(base) == 1.75
print("基准平均损失：", base_loss)

# 每一行都从同一个基准w=1、b=0出发，不累计改动。
for h in [0.1, 0.01]:
    weight_trial = LinearNeuron(base.weight + h, base.bias)
    weight_loss = evaluator.evaluate(weight_trial)
    weight_rate = (weight_loss - base_loss) / h

    bias_trial = LinearNeuron(base.weight, base.bias + h)
    bias_loss = evaluator.evaluate(bias_trial)
    bias_rate = (bias_loss - base_loss) / h

    assert abs(weight_loss - (1.75 - 2 * h + 0.75 * h * h)) < 0.000001
    assert abs(bias_loss - (1.75 - 1.5 * h + 0.5 * h * h)) < 0.000001
    assert abs(weight_rate - (-2 + 0.75 * h)) < 0.000001
    assert abs(bias_rate - (-1.5 + 0.5 * h)) < 0.000001

    print("只改变w：", h, weight_loss, weight_rate)
    print("只改变b：", h, bias_loss, bias_rate)

assert base.weight == 1
assert base.bias == 0
assert data.xs == [-1, 0, 1, 2]
assert data.ys == [-1, 1, 3, 5]
```

数据集保证非空、输入与标签数量相同；今天不扩大到坏数据校验。上面的断言公式是这组数据的核验值，不用于替代真实forward计算。

| h | 只增大w：损失 / 变化率 | 只增大b：损失 / 变化率 |
|---|---|---|
| 0.1 | 1.5575 / −1.925 | 1.605 / −1.45 |
| 0.01 | 1.730075 / −1.9925 | 1.73505 / −1.495 |

与你的差别只有三类：mean在所有样本累计结束后返回；evaluate不再计算无人使用的single_loss；补上你尚未完成的邻近参数试探及重复调用检查。后两种变化率对应**四条样本的平均损失**，不是后面单样本实验的−6和−3，两者的数据不同。

额外创建targets是接口组织选择，不是为了让类“更高级”。在SquaredLoss.mean里调用self.forward时，self是损失对象，调用的不是LinearNeuron.forward。

</details>

## 四、今天做什么，以及DAY25阶段检查

| 顺序 | 时间 | 任务与文件 |
|---|---:|---|
| Python复习 | 15分钟 | [01：35闭卷重写](01_Python复习_LeetCode35_搜索插入位置.py)，另做下面两句口述 |
| Python新题 | 55分钟 | 栈的理论与操作，[00：20有效的括号](00_Python新题_LeetCode20_有效的括号.py) |
| C++ | 50分钟 | 普通函数，[02：区间判断](02_C++基础_函数判断闭区间.cpp)及[03：范围筛选求和](03_C++变式_函数统计范围内合格数字.cpp) |
| 教材与模型 | 50分钟 | [04：对象组合与偏导数](04_模型实践_对象组合与偏导数.py)，先修损失再比较参数 |
| 反馈与保存 | 10分钟 | 按需看昨天示范、记录一个真实卡点、保存代码 |

今天是约定的第二次进度检查，不增加一套考试或记录表：

- 已有通过证据：283的原地版本在DAY22通过补测；这次size和get_item均被实际调用并正确工作；二分主线可继续。
- DAY20范围筛选仍有实质缺口：旧代码从threshold开始，输入`5 8 3`得到33，而区间[5,8]内的合格和应为26。今天03把这项计算拆成普通函数，在新内容中验证，不重做整天循环。
- vector副本在今天02开头用一次小检查补齐。
- DAY20的Embedding接入网络仍没有完整代码证据。模型部分只安排简短连接口述，不把它自动记为通过，也不要求重写整个旧项目；完整连接留在阶段整合检查。
- 模型新增的缺口是mean提前返回及偏导数实验未完成。今天优先处理它们，DAY26再做学习率、参数/超参数、单样本更新和一次全批量更新；DAY27仍做fit。若实际用时或理解进度不足，DAY28如实列出未通过项，不声称“计划写了就学会了”。

## 五、Python：为什么括号需要“记住最近没处理完的事情”

### 1. 数数量还不够

新题为[LeetCode 20：有效的括号，简单](https://leetcode.cn/problems/valid-parentheses/description/)。输入只含`(`、`)`、`[`、`]`、`{`、`}`，判断括号类型与嵌套顺序是否都正确，返回布尔值。

先比较`([])`和`([)]`：每种左、右括号数量都相同，但后一种不合法。原因不是“数目少了”，而是遇到`)`时，最近打开、尚未关闭的却是`[`。括号必须先把内层关掉，再处理外层。

因此这里的状态不能只保存“出现了多少个左括号”，还要保存**尚未配对的左括号及其先后顺序**。用栈正好能够表达这种约束。

### 2. 栈是什么，为什么适合这里

**栈（stack）**是一种后进先出（last in, first out，LIFO）的结构。像一摞盘子：最后放上去的在最上面，先取的也是它。栈顶（top）就是当前最上面那项。

对应括号，最后打开的内层括号必须先闭合。以`([])`为例，尚未解决的内容先是`(`，再是`(`和`[`；读到`]`之后，`[`那层结束，剩下的才是`(`。这个过程没有在数组中查找某个数，所以二分查找不是合适工具。

栈并不是Python独有的新类型，也不是必须安装一个库。今天用已经熟悉的列表实现：把列表右端看作栈顶。

### 3. 三个操作要分清：压入、查看、弹出

```python
stack = []
stack.append(10)
stack.append(20)
print(stack[-1])       # 20：查看最后一项，没有删除
removed = stack.pop()
print(removed)         # 20：被取出来的那项
print(stack)           # [10]：列表已经变了
print(not stack)       # False：它还不空
stack.pop()
print(not stack)       # True：现在空了
```

- **压栈（push）**：在这里就是append(value)，把一项放到右端；append本身不返回修改后的列表。
- **查看栈顶**：stack[-1]读最后一项，不移除它。
- **弹栈（pop）**：不带参数的pop()移除并返回最后一项，列表会缩短。
- 空列表没有最后一项；空时使用pop()或[-1]会报IndexError。`not stack`在列表为空时为True，便于先判断有没有可用的元素。

这与Python官方介绍的[用列表作为栈](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-stacks)一致。今天只在右端操作，不使用pop(0)或引入队列。

### 4. 新题要求：你负责把理解组织成程序

文件00中写`Solution.isValid(self, s)`，返回True或False，不能只打印。你可以用已经学过的if/elif判断类型，也可以用字典表示对应关系；没有唯一指定的写法。

| s | 预期 | 这个例子在检查什么 |
|---|---|---|
| `()` | True | 一对括号 |
| `()[]{}` | True | 多组并列 |
| `{[()]}` | True | 多层嵌套 |
| `([)]` | False | 数量相同但顺序不对 |
| `(]` | False | 类型不匹配 |
| `]` | False | 没有左括号可配对 |
| `((` | False | 读完后还有未关闭的内容 |
| `(()` | False | 部分已匹配，不代表全部匹配 |

按官方输入范围，s非空且只包含这六类字符；无需额外编写过滤字母、空格等功能。测试空字符串可以作为自选扩展，不作为本题必交条件。

自己写三步、实现、断言。只有困难时才来要提示，我不会提前给你完整循环。独立分析时尤其想清：栈中保存的东西究竟代表什么；一个配对完成以后，它还应不应该留在“未完成”列表里。

算法目标是每个字符最多被检查、放入、取出常数次，因此时间O(n)；最坏全部是左括号，栈中保留n项，额外空间O(n)。Python列表末尾追加通常按均摊O(1)分析：偶尔需要扩容，但一长串操作平均到每次仍是常数开销。今天理解这个结论即可，不另学内存扩容实现。

### 5. 旧题与到期口述，不挤掉新题

文件01闭卷重写35，15分钟内先自己完成，不打开前面的答案。输入数组升序、没有重复项；返回位置，不真的插入，也不调用现成二分库。

检查`[-3,1,8]`分别查8、2、−5、10，结果应为2、2、0、3；`[4]`分别查4、3、5，结果应为0、0、1。确认输入列表未改变。

另外两项只口述，不再写两个文件：

- 1480第7天回访：`[3,-2,4]`的动态和是什么？负数出现时累计状态该不该清零？
- 26第3天回访：`[1,1,2]`处理后的有效长度是什么？有效前缀以外的内容是否必须被物理删除？

如果口述卡住，告诉我卡在哪，我来调整后续复习位，不让你今天额外做一套题。

## 六、C++：让一个计算有清楚的输入和返回值

### 1. 为什么从main里拆出函数

之前输入、计算和打印都写在main里，小程序可以这样写。现在想对同一种计算换三组数据验证，若把整段计算复制三遍，很容易改了第一段却忘了后两段。

**函数（function）**把一项计算单独命名：调用时给它输入，完成后把结果交回来。它让代码可以复用，也让“这一步到底算得对不对”能够单独检查，而不是让程序显得高级。[C++函数官方说明](https://learn.microsoft.com/en-us/cpp/cpp/functions-cpp?view=msvc-170)

下面是与作业不同的独立示例：给整数增加2。

```cpp
#include <iostream>

int add_bonus(int value) {
    int result = value + 2;
    return result;
}

int main() {
    int first = add_bonus(3);
    int second = add_bonus(10);
    std::cout << first << "\n";
    std::cout << second << "\n";
    return 0;
}
```

输出5和12。逐部分理解：

- 名字前的int是**返回类型（return type）**，说明这个函数会交回一个整数。
- 括号里的`int value`是**形参（parameter）**，是接收本次输入的局部名字。调用时的3、10是**实参（argument）**，也就是实际送进去的值。
- 函数体的result是本次调用的局部变量（local variable）。main不能直接使用这个result；需要通过返回值拿到结果。
- `return result`交回数值并结束本次调用。`std::cout`只是显示内容，不能替代这个返回值。
- 两次调用各自计算，不会把上一次的result自动拿来累加。后面求和函数的total也应当每次从本次初值开始。

今天把函数定义写在main前面即可，暂时不讲函数声明分文件、引用、指针或类。不要因为以前见过某个写法，就假定今天必须都会。

### 2. 判断型函数返回bool

**布尔类型（bool）**只有true和false，适合回答“是不是”。在默认输出设置下，cout把true显示为1，把false显示为0；C++写小写true/false，Python才写True/False。

“同时满足”用`&&`连接两个比较表达式。例如两个比较都为true，整个条件才为true。不要写数学式的连比`low <= value <= high`：C++会先把左边算成布尔值，再拿这个0或1去与high比较，不是你想要的区间判断。

### 3. 一小段检查：打印不是测试副本独立性

今天02的main开头，自己建立original，内容为3、7；建立它的独立副本，把副本第一项改为9。**修改之后**检查原容器第一项仍为3、副本第一项为9，两者长度仍为2。

为了不把这些检查混进题目的输出，可以用**断言（assert）**：条件真时继续，条件假时报告失败并终止。C++需要`#include <cassert>`；本课的编译命令不会关闭断言。

独立语法示例是`assert(2 + 3 == 5);`，它通过时不打印任何内容。你来写本题的容器检查，老师不预填。这只是02里的短检查，不是第六份作业，也不需要另建测试框架。

### 4. 文件02：区间判断函数

你自己定义`bool in_closed_range(int value, int low, int high)`：value在闭区间[low,high]内时返回true，否则false。闭区间意味着两个端点都算。main完成上面的副本短检查后，读取value、low、high，调用函数并输出一行1或0。

本题保证low不大于high，三个数都在−30到30之间。函数里面不读输入、不打印；main负责与终端交互。这样后续更换输入来源时，计算不用重写。

| 输入：value low high | 输出 |
|---|---:|
| `5 3 8` | 1 |
| `3 3 8` | 1 |
| `8 3 8` | 1 |
| `2 3 8` | 0 |
| `9 3 8` | 0 |
| `-2 -2 -2` | 1 |

先自己分析，再实现。还可以在main中连续调用两次这个函数，用断言检查各自结果，不能靠把一次结果固定写成1通过。

### 5. 文件03：用函数解决之前的范围筛选问题

自己定义`int sum_at_least(int start, int end, int threshold)`：只考虑[start,end]内的整数，将其中大于或等于threshold的数相加并返回。

start和end决定“允许考虑的范围”，threshold只决定“范围里的数是否合格”。门槛比起点低，不代表可以把范围外的数也加进来。这正是DAY20旧程序`5 8 3`算成33的原因。

三个输入均在−30到30之间；start大于end时范围为空，约定返回0。main读入三个整数，调用函数，输出一行总和。求和放在函数中，不能仅把main改个名字而继续依赖外面的全局累计值。

| 输入：start end threshold | 返回并输出 |
|---|---:|
| `5 8 3` | 26 |
| `5 8 7` | 15 |
| `5 8 9` | 0 |
| `-2 2 0` | 3 |
| `4 4 4` | 4 |
| `8 5 0` | 0 |

程序中再连续调用`sum_at_least(5,8,3)`和`sum_at_least(5,8,9)`并用断言核对26、0。这用来确认局部累计不串到下一次调用，不额外打印测试内容。范围内逐项查看的实现，时间随范围长度增长，额外空间O(1)；今天不要求推求和公式。

## 七、教材与模型：先让评估可靠，再问参数该往哪里动

### 1. 把这几天还原成同一项任务

教材主线仍是第2章：2.1提供样本，2.2.1选择模型，2.2.2衡量预测错误，现在为2.2.3学习参数做准备。本课求导只取附录B.1需要的部分：本地PDF第409页（书内394页）的导数定义，以及PDF第410页（书内395页）的偏导数解释，不学该页其余高阶展开。

参考[本地《神经网络与深度学习》](../../学习资料/AI%20agent/神经网络与深度学习%20%28邱锡鹏%29.pdf)。下面围绕你现有代码重新讲，不要求逐页背教材。

我们要解决的事情一直是：给模型输入x，希望预测接近样本标签y。已有线性模型`预测 = w×x+b`，但随便指定w、b通常预测不好。

最初可以人工试三组参数，选表现最好的一组；后来你写出了SquaredLoss，终于能用同一把尺子比较“好多少”。一旦要比较许多模型，如果每次都手工搬数据、算预测、算损失，容易漏样本或改变比较标准，于是需要LossEvaluator组织这项重复计算。

评估器本身不产生新的预测公式，也不会训练。它的价值是让同一份数据、同一种损失能够反复评价不同参数。**先能正确评价，才有资格比较参数微调的影响；能判断影响方向后，下一课才能据此更新参数。**

### 2. 你写的是对象组合，不是把类定义一层层套起来

你的四个class并排定义。运行时，评估器保存数据集和损失对象，再调用它们的方法。这叫**对象组合（object composition）**：一个对象借助其他对象完成更完整的任务。人话就是“评估器知道到谁那里拿样本、让谁打分”。

用昨天的名字，创建之后的关系如下：

| 当前名字或属性 | 实际指向什么 | 负责什么 |
|---|---|---|
| data | 一个RegressionDataset实例 | 保存xs、ys，按下标取一对x、y |
| mse_loss | 一个SquaredLoss实例 | 对预测和标签算损失 |
| evaluator.dataset | 上面那个data对象 | 评估器没有另造一套样本 |
| evaluator.loss | 上面那个mse_loss对象 | 评估器复用同一种损失计算 |
| linear_1_0 | 一个LinearNeuron实例 | 保存w=1、b=0，并计算预测 |

在这里，`self.dataset = dataset`保存的是同一个Python对象的引用，没有把整个数据集复制一遍。这与昨天C++的`vector<int>`按值复制不同，不能机械套用两种语言的语义；今天不要求学习C++引用。

调用`evaluator.evaluate(linear_1_0)`时：

- evaluate里的self是evaluator，model是这次传进来的linear_1_0。
- `self.dataset.get_item(i)`在data上执行get_item。进入get_item方法后，那个方法自己的self是data，不是evaluator。
- `model.forward(x)`在linear_1_0上执行forward，那个方法里的self指向模型，因此能读到模型的weight与bias。
- `self.loss.mean(...)`在mse_loss上执行mean，里面的self是损失对象。它再调用`self.forward(...)`时，使用的是SquaredLoss的公式，不是模型公式。

**self不是整个文件共享的同一个人；哪个实例的方法正在运行，那个方法里的self就代表哪个实例。** 不需要背“嵌套了几层”，沿着点号左边找具体对象就能判断。

为什么不让损失对象自己保存一个固定的模型？因为同一个损失尺子要比较很多模型。如果它偷偷绑定了某一套权重，再传入别的模型时就容易评估错对象。当前分工是：模型负责预测，损失负责评分，评估器负责组织。

### 3. 多对象并不等于复杂：跟着一条样本走

固定x=2、y=5，模型w=1、b=0。数据集交出的是两个数2和5；模型只拿2，返回预测2；损失拿预测2及标签5，返回4.5。评估器负责把这些调用接上。

当样本不止一个时，mean要把所有对应损失加起来再求平均。因此return必须位于累计完成之后。这就是本次错误与对象协作的连接点：**对象关系没接错，也可能在某个方法内部提前结束，导致外层收到一个错误但看起来正常的数。**

你不必把所有类推翻。今天复用已理解的构造函数和forward，从空白重写mean与evaluate两个核心方法，换一组数据检查是否真正明白。

用2分钟口述一下旧Embedding连接：DAY20里“猫”查得`[0.5]`，单输入神经元要的是一个数，所以送入的是0.5，而不是字符串“猫”或整个列表。网络A的两层为`ReLU(2x+1)`、`ReLU(−h+4)`。请说出中间值与最后输出，并指出这条链有没有更新Embedding。这里只核对“一个部件的输出如何成为下一个部件的输入”，不重写网络、不以老师讲过替代你已通过的证据。

### 4. 有了可靠损失，为什么还要导数

目前可以比较w=1和w=2，但这两个候选仍是人选的。参数很多时，不可能把所有组合都试遍。我们需要更局部的问题：**站在当前参数位置，稍微增加其中一个参数，损失大约朝哪边变化、变化多快？**

仍用x=2、y=5、w=1、b=0：预测2，误差`e=预测−标签=−3`，损失4.5。将w增大0.1、b不变，预测变为2.2，损失变为3.92。

损失变化量是`3.92−4.5=−0.58`；w变化量是0.1；二者相除得到−5.8。这个−5.8是**变化率**，不是损失本身，也不是新的权重。负号说明在这次小幅增大w时，损失下降了。

将步子改为0.01，得到的变化率是−5.98。步子继续趋近0时，对应的极限是导数。在多参数模型中，只动w、保持b和样本不动，得到的是对w的**偏导数（partial derivative）**。

“偏”不是不完整或不准确，而是“只看这一个方向”。若w和b一起变，这个比值就混入两种影响，不能称为只对w的偏导数。

### 5. 不背公式：为什么对w是e×x，对b是e

单样本损失为`L = e²/2`，其中`e = w×x+b−y`。

先只把w增加h。因为预测公式里w乘着x，误差就从e变为`e+x×h`。代入平方损失：

```text
新损失 − 旧损失
= [(e+xh)² − e²] / 2
= [2exh + x²h²] / 2
= exh + x²h²/2

再除以h，变化率为 ex + x²h/2。
当h趋近0，后一项趋近0，因此对w的偏导数为 e×x。
```

这里用到`(a+b)²=a²+2ab+b²`，不是把一段神秘梯度公式直接丢给你。固定本例e=−3、x=2，结果为−6。

如果只把b增加h，误差直接增加h，没有再乘x。把上面的xh换成h，变化率变为`e+h/2`，h趋近0时留下e，即−3。

**偏置对每条预测直接加同样的量；权重的影响先乘输入x。** 这就是两个偏导数看起来不一样的原因。x=0时，改变w不影响这个样本的预测，所以对w的偏导数为0；但对b不一定为0。

所有方向的偏导数放在一起称为**梯度（gradient）**，这个两参数模型就是“对w的数、对b的数”这一对。今天先算清它们，下一课再用学习率决定实际移动多大，并更新模型自身参数。

非零h算出的叫数值近似；推导得到的−6、−3是此处单样本的精确导数。h不能取0，也不需要盲目取得极小，浮点计算太小可能损失精度；本课只用0.1、0.01。没有写参数更新循环，就不能说已经完成梯度训练。

## 八、文件04：让你能解释每一次调用，再独立做变化率实验

### 1. 这次明确复用什么、自己写什么

只保留已有四个类：LinearNeuron、RegressionDataset、SquaredLoss、LossEvaluator，不增加GradientDescent或Trainer。

- 可以复用已经理解的LinearNeuron、RegressionDataset，以及SquaredLoss.forward，不要求重抄。
- 关掉参考，从空白重新实现SquaredLoss.mean与LossEvaluator.evaluate，自己写调用与测试。
- mean接收预测列表和标签列表，返回一项平均损失。evaluate接收模型实例，使用自身保存的数据集与损失对象，返回这个模型在这份数据上的平均损失。
- 数据集非空、输入标签数量相等。预测必须来自model.forward，取样必须实际使用size/get_item。
- 评估不改模型参数，不把上次预测或total留到下一次调用。不写死期望值冒充计算结果。

### 2. 先验证多样本，避免“恰好测不出错误”

创建数据集：输入`[0,2]`，标签`[1,5]`。用同一个评估器依次评价模型`(w,b)=(1,0)`、`(2,1)`、再次`(1,0)`，平均损失应为2.5、0、2.5。

再单独调用mean：预测`[0,0]`、标签`[1,3]`，应得到2.5。若仍把return放在循环内，会得到0.25；这个检查可以直接定位损失方法，不用盯着四个类一起猜。

把两条样本各自的预测、单条损失手算出来即可，不要求长篇记录。确认上述结果后再进入下一步，因为仅用单样本并不能暴露提前return的问题。

### 3. 换到单样本，隔离一个参数方向

再创建一个数据集：输入`[2]`、标签`[5]`，并创建对应的新评估器。损失对象可以复用。基准模型仍为w=1、b=0，基准损失应为4.5。

对h=0.1、0.01分别比较：只增大w的模型；只增大b的模型。每次都从同一个基准参数出发，不在上一轮试探结果上继续加h。用评估器计算新损失，再用`(新损失−基准损失)/h`计算变化率。

| 改哪一个参数 | h | 新单样本损失 | 变化率 |
|---|---:|---:|---:|
| w | 0.1 | 3.92 | −5.8 |
| w | 0.01 | 4.4402 | −5.98 |
| b | 0.1 | 4.205 | −2.95 |
| b | 0.01 | 4.47005 | −2.995 |

用昨天已经学过的`abs(实际值−预期值) < 0.000001`验证，不先四舍五入再相减。最后输出公式计算的两个偏导数−6、−3，与数值近似对照；公式也应使用实际x、y、预测计算，不把−6、−3固定写进去。

最终还要确认：基准模型的w、b没变；第一个两样本评估器再次评估基准模型仍返回2.5。这样同时验证两个评估器保存的是各自的数据，不会因为新建了第二份数据就把第一份偷偷替换。

今天产物是**可靠评估＋参数方向检查**，不是自动训练。若mean与对象调用仍卡住，先把实际调用和结果发给我；不要为赶日期直接照抄训练器。

## 九、运行与简短反馈

在仓库根目录使用现有Python解释器；你的环境使用python的话，把下面的python3替换即可。全部本地执行，不需要GPU或新依赖。

```bash
cd /Users/chen/CCY/Algorithm-Learning-Days
python3 "DAY25/00_Python新题_LeetCode20_有效的括号.py"
python3 "DAY25/01_Python复习_LeetCode35_搜索插入位置.py"
python3 "DAY25/04_模型实践_对象组合与偏导数.py"
```

分别编译两个C++文件，每组输入重新启动程序；无输出的断言通过后，再输入表中的三项整数：

```bash
mkdir -p .build/DAY25
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY25/02_C++基础_函数判断闭区间.cpp" -o .build/DAY25/in_range
./.build/DAY25/in_range
```

```bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY25/03_C++变式_函数统计范围内合格数字.cpp" -o .build/DAY25/range_sum
./.build/DAY25/range_sum
```

练习文件目前只有一句说明，Python运行不输出、C++缺main，都不等于已经完成。需要你手写实现和测试；不用修改昨天成果。

下面四个短回答可写在代码注释或自愿创建的课后总结中，不另建教师要求的记录表：

1. 为什么只数左右括号个数判断不了`([)]`？pop与读取[-1]有什么区别？
2. C++函数return与cout分别做什么？函数内的累计值为什么不应沿用上一次调用？
3. `evaluator.evaluate(model)`里面，取样、预测和损失分别由哪个对象执行？mean的return放在for内为何会错？
4. 在今天的单样本中，为何对w的偏导数比对b多乘一个x？只改w时还需要固定哪些东西？

顺带告诉我一个真实卡点或实际用时即可，已理解的内容不写学习流水账。示范代码由老师验证，独立掌握要靠你的实现、解释和后续闭卷结果验证。

下一课预定：Python新题1047、复习20；C++函数接收vector；模型从今天求出的方向出发，讲学习率与参数更新，再连接多样本平均梯度。当天仍先读你的代码和心得再定练习大小，不提前生成DAY26。
