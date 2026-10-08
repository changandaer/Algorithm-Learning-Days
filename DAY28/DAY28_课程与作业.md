# DAY28｜阶段验收：能解释、能独立写、能运行验证

今天是原计划约定的验收日，**不增加新LeetCode题型、C++语法或模型部件**。这是DAY28的例外安排，不是恢复“每天只复习”。验收后按结果继续新内容，不要求把以前每一天重新做一遍。

今天仍是一份课程、五份留白代码。三步分析由你写，不预填TODO。先完成第二节验收，再按需展开第五节昨天的示范答案，避免刚看答案就把重写当成闭卷能力。

## 一、DAY27评语：这次进步在哪里

我已阅读全部代码、注释中的尝试过程及《课后总结.md》。你明确说所有代码独立写出，这条反馈予以记录；教师补测验证计算正确性，限时与隔天保持程度由今天验收补充，不凭空打综合分。

| 项目 | 实际检查 | 评价 |
|---|---|---|
| 121 | 穷举长度1—7、价格0—3的21,844组数组，对照所有合法买卖组合，全部通过，输入未修改 | **你的最终写法正确**，O(n)时间、O(1)额外空间，不因不同于常见模板判错 |
| 20 | 穷举六种括号组成、长度0—6的55,987个字符串，与反复消除完整括号对的结果一致 | 配对、空栈、顺序错误与结束后剩余左括号都处理正确；空串是教师扩展检查，不额外要求 |
| C++基础与变式 | 均按C++17编译，无警告；各121组输入的元素结果正确 | 返回容器、连续调用、修改first不影响second正确。两题都缺题目规定的长度输出行，只修输出，不重学vector |
| 四个模型类 | 4组数据×49组参数，共196组评估与手算一致；数据和参数未被评估改动 | size、get_item、mean、evaluate均正确。**此前模型方法错误已经关闭**，不继续把旧错误算在你头上 |
| 实际模型运行 | 提交文件只有类定义，没有实例创建、方法调用或断言 | 实现正确，但直接运行不会执行评估。今天重点补“创建对象→调用→核对”的使用能力，不再只重抄四个类 |

### 121为什么你的写法也是对的

你先写了枚举买卖日期的版本，又考虑维护最低价，最后只在相邻两天上涨时计算利润。这个尝试过程说明你在主动调整状态，而不是单纯背答案。

你的low_price不是“每一天都更新的历史最低价”。例如一路跌到最后一天时，它可能仍保持旧值，但那天之后没有卖出的机会，不影响利润答案。更准确地说，它保存初始价格和已经遇到的上涨段起点中的最低价。

为什么只处理上涨终点够用？如果某个卖出日之前一天价格更高或相同，往前移卖出日不会使利润更差；一笔正利润交易总能找到一个不更差的上涨终点。对于它之前的最低买价，只要后来能涨起来，从那个低价走向卖出日的途中就会出现上涨，低价会在相应上涨起点被考虑到。平价平台也不会丢掉这个数。因此你不是简单把其他情况漏算了，而是跳过了不可能改善答案的时机。

常见写法每一天都更新最低价，状态更容易解释，因此示范采用它；**这是可读性的选择，不是要求把正确代码强行改成唯一标准答案**。你可以在今天验收继续用自己的方法，只需能说清上述逻辑。

### 心得中真正需要补清的两点

1. 实例属性并不等于“创建后不再变化”。模型的weight与bias就是属性，训练时恰恰需要改变。属性强调数据属于哪个对象，不强调永远不变，也不要求一定来自构造器参数。
2. `4w−10`随着w增大而增大；导数为负才表示固定其他参数时沿增大w方向局部下降。你题目给定w=3，此时导数是正2。多参数一起动能否下降，是第三节重点，不是措辞纠错。

`model.forward`是取得绑定到model的方法，尚未调用；`model.forward(2)`才调用并返回预测。你已经分清是否发生计算，补上“取得方法”和“调用方法”的区别即可。evaluate没有return会隐式返回None，这个小问昨天没有回答，今天用自己的调用结果确认。

## 二、先做阶段验收：题目说明可以看，旧实现和AI关闭

180分钟：Python50分钟、C++40分钟、模型60分钟、对照补缺30分钟。每个模块记录实际用时、是否看过提示即可，不增加记录表。若看了答案，诚实标为“参考后完成”，不算失败，但不能标为闭卷通过。

模型模块前20分钟阅读第三节回应疑问，后40分钟关闭示范完成第四节。它是“讲解后迁移验证”，不同于Python闭卷；不会把今天刚解释清楚的多变量问题冒充长期掌握。

### 00：704二分查找，25分钟

对无重复、升序、非空整数列表nums及target，返回目标下标；不存在返回−1。实现`Solution.search(self, nums, target)`，目标O(log n)时间，不调用现成搜索库。[官方题目](https://leetcode.cn/problems/binary-search/description/)

测试用`[-8,-2,1,6,11,19]`，target分别为−8、19、6、4，期望0、5、3、−1；单元素`[7]`分别查7、6，期望0、−1。自己补一个“两端缩到一起”的例子。用自己的话说明区间含义以及每轮为何能缩小，不要求背循环形式。

### 01：121买卖股票，25分钟

非空价格列表按日期排列，最多一笔先买后卖交易，买卖日不同；返回最大利润，不能盈利返回0。实现`Solution.maxProfit(self, prices)`，O(n)时间、O(1)额外空间，不修改日期顺序。[官方题目](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/description/)

测试：`[6,3,3,8,2,9]→7`、`[5,5,4,4]→0`、`[4]→0`、`[2,7,1,4]→5`、`[9,1,1,2]→1`、`[0,0,3]→3`。自己补一个最低价在最后一天的例子。正确的自己的写法可以保留，说明保存的状态，不要求背示范。

### 02：C++耗时统计，30分钟

用已有知识写一个小程序，不考引用、指针或平台类外壳。

- 输入n、n个耗时、limit；n范围0—20，耗时与limit均为0—1000的整数，输入合法。
- `int total_duration(std::vector<int> durations)`返回总耗时。
- `std::vector<int> over_limit(std::vector<int> durations, int limit)`返回严格超过limit的耗时，保持原顺序，不改变调用方容器。
- main负责读取和调用：第一行输出总耗时，第二行输出超时项数，之后每行输出一个超时值。不要打印其他提示或原始输入。

输入`5 4 10 0 7 10 7`时，输出四行：31、2、10、10。输入`0 7`时输出两行0；输入`3 7 7 7 7`时输出21与0。再自己测试全部超时的一组。打印长度只是补上已有输出要求，不是新算法。

### 03：C++返回值与副本，10分钟

复用自己02中的over_limit函数，main使用固定容器`[2,9,4]`。阈值5的返回结果保存在first，阈值10的返回结果保存在second；随后把非空first的首项改为99，再次对original调用阈值5的筛选，保存在third。

输出original、first、second、third，每份先打印长度，再逐行打印元素。四份最终应为`[2,9,4]`、`[99]`、`[]`、`[9]`。你自己写调用区，老师不预填。补一句：若误写成修改original[0]，为什么后续计算可能改变？这就是本次的简单错误定位题，不另塞一份陌生代码。

## 三、把昨天的数学疑问讲清：固定其他参数，不等于忽略它们

本节用于补清已经学过的偏导数与梯度下降，不新增优化器或训练器编程任务。依据本地邱锡鹏教材：附录B.1书内395页/PDF410页的偏导数定义；2.2.3.1书内30页/PDF45页的梯度更新公式。以下数值例子由老师重新设计。

### 1. 先回到你正在计算的那个损失

固定样本x=2、y=5，损失是`L(w,b) = (2w+b−5)²/2`。其中w、b可以调节，x、y是这条已知样本，不参与参数更新。

直接使用链式法则：

- `∂L/∂w = 2(2w+b−5)`；
- `∂L/∂b = 2w+b−5`。

注意对w的偏导一般仍包含b！“求导时固定b”不等于“公式里没有b”，而是计算这一项变化率时不让b跟着动。b换成别的当前值，偏导数也可能改变。

当b=0时，关于w的切片函数为`L(w,0)=(2w−5)²/2`，它的导数才简化为`4w−10`。不应把这个特定切片的公式当成所有b处通用的偏导表达式。

| w（b固定为0） | 损失 | 对w的偏导 | w略微增大时 |
|---|---:|---:|---|
| 1 | 4.5 | −6 | 损失下降 |
| 2.5 | 0 | 0 | 已在这个切片最低点，继续增大反而上升 |
| 3 | 0.5 | 2 | 损失上升 |

因此不能说“w增大，L一定减小”。在导数为负的区间里，固定其他参数，函数随w增加而下降；跨过最低点，导数符号会改变。你的“偏导数为负是否也有普通导数的含义”这个判断，在**其他变量固定的切片上**是对的。

### 2. w变化会不会自动导致b变化？

在当前模型中，w、b是两个可独立设置的参数。代码只执行`model.weight = 2.9`不会自动改bias；属性不是互相绑定的开关。但它们共同决定同一个预测，所以改变b会改变下一次计算得到的w偏导，这就是函数中的相互影响。

若优化程序同时修改w、b，就要用两者的新值重新算损失，不能只拿一个偏导判断整体。以旧点(w,b)=(3,0)为例，旧损失0.5：

| 新参数 | 发生什么 | 新损失 |
|---|---|---:|
| (2.9,0) | 只减小w | 0.32 |
| (2.9,0.4) | w减小，但b同时增大 | 0.72 |
| (2.8,−0.1) | 两个参数按旧梯度一起更新，学习率0.1 | 0.125 |

第二行正是你担心的情况：一个参数朝降低损失的方向移动，另一个参数却把整体结果推坏。因此担心多参数共同作用是有道理的，但不是“偏导数失效”，而是不能用单个偏导代替整个变化。

如果另有约束规定b必须随w变化，例如`b=h(w)`，那就应计算复合函数`L(w,h(w))`的导数，链式法则为`∂L/∂w + ∂L/∂b × h'(w)`。当前模型没有这种约束，不要求实现或背这个扩展公式；它只是回答“若b确实跟着变，该怎么办”。

### 3. 梯度为什么把所有偏导放在一起

在同一个旧参数点，记`g_w=∂L/∂w`、`g_b=∂L/∂b`。梯度就是把这些方向信息作为整体保存，并非让偏导数互相打架或消除影响。

参数发生较小变化Δw、Δb时，损失的一阶变化近似为：

`ΔL ≈ g_w×Δw + g_b×Δb`。

人话：每个参数“往哪里动、动多远”，乘上损失对它的敏感程度，再把这些贡献加起来。它是局部近似，不是任意大步子的精确等式。当前二次损失可以直接展开得到精确形式：设旧误差e=2w+b−5，则

`ΔL = e(2Δw+Δb) + (2Δw+Δb)²/2`。

前一项正是`g_wΔw+g_bΔb`，后一项解释了为什么大步子不能只看斜率。这里不需要另学高阶矩阵理论，展开平方就能检查。

梯度下降选择`Δw=−αg_w`、`Δb=−αg_b`，代入一阶近似：

`ΔL ≈ −α(g_w²+g_b²)`。

当学习率α为正、梯度不为零时，这一阶项为负，所以对当前光滑损失，**足够小的步长**会使整体损失下降。参数更多时，就是把更多平方项加起来，原则不变。不需要保证偏导之间“没有影响”，而是计算它们在**同一旧参数点**的数值，作为整体选择更新方向，再在新参数处重新计算。

仍以上面的(3,0)为例，梯度为(2,1)。α=0.1更新到(2.8,−0.1)，损失0.125；α=1更新到(1,−1)，损失反而为8。方向对，不代表步长随便多大都对；梯度为0也不保证一般复杂模型已经达到全局最优。

### 4. 这与self有什么关系

weight、bias需要保存在模型对象上，是因为预测与更新都要访问当前参数。**它们正是会变化的实例属性**。临时输入x不必存成self.x；同样，临时计算的误差、梯度也不必因为写在方法里就自动成为属性。

“保持其他参数固定”是求偏导时的数学操作，不是要求模型属性终身不变。完成评估后手动换一个参数，是验证属性变化与计算关联；这本身还不是自动训练。之后优化器才负责按规则改变它们。

## 四、模型04：这次验收调用链，不再只交类定义

共40分钟，包含手算、代码和测试。可以复用昨天的四个类构造器，关闭旧答案后补写forward、size、get_item、mean、evaluate；不要求为抄类名花时间。重点是自己编写调用区，实际执行并核对返回结果。

### A. 换数据、换模型，证明评估链能工作

接口仍为：LinearNeuron(weight,bias)；RegressionDataset(xs,ys)提供size/get_item；SquaredLoss提供forward/mean；LossEvaluator(data,loss)提供evaluate(model)。数据均合法、非空、配对等长，不增加异常处理新知识。

使用数据A：xs=[−2,1,3]、ys=[−3,3,7]；数据B：xs=[0,2]、ys=[1,5]。模型A：w=0、b=1；模型B：w=2、b=1。

你自己写实例创建、调用和检查：

- 两份size分别3、2；数据A第0项为(−2,−3)。
- 数据A评估模型A，平均损失28/3；评估模型B，损失0。
- 数据B评估模型A，平均损失4。
- 把模型A的weight改为2，不重建评估器，再评估两个数据集，损失都变为0。
- 检查两份原始数据未改变；把返回值保存并打印或断言，不能只定义类然后认为已经运行。

浮点数仍用已学的绝对误差容差判断。修改weight后结果变化，回答的是“属性能不能变、评估器实际使用哪一个模型”，不是训练循环验收。

### B. 用同一评估器核对不同参数，不新增求导程序

数据只含x=2、y=5。依次检查参数(3,0)、(2.9,0)、(2.9,0.4)，损失分别0.5、0.32、0.72。计算这三次评估并解释：哪次只改一个参数，哪次改了两个？为什么不能拿一个偏导的符号概括三种变化？

再独立手算x=1、y=4、w=2、b=1的损失及两个偏导；写明求各偏导时固定谁。不要求实现GradientDescent、batch_gradients、Trainer或fit。

### C. 用一句话回答即可

实例属性能否改变？evaluate缺少return时调用者拿到什么？你昨天独立写出的类，今天是否能独立创建实例并运行？仍不清楚哪一步就直接指出，不要求另写理论长文。

## 五、DAY27完整示范答案与对比：完成验收后再看

这是昨日参考，今天的独立题文件不预填实现。也不要求全抄示范。特别是121，你的正确算法可以保留。

<details>
<summary>00｜121：每天维护历史最低价的常见写法</summary>

```python
class Solution:
    def maxProfit(self, prices):
        lowest = prices[0]
        best = 0
        for index in range(1, len(prices)):
            price = prices[index]
            profit = price - lowest
            if profit > best:
                best = profit
            if price < lowest:
                lowest = price
        return best

solver = Solution()
assert solver.maxProfit([8, 2, 6, 1, 5]) == 4
assert solver.maxProfit([3, 6, 1, 2]) == 3
assert solver.maxProfit([9, 7, 4]) == 0
assert solver.maxProfit([3]) == 0
assert solver.maxProfit([2, 2]) == 0
assert solver.maxProfit([0, 4]) == 4
assert solver.maxProfit([2, 4, 1]) == 2
```

计算今天利润时，lowest来自之前的日期，然后再把今天纳入历史。你的版本只在上涨时更新与比较，仍然正确且复杂度相同；本版本的优势是状态含义在每天都一致，解释更短。旧枚举版本可保留注释，记录你怎样从O(n²)想到O(n)。

</details>

<details>
<summary>01｜20：你的核心实现无需修改</summary>

```python
class Solution:
    def isValid(self, s):
        stack = []
        pairs = {')': '(', ']': '[', '}': '{'}
        for char in s:
            if char in '([{':
                stack.append(char)
            else:
                if not stack:
                    return False
                if stack[-1] != pairs[char]:
                    return False
                stack.pop()
        return not stack

solver = Solution()
for text, expected in [('()[]{}', True), ('{[()]}', True),
                       ('([)]', False), ('(]', False),
                       (']', False), ('((', False), ('(()', False)]:
    assert solver.isValid(text) == expected
```

题目限定只含六种括号，所以直接查pairs符合输入前提，不要求为任意其他字符额外设计规则。时间O(n)，最坏额外空间O(n)。你最后的`return not left_bracket`正确，避免了只检查中途配对而漏掉剩余左括号。

</details>

<details>
<summary>02｜C++翻倍：只补长度行，保留你的容器逻辑</summary>

```cpp
#include <iostream>
#include <vector>

std::vector<int> doubled(std::vector<int> original) {
    std::vector<int> result;
    for (int value : original) {
        result.push_back(value * 2);
    }
    return result;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<int> original;
    for (int i = 0; i < n; i++) {
        int value;
        std::cin >> value;
        original.push_back(value);
    }
    std::vector<int> result = doubled(original);
    std::cout << result.size() << '\n';
    for (int value : result) {
        std::cout << value << '\n';
    }
    return 0;
}
```

你的while读入与参考for等价；先声明再赋值也合法。漏长度行时，空输入完全没有输出，和要求输出0不同。补一行即可，不需要为了名字拼写或排版返工。函数按值接收再创建结果，时间O(n)、额外空间O(n)。

</details>

<details>
<summary>03｜连续调用与副本：计算正确，补齐输出并在操作后观察原容器</summary>

```cpp
#include <iostream>
#include <vector>

std::vector<int> doubled(std::vector<int> original) {
    std::vector<int> result;
    for (int value : original) {
        result.push_back(value * 2);
    }
    return result;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<int> original;
    for (int i = 0; i < n; i++) {
        int value;
        std::cin >> value;
        original.push_back(value);
    }
    std::vector<int> first = doubled(original);
    std::vector<int> second = doubled(first);
    if (!first.empty()) {
        first[0] += 1;
    }
    std::cout << original.size() << '\n';
    for (int value : original) {
        std::cout << value << '\n';
    }
    std::cout << first.size() << '\n';
    for (int value : first) {
        std::cout << value << '\n';
    }
    std::cout << second.size() << '\n';
    for (int value : second) {
        std::cout << value << '\n';
    }
    return 0;
}
```

你的`first.size()>0`与`!first.empty()`都正确。你在修改之前打印original，其数值本身没有错；示范挪到修改之后，是为了直接观察操作后的状态，验证证据更明确。first修改后second未跟着变，这项副本能力已有正确实现证据。

</details>

<details>
<summary>04｜四类及完整调用区：你的方法正确，缺的是下面的运行验证</summary>

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


data_a = RegressionDataset([0, 2], [1, 5])
data_b = RegressionDataset([-1, 1, 3], [-1, 3, 7])
model_a = LinearNeuron(2, 1)
model_b = LinearNeuron(1, 0)
loss = SquaredLoss()
evaluator_a = LossEvaluator(data_a, loss)
evaluator_b = LossEvaluator(data_b, loss)

assert data_a.size() == 2
assert data_b.size() == 3
assert data_a.get_item(1) == (2, 5)
assert data_b.get_item(2) == (3, 7)
assert model_a.forward(2) == 5
assert model_b.forward(2) == 2
assert loss.forward(3, 5) == 2
assert loss.forward(5, 5) == 0
assert loss.forward(3, 5) == 2
assert loss.mean([1, 3], [1, 5]) == 1
assert evaluator_a.evaluate(model_b) == 2.5
assert abs(evaluator_b.evaluate(model_b) - 10 / 3) < 1e-9
assert evaluator_a.evaluate(model_a) == 0
assert evaluator_a.evaluate(model_b) == 2.5
assert (model_b.weight, model_b.bias) == (1, 0)
assert data_a.xs == [0, 2] and data_a.ys == [1, 5]
assert data_b.xs == [-1, 1, 3] and data_b.ys == [-1, 3, 7]
print('DAY27模型调用与测试通过')
```

与你相比：mean和evaluate逻辑等价；你先保存mse再return合法，取名xs/ys虽然实际是单个数，也不影响计算。今天不扣命名分，重点是补上真正的调用。这里只处理约定的合法非空数据；生产级校验不在本次范围。

</details>

### DAY27理论示范回答

1. self.weight是对象的当前权重，可以在训练时改变；x是本次输入。是不是属性取决于是否保存在该对象上，而非是否永远不变、是否所有方法都使用。
2. model.forward取得方法，model.forward(2)调用它；evaluate未return时结果是None，不是自动返回最后算出的数。
3. 给定x=2、y=5、w=3、b=0，预测6、误差1、损失0.5，两个偏导分别为2与1。固定b时，略增大w使损失上升。若b也变化，应一起代入或分析整体变化，不能只看一个偏导。
4. 你报告独立写出，予以记录；类方法补测通过。缺少实际调用区是交付证据不足，不等于这些方法不会写。今天用新的数据补足验证。

## 六、最后30分钟：对照与确定下一阶段起点

先检查自己的结果，再展开必要示范；只修真正出错的部分，不整篇抄答案。提交五份代码、主要运行结果，并用几句话说明用时与卡点。若用了提示，标出哪一题即可。

三条线分开判断：

- Python：704和121正确，能解释区间/状态及复杂度，才能记为本次限时验收通过；DAY27的20已经有正确实现，后续按间隔复习，不再当作空白欠题。
- C++：检查函数、输入循环、容器返回与边界，输出遗漏单独修；通过后再逐步安排已理解Python题的C++重写，**不直接假定已会引用、指针或平台外壳**。
- 模型：四类实现已正确，不需要继续按“所有类不会”授课。主要验证实际调用、属性可变与偏导条件；通过后可接回单次参数更新，然后全批量梯度和训练循环，一次接一个部件。

更新器、平均梯度、Trainer/fit、100步训练与未见样本预测仍没有独立完成证据，明确顺延，不为了DAY28结课而虚报。DAY20的Embedding接入网络也保留为待核验，不在今天额外增加第六份作业。下一课是否恢复新题、如何接回训练，以今天成果决定；今天不预生成DAY29。
