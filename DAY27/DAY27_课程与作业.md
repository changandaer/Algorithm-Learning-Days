# DAY27｜保存最优结果；让四个模型部件真正协作

今天只打开这一份文档。五份代码文件保持留白，三步分析由你自己写，不新增TODO或学习流程。全部在Mac本地完成，不用安装包或GPU。

**先回应你的反馈：模型支线今天不前进。** 你明确说隔一天便不能独立组织四个类，说明需要把代码与含义重新接起来，而不是继续叠加Trainer。今天不要求实现优化器、平均梯度函数或训练循环。Python继续新题，C++只学相邻的返回值知识。

## 一、DAY26评语：算对的、没完成的和真正的短板

已阅读全部代码及《课后总结.md》。下面的补测是教师验证，不代表已经验证了你的闭卷用时、AI使用情况或隔天独立性，因此不编造综合分数。

| 内容 | 检查证据 | 评价与下一步 |
|---|---|---|
| 1047 | 原有测试通过；另外穷举a/b/c组成、长度0—7的3,280个字符串，与独立消除方法对照通过 | 栈的实际运用正确，时间O(n)、额外空间O(n)。空串是教师扩展检查，不是额外扣分条件。你的分层if完全可以保留，不必为了像示范而压缩 |
| 字典统计与唯一字符 | 3,280组的计数与唯一字符索引均正确，但其中1,977组返回三项，不符合约定的两项 | 找字符的思路有效；需要统一函数交付的结果。重复while可删，但不是要求你整天重做字典 |
| C++总耗时 | 函数通过1,093组vector；编译无警告 | 求和、局部变量、空容器正确。main多打印了输入元素，题目只要总和；这是输出问题，不是否定函数能力 |
| C++超时数量 | 函数通过6,558组容器/阈值组合；编译无警告 | 严格大于阈值及每次调用重新计数正确，可以继续返回vector |
| 四个模型类 | 原文件有空方法体，语法检查报缩进错误，整份不能执行；隔离已写好的前两类后，forward和get_item正确，size报NameError | `len(xs)`没有读取实例属性；损失与评估器未完成。不是“全部类都不会”，但当前不能认定四类已能独立协作 |

字典具体例子：`analyze_text("aabc")`现在返回`({'a': 2, 'b': 1, 'c': 1}, 'b', 2)`。调用方写`counts, index = analyze_text("aabc")`会报“要接两项，却来了三项”。无唯一字符时你又返回两项，所以应统一为`(counts, index)`。这关系到函数能否被下一段代码使用，不是命名偏好。

你的字典遍历保留了字符首次出现顺序，所以确实能找到第一个唯一字符，不能误判成“字典无序”。问题在于`while`反复检查同一键的同一计数；它在当前代码中不是死循环，只是多余。一般字符集下当前时间可写作O(n+k²)，k是不同字符数；两次线性扫描可做到O(n)。先修返回值，不需要背复杂度推导。

心得里的前两问正确：get缺失时不插入键；20保存未闭合左括号，1047保存尚未消除字符，`abab`不能按次数删空。C++的`vector<int>`按值传参会得到独立的整数序列副本，复制n个元素通常需要O(n)时间和额外空间，不是免费；今天暂不研究指针。模型疑问在第五节直接用你的代码回答。

## 二、今天180分钟怎么用

| 模块 | 时间 | 今天交付 |
|---|---:|---|
| 复习 | 20分钟 | LC20独立补写；口述字典返回项数、1047相邻消除与344原地交换 |
| Python新题 | 45分钟 | 121：一次遍历保存最优信息 |
| C++ | 30分钟 | 返回vector；复用同一函数验证连续调用与副本 |
| 模型 | 75分钟 | self和参数→调用和返回→四类协作；直接求导解释符号 |
| 反馈保存 | 10分钟 | 运行结果、一个真实卡点，自己保存Git |

示范答案只看卡住的部分，不要求全部重抄。超过时间时先停在可运行的小段，并告诉我卡在哪里；不把未完成写成已掌握。原计划的Trainer/fit明确顺延，不在DAY28突击补教后立即要求闭卷通过。

## 三、Python：过去的信息怎样帮助今天做决策

### 1. 从1047过渡到121

昨天要保存“还没有被抵消的字符”，因为下一个字符可能与最后一个配对。今天不需要保存所有历史价格，但仍要问：**为了处理今天，过去哪些信息不能丢？** 这就是状态——程序为后续计算留下的必要信息，不是新学习方法。

[LeetCode121：买卖股票的最佳时机](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/description/)为简单题。列表按时间先后给出价格；只允许至多一次买入和一次卖出，买必须早于卖。返回最大利润，不返回日期，没有赚钱机会就返回0。官方输入至少有一天，因此无需为不存在的空价格表增加业务规则。

例如`[8, 2, 6, 1, 5]`：不能拿最低价1与最高价8相减，因为8发生在1之前。可以买2卖6，也可以买1卖5，最大利润都是4。排序也不行：排序会抹掉真实日期顺序。

固定某天为卖出日，利润等于“今天价格−之前买入价”。今天价格已经固定，之前买价越低，这笔交易越好。所以不用记下所有过去价格，只需要知道此前最低买价。但是今天算出的最好交易，不一定比昨天已经发现的交易更好，因此还要保留截至目前的最大利润。

小例子：已经看过`[6, 3, 5]`，历史最低价是3，已发现利润2。下一天价格4，只能带来候选利润1，不能因此丢掉以前的利润2。再下一天价格8，才可能改善已知结果。你需要自己安排变量初值、比较和更新顺序，注意不能用未来价格帮助过去买卖。

如果用`min`或`max`：`min(7, 4)`返回4，`max(2, 5)`返回5，它们只返回结果，不会自动改掉原变量。也完全可以使用你熟悉的if，不要求为一道题背新写法。

为什么能更快？枚举所有买卖日期可能检查约n²对组合；只保存必要的历史信息，每天做固定次数比较，可以做到O(n)时间、O(1)额外空间。“只返回一个数”并不自动代表O(1)空间，还要检查你有没有另外保存长度随n增长的列表。

### 2. 新题00的要求

独立完成`Solution.maxProfit(self, prices)`，不排序，不改输入列表。自己写三步分析、代码和测试。先求正确，再确认没有双重枚举买卖日期。

| 输入 | 期望 |
|---|---:|
| [8, 2, 6, 1, 5] | 4 |
| [9, 7, 4] | 0 |
| [3] | 0 |
| [2, 2] | 0 |
| [3, 6, 1, 2] | 3 |
| [0, 4] | 4 |
| [2, 4, 1] | 2 |

完成后口述：为什么不能直接“最大值减最小值”？你保留的两个信息各有什么用？这比背循环更重要。今天不给完整算法循环。

### 3. 复习01：LC20独立补写

沿用DAY25已教的题意与DAY26讲解：字符串只含`()[]{}`，括号类型、顺序都要匹配，每个左括号都需要被关闭。完成`Solution.isValid(self, s)`。关闭昨天参考答案，测试`"()[]{}"→True`、`"([{}])"→True`、`"(]"→False`、`"([)]"→False`、`"(("→False`、`")("→False`。不要求实现未教过的新容器。

其余只简短口述，不另开文件：1047为何`"abbaca"`得到`"ca"`；344如何保证交换修改的是原列表；字典函数成功与失败时为什么都应返回两项。如果LC20仍卡住，保留自己尝试的状态变化，不直接复制完整答案。

## 四、C++：函数除了返回一个数，也能返回一组数

### 1. 返回类型决定交付什么

昨天`int total_duration(...)`交付一个整数。今天返回类型换成`std::vector<int>`，函数就可以交付整数序列。下面只演示返回容器，不是今天翻倍题的答案：

```cpp
#include <iostream>
#include <vector>

std::vector<int> make_sample() {
    std::vector<int> values = {4, 9};
    return values;
}

int main() {
    std::vector<int> received = make_sample();
    std::cout << received.size() << '\n';  // 2
    std::cout << received[1] << '\n';      // 9
    return 0;
}
```

`return values`交付容器的值，不只是交付长度。函数结束后调用方仍能正常使用返回结果，不需要你手动保住局部变量。编译器可以优化返回过程，不能笼统说每次return必然重新复制整份数据；当前先理解正确的使用方式。

与此区分：参数写成`std::vector<int> values`，是**按值传参**。main有一份，函数参数有自己的副本，修改参数里的整数不会改main的那份。对于今天的`vector<int>`，复制要保存并复制这些整数，n越大，时间和内存成本一般越大。这个结论不要直接推广成“任何复杂对象都是深复制”。

`std::vector<int> another = original;`也会建立独立的整数容器。修改`another[0]`不会修改`original[0]`。这正是前两天尚未留下证据的能力，今天通过返回值练习自然验证，不额外抄概念。

### 2. 基础02：返回翻倍结果

编写`std::vector<int> doubled(std::vector<int> values)`，返回每项乘2后的容器，顺序不变，不影响调用方原容器。可使用已学的push_back、下标或范围遍历，自己决定实现。

main读入非负整数n，再读n个整数（练习范围−10到10）。调用函数后，先输出结果长度，再每行输出一个结果元素。n为0时仅输出0。不要额外输出原始输入或提示文字。

测试：`3 2 -1 0`得到长度3与`4、-2、0`；`0`得到0；`1 7`得到长度1与14。口述时间和空间随元素数怎样变化。

### 3. 变式03：连续调用后的结果互不串改

复用自己02里写好的函数，不要求再设计新算法。main同样读取n和n个整数，保存为original。把original的翻倍结果保存在first，再把first的翻倍结果保存在second。随后仅当first非空时，把first的第一个元素加1。最后按original、first、second顺序各输出长度及每个元素，一项一行。

输入`2 2 -1`时，最终三份内容分别是`[2,-1]`、`[5,-2]`、`[8,-4]`。second在first后来被修改之前已计算好，不应跟着变。输入`0`时输出三行0，不访问第0项。再测`1 0`，三份内容分别为`[0]`、`[1]`、`[0]`。

这题检查的是“调用返回结果”和“独立容器”，不是学引用、指针或C++ LeetCode。仍用C++17和已有编译方式。

## 五、模型主课：不是见到变量就加self

### 1. 先把四个部件放回同一个任务

我们要判断一个线性神经元预测得好不好：先从数据集中取一对输入x与真实答案y，模型用当前w、b算出预测值，然后损失函数比较预测与真实答案，最后把所有样本的损失取平均。

四个类不是四种互不相关的理论：模型负责**怎么算预测**；数据集负责**保存、取出样本**；损失负责**两个数差多少**；评估器负责**把这些部件按任务顺序调用起来**。未来训练器需要同样的评估链条，但今天先让这一条链可靠运行，不添第五个部件。

教材依据：邱锡鹏《神经网络与深度学习》2.2.2—2.2.3，参数更新见书内30页/PDF45页；求导规则见附录B.1书内395页/PDF410页。这里用你正在写的线性模型重讲，不要求通读矩阵微积分。

### 2. self、参数、局部变量分别是什么

**实例属性**是挂在某个对象上的数据。人话：这个对象随身保存的东西，下一次调用还要用，例如某个神经元自己的weight和bias。

**参数**是调用时传给方法的名字；**局部变量**是在这次方法执行中使用的名字。人话：这次办事临时拿来的材料和中间计算结果，不因为方法写在类里面就自动装进对象。

```python
class LinearNeuron:
    def __init__(self, initial_weight, initial_bias):
        self.weight = initial_weight
        self.bias = initial_bias

    def forward(self, x):
        prediction = self.weight * x + self.bias
        return prediction
```

这里故意把初始化参数改名为initial_weight，说明两边不是一个名字的魔法：右边是这次传入的值，左边是给当前对象建立的weight属性。`self.weight`以后能再读取；`initial_weight`并不会自动出现在其他方法里。

`forward`中的x由本次调用提供，因此写x；weight、bias是对象已经保存的参数，因此写`self.weight`、`self.bias`。prediction是本次算出的局部结果，因此直接写prediction。**同一个方法内可以同时出现加self和不加self的变量。**

设`model = LinearNeuron(2, 1)`，调用`model.forward(3)`时，self就是model，x就是3，返回7。可以把它理解成把model和3分别送进self与x的位置；你不需要在正常调用时再手动传model一次。不同模型有各自属性，self并不是固定指向某一个全局模型。[Python官方类教程](https://docs.python.org/3.11/tutorial/classes.html#instance-objects)

### 3. 直接回答：为什么loss用prediction，而不是self.prediction？

当前损失方法的接口是`forward(self, prediction, target)`。每次调用都会传入两个数；方法没有把它们保存成属性，所以应使用参数prediction和target。写`self.prediction`是在要求读取“这个损失对象已保存的prediction属性”，不是读取同名参数。

例如`loss.forward(3, 5)`这次算2；下一次`loss.forward(5, 5)`算0。同一个损失对象可以反复处理不同预测，没有必要持续记住上一次预测。它也不需要自己的weight或bias，所以没有必须编写的初始化数据。

**使用self.prediction并非语法上不允许。** 如果你确实提前执行过`self.prediction = prediction`、`self.target = target`，就能读取这两个属性，但你同时改变了类的设计：要负责每次更新它们，避免意外拿旧值计算。当前设计只临时计算两个数的差，直接用参数更简单。不能把“标准写法”理解成唯一合法写法。

同理，数据集的`get_item(self, index)`中，`self.xs`与`self.ys`是长期保存的两个列表，index是这次要取的位置，不是`self.index`。你已有这段正确代码，它其实已经同时体现了两种变量来源。

`size`写成`len(xs)`会尝试寻找普通名字xs，不会自动跳进`__init__`寻找曾经的参数，更不会自动转换成`self.xs`。应读取当前数据集自己保存的列表。不要通过在文件末尾增加全局xs来“消除报错”，那会掩盖多数据集时算错的问题。

### 4. 拆开你写的那一行

你的提议是：

```python
def prediction(self, model, data):
    mse = ((self.model.forward - self.data.ys) ** 2) / self.data.size
```

方法叫prediction没有语法错误，把model和data传给一个方法也完全可以。真正需要逐层检查的是：

| 表达式 | 实际含义 | 本任务需要什么 |
|---|---|---|
| model | 这次传进来的模型对象 | 可用它计算预测 |
| self.model | 当前对象保存的model属性 | 你没有建立这个属性，参数不会自动变成属性 |
| model.forward | 方法本身，还没有进行预测 | 要传入一个x，调用`model.forward(x)`得到数 |
| data.ys | 一整份标签列表 | 单样本平方损失需要对应的一个y |
| data.size | 方法本身 | `data.size()`才得到样本数量 |
| mse = 计算结果 | 把结果存为局部变量 | 调用者要拿到结果，还需要return |

这里至少有“没有建立的属性”“方法还没调用”“列表与数混用”三个不同问题，不是给某个名字统一加上或去掉self就能解决。

数学上，本课一条样本损失为`(预测−标签)**2/2`；多条样本先各算这一项，再求平均。不能把一个预测直接减整份标签列表，也不能省掉逐样本对应。不要为了写成一行而让这些中间含义消失。

允许设计一个方法直接接收model和data，内部完成取样、预测、求平均；那实际上承担了评估器的职责。我们拆成四类，是为了分别验证每一段计算，**不是Python规定模型必须写成四个类**。

### 5. 评估器的self为什么又不一样

评估器初始化时保存数据对象与损失对象，因此在`evaluate(self, model)`里用`self.data`和`self.loss`；待评估的model是本次传入的，所以用model。

设evaluator保存data_a与loss，调用`evaluator.evaluate(model_b)`：在evaluate里self是evaluator；取样时调用`self.data.get_item(0)`，进入get_item后，那个方法的self是data_a；调用`model_b.forward(x)`时，forward里的self是model_b；调用`self.loss.forward(prediction, target)`时，损失方法里的self是loss。

**self始终代表当前方法的接收对象，不是整份文件里同一个东西。** 对象组合只是一个对象保存另一个对象，然后调用它；不需要“类里面再定义类”，也不涉及继承。

类名相同不代表对象相同，方法同名也不代表工作相同。模型forward把输入变为预测；损失forward把预测和标签变为损失。看调用接收对象与参数，就能知道正在算哪一步。

### 6. 直接求导：到底是谁对谁求？

你已经有导数基础，今天不再用极限兜圈子。固定一条样本x、y，把损失看成w、b的函数：

`L(w, b) = 1/2 × (w*x + b - y)²`。

对w求偏导时，把x、y、b都当常量。链式法则给出：

- `∂L/∂w = (w*x+b-y) × x`；
- `∂L/∂b = (w*x+b-y) × 1`。

这叫**损失对权重/偏置求导**，不是权重对损失求导，也不只是预测对权重求导。预测对w的导数为x，它只是链式法则中的后一项。

固定x=2、y=5、b=0，得到`L(w)=1/2(2w-5)²=2w²-10w+12.5`，所以`L'(w)=4w-10`。w=1时导数为−6；在w<2.5这个区间，导数为负，函数随w增大而下降。这就是你熟悉的“导数符号判断单调性”，不是另一个神经网络规则。代入验证：w=1损失4.5，w=1.1损失3.92。负的是斜率，不是损失值。

梯度下降`w新 = w旧 - 学习率×∂L/∂w`：学习率为正，导数为负时减去负数，w增大；导数为正时w减小，沿着局部降低损失的方向移动。但步子过大可能越过最低点，并不保证任何学习率都下降。改变w、b时应先用同一组旧参数算出两项梯度，再更新。

全批量也是同一逻辑：平均损失是各样本损失之和除以N，其导数就是各样本导数之和除以N。必须在**同一个参数位置**求这些导数，才能称为该位置平均损失的梯度。边看样本边改参数会变成另一种更新过程，不再是这一次全批量更新。今天理解到这里，不再加实现任务。

## 六、模型04：分三段跑通，不新增训练器

只使用LinearNeuron、RegressionDataset、SquaredLoss、LossEvaluator。可复用你能解释的构造器和已正确的forward/get_item；自己修正size，独立补写损失计算及评估方法，再编写调用区。每段运行通过再继续，不要求一次从记忆抄出整套类。当天答案不预填进练习文件。

接口说明（不是让你照抄实现）：

- LinearNeuron保存weight、bias，`forward(x)`返回`w*x+b`。
- RegressionDataset保存xs、ys，`size()`返回数量，`get_item(index)`返回对应的一对数。本题只给等长、非空的合法数据。
- SquaredLoss的`forward(prediction, target)`返回单条半平方损失；`mean(predictions, targets)`返回多条平均值。本题也是等长、非空列表。
- LossEvaluator初始化接收data与loss并保存；`evaluate(model)`取样并预测，通过loss求平均，返回一个数。它不修改模型参数或原始数据。

### A段：对象保存什么，调用传入什么

准备两个模型：A的w=2、b=1，B的w=1、b=0。两个数据集：A为xs=[0,2]、ys=[1,5]；B为xs=[-1,1,3]、ys=[-1,3,7]。

验证两个size分别为2、3；A取第1项得到(2,5)，B取第2项得到(3,7)。两个模型对输入2分别返回5、2。调用区不要创建叫xs的全局变量来掩盖size的问题。

### B段：同一个损失对象多次计算

单条输入(3,5)得到2，接着(5,5)得到0，再调用(3,5)仍得到2。预测列表[1,3]与标签[1,5]的平均损失为1。先手算，再写代码检查，尤其注意return放在哪里。

### C段：换数据与换模型，不换评估算法

创建两个评估器，分别保存数据A、B，可以共用同一个损失对象。

| 调用 | 期望平均损失 |
|---|---:|
| 评估器A评估模型B | 2.5 |
| 评估器B评估模型B | 10/3 |
| 评估器A评估模型A | 0 |
| 再用评估器A评估模型B | 2.5 |

对B数据、B模型手算：三个误差为0、−2、−4，单条损失为0、2、8，平均10/3。浮点数比较可以沿用`abs(实际-期望)<1e-9`，不要求显示无限位小数。每次评估后模型B仍为w=1、b=0。通过这些替换检查理解，而不是只让一份固定样例碰巧运行。

今天只有四个简短理论回答，可写代码末尾注释，不另建表格：

1. 用你自己的代码举例，什么应写self.，什么不需要？依据不是“是不是在类里”。
2. `model.forward`与`model.forward(2)`分别是什么？evaluate不return会让调用方拿到什么？
3. x=2、y=5、w=3、b=0时，损失、对w与b的偏导数分别是多少？增大w在这一点附近会怎样？
4. 今天哪一段能关闭示范独立写出，哪一段仍卡住？只写真实情况。

## 七、DAY26全部示范答案与逐题对比（按需展开）

这些是昨天作业的参考，不是今天要全抄的任务。尤其最后的更新器和平均梯度部分只作昨日答案存档，**不要求今天实现或提前读完**。今天模型练习使用不同数据检验理解。

<details>
<summary>00｜1047：你的算法正确，参考只简化分支</summary>

```python
class Solution:
    def removeDuplicates(self, s):
        stack = []
        for char in s:
            if stack and stack[-1] == char:
                stack.pop()
            else:
                stack.append(char)
        return "".join(stack)

solver = Solution()
for text, expected in [("abbaca", "ca"), ("azxxzy", "ay"),
                       ("aaaa", ""), ("abab", "abab"), ("a", "a")]:
    assert solver.removeDuplicates(text) == expected
```

`and`在左侧为空时不会继续读`stack[-1]`，这叫短路求值。你先判断空再判断末项的写法同样正确，并不需要改。

</details>

<details>
<summary>01｜字典：统一返回两项，去掉重复检查</summary>

```python
def analyze_text(s):
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    for index in range(len(s)):
        if counts[s[index]] == 1:
            return counts, index
    return counts, -1

assert analyze_text("") == ({}, -1)
assert analyze_text("aabc") == ({"a": 2, "b": 1, "c": 1}, 2)
assert analyze_text("abacb") == ({"a": 2, "b": 2, "c": 1}, 3)
assert analyze_text("aabb") == ({"a": 2, "b": 2}, -1)
assert analyze_text("z") == ({"z": 1}, 0)

# 昨日字典操作短检查；不影响上面的主算法。
counts, index = analyze_text("aabc")
assert counts.get("z", 0) == 0
assert "z" not in counts
for char, count in counts.items():
    print(char, count)
assert sum(counts.values()) == 4
copied = counts.copy()
copied["a"] = 99
assert counts["a"] == 2
```

你的计数无需重学。参考第二遍直接按原文位置查计数，使“第一个”的含义更直观；不是说遍历字典一定错。`return counts, index`两种分支一致，调用方就能稳定接收。

</details>

<details>
<summary>02｜C++总耗时：保留你的求和，去掉main里的额外打印</summary>

```cpp
#include <cassert>
#include <iostream>
#include <vector>

int total_duration(std::vector<int> durations) {
    int total = 0;
    for (int duration : durations) {
        total += duration;
    }
    return total;
}

int main() {
    std::vector<int> original = {3, 7};
    std::vector<int> copied = original;
    copied[0] = 9;
    assert(original[0] == 3);
    assert(copied[0] == 9);
    assert(total_duration({}) == 0);
    assert(total_duration({2, 5}) == 7);
    assert(total_duration({1}) == 1);

    int n;
    std::cin >> n;
    std::vector<int> durations;
    for (int i = 0; i < n; i++) {
        int value;
        std::cin >> value;
        durations.push_back(value);
    }
    std::cout << total_duration(durations) << '\n';
    return 0;
}
```

空容器时循环不执行，total仍为0，所以无需单独分支；你写空判断也是对的。断言通过时不打印东西。原main逐项打印用于观察可以理解，最终输出约定只需总和。

</details>

<details>
<summary>03｜C++超时数量：你的核心实现正确</summary>

```cpp
#include <cassert>
#include <iostream>
#include <vector>

int count_over_limit(std::vector<int> durations, int limit) {
    int count = 0;
    for (int duration : durations) {
        if (duration > limit) {
            count++;
        }
    }
    return count;
}

int main() {
    assert(count_over_limit({}, 8) == 0);
    assert(count_over_limit({8, 9, 7}, 8) == 1);
    assert(count_over_limit({8, 8}, 8) == 0);
    int n;
    std::cin >> n;
    std::vector<int> durations;
    for (int i = 0; i < n; i++) {
        int value;
        std::cin >> value;
        durations.push_back(value);
    }
    int limit;
    std::cin >> limit;
    std::cout << count_over_limit(durations, limit) << '\n';
    return 0;
}
```

参考count只是把含义写得直观，你的total命名不会改变正确性。每次调用重新建立局部计数，比单纯通过一次样例更重要，这一点已经通过补测。

</details>

<details>
<summary>04A｜模型前四类：对照self、输入和返回；不要机械全抄</summary>

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
single_data = RegressionDataset([2], [5])
single_evaluator = LossEvaluator(single_data, loss)
single_model = LinearNeuron(1, 0)
assert single_data.size() == 1
assert single_evaluator.evaluate(single_model) == 4.5
assert loss.mean([0, 2], [1, 5]) == 2.5
```

这里假定数据合法、非空且配对等长，与你当前练习一致；不是完整生产级数据校验库。你的LinearNeuron和get_item已经写对，size只修读取来源。损失的参数与属性不混用，评估器把每个样本的数值送给下一段方法，最后返回平均损失。

</details>

<details>
<summary>04B｜昨日未完成部分的完整存档：一步更新与全批量梯度（今天不要求做）</summary>

本段接在04A代码之后运行，不引入Trainer或fit。

```python
class GradientDescent:
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate

    def step(self, model, grad_w, grad_b):
        model.weight -= self.learning_rate * grad_w
        model.bias -= self.learning_rate * grad_b


def batch_gradients(model, data):
    total_w = 0
    total_b = 0
    for i in range(data.size()):
        x, y = data.get_item(i)
        error = model.forward(x) - y
        total_w += error * x
        total_b += error
    return total_w / data.size(), total_b / data.size()


# 单样本：两项梯度都在更新前计算。
x, y = single_data.get_item(0)
error = single_model.forward(x) - y
grad_w = error * x
grad_b = error
assert (grad_w, grad_b) == (-6, -3)
optimizer = GradientDescent(0.1)
optimizer.step(single_model, grad_w, grad_b)
assert abs(single_model.weight - 1.6) < 1e-9
assert abs(single_model.bias - 0.3) < 1e-9
assert abs(single_evaluator.evaluate(single_model) - 1.125) < 1e-9

# 学习率0：另建相同初始模型，不延续刚刚更新的参数。
unchanged = LinearNeuron(1, 0)
GradientDescent(0).step(unchanged, -6, -3)
assert single_evaluator.evaluate(unchanged) == 4.5

# 全批量：所有样本使用同一份旧参数，算完后只更新一次。
batch_data = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
batch_model = LinearNeuron(0, 0)
batch_evaluator = LossEvaluator(batch_data, loss)
assert batch_evaluator.evaluate(batch_model) == 4.5
grad_w, grad_b = batch_gradients(batch_model, batch_data)
assert (grad_w, grad_b) == (-3.5, -2.0)
optimizer.step(batch_model, grad_w, grad_b)
assert abs(batch_model.weight - 0.35) < 1e-9
assert abs(batch_model.bias - 0.2) < 1e-9
assert abs(batch_evaluator.evaluate(batch_model) - 3.021875) < 1e-9
```

这是参考实现的验证结果，不是你的完成记录。你尚未实现这些部分，今天也不因此增加第六份作业。先把四类协作独立跑通，再回来接上参数更新。

</details>

### DAY26理论问题示范回答

1. 键是字符，值是出现次数；get缺失时返回默认值但不插入。你答对了。
2. 20存未闭合左括号，1047存未抵消字符；抵消必须相邻，次数不能代替顺序。你答对了。
3. `vector<int>`按值传入后内容起初相同，但整数容器独立；复制n项需要时间和内存，不能说没有成本。今天不要求解释内存地址。
4. 对损失L求关于w、b的偏导。负导数表示相应变量增大时，函数在该点附近沿下降方向变化；减去梯度就是走相反方向。全批量要在同一参数位置把各样本梯度平均，具体公式见第五节。
5. 加不加self由数据属于哪里决定，不由“是不是类的方法”决定。调用参数不会自动成为属性；forward要调用才得到预测，标签列表要逐样本对应，结果要return。这正是今天的主要练习，不以昨天曾经运行成功就跳过去。

## 八、今天交付到哪里，明天如何判断

只交这五份代码及必要运行结果；心得仍可自由写，不要求新增记录文件。模型完成A/B/C哪一段就如实说明。老师下次会读取代码里的备注及课后总结。

DAY28不增加新知识：按DAY27实际结果验收Python、C++与四类评估链及已讲导数。参数更新、平均梯度、Trainer/fit、最终100步训练实验目前仍是**待完成目标**；如果没有独立实现证据，就顺延后续课，不宣称本轮训练系统已完成。DAY20的Embedding完整接入也仍待独立验证，不悄悄销账。

今天的进步标准不是记住四份代码，而是换模型、换数据、隔开调用后，仍能说清每个值从哪里来、怎样算、返回给谁。
