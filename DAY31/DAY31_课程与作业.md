# DAY31｜有序数组的平方、指针与数组传参、训练器的一步训练

> 2026-10-21发布。依据[学习与授课总约定](../学习与授课总约定.md)与[DAY29—DAY39阶段计划](../DAY29-DAY39_阶段计划.md)，约4小时，Mac本地运行。
>
> 五份练习只留题目说明，三步分析由你自己写。Python新题977、复习27；C++进入地址与指针；模型先接好原实例更新，再组合Trainer。文末给出DAY30全部示范与逐题对照，按疑问选读，不要求再抄一遍。

## 一、DAY30评阅：你已经推进到了哪里

我阅读了五份代码、其中的理论注释，以及《课后总结.md》，并运行原脚本与额外测试。教师补测说明计算行为，不代替你的闭卷用时和独立实现证据；本次不凭猜测给综合分。

| 项目 | 核对结果 | 结论 |
|---|---|---|
| 27 | 穷举长度0—7、值为0—2的列表，val为0—3，共13,120组；返回的k与原列表有效前缀全部正确 | 交换法正确，O(n)、O(1)，已理解原地处理；提交平台时只返回k |
| 26 | 枚举长度1—10、值为-2—2的非递减列表，共3,002组，k与前缀全通过 | 你比较相邻读取值的写法正确，不必强换成示范的“最后保留值”比较 |
| C++02 | C++17编译无警告，100组完整输入的所有数据结果通过 | 固定数组、求和、筛选计数与逐项副本正确；前三项同一行与题目分三行的差别只需短修 |
| C++03 | 输出5 4、2、BOSS LOSS_OK、1 0，数值正确；有一条有符号/无符号比较警告 | 固定文本实验成立；终止标记与存储长度需要区分；参考补直接包含string头文件与早期终止测试 |
| 平均梯度 | 180组数据与参数组合，对照数值求导，验证重复调用不改状态、数据重复后均值不变，均通过 | 平均梯度计算正确，可以复用，不再重抄 |
| 更新调用 | 原脚本输出4.5、0.35、0.2、3.021875；但旧neuron仍为(0,0)，新参数用于新建neuron_new | 新参数数学正确；本次step只返回结果、没有修改原模型，需要接回原实例 |
| 理论心得 | 原地修改与全批量梯度的主旨正确；“终端输入发生在程序启动前”需纠正 | 先看下方解释，再继续今天内容 |

### 1. 先确认：26的非标准写法是对的

你写的是比较nums[query-1]和nums[query]，示范比较当前值与最后一个已保留值。两种写法在本题条件下都可以。

关键是：在处理query之前，之前的覆盖写入没有改变“上一个刚读取的原值”。如果上一步写入位置小于query-1，它改的是更靠前的位置；如果等于query-1，它只是把那个位置的值写回自己。因此相邻读取值仍能判断是否进入一个新的同值区间。输入已经排序，每个区间只保留一次即可。

这份代码不需要为了和示范一样而重写。今天只口述为什么成立，后续按间隔复习。

27中交换也正确，额外维护了被移除值的尾部位置；尾部不参与官方判定，直接覆盖也能解题。你的返回`auxiliary, nums`是为了观察两个结果而返回了元组；平台接口只接收整数，把返回改成auxiliary，再在调用处查看原nums即可。这是一次局部接口修正，不用重学整题。

### 2. 你问的两个char数组，都算C风格字符串吗？

`char arr[5] = {'h','i','!','\0'};`的实际存储是：

```text
下标      0    1    2     3      4
内容     'h'  'i'  '!'  '\0'   '\0'
```

最后一格也为0，因为数组用初始化列表给了一部分元素，剩余元素会被零初始化。它保存的C风格字符串是"hi!"，可见长度3，存储5个char。

`char arr[] = "hi";`保存'h'、'i'、'\0'，文本"hi"，可见长度2，存储3个char。

**两者都是合法的、以空字符结束的字符串，但文本内容和数组大小都不同。** 如果第一份改为'h'、'i'、'\0'并仍定义长度5，文本可以相同，存储大小仍不同。

字符数组也可以只是若干字符，未必有终止标记。你的固定"LOSS"循环遍历到sizeof(code)-1，对这个字面量初始化的数组算对了；若文字提前遇到'\0'而后面还有'S'，就应停止。文末参考用"LO\0SS"让这个差别看得见。

### 3. 输入发生在什么时候？和调用有什么关系？

你的心得说“终端输入是程序启动前……传给main”，这部分时间顺序需要改成：

程序启动 → 进入main → 执行cin读取 → 把读到的值存进变量 → 运行到调用语句时，把实参交给函数。

终端键盘输入由cin等操作在运行期间读取。用户即使提前粘贴了内容，也不改变“程序执行读取语句才取得这些值”的关系。函数调用也在运行期间发生。命令行参数是另一种输入方式，今天先不展开。

重载选择是编译器检查调用表达式时完成的，例如代码里写了两个实参就匹配相应版本。cin读到的数字改变实参的值，不会自行增删调用表达式里的实参数量。

### 4. 模型差别为什么值得现在补上？

DAY29你的step会修改model属性；DAY30改成只算局部w、b再return。这两种设计都能做出数学正确的程序，但调用方式不同：

- 修改对象的step：调用后原模型参数改变。
- 只返回参数的step：调用者必须把结果写回原模型，原模型才改变。
- 新建neuron_new：得到另一模型，旧neuron不会自动更新。

你这次确实创建了新模型，新损失也算对了。今天Trainer要持续持有同一个模型并在下一次使用它，所以需要统一成第一种接口。先修step并用一次调用验证，然后继续组装，不安排一天只复习对象。

今天的时间：Python65分钟、C++100分钟、模型65分钟、保存与反馈10分钟。

## 二、Python：新题977，复习27（65分钟）

### 1. 27闭卷复习与接口修正，15分钟

文件：`01_Python复习_LeetCode27_移除元素.py`。

沿用昨天的交换思路也可以。实现`Solution.removeElement(self, nums, val)`，原地保留非val值，只返回整数k。不要为尾部排序或全部填val额外花时间。

测试：[3,2,2,3]排除3→k2，前缀两个2；[]排除0→0；[1,1,3]排除2→3；[2,2]排除2→0。在调用处查看nums[:k]，不要求函数返回nums。

26今天一分钟口述“为何比较相邻读取值也正确”，不用再开第六份代码作业。

### 2. 新题：有序数组的平方

[LeetCode977官方题目](https://leetcode.cn/problems/squares-of-a-sorted-array/)，简单：输入非空、非递减整数列表，返回各元素平方组成的、仍非递减的新列表。接口为`Solution.sortedSquares(self, nums)`。本题允许创建结果列表；课程约定不修改输入，方便检查。

例如[-4,-1,0,3,10]平方后是[16,1,0,9,100]，直接平方并不保持顺序。原因在负数：-4比-1小，但平方16比1大。平方大小取决于离0有多远，而不是原值的大小。

**绝对值（absolute value）**表示数到0的距离。已有函数abs(-4)得到4，abs(3)得到3；也可以直接比较两个数的平方，不强制使用abs。

### 3. 有序信息能帮我们排除什么

先看一个更小的例子[-5,-2,1,3]：

| 当前还没处理的值 | 最大平方来自哪里 | 为什么 |
|---|---|---|
| [-5,-2,1,3] | 左端-5 | 离0最远 |
| [-2,1,3] | 右端3 | 离0最远 |
| [-2,1] | 左端-2 | 离0最远 |

在非递减区间中，中间元素不可能比两端都离0更远。于是可以从剩余区间的两端挑出当前最大平方。这个结论正好把“处理全部元素找最大”缩成“只比较两端”。

**双指针（two pointers）**在这里是用两个列表下标表示剩余区间的左右端，不涉及C++地址。每处理一个端点，剩余区间就缩小。你已会344的两端下标，今天复用这种状态，但处理目标从交换字符变成安排平方后的顺序。

新问题留给你：如果每次得到的是最大值，结果应该从哪边填？什么情况下区间为空？相等时选择任一端是否会漏数据？

要预留固定长度结果列表，可以用已学语法`[0] * n`，例如[0]*3得到[0,0,0]；随后按下标写值。今天不提供完整循环、指针初值和预填三步，你自己组织。

### 4. 独立实现与测试，约40分钟＋检查10分钟

文件：`00_Python新题_LeetCode977_有序数组的平方.py`。

目标O(n)时间，结果列表O(n)空间。线性方法卡住时，先写出“平方后排序”的可运行版本作为自己的对照，再思考如何利用两端；排序版通常为O(n log n)，不算完成线性目标。无需抄两份完整模板。

| 输入 | 预期返回 |
|---|---|
| [-4,-1,0,3,10] | [0,1,9,16,100] |
| [-7,-3,2,3,11] | [4,9,9,49,121] |
| [-3,-2,-1] | [1,4,9] |
| [0,2,3] | [0,4,9] |
| [-2,2] | [4,4] |
| [0] | [0] |

检查输入是否保持不变；解释为什么每一步只排除一个端点、最后仍能处理奇数长度的中间项。先从数据推理，不背两端比较的固定代码。

## 三、C++：从值到地址，再把原数组交给函数（100分钟）

教材选读《C++ Primer Plus》4.7（书内97—100页）与7.3、7.3.1—7.3.2（212—213页）。PDF页码分别加18。本课用指向现有变量的指针，不申请动态内存。

### 1. 为什么有了变量名，还需要地址

昨天main能直接读取数组元素，但要让一个函数修改main里的原数据，就需要告诉它“这份数据在哪里”。

**地址（address）**用来标识对象所在的位置。人话：变量保存内容，地址帮助找到存放这份内容的格子。真实地址由运行环境安排，不用背它打印出来的数字。

```cpp
#include <iostream>
int main() {
    int score = 12;
    int* location = &score;
    std::cout << score << " " << *location << "\n";
    *location = 18;
    std::cout << score << "\n";
    std::cout << (location == &score) << "\n";
    return 0;
}
```

输出12 12、18、1。逐个拆开：

- `int score = 12;`创建保存整数的变量。
- `&score`：**取地址（address-of）**，取得score的位置；这里&是一元取地址运算符。
- `int* location`：声明一个**指针（pointer）**变量，它保存int对象的地址。声明中的*参与描述类型。
- 表达式`*location`：**解引用（dereference）**，访问这个地址指向的对象。这里*是操作，不是乘法。
- `*location = 18;`改的是score的内容，location仍指向score。

不要把location和*location混为一谈：前者是地址值，后者是沿该地址找到的整数。指针变量也有自己的存储位置，但今天不引入指针的指针。

### 2. 改指向，与改内容怎样区分

```cpp
#include <iostream>
int main() {
    int first = 6;
    int second = 20;
    int* p = &first;
    int* q = p;
    *q = 9;
    p = &second;
    *p = 25;
    std::cout << first << " " << second << " " << *q << "\n";
    return 0;
}
```

输出9 25 9。q复制了p当时保存的地址，所以开始时两者都能找到first。后来p改指向second，q仍指向first。复制地址没有复制整数，也没有把两个指针变量永久绑在一起。

每个指针单独写声明，先避免`int* p, q;`这种容易误读的形式：那里面只有p是指针，q仍是int。

**空指针（null pointer）**用nullptr表示当前不指向对象，例如`int* p = nullptr;`。可以比较p是否等于nullptr，不能解引用它；`if (p != nullptr)`检查非空后才可以继续访问指向对象。非空也不自动证明地址永远有效，今天只使用仍在作用域内的现有变量和数组。

### 3. 指针传参仍有值传递，为什么原数却能改变

函数接收`int* p`时，复制的是地址。函数自己的p与调用者指针是两个变量，但保存相同地址，都能找到原整数。

一个不同于作业的最小例子：

```cpp
#include <iostream>
void clear_value(int* target);

int main() {
    int value = 17;
    clear_value(&value);
    std::cout << value << "\n";
    return 0;
}

void clear_value(int* target) {
    if (target != nullptr) {
        *target = 0;
    }
}
```

输出0。调用方传&value，函数通过*target修改原整数。若函数只是写`target = nullptr;`，改变的只是函数自己的指针副本，不会把调用者的指针也设成空。若函数参数是普通int，则修改那个副本也不会修改value。

至此，你已有三种实际行为可以对照：复制整数；复制vector；复制地址后访问原对象。明天再学习引用，今天不把&的其他用法同时塞进来。

### 4. 数组名如何参与调用

在很多表达式中，原生数组会转换为指向首元素的指针（array-to-pointer conversion）。人话：函数要处理这一排格子时，先交给它第一格在哪里。

例如main里有`int values[3] = {4,8,12};`，那么`int* p = values;`得到首元素地址，也可以写成`&values[0]`。

- p[0]读取第一项4；p[1]读取第二项8。
- 在有效范围内，p[i]与*(p+i)表示相同元素。
- p+1表示走到下一个int元素的位置，移动的是一个元素所占空间，不是固定加一个字节。
- 只在同一数组的合法范围内移动；数组末尾后一位置可以作为边界，但不能解引用。作业使用i<length，不另练边界指针。

数组本身不等于指针对象。昨天在完整数组处sizeof(values)得到整个数组字节数；转换后得到的指针只保存地址，不能靠sizeof(p)还原数组长度。

### 5. 为什么数组和长度必须一起传

下面两种普通函数形参在这里等价：

```text
int sum_values(int values[], int length);
int sum_values(int* values, int length);
```

它们是同一参数类型的两种声明写法，不能靠这两种写法重载。形参处即使写values[6]，也不替你自动传入或检查6个元素。今天统一使用int*写法，避免把形参误看成完整数组。

函数可以使用values[i]访问原数组，但它不知道原数组到底有多长，需要调用者同时传length并保证长度合法。函数里写sizeof(values)/sizeof(values[0])算的是指针大小与int大小的比值，不是原数组元素个数。

这也解释昨天的差异：普通vector值参数会复制容器；普通数组传参按上述规则接收地址，函数对values[i]赋值就会改变原数组。不要根据参数都用了相同名字，就认为行为相同。

### 6. 两项练习，45分钟手敲＋10分钟检查

**02：用地址修改一个整数（约20分钟）**

文件：`02_C++核心_指针读写与空指针.cpp`。

- 声明并定义`void add_to(int* target, int delta)`。target非空时让指向整数增加delta；为空时不做事。
- main读取两个整数作为原值、增量，先建立指向原值的指针，再复制出另一个指针。
- 用其中一个指针调用函数；第一行输出原值更新结果、通过另一个指针读到的结果，两者应相同。
- 将第一个指针改指向main中新建的另一个整数100，通过它写成200；第二行输出原值、另一个整数、第二个指针读到的值。
- 再以nullptr调用add_to，程序正常结束；不读取空指针。

输入10 5：第一行为15 15，第二行为15 200 15。输入-2 0：第一行为-2 -2，第二行为-2 200 -2。变量仍在main作用域，今天不讨论返回局部变量地址。

**03：数组首地址＋长度，原地平移耗时（约25分钟）**

文件：`03_C++应用_数组传参与长度.cpp`。

main建立容量6、全部初始化为0的int数组。输入n（0—6）、n个非负耗时、delta（0—10）。两个普通函数由你实现：

| 接口 | 作用 |
|---|---|
| int sum_values(int* values, int length) | 返回前length项总和，不修改数组 |
| void shift_values(int* values, int length, int delta) | 让前length项各增加delta，修改原数组 |

先求旧总和，再调用shift_values，最后求新总和。前两行输出旧总和与新总和；第三行按顺序输出更新后的前n项，n=0时第三行为空行。声明在main前、定义在后，长度由main显式传入。

输入3 4 10 20 2：前两行34、40，第三行6 12 22。输入0 5：0、0、空行；输入6 1 2 3 4 5 6 0：两次均21，数组不变。额外检查n=3时未纳入处理的后三项仍为0，可以临时打印或用已知断言，不增加正式输出行。

本题不接受越界输入，接口允许length=0；长度0不访问任何项。无须从函数内猜长度，不新建第二份数组假装修改原数据。

编译方式：

```bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY31/02_C++核心_指针读写与空指针.cpp" -o /tmp/day31-pointer
/tmp/day31-pointer
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY31/03_C++应用_数组传参与长度.cpp" -o /tmp/day31-array
/tmp/day31-array
```

## 四、模型：把一次训练组织成可重复调用的对象（65分钟）

教材承接《神经网络与深度学习》2.2.3.1梯度下降与2.3.1线性回归参数学习。Trainer是本课程组织代码的选择，教材不要求使用这个类名。

### 1. 先看完整因果链，为什么现在才需要Trainer

DAY30你已经能正确从一批数据计算平均梯度，说明数学计算不必推倒重来。接下来要反复使用同一套流程：评估旧模型、求当前梯度、更新模型、评估新模型。

如果每次在调用区重新拼这些操作，容易发生你这次的情况：新参数虽然算对，但后续另建模型，下一次又对旧neuron计算。真正需要的是让“持有哪份数据、更新哪一个模型、用哪个学习率”保持一致。

**训练器（trainer）**负责组织已有部件完成一次训练。人话：它安排谁先工作、结果交给谁；预测、损失、求梯度和修改参数仍由已经会的部件完成。

这也是面向对象的**组合（composition）**：对象持有其他对象，再调用它们的方法。Trainer里保存模型，不会自动复制或再造模型；以后模型参数改变，训练器和外部看到的是同一个对象。

### 2. 先把更新器的约定接好，5—10分钟

把你现有step中的局部计算改为写回传入model的weight和bias，然后直接调用step，不创建neuron_new。本节不提供两行赋值答案，你可按昨天自己已写过的版本恢复；文末参考给出DAY30完整正确接口。

在写Trainer前先验证：模型w=b=0，平均梯度(-3.5,-2)，α=0.1；调用后原模型变为(0.35,0.2)，原评估器读它得到3.021875。保持另一个名字指向原模型，更新后用is确认对象没有换。

这一步修正的是更新责任。只return参数的设计也能实现训练，但本课程为了让后续调用一致，约定step修改模型、不返回新模型。

### 3. 一次训练时，哪些状态应该长期保存

沿用这些部件：

| 部件 | 长期保存什么 | 本次做什么 |
|---|---|---|
| LinearNeuron | weight、bias | forward预测 |
| RegressionDataset | xs、ys | size和get_item取样 |
| SquaredLoss | 本课不必保存新状态 | 计算半平方损失 |
| LossEvaluator | 数据、损失对象 | evaluate评估，不改模型 |
| GradientDescent | learning_rate | step修改模型 |
| batch_gradients | 普通函数，无需实例 | 使用当前模型算平均梯度，不改参数 |
| Trainer | 模型、数据、损失、更新器、评估器 | 安排一次完整训练 |

在Trainer的构造方法中保存传入对象，另用同一data和loss建立一个LossEvaluator。它持有的是对象，不是某次预测结果。梯度、更新前后损失是某次train_step的临时变量，不必都保存为self属性。

`self.model.forward(x)`要分两层看：self是训练器，self.model取得它保存的神经元，forward(x)由那个神经元计算。不是“类嵌进类才会预测”，只是沿着已有对象找到另一个对象。

不把所有部件都叫self：执行model.forward时，那个方法里的self是神经元；执行optimizer.step时，那里的self是优化器。方法的接收对象不同，self所指就不同。

### 4. 返回什么，以及为什么第二次要重新求梯度

本课接口固定为`Trainer(model, data, loss, optimizer)`，方法`train_step(self)`无额外显式参数，返回两个数字：更新前平均损失、更新后平均损失。

一次调用只更新一次。你自己组织操作顺序；要求梯度在旧参数处算完，更新后再评估。返回损失是为了让调用者观察变化；实际参数已经改在原模型上，不靠返回损失去修改参数。

对固定数据，α=0.1：

| 调用 | 更新前(w,b) | 当前平均梯度 | 更新后(w,b) | 损失前→后 |
|---|---|---|---|---|
| 第一次 | (0,0) | (-3.5,-2) | (0.35,0.2) | 4.5→3.021875 |
| 第二次 | (0.35,0.2) | (-2.875,-1.625) | (0.6375,0.3625) | 3.021875→2.0298046875 |

第二次的梯度不同，因为当前预测变了，每个误差也变了。若反复拿第一次梯度更新，只是在沿一个旧方向反复走，不是这里的梯度下降迭代。

本数据和步长下两次下降可验证。不要把它扩展为“任何模型、任何学习率，每一步都必然下降”；DAY33会做学习率对照。

### 5. 独立实践：只新增训练器，不重新发明旧类

文件：`04_模型实践_Trainer单步训练.py`。

允许复用自己已正确的四类、batch_gradients，以及修正后的GradientDescent。新增Trainer与实际调用区由你写，不提供类骨架或完整train_step循环。

要求：

- 构造方法按本节接口接收对象，保存到实例，并建立对应评估器。
- train_step返回两项损失，并恰好更新同一模型一次；不新建模型、不改数据、不打印内部流水账。
- 使用x=[-1,0,1,2]、y=[-1,1,3,5]、w=b=0、α=0.1，显式调用两次train_step，核对上表。今天不写100次循环或fit。
- 保留外部模型名字，验证两次调用后仍是原对象；第一次返回的新损失应等于第二次返回的旧损失。
- 再创建一个独立模型和学习率0的训练器，调用一次：损失4.5→4.5，参数仍为0、0。不要意外让它与前一个训练器共用被修改后的模型。
- 原数据集和损失对象可以复用，因为它们不被训练过程修改。模型是否需要独立，要看实验是否希望共享参数。

手算10分钟：用x=[0,1]、y=[1,3]、旧w=1、b=0、α=0.1，计算旧平均损失、两梯度、新参数和新平均损失，再用自己的Trainer验证。不要用课程表格照抄代替推导。

今天最终新增能力是：从外面调用一次train_step，就能在原模型上完成一次完整训练。DAY32将在这个基础上增加fit与100步实验，仍从已验证的部件接起。

## 五、今天怎样交付与保存

五份代码和必要运行结果即可。三步分析仍由你自己写；心得可放代码注释或自建总结，不强制加表。

重点口述三项：

1. 977为什么能只看剩余区间两端？27在函数外怎样取得修改后的前缀？
2. p、*p、&value分别是什么？函数复制了指针，为什么仍能修改原数组？
3. train_step里每个对象负责什么？第二次调用为什么会接着第一次的模型，而不是回到初始值？

本次优先级：27做局部返回修正、模型先接好原实例，再学新内容；不因格式、变量名或少一条记录停整天。独立用时和看过哪些提示如实注明一句即可，方便我判断下一课大小。

## 六、DAY30全部示范答案与逐题比较

以下是昨天内容。26和27允许与你代码不同，只要解释与验证成立。先完成今天的闭卷27，再按需展开；其余参考可直接对照，不要求全部重抄。


<details>
<summary>00｜27：保留你的交换方法，只修返回值与测试接口</summary>

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
for original, val, expected in [
    ([4, 1, 4, 2, 1], 4, [1, 2, 1]),
    ([4, 4, 4, 2, 1], 4, [2, 1]),
    ([1, 2, 3], 4, [1, 2, 3]),
    ([2, 2], 2, []),
    ([], 7, []),
]:
    values = original.copy()
    k = solver.removeElement(values, val)
    assert isinstance(k, int)
    assert k == len(expected)
    assert values[:k] == expected
```

你的交换逻辑已正确。示范删去pass分支，只保留需要动作的条件，属于简化；重要修改只有return只交k。测试检查有效前缀，不规定尾部。isinstance用于教师测试返回类型，本课不要求背它。

auxiliary表示已保留的项数，也指向下一写入位置。它落后时指向已处理范围内的待替换位置；尚无val时与读取位置相同。比“永远保存最小目标值下标”更通用的解释是“有效前缀之后的下一格”。不要求因描述不够通用重写正确算法。

</details>

<details>
<summary>01｜26：参考沿用你比较相邻读取值的方法</summary>

```python
class Solution:
    def removeDuplicates(self, nums):
        auxiliary = 1
        for query in range(1, len(nums)):
            if nums[query - 1] != nums[query]:
                nums[auxiliary] = nums[query]
                auxiliary += 1
        return auxiliary

solver = Solution()
for original, expected in [
    ([0, 0, 1, 1, 1, 2], [0, 1, 2]),
    ([1, 2, 3], [1, 2, 3]),
    ([3, 3, 3], [3]),
    ([-2, -2, 0, 4, 4], [-2, 0, 4]),
    ([7], [7]),
]:
    values = original.copy()
    k = solver.removeDuplicates(values)
    assert k == len(expected)
    assert values[:k] == expected
```

算法与你相同。时间O(n)，额外空间O(1)，题目非空输入条件下成立。你测试整个nums的具体尾部会把实现细节固定死，参考只比较nums[:k]；尾部换一种合法排列也不该判错。这是测试范围的简化，不改变算法。

你的心得“使用已有信息节省时间”方向正确，具体到26，已有信息就是“输入有序、相同值连续出现”。能指明是哪条信息发挥作用，比泛泛说节省复杂度更能帮助下一题迁移。

</details>

<details>
<summary>02｜固定数组：数据逻辑与你相同，参考按约定逐行输出</summary>

```cpp
#include <iostream>
int main() {
    int values[5] = {};
    int length = sizeof(values) / sizeof(values[0]);
    for (int i = 0; i < length; ++i) {
        std::cin >> values[i];
    }
    int total = 0;
    int count = 0;
    for (int i = 0; i < length; ++i) {
        total += values[i];
        if (values[i] > 10) {
            ++count;
        }
    }
    int copied[5] = {};
    for (int i = 0; i < length; ++i) {
        copied[i] = values[i];
    }
    copied[0] = 99;
    std::cout << length << "\n" << total << "\n" << count << "\n";
    for (int i = 0; i < length; ++i) {
        std::cout << values[i] << " ";
    }
    std::cout << "\n";
    for (int i = 0; i < length; ++i) {
        std::cout << copied[i] << " ";
    }
    std::cout << "\n";
    return 0;
}
```

与你相比，只是把输入直接写进数组、保存一次长度、按规定换行。你的临时value和while/for选择都合法。直接包含vector头文件但没用到，不是本题掌握与否的重点。关于下标0—4、下标5越界的解释正确。

这里已知数组长度5，用int保存长度足够；通用大型容器的索引类型后续再系统处理。

</details>

<details>
<summary>03｜字符数组：明确终止位置，并补上你提问的存储对照</summary>

```cpp
#include <iostream>
#include <string>
int main() {
    char code[] = "LOSS";
    std::string text = "LOSS";
    int capacity = sizeof(code);
    std::cout << capacity << " " << text.size() << "\n";

    int count = 0;
    for (int i = 0; i < capacity && code[i] != '\0'; ++i) {
        if (code[i] == 'S') {
            ++count;
        }
    }
    std::cout << count << "\n";
    code[0] = 'B';
    text += "_OK";
    std::cout << code << " " << text << "\n";

    char empty[] = "";
    std::string empty_text = "";
    std::cout << sizeof(empty) << " " << empty_text.size() << "\n";

    char first[5] = {'h', 'i', '!', '\0'};
    char second[] = "hi";
    std::cout << first << " " << sizeof(first) << "\n";
    std::cout << second << " " << sizeof(second) << "\n";

    char early_stop[] = "LO\0SS";
    int early_capacity = sizeof(early_stop);
    int early_count = 0;
    for (int i = 0; i < early_capacity && early_stop[i] != '\0'; ++i) {
        if (early_stop[i] == 'S') {
            ++early_count;
        }
    }
    std::cout << early_stop << " " << early_count << "\n";
    return 0;
}
```

前四行与你相同；新增hi! 5、hi 3、LO 0说明存储大小与文本结束位置。这些是昨天知识的对照，不是新作业。

你的循环对固定LOSS正确，只是没有利用终止标记。对early_stop，如果仍遍历整个数组到最后一格，会把文本结束后的两个S计入；按C字符串规则应得到0。原源码在int下标与sizeof的无符号结果比较时产生一条警告，参考用本例安全的小int容量，去掉类型不一致；不是要求为此重学整个数组。

另外直接使用std::string应包含<string>。本机<iostream>间接带入了所需声明而编译通过，不应依赖这一偶然包含关系。

</details>

<details>
<summary>04｜平均梯度与原实例更新：参考保留你的正确计算，接回参数修改</summary>

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
        return ((prediction - target)**2)/2
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
        for index in range(self.dataset.size()):
            xs,ys = self.dataset.get_item(index)
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
    g_w,g_b = 0,0
    for i in range(data.size()):
        xs,ys = data.get_item(i)
        g_w += (model.forward(xs) - ys) * xs
        g_b += model.forward(xs) - ys
    
    return g_w/data.size(),g_b/data.size()

model = LinearNeuron(0, 0)
alias = model
data = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
loss = SquaredLoss()
evaluator = LossEvaluator(data, loss)
optimizer = GradientDescent(0.1)

before = evaluator.evaluate(model)
grads_first = batch_gradients(model, data)
grads_again = batch_gradients(model, data)
assert grads_first == grads_again == (-3.5, -2.0)
assert model.weight == 0 and model.bias == 0
assert abs(before - 4.5) < 1e-9

doubled = RegressionDataset(data.xs * 2, data.ys * 2)
assert batch_gradients(model, doubled) == grads_first

optimizer.step(model, grads_first[0], grads_first[1])
assert model is alias
assert abs(model.weight - 0.35) < 1e-9
assert abs(model.bias - 0.2) < 1e-9
assert abs(evaluator.evaluate(model) - 3.021875) < 1e-9
assert data.xs == [-1, 0, 1, 2] and data.ys == [-1, 1, 3, 5]

single_model = LinearNeuron(0, 1)
single_data = RegressionDataset([2], [5])
assert batch_gradients(single_model, single_data) == (-8.0, -4.0)

manual_model = LinearNeuron(1, 0)
manual_data = RegressionDataset([0, 1], [1, 3])
manual_evaluator = LossEvaluator(manual_data, loss)
assert abs(manual_evaluator.evaluate(manual_model) - 1.25) < 1e-9
manual_grads = batch_gradients(manual_model, manual_data)
assert manual_grads == (-1.0, -1.5)
optimizer.step(manual_model, manual_grads[0], manual_grads[1])
assert abs(manual_model.weight - 1.1) < 1e-9
assert abs(manual_model.bias - 0.15) < 1e-9
assert abs(manual_evaluator.evaluate(manual_model) - 0.94625) < 1e-9
print("DAY30平均梯度与同实例更新验证通过")
```

四类与batch_gradients保留你的计算。两次forward虽可合成一次，但目前结果正确，不以此扣核心理解分。关键修改在step：把值写回传入model；调用区不创建neuron_new。

你能正确说明“所有样本用同一旧参数，先算平均梯度再更新”，这与已通过数值核验的batch_gradients对应。当前缺口是最后的状态更新接口，并非平均梯度数学不会。指定手算及重复数据验证在原提交未保留，参考补齐这些场景；不直接认定你没理解。

这里mse变量名实际保存半MSE，计算仍符合本课程损失约定。后续做指标时再明确命名，不为了它暂停训练进度。

</details>

### DAY30理论示范回答

1. 原地覆盖修改传入列表的元素；新建答案列表若未写回原输入，就没有完成原地任务。26的有序性使相同值相邻，不必每次扫描全部历史结果。
2. cin在程序运行到读取语句时取输入；编译器根据源代码中调用的实参列表选择重载。两者不能用“一个启动前、一个启动后”区分。
3. 字符数组有固定存储大小；作为C风格字符串解释时，文本在首个'\0'结束。终止标记之后还可能有其他存储格子。std::string有自己的长度管理，size()不把末尾终止标记计作字符；本课只处理ASCII小例子。
4. 同一旧参数处各样本梯度平均，才是该处平均损失的梯度；全部算完再更新一次，符合全批量定义。逐样本算完就更新是另一种训练方式。
5. DAY30手算：x=[0,1]、y=[1,3]、w=1、b=0，预测[0,1]，误差[-1,-2]，平均半平方损失1.25，平均梯度(-1,-1.5)；α=0.1后参数(1.1,0.15)，新预测[0.15,1.25]，新平均损失0.94625。

### 教材定位与阅读范围

- [C++ Primer Plus中文版](../../学习资料/C++/C++%20Primer%20Plus：中文版（第六版）%20(Stephen%20Prata).pdf)：4.7与7.3相关页，用于核对取地址、解引用和数组参数；动态内存部分留待DAY33。
- [神经网络与深度学习](../../学习资料/AI%20agent/神经网络与深度学习%20(邱锡鹏).pdf)：2.2.3.1式2.27—2.28、2.3.1线性回归参数学习。本课仍用平均半平方损失；教材2.3.1.1为简化推导省略1/N，不能因此在我们的平均梯度代码中也忘除样本数。

