# DAY32｜安全合并有序数据、引用与const、完成100步模型训练

> 2026-10-23发布。依据[学习与授课总约定](../学习与授课总约定.md)与[阶段计划](../DAY29-DAY39_阶段计划.md)，每天约4小时。今天新题88、复习修正977；C++学习引用与只读接口；模型为正确的Trainer新增fit。
>
> 五份练习仍只放题目说明。自己的三步分析保留，不增加记录流程。DAY31完整示范与比较在文末，可按疑问展开。今天的新题、新函数由你实现。

## 一、DAY31评语：有进步，也找到了一个需要真正修正的循环问题

已经阅读五份代码、代码注释及《课后总结.md》，运行原脚本并补测。原脚本都能运行；额外输入揭示的问题如下。闭卷用时与提示情况未记录，综合评分仍待独立验收。

| 项目 | 核对结果 | 评价与今天的动作 |
|---|---|---|
| 977 | 原样例及已有断言通过；枚举长度1—8、值-2—2的1,286组有序输入，808组正确、478组结果错误 | 两端取最大方向正确；相等时一次填两格与固定n轮冲突，需要修循环推进 |
| 27 | 13,120组输入的k与原列表前缀全部正确 | 交换思路正确；返回元组的问题仍在，改为只返回k即可 |
| C++02 | C++17编译无警告，100组完整输入通过 | 指针副本、改指向与改内容正确；空指针判断已写，原调用区未实际传nullptr |
| C++03 | 编译无警告，100组完整输入通过，含n=0、n=6、delta=0 | 显式传长度、读原数组、原地修改正确 |
| 模型Trainer | 140组数据、参数和学习率场景，每组连续两步，对照独立公式通过，含学习率0 | 平均梯度、原实例更新、训练流程与返回损失均正确，已具备新增fit的基础 |
| 理论心得 | 能解释平方最大值在两端、对象参数能被下一次使用；提出普通函数与类的疑问 | 加深循环状态、函数与类的分工；手算及完整闭卷保持仍需另有证据 |

这些测试是教师提供的实现证据。缺一条记录不要求整天重学，确实错误的循环通过小反例修正后继续新题。

### 1. 977的错误来自哪里

看[-2,-1,-1]，正确答案应为[1,1,4]：

| 外层轮次 | 你的动作 | 结果与位置 |
|---|---|---|
| 第1轮 | 左端绝对值2较大，填右端4 | square=[0,0,4]，待写位置变1 |
| 第2轮 | 剩余两端绝对值都1，一次填两项 | square=[1,1,4]，待写位置变-1，实际已经完成 |
| 第3轮 | for仍要执行，-1又满足“!=0” | 继续写负下标，把已经正确的4覆盖成1 |

Python的-1下标表示最后一项，因此这次没有报错，而是悄悄改坏结果。不能用“没有异常”判断循环边界正确。

你会比较两端、会从后填，也会移动下标。真正要接上的关系是：**每轮做多少工作，循环总共就应该安排多少轮。** 相等时一次处理两项也可以，但必须配套正确的剩余区间与停止判断。最容易验证的修法是每轮只处理一个元素，相等时任选一端，让n轮恰好填n项。你自己在复习文件重写；文末给完整参考。

这条原则也用于今天88：写入位置必须只覆盖已经安全处理的位置，不能让一个分支多做一步而其他状态没同步。

### 2. 27保留你的算法，局部修正即可

你的[3,2,4,2,3]排除3，正确有效长度为3，前缀[2,4,2]，不是注释里的2；代码算得对，例子漏了合法值4，改注释即可。

返回值应为k这个整数。原列表已修改，调用者本来就拿着nums，可以在外面看nums[:k]，无需再把nums放入返回值。今天口头说明并在原代码的后续自测中改一次即可，不新增第三道Python必做题，也不代改你的提交。

### 3. 为什么batch_gradients可以是普通函数，不写成类？

因为它完成一次计算，所需信息都已由model和data传入；这次用到的梯度累计只是临时变量，调用结束就可以交回结果，没有必须跨调用保存的新状态。

**普通函数（function）**很适合“收到输入→计算→返回”。**类（class）**适合把一组持续保存的状态与相关操作组织在一起。不是模型有关的每段代码都要包进类。

对应到你的实现：
- batch_gradients只需当前模型和数据，不必另外创建一个“梯度计算对象”。
- LinearNeuron保存持续变化的权重、偏置，forward反复使用它们，适合用类。
- GradientDescent保存学习率，step反复使用；它也能写成带学习率参数的普通函数，当前类设计便于配置和组合。
- Trainer保存同一模型、数据、损失和优化器，把一套训练过程组织起来，后面fit会多次使用。

如果确实需要保存缓存或自定义计算策略，也可以再设计梯度计算类。**判断依据是状态与职责，不是“面向对象越多越高级”。**

你说“第二次接着第一次，因为参数已经改了”正确；不必进一步推成“只有类才有持续状态”。普通函数同样能修改传入对象，关键是后一次仍使用已经更新的那个对象。你第二次新建了Trainer，但传入的是同一个model，因此结果正确；今天复用同一个Trainer，代码更直接。

### 4. C++注释补一句就清楚

p[i]与*(p+i)在合法范围内等价，你理解的元素偏移也正确。不过“数组名和指针都是指针变量”不准确：指针变量可以改指向；数组对象不会因此变成指针变量，也不能给数组名重新赋一个地址。

这不影响你已经写对的数组调用。今天引用和指针一起比较时，把“对象”“对象地址”“保存地址的变量”分开看即可。

今天时间：Python65分钟（977修正20、新题35、测试10），C++100分钟，模型65分钟，保存反馈10分钟。

## 二、Python：复习977，新增88（65分钟）

### 1. 977修正复写，20分钟

文件：`01_Python复习_LeetCode977_有序数组的平方.py`。

关闭旧实现和文末示范，继续使用两端取最大，输出新列表、输入不改。目标O(n)时间，结果空间O(n)。自己决定每轮处理数量、下标推进和停止条件，不预填三步。

优先测[-2,-1,-1]→[1,1,4]、[-2,-1,1,2]→[1,1,4,4]、[-2,2]→[4,4]、[0]→[0]、[-3,-2,-1]→[1,4,9]。解释“左右相等时只选一个端点，为什么另一份数据仍会在后面被处理”。

修正卡住时可以看文末，但看后关闭再写，不让它取消今天88新内容。

### 2. 新题88：两个有序区间怎样放回同一份存储

[LeetCode88官方题目](https://leetcode.com/problems/merge-sorted-array/description/)，简单。接口：`Solution.merge(self, nums1, m, nums2, n)`。

nums1前m项是有效数据，后面n项预留位置；nums2有n项有效数据。把两组数据合并成非递减顺序，**结果写回nums1，不返回合并列表**。本课程要求保留nums2，目标O(m+n)时间、O(1)额外空间。

例如nums1=[1,2,3,0,0,0]、m=3，nums2=[2,5,6]、n=3，最终nums1=[1,2,2,3,5,6]。末尾0只是预留位置，是否有效由m决定，不能靠“值是不是0”判断。

如果nums1=[0,0]、m=1，nums2=[-1]、n=1，第一个0是真数据，第二个0是空位，最终[-1,0]。这正好检验你有没有读清“有效长度”。

### 3. 为什么从前面写容易丢数据

把[2,4,0,0]与[1,3]合并。如果先把较小的1写到nums1[0]，原来的2还没安置就被覆盖了。新列表能暂存它，但今天希望使用原来的预留空间。

你在977里已经把最大值放到结果最右边。88也可以先考虑两个有效区间各自最大的值：它们在哪里？结果最右边的预留位置是否已经需要保留原数据？安置一个值后，哪一组的有效区间缩小？

**合并（merge）**利用两个输入各自已经有序，从两组候选里选择下一项，逐步形成有序结果。它不是把所有数据再完整排序一遍。今天不给完整循环或伪代码，你把“读位置、写位置、剩余有效数据”自己对应到小例子。

结束时尤其要想两种情形：nums2先用完，nums1剩余部分要不要搬？nums1有效部分先用完，nums2剩余值应该放哪里？m=0不代表nums1没有存储，它仍有预留位置。

### 4. 独立实现与测试，约35分钟＋10分钟检查

文件：`00_Python新题_LeetCode88_合并两个有序数组.py`。

| nums1 / m | nums2 / n | 最终nums1 |
|---|---|---|
| [1,2,3,0,0,0] / 3 | [2,5,6] / 3 | [1,2,2,3,5,6] |
| [1] / 1 | [] / 0 | [1] |
| [0] / 0 | [1] / 1 | [1] |
| [2,4,0,0] / 2 | [1,3] / 2 | [1,2,3,4] |
| [0,0] / 1 | [-1] / 1 | [-1,0] |
| [2,2,0,0] / 2 | [2,2] / 2 | [2,2,2,2] |

调用后检查nums1，而不是把方法返回值当合并结果。没有显式return值时得到None，这与本题接口一致。不通过`nums1 = new_list`只改局部名字来替代写回。

面试表达只需说清：哪部分还没处理、为什么当前写入不会破坏未来数据、每轮至少减少了什么。三步仍由你自己写。

## 三、C++：引用让函数直接使用原对象，const限制修改（100分钟）

教材选读《C++ Primer Plus》8.2.1—8.2.3，书内256—261页（PDF274—279页）。从昨天的指针修改原数据接起。

### 1. 已经会指针，引用还解决什么问题

昨天函数接收地址，通过*target访问原对象。若希望把一个已有对象交给函数使用，又不想每次在调用处写取地址、函数内写解引用，可以使用**引用（reference）**。

引用相当于给已有对象再取一个名字。它不是先复制一份内容。今天只学指向现有对象的普通左值引用，暂不加入移动语义。

```cpp
#include <iostream>
int main() {
    int duration = 12;
    int& other_name = duration;
    other_name += 3;
    std::cout << duration << " " << other_name << "\n";
    std::cout << (&duration == &other_name) << "\n";
    return 0;
}
```

输出15 15、1。声明里的&表示“引用类型”，表达式里的&duration则仍是取地址；同一个符号在不同语法位置含义不同。

引用声明时就要绑定对象。绑定后`other_name = another_value;`是把值写到原对象，不是让引用改为另一个对象的别名。相比之下，昨天的指针p可以通过`p = &another;`改指向。

### 2. 值传递和引用传递，调用看起来相似，结果不同

```cpp
#include <iostream>
void change_copy(int value) {
    value += 5;
    std::cout << value << "\n";
}
void change_original(int& value) {
    value += 5;
}
int main() {
    int score = 10;
    change_copy(score);
    std::cout << score << "\n";
    change_original(score);
    std::cout << score << "\n";
    return 0;
}
```

输出15、10、15。第一个函数改了自己的整数副本；第二个的value是调用者score的别名，改它就是改score。

调用处都像传普通变量，是否修改原对象要读声明。函数签名因此不仅告诉你类型，也表达数据是否可能被改。不要仅凭`function(values)`的外观判断是否复制。

| 参数写法 | 本课含义 | 调用形式 | 是否能通过它改原数据 |
|---|---|---|---|
| int value | 整数副本 | f(x) | 否 |
| int* p | 地址副本，沿地址访问原对象 | f(&x) | 有效地址下可用*p修改 |
| int& value | 原整数的别名 | f(x) | 可以 |
| const int& value | 通过该名字只读访问 | f(x) | 不能通过该引用修改 |

本课普通引用应绑定有效对象，没有用nullptr表示“没绑定”的正常状态；需要可选空值时，昨天的指针可以明确表示。别通过空指针解引用伪造引用。

### 3. vector为什么特别值得用引用传参

普通`std::vector<int> values`形参会复制整个容器。若n项只读统计就复制n项，数据变大后会带来额外成本。

引用形参`std::vector<int>& values`直接使用原容器，函数内修改元素会改到调用者数据。昨日原生数组传参按地址访问原元素，今天vector通过引用也能达到访问原对象的目的，但两者的类型和长度管理不同；不要把规则混成“所有容器默认都是地址”。

范围for也要留意：
```text
for (int value : values)       // 每次value是元素副本，修改value不改元素
for (int& value : values)      // 每次value引用实际元素，修改value会改元素
```

你可以继续用已会的下标循环；若使用范围for修改元素，要明确&的作用。只读取时用int value复制一个小整数就足够，不要求每个循环都加引用。

### 4. const：让“只读”成为编译器检查的约定

**const**表示通过这个声明限制修改。普通`const int limit = 10;`初始化后不能再对limit赋新值。

`const std::vector<int>& values`表示不复制容器，并且不允许函数通过这个引用修改容器。它非常适合求总和、统计数量、评估等只读工作。

例如声明`int number_of_items(const std::vector<int>& values);`，函数可以读size()和元素，不能对values[0]赋值、push_back或清空它。下面的完整小例子只验证只读传参：

```cpp
#include <iostream>
#include <vector>
int number_of_items(const std::vector<int>& values) {
    return values.size();
}
int main() {
    std::vector<int> current = {3, 7};
    const std::vector<int> fixed = {2, 4, 6};
    std::cout << number_of_items(current) << " "
              << number_of_items(fixed) << "\n";
    return 0;
}
```

输出2 3。普通容器和const容器都能交给这个只读接口。这里示例长度很小，int能容纳；不把size()转换问题变成今天的主要内容。

const引用不等于原对象从此不能改变：如果原对象本来可修改，外部仍可能通过别的合法名字修改它；这个函数只承诺不通过自己的const引用修改。

和昨天指针对照：`const int* p`限制通过*p改整数，但p本身仍可以改指向。今天先看懂这句话，不增加const指针组合的额外作业。

### 5. 两项独立实践，45分钟手敲＋10分钟检查

**02：改副本与改原容器**

文件：`02_C++核心_值传递与引用传递.cpp`。

自行实现两个函数：

| 接口 | 作用 |
|---|---|
| std::vector<int> shifted_copy(std::vector<int> values, int delta) | 修改本地副本，各项加delta，返回它 |
| void shift_original(std::vector<int>& values, int delta) | 原容器各项加delta |

main读取n（0—6）、n个整数、delta（-10—10）。先调用shifted_copy，把返回结果存为另一个容器；打印原容器和返回容器。再调用shift_original处理原容器，最后打印原容器。三行分别输出各容器元素，空容器对应空行。

输入3 4 10 20 2，三行应为4 10 20、6 12 22、6 12 22。输入0 5，输出三个空行；输入2 -1 3 0，三行内容相同但来自不同对象。

只读与修改职责由形参体现；调用后原容器是否改变，需要用结果验证，不凭函数名猜。

**03：只读统计接口**

文件：`03_C++应用_const引用统计.cpp`。

自行实现`int total_duration(const std::vector<int>& values)`和`int count_over(const std::vector<int>& values, int threshold)`。返回总和、严格超过阈值的数量，不修改原容器、不打印。

main读取n（0—6）、n个非负整数、threshold（0—30）；第一行输出总和，第二行输出数量，第三行打印原容器。最后建立const容器{2,10,15}，调用同样接口，阈值10，第四行输出27 1。

输入3 4 10 20 10：前三行34、1、4 10 20，最后27 1。空容器输入0 10：总和0、数量0、空行，最后仍27 1。用输入前后内容核对只读承诺。

声明在main前、定义在后。若临时尝试在const引用函数里改values[0]，编译器应拒绝；看懂错误后撤掉该行，最终程序正确编译。这是一条可选观察，不新建第六份练习。

编译：
```bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY32/02_C++核心_值传递与引用传递.cpp" -o /tmp/day32-reference
/tmp/day32-reference
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY32/03_C++应用_const引用统计.cpp" -o /tmp/day32-const
/tmp/day32-const
```

## 四、模型：从两次调用到能持续学习的fit（65分钟）

教材承接《神经网络与深度学习》2.2.3.1迭代更新、2.2.3.2停止条件，以及第2.3节线性回归。fit是课程对训练循环的封装，沿用你已经写对的Trainer和平均梯度。

### 1. 一次改得更好，怎样逐步接近目标关系

模型w=b=0时，总是预测0；第一次更新让预测靠近标签；第二次根据新误差继续调整。随着参数变化，每次都重新计算当前梯度，才是一次次在新的位置寻找下降方向。

```text
当前参数 → 当前预测 → 平均损失与梯度 → 更新参数
   ↑                                    |
   └──────── 下一步使用更新后的参数 ───────┘
```

你已实现这个环中的一次，即train_step。现在新增`fit(steps)`，让同一个训练器连续调用它指定次数，并把损失记录下来。不要在循环内把模型重置为(0,0)，也不要重建优化器或数据集。

**迭代（iteration）/训练步（step）**指一次参数更新。**轮次（epoch）**指训练数据被完整遍历一次。本课每次使用全体样本做一次更新，所以一次训练步对应一轮；以后小批量训练一轮通常包含多次更新，二者不总相同。

### 2. loss序列怎样回答“训练到底有没有工作”

只看最后一次损失，可能看不出初值多大、下降是否停滞。把每一步的损失存成列表，就得到数值形式的**学习曲线（learning curve）**。

本课fit约定返回**初始损失＋每次更新后的损失**，因此steps=100返回101个数。history[0]表示训练前，history[1]表示一步后，history[-1]表示最后一次后。steps=0返回只含当前损失的列表，不更新参数。

这里只保存数字，不用Matplotlib、文件保存或计时库。现有列表、append和循环足够。

固定实验的参考检查点：

| 完成更新次数 | 平均半平方损失（约） |
|---|---:|
| 0 | 4.5 |
| 1 | 3.021875 |
| 2 | 2.0298046875 |
| 10 | 0.0862333634 |
| 50 | 0.0000108339 |
| 100 | 0.00000000841 |

这些是这组线性数据和α=0.1下的结果，不要求所有模型都这样单调下降。DAY33会比较学习率为0、正常值和过大值。

### 3. 何时停止，为什么今天先用固定步数

停止条件必须具体：例如最多更新100次；或者梯度很小、训练损失变化很小；或者独立验证集的表现不再改善。

“收敛（convergence）”在这里可以先理解为迭代逐渐接近稳定结果；训练损失下降不自动证明未见数据表现好。教材的提前停止需要观察验证集，不应该用最终测试答案不断调参数。

今天只实现固定步数，便于核对是否真的更新100次。loss阈值是验收结果条件，不用它提前终止本次100步实验；其他停止策略先理解用途，不要求同时加多个接口。

### 4. 未见输入用来检查学到的关系

训练输入[-1,0,1,2]，标签[-1,1,3,5]来自y=2x+1。训练程序应只利用样本求梯度，不把2和1直接赋给参数。

100步后应接近w=1.999918、b=1.000133，输入3、4的预测约为6.999887、8.999805。它们没出现在训练输入中，可检查模型是否接近这条关系。

这组数据是人工线性数据，x=3、4位于训练范围外。预测正确说明当前线性模型和训练流程适合这个构造问题，不能据此宣称对任意现实数据都能外推。后面评估与模型局限课会继续解释。

### 5. 独立实现：只新增fit与实验调用（25分钟代码＋10分钟手算）

文件：`04_模型实践_fit训练循环.py`。

复用你DAY31正确的六个类和batch_gradients（六类为模型、数据、损失、评估器、优化器、训练器），不要重新抄出一套略有不同的实现。

新增`Trainer.fit(self, steps)`：
- steps为非负整数；在当前模型上执行恰好steps次train_step。
- 返回本节约定的损失列表，长度steps+1；没有循环内return，也不把return写成每轮提前结束。
- 每次都通过已有train_step求新梯度、更新同一模型；不使用一个固定旧梯度更新100次。
- fit可再次调用，接着当前参数继续训练；只重建本次返回的记录列表，不重置模型状态。

主实验：数据按本节固定，初始w=b=0、α=0.1，运行fit(100)。检查长度101、初始损失4.5、末损失小于0.001、预测3与4的绝对误差分别小于0.01；打印初值、末值、最终参数、两预测即可，不刷屏打印所有循环内部结果。

再在同一文件完成两个短验证：
1. 新建独立同配置模型，先fit(10)，再fit(90)，终点应与fit(100)一致（浮点容差1e-9）；第二段记录的首项应等于第一段的末项。
2. 对当前模型运行fit(0)，只返回当前损失，参数保持不变。

零学习率原实现已由教师补测通过；本次不重复加一整套对照作业，明天统一做学习率实验。今天可以观察自己想补的案例，不因此多建文件。

手算：x=[0,1]、y=[1,3]、初始w=b=0、α=0.1，连续计算两步参数。第二步要重新算误差和梯度。把结果交给自己的fit(2)核对，不额外写长报告。

## 五、交付与下一步

今天五项：88新题、977修正复习、C++副本/引用实验、const只读统计、模型fit。仍由你写三步分析，课后总结自愿。

优先检查：
- Python能说明每轮处理数量与终止条件，写入不破坏未读数据；
- C++能用形参解释复制、修改原对象与只读访问；
- 模型fit使用原状态继续训练，损失记录与更新次数对应。

只需口述：88为什么从后填安全；引用赋值为什么不改绑定；普通函数与类怎样选择；fit(10)再fit(90)为什么接得上。用时和参考过的范围注明一句，方便下一课判断独立掌握程度。

DAY33按计划检查三条线进度：Python新题349、C++内存与生命周期、模型学习率对照。具体任务在读完今天反馈后生成。今日原代码不代改，Git由你保存提交。

## 六、DAY31全部示范与对照

先完成977的独立修正，再按需展开第一题参考。其他参考可直接用于对照；不要求全部重新手敲。今天88、引用作业与fit实现不在这里预填。


<details>
<summary>00｜977：保持两端比较，每轮只填一格</summary>

```python
class Solution:
    def sortedSquares(self, nums):
        result = [0] * len(nums)
        left = 0
        right = len(nums) - 1
        write = len(nums) - 1

        while left <= right:
            if abs(nums[left]) > abs(nums[right]):
                result[write] = nums[left] ** 2
                left += 1
            else:
                result[write] = nums[right] ** 2
                right -= 1
            write -= 1
        return result

solver = Solution()
for original, expected in [
    ([-4, -1, 0, 3, 10], [0, 1, 9, 16, 100]),
    ([-2, -1, -1], [1, 1, 4]),
    ([-2, -1, 1, 2], [1, 1, 4, 4]),
    ([-2, 2], [4, 4]),
    ([-3, -2, -1], [1, 4, 9]),
    ([0], [0]),
]:
    values = original.copy()
    assert solver.sortedSquares(values) == expected
    assert values == original
```

你的比较方向与从右填结果已正确。参考做三处简化：相等时选择右端一次；每轮只把write减1；以剩余区间是否为空控制循环。没有再单独把write==0做成特殊分支，所以不会完成后又用负下标覆盖结果。

时间O(n)，结果列表O(n)，输入保持不变。测试直接核对已知结果；每种长度、两端相等与负数重复都要考虑，避免只用一个包含0的样例判断全部正确。

</details>

<details>
<summary>01｜27：你的交换算法正确，只修平台返回类型</summary>

```python
class Solution:
    def removeElement(self, nums, val):
        auxiliary = 0
        for query in range(len(nums)):
            if nums[query] != val:
                nums[auxiliary], nums[query] = nums[query], nums[auxiliary]
                auxiliary += 1
        return auxiliary

solver = Solution()
values = [3, 2, 4, 2, 3]
k = solver.removeElement(values, 3)
assert k == 3
assert values[:k] == [2, 4, 2]
assert solver.removeElement([], 0) == 0
```

你已正确维护有效前缀。参考省掉pass分支，行为相同；return只交整数。三步分析中[3,2,4,2,3]排除3要保留4，修这一行例子即可。算法O(n)、O(1)。

</details>

<details>
<summary>02｜指针读写：保留你的实现，补一次nullptr调用</summary>

```cpp
#include <iostream>
void add_to(int* target, int delta);

int main() {
    int original;
    int delta;
    std::cin >> original >> delta;
    int* position = &original;
    int* copied_position = position;
    add_to(position, delta);
    std::cout << original << " " << *copied_position << "\n";

    int another = 100;
    position = &another;
    *position = 200;
    std::cout << original << " " << another << " "
              << *copied_position << "\n";

    add_to(nullptr, delta);
    return 0;
}

void add_to(int* target, int delta) {
    if (target != nullptr) {
        *target += delta;
    }
}
```

调用和输出与你等价。你的nullptr判断已正确，原main没有实际传空指针；参考补这一次调用，验证函数不访问空地址。无需把已会的普通指针读写重做一天。

</details>

<details>
<summary>03｜数组传参：参考保持int*与显式长度</summary>

```cpp
#include <iostream>
int sum_values(int* values, int length);
void shift_values(int* values, int length, int delta);

int main() {
    int values[6] = {};
    int n;
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cin >> values[i];
    }
    int delta;
    std::cin >> delta;
    std::cout << sum_values(values, n) << "\n";
    shift_values(values, n, delta);
    std::cout << sum_values(values, n) << "\n";
    for (int i = 0; i < n; ++i) {
        std::cout << values[i] << " ";
    }
    std::cout << "\n";
    return 0;
}

int sum_values(int* values, int length) {
    int total = 0;
    for (int i = 0; i < length; ++i) {
        total += values[i];
    }
    return total;
}

void shift_values(int* values, int length, int delta) {
    for (int i = 0; i < length; ++i) {
        values[i] += delta;
    }
}
```

你的location=&array_in_built[0]与直接传数组名在此调用中等价。参考省去中间指针变量，不代表你多写这个变量错了。n=0时数组仍实际有6格，只是函数处理长度0，所以不访问任何项。

sum_values的int*能读也有能力写，实际实现没有修改；今天学const之后能进一步把只读意图写进接口。文末先保留昨天已教写法，便于看清进度。

</details>

<details>
<summary>04｜Trainer：你的六个类及平均梯度已正确，参考补连续调用断言</summary>

```python
class LinearNeuron:
    def __init__(self,weight,bias):
        self.weight = weight
        self.bias = bias
    def forward(self,x):
        return self.weight * x + self.bias

class RegressionDataset:
    def __init__(self,xs,ys):
        self.xs = xs
        self.ys = ys
    def size(self):
        return len(self.xs)
    def get_item(self,index):
        return self.xs[index],self.ys[index]

class SquaredLoss:
    def forward(self,prediction,target):
        loss = ((prediction - target)**2)/2
        return loss
    def mean(self,predictions,targets):
        total = 0
        for i in range(len(predictions)):
            total += self.forward(predictions[i],targets[i])
        return total/len(predictions)

class LossEvaluator:
    def __init__(self,dataset,loss):
        self.dataset = dataset
        self.loss = loss
    def evaluate(self,model):
        predictions = []
        for i in range(self.dataset.size()):
            xs,ys = self.dataset.get_item(i)
            prediction = model.forward(xs)
            predictions.append(prediction)
        mse = self.loss.mean(predictions,self.dataset.ys)
        return mse

class GradientDescent:
    def __init__(self,learning_rate):
        self.learning_rate = learning_rate
    def step(self,model,g_w,g_b):
        model.weight -= self.learning_rate * g_w
        model.bias -= self.learning_rate * g_b

def batch_gradients(model, data):
    g_w ,g_b = 0,0
    for i in range(data.size()):
        xs,ys = data.get_item(i)
        g_w += (model.forward(xs) - ys) * xs
        g_b += (model.forward(xs) - ys) * 1
    return g_w/data.size(),g_b/data.size()

class Trainer:
    def __init__(self,model,data,loss,optimizer):
        self.model = model
        self.data = data
        self.loss = loss
        self.optimizer = optimizer

        # 建立对应的评估器
        self.evaluator = LossEvaluator(self.data,self.loss)
    def train_step(self):
        #1.用旧参数计算损失
        old_loss = self.evaluator.evaluate(self.model)

        #2.计算平均梯度
        mean_g_w,mean_g_b = batch_gradients(self.model,self.data)

        #3.计算新参数并更新模型参数
        self.optimizer.step(self.model,mean_g_w,mean_g_b)

        #4.用更新参数后的模型重新计算新损失
        new_loss = self.evaluator.evaluate(self.model)

        return old_loss,new_loss

model = LinearNeuron(0, 0)
alias = model
data = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
loss = SquaredLoss()
optimizer = GradientDescent(0.1)
trainer = Trainer(model, data, loss, optimizer)

old_first, new_first = trainer.train_step()
assert abs(old_first - 4.5) < 1e-9
assert abs(new_first - 3.021875) < 1e-9
assert abs(model.weight - 0.35) < 1e-9
assert abs(model.bias - 0.2) < 1e-9

old_second, new_second = trainer.train_step()
assert abs(old_second - new_first) < 1e-9
assert abs(new_second - 2.0298046875) < 1e-9
assert abs(model.weight - 0.6375) < 1e-9
assert abs(model.bias - 0.3625) < 1e-9
assert trainer.model is model and model is alias
assert data.xs == [-1, 0, 1, 2] and data.ys == [-1, 1, 3, 5]

still = LinearNeuron(0, 0)
still_trainer = Trainer(still, data, loss, GradientDescent(0))
old_still, new_still = still_trainer.train_step()
assert old_still == new_still == 4.5
assert still.weight == 0 and still.bias == 0

manual_model = LinearNeuron(1, 0)
manual_data = RegressionDataset([0, 1], [1, 3])
manual_trainer = Trainer(manual_model, manual_data, loss, GradientDescent(0.1))
manual_old, manual_new = manual_trainer.train_step()
assert abs(manual_old - 1.25) < 1e-9
assert abs(manual_new - 0.94625) < 1e-9
assert abs(manual_model.weight - 1.1) < 1e-9
assert abs(manual_model.bias - 0.15) < 1e-9
print("DAY31 Trainer验证通过")
```

类与平均梯度保留你的计算；train_step已正确。参考主要将第二次新建Trainer改为直接复用同一trainer，并补参数、损失连续性、数据不变、学习率0与指定手算案例的断言。

你原代码第二次创建的Trainer拿到相同model，故也会接着已更新的参数，并没有重置。这里是减少不必要的创建，不是修正数值错误。batch_gradients写普通函数即可，理由见第一节；无需再造一个只包一条计算流程的类。

</details>

### DAY31理论示范回答

1. 非递减区间内离0最远的数一定可以在两端找到，因此最大平方来自两端。相等时任选一份处理；只要每轮保留另一份的待处理状态，它随后仍会被处理。
2. 27方法只返回整数k；函数外原nums已被修改，用nums[:k]观察有效结果。不要靠再次返回列表才能看到变化。
3. p是保存地址的指针变量；*p访问p所指对象；&value取得value的地址。指针参数复制地址，不复制被指对象，所以通过它访问的仍是原数据。
4. data提供样本，model预测并保存参数，loss衡量误差，batch_gradients算平均梯度，optimizer修改参数，evaluator评估，Trainer组织顺序。
5. 你的“参数第一次已修改，第二次接着用”正确；持续状态也可由普通函数操作。是否使用类取决于状态和职责组织。
6. DAY31手算：x=[0,1]、y=[1,3]、w=1、b=0，平均损失1.25，平均梯度(-1,-1.5)，α=0.1后参数(1.1,0.15)，平均损失0.94625。原提交没有这组独立手算记录，不直接认定不会。

### 教材定位

- [C++ Primer Plus中文版](../../学习资料/C++/C++%20Primer%20Plus：中文版（第六版）%20(Stephen%20Prata).pdf)：8.2.1—8.2.3，重点阅读书内256—261页的引用绑定、引用参数、const限制。
- [神经网络与深度学习](../../学习资料/AI%20agent/神经网络与深度学习%20(邱锡鹏).pdf)：2.2.3.1、2.2.3.2。教材的迭代与停止思想用于本课；Trainer.fit是课程代码设计，不照抄教材框架。


