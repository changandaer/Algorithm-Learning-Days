# DAY30｜补牢原地修改，理解固定数组，完成一次全批量更新

> 约4小时，Mac本地Python与C++17。依据[总约定](../学习与授课总约定.md)和[阶段计划](../DAY29-DAY39_阶段计划.md)。
>
> 按你的最新要求：今天保留27、26，不增加977。977明确待补，不算已经学习，也不挤成第三道必做题。今天仍为一份课程、五份留白代码；自己的三步分析保留，不增加TODO和记录表。

## 一、DAY29评语：哪些已会，哪些需要练

已阅读五个代码文件和其中的心得、理论注释；DAY29目录没有另一个独立心得文件。原代码保持不动。以下测试是教师补测，不冒充你的闭卷成绩。

| 项目 | 实际证据 | 评价与下一步 |
|---|---|---|
| 27 | 仅有题目注释 | 未完成，不按错误实现扣分；今天继续 |
| 26 | 返回(3,[0,2,5],[0,0,2,2,5])，原列表未改变 | 找不同值的思路有效，但未满足原地修改与返回整数的接口；这是本次Python核心短板 |
| C++02 | C++17编译无警告，150组完整输入输出通过 | 声明、定义、参数、返回数据和main输出已接好；此前“数量混进结果”已修复 |
| C++03 | 编译无警告，按你的输入协议150组完整程序测试通过 | 两个统计函数均正确；尚未实际调用省略默认参数的版本。main要求额外读入阈值和上下界，与原题四次固定调用不同 |
| 模型 | 原脚本得到8→2的损失变化；另108组参数、输入、学习率组合的更新及评估通过 | 已在原模型上完成真实一步更新，梯度先算完再修改也正确；不用再重学四个类 |
| 理论及独立性 | C++02两问有回答，03提出具体疑问；模型指定第二组手算、零学习率测试未保留 | 有实现和理解证据，完整口述、用时、提示情况仍待验收；不凭部分成果虚构总分 |

模型补测包括学习率0和x=0，确认你的实现能处理，不等于你已亲自完成这些验证。你的step返回新参数，再用返回值给同一对象赋值，数值正确、对象没换；只是重复赋值。今天可以简化成只调用step，不用为了接口风格否定已有成果。

### 1. “过几天又不会做，正常吗？是不是只能多刷？”

会发生，尤其是刚从“看懂答案”过渡到“独立选择状态”的时候。但不能只用“正常”安慰你，然后让你机械重抄。

你这次不是连循环、判断都不会：你能独立建立结果列表、判断是否出现过、统计数量。卡点很具体：**不允许另建答案列表时，结果应该放在哪里？**

你现在的列表查找每次最多扫过已有结果，最坏O(n²)；结果列表占O(n)额外空间。这能作为“先做出正确内容”的第一版，下一步才是利用输入有序与原数组空间，改为O(n)、O(1)。

融会贯通不靠背“两个指针”四个字，而是能解释两个位置各自负责什么：

- 一个位置负责看下一份原数据；
- 一个位置负责指出下一份有效结果应放哪里。

它们是列表下标，不是今天要学C++内存指针。列表已经分配了足够位置，可以把结果覆盖写到前面；尾部不用整理干净。

仍沿用自己的三步，不再创造新方法：换一组小输入，说清结果应放到哪里，再关掉示范写。下一次复习换数据，检查是否能自己恢复这两个位置的含义，而不是记得变量名。

### 2. C++能否根据我输入几个参数，自动选择函数？

**重载选择看的是源代码里的调用表达式，不是终端中你输入几个数字。**

你的main明确写了三次读取：先读容器，再读threshold，再读lower和upper。程序执行到每一条cin就会尝试读取对应数据；它不知道你打算跳过后面的读取。回车通常只是空白分隔符，不表示“本次函数参数结束”。

例如代码已经写成：

```cpp
count_over(values, threshold);
```

编译器看到两个实参，就确定应使用哪一类重载。运行时用户输入20还是0，只改变threshold的值，不改变这个调用的实参数量。

要由用户决定功能，需要先约定输入协议，例如“模式1＝默认阈值；模式2＝自定阈值；模式3＝区间”。再用已学的if/else选择执行哪一句调用。每个分支里的调用依然由编译器根据参数列表匹配。其他输入设计也可以，**不是永远只能写if，但必须有人实现输入解析和分派逻辑**。

小例子：与耗时题无关，只观察“输入决定走哪个分支”。

```cpp
#include <iostream>
int adjust(int value, int extra = 2);

int main() {
    int mode;
    std::cin >> mode;
    if (mode == 1) {
        std::cout << adjust(7) << "\n";
    } else if (mode == 2) {
        int extra;
        std::cin >> extra;
        std::cout << adjust(7, extra) << "\n";
    } else {
        std::cout << "invalid mode\n";
    }
    return 0;
}

int adjust(int value, int extra) {
    return value + extra;
}
```

输入1输出9；输入2 5输出12；输入2 0输出7。模式2不输入第二个数，程序就需要继续等输入。默认参数是省略**代码里的实参**时使用，不是你在终端不输入就会自动使用。

今天先口述上述区别，并在原03的临时副本或运行区自行补一次只传容器的调用即可；不要求再写一整套菜单程序。数组学习继续推进。

## 二、Python：保留27与26，先尝试，再展开文末答案（65分钟）

文件：
- `00_Python继续_LeetCode27_移除元素.py`
- `01_Python巩固_LeetCode26_原地去重.py`

今天允许先用20分钟补原地修改理解，再做两题约35分钟，最后10分钟测试。27仍是未完成的新题，不把它标成复习通过。

### 原地修改怎样改变数据

以下是一个单独的下标覆盖例子，不是两道题的完整算法：

```python
values = [8, 8, 5, 6]
values[1] = values[2]
print(values)  # [8, 5, 5, 6]
```

发生的是：读出第2号位置的5，写入第1号位置；列表长度没变，后面的5也没被删除。**赋值不是把元素搬走，而是把一个值写进另一个位置。**

在筛选任务中，前面的格子可以用于保存结果。仍未读取的元素必须保留，所以要思考写入位置是否会跑到读取位置前方、覆盖未来数据。用“小输入跟踪位置”检查，而不是凭运行一个样例碰运气。

26的输入有序，同值聚在一起；不需要每次到一个新列表里搜索是否出现过。你只需知道什么信息能代表“已经留下的最后一个不同值”。27则不关心去重，只排除val。

| 题目 | 必须留下什么 | 不能误做什么 |
|---|---|---|
| 26 | 每个不同值一次，保持有序 | 返回新列表但不修改原输入 |
| 27 | 每一个不等于val的值 | 把合法的重复记录也去掉 |

### 27要求

沿用[官方题目](https://leetcode.cn/problems/remove-element/)：实现`Solution.removeElement(self, nums, val)`，修改nums的前k项并返回整数k；前缀顺序不限，尾部不检查。目标O(n)时间、O(1)额外空间。

测试：[]排除7→k0；[4,1,4,2,1]排除4→k3，包含两个1和一个2；[2,2]排除2→k0；[1,1,3]排除2→k3；[5]排除0→k1。

### 26要求

沿用[官方题目](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/)：接口为`Solution.removeDuplicates(self, nums)`。非空、已排序输入，原地写入不重复的有序前缀，只返回k。目标O(n)、O(1)。

测试：[0,0,2,2,5]→k3，前缀[0,2,5]；[7]→1；[3,3,3]→1；[-2,-2,0,4,4]→3，前缀[-2,0,4]。

先试写，不预填三步。若仍卡住，可以展开文末对应示范，重点解释状态为什么成立，再关闭示范重写。参考后完成不叫失败，也不要记成未看答案的闭卷通过。今天完成后由我安排后续间隔复习，你不需要新建打卡表。

## 三、C++：为什么有vector，还要理解原生数组（100分钟）

教材选读本地《C++ Primer Plus》第4章4.1—4.2，书内70—75页（PDF88—93页）。今天只学固定大小与字符存储，数组传参、指针留到后续。

### 1. 固定格子和可增长容器

**原生数组（built-in array）**是一块连续放同类型元素的固定大小存储。人话：先摆好四个同样规格的格子，再往里面放数；它不像vector那样提供push_back自动扩充。

```cpp
#include <iostream>
int main() {
    int readings[4] = {6, 9, 12, 15};
    readings[1] = 10;
    std::cout << readings[0] << " " << readings[1] << "\n";
    std::cout << sizeof(readings) / sizeof(readings[0]) << "\n";
    return 0;
}
```

输出6 10，下一行4。定义里的[4]表示元素个数；之后使用readings[1]表示访问编号1的元素。合法下标为0、1、2、3，不包括4。

在本课这种局部数组中：
- `int a[4] = {};`把四项都初始化为0。
- `int a[4] = {6,9};`得到6、9、0、0，不是只建两个格子。
- `int a[] = {6,9};`由初始化内容确定大小2，以后仍不能自动增长。
- `int a[4];`没有初始化，不能读取未赋过值的项；不要靠偶然看到0来推断规则。

标准C++17中，普通局部原生数组的大小需要编译时可确定。先cin读n再写`int a[n];`是某些编译器扩展，不作为本课写法。需要运行时可变长度，通常用vector；今天练习固定大小数组。

### 2. 下标、长度和字节数不是一回事

**sizeof**给出对象占用的字节数。人话：整个柜子占多少空间，不直接等于柜子有几个格子。对于这里的完整数组：

```text
元素个数 = 整个数组字节数 / 一个元素字节数
```

不硬编码int一定占4字节，也不把sizeof(vector对象)当成容器元素数量。

这里能计算，是因为作用域内看到的是完整数组。以后数组作为普通函数参数时，这个公式不能直接照搬；DAY31会解释，不要求现在记指针细节。今天原生数组实验先留在main中，不强行拆成未教过的数组参数函数。

**越界（out of bounds）**就是访问格子之外的位置。C++原生数组下标通常不会替你检查，越界属于未定义行为，可能崩溃，也可能貌似正常；不要故意越界看输出证明语言规则。循环访问条件应保证下标小于元素个数。

另一个区别：原生数组不能像vector那样直接写整体赋值`b = a;`。想复制内容，今天可以用已学的循环逐项复制；复制后它们是两份数组。

| 操作 | 原生int数组 | vector<int> |
|---|---|---|
| 定义后元素数量 | 固定 | 可增长 |
| 读写某项 | 下标 | 下标 |
| 读取元素数量 | 本课在完整数组处计算或保存固定长度 | size() |
| 追加 | 没有push_back | push_back |
| 整体赋值复制 | 不支持直接数组赋值 | 支持 |
| 下标自动安全检查 | 不保证 | operator[]也不保证 |

数组不是比vector更高级的“毕业版本”。学习它为了理解长度与存储边界；日常可变数据仍优先使用合适的标准容器。

### 3. 字符数组怎样变成文本

char能保存一个字符；char数组能放一串字符。但**C风格字符串（C-style string）**有额外约定：以空字符`'\0'`标记文本结束。

人话：固定盒子里放文字，还要放一张“文字到这里结束”的标记。标记占一个位置，不是可见的字符0（`'0'`）。

```cpp
#include <iostream>
#include <string>
int main() {
    char code[] = "AI";
    std::string text = "AI";
    std::cout << sizeof(code) << " " << text.size() << "\n";
    code[0] = 'M';
    text += "!";
    std::cout << code << " " << text << "\n";
    return 0;
}
```

输出3 2、MI AI!。code有'A'、'I'、'\0'三个char；sizeof(char)按定义为1字节。text.size()是文本中char的数量，不包含末尾终止标记。今天只用ASCII字符，不把UTF-8中文的字节数误当汉字数。

`char code[2] = "AI";`在C++里空间不够，因为还要放终止标记。相反，`char code[2] = {'A','I'};`可以作为两个字符的数组，却不是以空字符结尾的字符串，**不能直接拿cout按C字符串输出**。可以用已知长度逐字符输出，不越界找不存在的结束标记。

char数组也不能定义后直接`code = "NEW";`。std::string负责管理文本长度与存储，支持赋值、+=和size()，通常更适合文本处理。理解字符数组是为了看懂底层约定，不是要求日后放弃string。

### 4. 两项独立练习（45分钟手敲＋10分钟检查）

**02：固定耗时数组**

文件：`02_C++核心_固定数组与长度.cpp`。

- main内创建长度5的int数组，读取恰好5个非负整数。
- 用循环求总和、严格大于10的数量；按顺序输出“元素个数、总和、超阈值数量”，各一行。
- 自己创建第二个同长度数组，逐项复制第一份，把第二份下标0改为99。
- 最后两行分别输出原数组与副本，元素用空格隔开。不要直接数组整体赋值，不引入指针。

输入4 10 12 20 20：前三行为5、66、3；后两行为4 10 12 20 20和99 10 12 20 20。
输入0 0 0 0 0：前三行为5、0、0。说明为什么不能访问下标5；程序不要实际访问它。

**03：字符存储与文本操作对照**

文件：`03_C++应用_字符数组与string.cpp`。

- 创建可容纳字符串"LOSS"及结束标记的char数组，并创建内容为"LOSS"的std::string。
- 输出数组存储字节数与string.size()，应为5和4。
- 用循环统计字符数组在终止标记前有几个'S'；循环需同时受数组边界和终止标记约束。应为2。
- 修改字符数组首字符为'B'；给string追加"_OK"；输出BOSS和LOSS_OK。
- 再分别用一个空字符串数组`char empty[] = "";`与空string验证：前者占1字节、可见长度0；后者size为0。空数组实验不要修改首字符或覆盖结束标记。
- 在注释里解释char、字符数组、C风格字符串、std::string之间的关系，不要只背四个名字。

这里用&&结合两个条件：先检查下标还在数组范围内，再检查对应字符不是'\0'。**短路求值（short-circuit evaluation）**意味着左边为假就不求右边，人话：先确认格子存在，再打开看内容。不要把顺序写反。

在仓库根目录编译：
```bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY30/02_C++核心_固定数组与长度.cpp" -o /tmp/day30-array
/tmp/day30-array
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY30/03_C++应用_字符数组与string.cpp" -o /tmp/day30-text
/tmp/day30-text
```

## 四、模型：从“照顾一个样本”到“共同决定一步”（65分钟）

教材承接《神经网络与深度学习》2.2.3.1的式2.28和2.2.3.3，书内30—31页、PDF45—46页。今天将你已正确的单样本更新接到平均损失，不新增Trainer类。

### 1. 为什么一个样本的好方向不一定适合所有样本

昨天一个x、y给出误差，再算两个梯度。若有很多样本，每个样本都能提出“该怎样改”的意见，而且可能相反：某个样本嫌预测太大，另一个嫌太小。

我们先明确目标：让**全体样本的平均损失**下降，而不是只把最后看到的样本拟合好。

对第i个样本：
```text
e_i = w*x_i + b - y_i
L_i = e_i²/2
平均损失 J = (L_1 + ... + L_N)/N
```

N为非零样本数。在同一组w、b下比较这些样本，J才代表“这个模型目前整体怎样”。

### 2. 为什么平均损失对应平均梯度

有限个可求导函数相加，其导数等于各自导数相加；再除以固定的N，导数也除以N。因此：

```text
∂J/∂w = (e_1*x_1 + ... + e_N*x_N)/N
∂J/∂b = (e_1 + ... + e_N)/N
```

人话：每个样本在同一个模型状态下投出修改意见，把意见平均后走一步。这里不是先把x、y平均再当成一个样本训练；一般情况下“乘积的平均”不等于“平均值的乘积”。

也不是先把每个样本都训练完，再平均参数。那样后面样本已经看到了变化后的模型，不再对应上述求导公式。

### 3. 完整数值例子：为后面的100步训练接好数据

使用固定训练集：x=[-1,0,1,2]，y=[-1,1,3,5]，旧w=b=0。

| x | y | 旧预测 | e | 单样本半平方损失 | w梯度e*x | b梯度e |
|---|---|---|---|---|---|---|
| -1 | -1 | 0 | 1 | 0.5 | -1 | 1 |
| 0 | 1 | 0 | -1 | 0.5 | 0 | -1 |
| 1 | 3 | 0 | -3 | 4.5 | -3 | -3 |
| 2 | 5 | 0 | -5 | 12.5 | -10 | -5 |

平均损失18/4=4.5；平均w梯度为-14/4=-3.5；平均b梯度为-8/4=-2。

学习率0.1，一次全批量更新后w=0.35、b=0.2。新预测为[-0.15,0.2,0.55,0.9]，新平均半平方损失为3.021875，小于4.5。

看清“平均b梯度”为-2，而平均x为0.5，二者相乘是-1，不是正确的w梯度-3.5。因为每个误差与自己的x配对，不能把配对关系扔掉。

梯度求平均还有实用意义：把同样的数据重复一遍，样本数翻倍但平均损失、平均梯度不变。若只求和不除N，同样学习率下相当于把更新幅度翻倍。不是说求和永远错，而是它对应另一个尺度；今天约定平均损失，就用平均梯度。

### 4. 全批量与逐样本不是同一段循环换个位置

**全批量梯度下降（batch gradient descent）**：用全部训练样本在同一旧参数下算平均梯度，更新一次。

**逐样本更新**：处理一个样本就更新，下一个样本用的是新参数。随机选取或打乱样本的逐样本训练是随机梯度下降的一种典型用法。它是有用的方法，不是错误；只是今天不实现它。

用两个样本x=[0,1]、y=[1,3]，初始w=b=0，α=0.1：

- 全批量：平均梯度(-1.5,-2)，一步变成(0.15,0.2)。
- 按顺序逐样本：第一个样本先把b改成0.1；第二个样本误差成了-2.9，再更新，最终为(0.29,0.39)。

结果不同是因为更新次数和计算梯度的位置不同，不是小数误差。今天的step必须放在平均梯度函数返回之后，不放进遍历样本的循环。

### 5. 新函数负责计算，旧更新器负责修改

文件：`04_模型实践_平均梯度与全批量更新.py`。

复用你已正确的四个类和GradientDescent；可以保留step返回两个参数的写法但忽略返回值，也可以删掉那条多余return。**别同时删除return又继续解包接收结果**，否则会尝试拆开None。

今天独立新增普通函数`batch_gradients(model, data)`：

- 接收已有模型与非空、输入标签等长的数据集对象；
- 遍历每个样本，在当前模型下算两个梯度并求平均；
- 返回两个数，顺序为平均w梯度、平均b梯度；
- 不修改模型、数据、学习率，不调用step，也不新建模型；
- 使用已有size()、get_item()、forward()，不引入库。

返回两个数的用法与你现有函数一样，例如`first, second = some_function()`；接收方的变量名由你决定，不提供循环骨架。

主调用区要求：

1. 创建上表数据、w=b=0模型、损失、评估器和学习率0.1的更新器。
2. 评估旧损失；调用平均梯度函数；确认此时参数仍为0、0。
3. 调用旧step一次；再评估。输出两梯度、新参数、前后损失，对照上表。
4. 保留同一模型和评估器，数据不变；今天不写训练循环。

三个小检查放在同一文件，不增加作业：

| 测试 | 预期 |
|---|---|
| 相同旧模型连续调用batch_gradients两次，不调用step | 返回相同，参数不变 |
| 数据整体重复一遍，仍在旧参数下算 | 平均梯度仍(-3.5,-2)，不是翻倍 |
| 单样本x=[2]、y=[5]，旧w=0、b=1 | 梯度(-8,-4)，退化回昨天的结果 |

独立手算x=[0,1]、y=[1,3]且旧w=1、b=0时的平均损失、两个平均梯度及α=0.1的新参数，再用自己的代码核对。过程写在代码注释即可；先自己算，不把课堂表格照抄当手算。

今天新增的价值：模型不再只听一个样本，而是让一批数据共同决定更新方向。DAY31才把这些已会部件组合到Trainer，DAY32才反复更新。一步批量结果正确仍不等于训练循环和泛化通过。

## 五、交付与后续节奏

提交五份代码与必要运行结果。三步仍由你自己写；心得可以直接注释，不强制另建文件。

今天重点口述三件事：
1. 原地覆盖与建立新列表有何区别？26为什么不必全表查重？
2. 终端输入与源代码函数调用为何不同？字符数组存储长度与可见文本长度为何不同？
3. 为什么同一旧参数、平均梯度、最后更新这三件事必须配套？

DAY30的977顺延：下一次先给它安排新题位，再调整相邻Python复习/新题位置。其余题目不删除、不虚报覆盖，DAY33明确检查是否需延长Python覆盖时间。C++、模型各自推进，不为迁就日期强行加第三道题。当天测试/实现优先，超时先削减重复抄写，不跳过核心概念。

## 六、DAY29五题示范与逐题比较

27、26仍是今天作业，先尝试第二节。按你要求提供完整答案，放在折叠区防止无意先看到。展开后要关闭重写，不算闭卷首做；其他三题可直接对照。


<details>
<summary>00｜27移除元素：尚未提交实现，以下是参考而非你的错误清单</summary>

```python
class Solution:
    def removeElement(self, nums, val):
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write] = nums[read]
                write += 1
        return write

solver = Solution()
for original, val, expected in [
    ([], 7, []),
    ([4, 1, 4, 2, 1], 4, [1, 2, 1]),
    ([2, 2], 2, []),
    ([1, 1, 3], 2, [1, 1, 3]),
    ([5], 0, [5]),
]:
    values = original.copy()
    k = solver.removeElement(values, val)
    assert k == len(expected)
    assert values[:k] == expected
```

write是下一次写有效值的位置，同时等于已保留项数。遇到不需要的值，只推进读取；遇到需要的值，写到前缀后再扩大有效范围。write不会超前于read，所以不会覆盖尚未读取的未来位置。本实现保持顺序，故测试可直接比列表；别的合法乱序实现应比较内容与次数。时间O(n)、额外空间O(1)，测试里的copy不属于解题算法。

</details>

<details>
<summary>01｜26：对比你的新列表方案，原地版本改变在哪里</summary>

```python
class Solution:
    def removeDuplicates(self, nums):
        write = 1
        for read in range(1, len(nums)):
            if nums[read] != nums[write - 1]:
                nums[write] = nums[read]
                write += 1
        return write

solver = Solution()
for original, expected in [
    ([0, 0, 2, 2, 5], [0, 2, 5]),
    ([7], [7]),
    ([3, 3, 3], [3]),
    ([-2, -2, 0, 4, 4], [-2, 0, 4]),
]:
    values = original.copy()
    k = solver.removeDuplicates(values)
    assert k == len(expected)
    assert values[:k] == expected
```

题目保证非空，首项直接保留，所以有效长度从1开始。nums[write-1]是已保留的最后一个不同值；输入有序，当前值等于它就不必重复保留，否则写入下一格。O(n)时间、O(1)额外空间。

你的count和unique_elements计算出正确内容；差别不是变量命名，而是存储位置和接口：
- 你用append把答案写进新列表；这里用下标覆盖原列表。
- 你用not in反复搜索历史结果；这里利用有序性只比较最后保留值。
- 你返回三元组；平台要整数k并检查原输入前缀。
- remove_duplicates作为自定义函数名合法；提交平台时要符合removeDuplicates接口，不把命名问题误判为算法问题。

</details>

<details>
<summary>02｜筛选接口：你的实现正确，参考只整理布局</summary>

```cpp
#include <iostream>
#include <vector>
std::vector<int> over_limit(std::vector<int> values, int limit);

int main() {
    int n;
    std::cin >> n;
    std::vector<int> values;
    for (int i = 0; i < n; ++i) {
        int value;
        std::cin >> value;
        values.push_back(value);
    }
    int limit;
    std::cin >> limit;
    std::vector<int> result = over_limit(values, limit);
    std::cout << result.size() << "\n";
    for (int value : result) {
        std::cout << value << "\n";
    }
    return 0;
}
std::vector<int> over_limit(std::vector<int> values, int limit) {
    std::vector<int> result;
    for (int value : values) {
        if (value > limit) {
            result.push_back(value);
        }
    }
    return result;
}
```

你用while输入、先声明result再赋值都正确。参考使用for与初始化合并，不要求强改。数量与数据分开、函数不能直接读main局部变量，两条理论回答正确。按值复制参数会占O(n)额外空间，返回结果也最多O(n)；不是原地算法，不要求O(1)。

</details>

<details>
<summary>03｜两个重载＋四种调用：补齐默认参数验证</summary>

```cpp
#include <iostream>
#include <vector>
int count_over(std::vector<int> values, int threshold = 10);
int count_over(std::vector<int> values, int lower, int upper);

int main() {
    int n;
    std::cin >> n;
    std::vector<int> values;
    for (int i = 0; i < n; ++i) {
        int value;
        std::cin >> value;
        values.push_back(value);
    }
    std::cout << count_over(values) << "\n";
    std::cout << count_over(values, 20) << "\n";
    std::cout << count_over(values, 10, 20) << "\n";
    std::cout << count_over(values, 0) << "\n";
    return 0;
}
int count_over(std::vector<int> values, int threshold) {
    int count = 0;
    for (int value : values) {
        if (value > threshold) {
            ++count;
        }
    }
    return count;
}
int count_over(std::vector<int> values, int lower, int upper) {
    int count = 0;
    for (int value : values) {
        if (value > lower && value <= upper) {
            ++count;
        }
    }
    return count;
}
```

输入5 4 10 12 20 20输出3、0、3、5；输入0输出四个0。你的函数体与这里的计算逻辑相同，问题在调用覆盖：你main没有省略threshold，所以默认值虽声明了却没用到。

按你的输入格式运行时，需要在容器数据之后继续给threshold、lower、upper。不要用只含容器的原题输入强行跑你的旧程序并分析垃圾输出：输入耗尽后读取失败，未初始化的局部整数不能继续使用。本次150组测试均提供了完整有效输入。通用输入错误处理以后再教，今天先明确协议。

</details>

<details>
<summary>04｜模型一步更新：保留你正确的类，简化重复赋值</summary>

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
        for i in range(self.dataset.size()):
            xs,ys = self.dataset.get_item(i)
            prediction = model.forward(xs)
            predictions.append(prediction)
        
        loss = self.loss.mean(predictions,self.dataset.ys)
        
        return loss

class GradientDescent:
    def __init__(self,learning_rate):
        self.learning_rate = learning_rate

    def step(self, model, grad_w, grad_b):
        model.weight -= self.learning_rate * grad_w
        model.bias -= self.learning_rate * grad_b

dataset = RegressionDataset([2], [5])
loss = SquaredLoss()
model = LinearNeuron(0, 1)
alias = model
evaluator = LossEvaluator(dataset, loss)
optimizer = GradientDescent(0.1)

old_loss = evaluator.evaluate(model)
x, y = dataset.get_item(0)
error = model.forward(x) - y
grad_w = error * x
grad_b = error
optimizer.step(model, grad_w, grad_b)

assert model is alias
assert abs(old_loss - 8) < 1e-9
assert abs(model.weight - 0.8) < 1e-9
assert abs(model.bias - 1.4) < 1e-9
assert abs(model.forward(2) - 3) < 1e-9
assert abs(evaluator.evaluate(model) - 2) < 1e-9
assert dataset.xs == [2] and dataset.ys == [5]

still = LinearNeuron(0, 1)
GradientDescent(0).step(still, -8, -4)
assert still.weight == 0 and still.bias == 1

zero_input = LinearNeuron(2, 1)
e = zero_input.forward(0) - 3
GradientDescent(0.1).step(zero_input, e * 0, e)
assert zero_input.weight == 2
assert abs(zero_input.bias - 1.2) < 1e-9
assert abs(loss.forward(zero_input.forward(0), 3) - 1.62) < 1e-9
print("DAY29一步更新验证通过")
```

你的两次forward都在参数更新前，计算正确；参考只是把误差存一次。你return两个参数后再赋给已修改的属性，也没有多更新一次——只是把同样的值再写回去。参考不返回、直接调用，更能体现更新器修改模型状态的职责。

你在更新前检查身份，参考在更新后检查；教师补测确认你的step没有换对象，这个旧缺口已关闭。仍需要你自己解释手算与零学习率含义，不用重抄四类。

</details>

### DAY29理论示范回答

1. 27保留所有非val值，26保留每个不同值一次；两题都是把结果写入原输入的有效前缀。
2. 重载提供不同参数列表的版本；默认参数为省略的末尾实参提供值。只改返回类型不能区分同一参数列表的调用。
3. step里的self是更新器，model是被更新的神经元。两梯度先由旧参数算出，再修改两个参数，才对应同一个位置的梯度下降。
4. x=1、y=4、w=2、b=1：预测3，误差-1，损失0.5，两个梯度均-1；α=0.1后w=2.1、b=1.1，预测3.2，损失0.32。
5. x=0时w乘在0上，无论怎样微调w都不影响该样本预测，所以w梯度为0；b仍能影响预测。学习率为0则有方向也不移动。

### 教材定位

- [C++教材](../../学习资料/C++/C++%20Primer%20Plus：中文版（第六版）%20(Stephen%20Prata).pdf)：4.1—4.2，今天以固定数组和终止标记为重点，不照搬未教的指针。
- [神经网络教材](../../学习资料/AI%20agent/神经网络与深度学习%20(邱锡鹏).pdf)：2.2.3.1、2.2.3.3，平均梯度承接已有单样本公式。

