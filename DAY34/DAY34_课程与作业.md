# DAY34｜双指针专题①：先学完整思路，再用同类旧题练；图像帧结构；训练数据与未见数据

> 2026-10-31。依据更新后的[学习与授课总约定](../学习与授课总约定.md)和[阶段计划](../DAY29-DAY39_阶段计划.md)。约4小时：Python65分钟、C++100分钟、模型65分钟、保存反馈10分钟。
>
> 算法从今天改法：同专题集中练，新题老师完整示范，旧题你独立练。三步仍是“输入输出→执行阶段→状态与检查”。今天精讲905，复习27；88在文末讲评，DAY36复习位重写，不额外加第三道题。五份代码文件继续留白。

## 一、DAY33部分提交评阅

已读取五份文件及其中的注释；349文件为空，目录中未见另外的心得文件。以下测试评价实际行为，闭卷用时、提示情况与未保留理论不能凭空打分。你反馈算法耗时很久，本次据此调整教学方式，而不是把“再多刷几遍”当唯一办法。

| 项目 | 实际核对 | 评语与处理 |
|---|---|---|
| 349 | 空文件 | 未完成；转到后续哈希专题，不假称已经掌握，也不加到今天成为第三题 |
| 88 | 原脚本IndexError；399组小型有序组合中165组正确、107组错误、127组越界 | 主要是first/second所属数组写反、停止条件随之混乱；不是你完全不会循环，先练变量角色 |
| C++02 | 当前编译无警告，100组非空输入通过；n=0输出nan | 申请、释放与非空统计正确；空图总和除以0需改为约定-1 |
| C++03 | 本机当前可编译，100组非空输入通过；空图平均值也是nan | 亮度限制、返回副本和原图保持正确；补空图判断，直接包含<vector>，不要依赖其他头文件间接提供声明 |
| 模型 | 三场各21项损失与独立公式逐项一致；0、0.1、2使用不同模型，均从(0,0)开始 | 公平对照正确，已能组织真实实验；今天可继续数据与评估，不重抄六类 |

### 1. 88这次不是只差一个符号

你声明first=m-1，说明first属于nums1；second=n-1属于nums2。但判断却访问nums1[second]与nums2[first]，取值和递减也跟着互换。

用nums1=[1]、m=1，nums2=[]、n=0看：first=0、second=-1；你的while first>=0仍进入，随后读取nums2[first]，而nums2没有元素。这个小例子已经足够定位“哪个位置属于哪个输入”的错误。

你有从后写的方向，但还不能稳定把变量职责翻译成代码。今天先在更小的读写双指针任务里完整看一次示范，再用27练相同关系；之后再回到两个输入的合并。不是继续要求你对着88死磕。

### 2. 释放与置空：你的房间类比只需修一处

new[]申请数据，delete[]释放对应存储，这部分你已写对。pixels=nullptr只是改掉你这个指针变量保存的地址，**不是通知操作系统回收房间**。真正释放是delete[]完成的。

因此删除后清空指针能减少误用，但它不能替代释放；若其他名字也保存旧地址，它们也不会被自动清空。无需为此整天重学指针，今天继续用容器保存图像帧。

你在统计后释放数组，再打印已经保存的total和counts合法；打印的是统计结果，不是读已释放像素。问题只是n=0时没有平均值，需在除法前判断。

### 3. 模型学习率实验已完成，另一个原因怎样理解

你问“损失不降，除了学习率不合适，还有什么原因？”没有唯一的第二个答案，需要看当前行为：

- 计算了梯度但没写回模型，或每步又把参数重置，参数实际上没持续变化。
- 已在当前目标的最优点附近，梯度很小，损失可能稳定；不意味着程序错。
- 数据存在误差、模型表达能力有限，损失可能降到某个非零水平，继续训练也未必能变成0。

在本次数据和初值下，先检查学习率是否为0、梯度是否非零、调用后原模型参数是否改变。你的当前实现已经通过三场公式核对，不继续把过去“没有写回参数”算成现在的错误。

三场结果：
- α=0：一步和20步损失都4.5；
- α=0.1：一步3.021875，20步约0.0023268；
- α=2：一步30.75，20步约2.349×10^17。

你用三个字典保存摘要，能够比较结果；原作业没有保存题目要求的完整“学习率→损失序列”总字典，不影响已计算的序列。最终参数打印、独立100步预测和指定手算仍缺原提交证据，今天不为缺输出停课。

## 二、算法改法与今天的专题（65分钟）

### 1. 仍用三步，只改变谁先示范、怎样练

新题由我演示三个关键判断：题目要求什么结果；为什么选这个办法；变量怎样对应每次动作。你先跟小数据看明白，再关闭答案重写。复习题才先独立做，卡住约10分钟看小提示，约20分钟仍无推进就看针对性解释，不让它占掉半天。

今天进步的证据不是“记住905答案”，而是做27时能否自己说出读、写两个位置的职责，保留条件改变后能否改对代码。

新题约35分钟（讲解与关闭重写），复习20分钟，测试与简短解释10分钟。无需再写一份方法论心得。

### 2. 先总结今天这一类的套路：读位置＋写位置

**双指针（two pointers）**在本专题表示用两个下标保存处理进度，不是C++内存地址。

当你要扫描数组、把符合某条件的元素放到前面，而且允许改原数组时，可以考虑：
- 读位置：现在检查哪一个输入元素；
- 写位置：下一份符合条件的结果放在哪里；
- 每检查一个元素，读位置推进；只有确实保留了一个符合条件的元素，写位置才推进。

不是所有双指针题都用这套：88有两个输入各自的读位置，977从两端选择最大值。今天先练一种，下两节再连接差异，不把它们混成唯一模板。

## 三、新题905精讲：我会怎样把题意变成代码

[LeetCode905：按奇偶排序数组](https://leetcode.com/problems/sort-array-by-parity/description/)，简单。把所有偶数放到所有奇数前面，返回任何满足要求的数组；两组内部顺序不限。官方没有要求必须原地，本课选择原地实现，练O(n)时间、O(1)额外空间。

### 第一步：用最小例子确认要交什么

输入[3,1,2,4]，返回[2,4,3,1]合法，[4,2,1,3]也合法。不能丢失3或1，也不能把重复值合并。这里“排序”不要求从小到大，只要求偶数整体在前。

**偶数**是除以2余数为0的整数。Python的%求余数：4%2得到0，3%2得到1，因此判断num%2==0。0也是偶数。

这一步就排除两个误解：不需要完整数值排序，不需要去重。接口是sortArrayByParity(self, nums)，返回列表，不是27那样只返回有效长度。

### 第二步：从直观办法找到本专题的动作

直观办法是另建两个列表，分别装偶数、奇数，再拼起来。它能做对，但额外保存了输入规模的数据。

现在换一个问题：原数组已经有足够格子，能不能把遇到的偶数直接放到前面？

从左向右看数组，维护一段“已经摆好的偶数前缀”。遇到奇数先略过，遇到偶数就把它与前缀后面的那一格交换，再让前缀扩大一格。交换保留了所有值，不会把原来的奇数弄丢。

这里选择交换而不是只覆盖，是因为905最后仍要保留全部奇数；27只检查非val前缀，因此可以覆盖，也可以用你已有的交换法。

### 第三步：给状态职责，再逐轮对应代码

定义read为当前检查位置，write为下一个偶数应该放的位置。最开始一个偶数都没安排，所以write=0；read从第0项开始扫。

每次检查之前：
- 下标小于write的部分，已经都是偶数；
- write到read之前是已检查的奇数；
- read及后面还没处理。

用[3,1,2,4]走一遍：

| 当前read / 值 | 动作 | 数组变化 | 下一write |
|---|---|---|---:|
| 0 / 3 | 奇数，暂不交换 | [3,1,2,4] | 0 |
| 1 / 1 | 奇数，暂不交换 | [3,1,2,4] | 0 |
| 2 / 2 | 和第0格交换 | [2,1,3,4] | 1 |
| 3 / 4 | 和第1格交换 | [2,4,3,1] | 2 |

为什么不破坏未来数据？write始终不超过read。写位置在read之前时，那一格是已检查的奇数；交换把它放到当前格，当前格之后再也不需要作为未读输入重查。write==read时只是和自己交换，也成立。

**完整参考，新题今天允许先学：**

```python
class Solution:
    def sortArrayByParity(self, nums):
        write = 0
        for read in range(len(nums)):
            if nums[read] % 2 == 0:
                nums[write], nums[read] = nums[read], nums[write]
                write += 1
        return nums
```

逐段看：
- write=0：偶数前缀目前长度为0；
- for每次检查一个原位置，不因某个分支多处理两项；
- 条件只问当前值是否偶数；
- 同时赋值交换两个元素，保留两份数据；
- write只在放入一个偶数后加1；
- 最后原数组已经分区完成，返回它。

没有必要额外把奇数排序。每项被检查一次，交换是常数次操作，因此O(n)时间、O(1)额外空间。

### 4. 关闭参考，从空白实现与验证

文件：`00_Python精讲重写_LeetCode905_按奇偶排序.py`。

先用自己的话复述两个下标分别干什么，再关掉参考写。今天的新题不要求“从未看答案”；我们检查的是看懂后能否自己恢复思路，并在复习题迁移。

测试[3,1,2,4]、[0]、[1,3,5]、[2,4,6]、[2,1,2,1]。顺序不限，不要只与某一个完整列表硬比。

怎样检查：
1. 输出值与次数应和输入一致。测试中可用sorted(结果)==sorted(原输入副本)比较；sorted返回排好序的新列表，只用来检查，不放进解题算法。
2. 一旦出现奇数，之后不能再出现偶数。可以自己用小循环检查，也可先肉眼核对；不用新测试框架。
3. 额外空间看函数内部，测试保存输入副本不算作解法本身的空间。

## 四、复习27：用同一套路自己完成（20分钟）

文件：`01_Python专题复习_LeetCode27_移除元素.py`。

实现removeElement(self, nums, val)：原地把不等于val的项放在前k格，只返回整数k；后面不用清空。O(n)、O(1)。

和905一样，仍可用“读位置检查、写位置安排”。但保留条件从“偶数”变成什么？返回结果从列表变成什么？请你自己回答、自己写三步，题内不预填答案。

测试[4,1,4,2,1]排除4→k3，前缀含两个1和一个2；[2,2]排除2→0；[]排除0→0；[1,1,3]排除2→3。

卡住10分钟才看这句提示：写位置既是下一份结果放的位置，也等于已经保留的数量。还卡住就回看905的逐轮表，换掉保留条件，而不是再花半小时猜变量名。

## 五、C++与机器人：把一张图的相关信息装在一起（100分钟）

昨天我们只有一排像素。今天继续同一相机任务：如果四台相机先后拍了很多张图，只拿到[0,20,120,250]，你不知道是哪台拍的、什么时候拍的，也不知道这四格应摆成一行还是两行。

### 1. 先把需要保存的信息讲清楚

**帧（frame）**：这里就是一次拍到的一张图。
**时间戳（timestamp）**：给拍摄时刻记一个数字。本课用相对固定起点的秒数，例如1.5秒；暂不读取系统时钟。
**字段/成员（field/member）**：一份记录中的一项内容，例如宽、相机编号。

我们希望一份图像记录同时保存：
- camera_id：相机编号，本地练习0—3；
- timestamp：拍摄时刻，double秒；
- width、height：图有几列、几行；
- pixels：按行保存的像素，vector<int>。

2列2行且像素为[10,20,30,40]，就是第一行10、20，第二行30、40。这里都是灰度值，不是空间里的米。记录拍摄信息是为了后面正确配对连续图像；它本身还没有估计机器人位置。

真实ROS传图也需要约定数据及其说明。今天先把一份记录写清楚，未来再把它适配成真实消息，不引入通信API。

### 2. struct怎样把相关字段放在一起

**结构体（struct）**是你定义的一种数据类型，可以把不同类型的相关内容组合起来。人话：把同一张图的标签和像素放到一张记录卡上，避免分别传五个变量而配错。

一个更小的例子，只放编号和时刻：

```cpp
#include <iostream>
struct FrameHeader {
    int camera_id = 0;
    double timestamp = 0.0;
};

int main() {
    FrameHeader header;
    header.camera_id = 2;
    header.timestamp = 1.5;
    std::cout << header.camera_id << " " << header.timestamp << "\n";
    return 0;
}
```

输出2 1.5。逐个对应：
- struct FrameHeader{...};定义一种类型，结尾分号不能漏；
- 花括号内是这类记录有哪些成员，以及本例默认值；
- FrameHeader header;创建一份记录对象，类似Python中按某种类的定义创建具体实例；
- header.camera_id用点号找到这份记录的字段，给它赋值不影响另一份记录；
- 声明类型本身不会拍照，也不会自动调用处理函数。

类型定义放在需要使用它的函数前。今天只用公开数据成员，public/private与成员方法在下一课真实需要管理状态时再讲。

### 3. 旧函数怎样接到新记录上

ImageFrame里包含vector<int> pixels，读像素就是frame.pixels，长度是frame.pixels.size()。你昨天的brighten_copy可以接收frame.pixels，不必因为数据外面多一层记录就重写亮度算法。

只读整帧的接口可以写成`double mean_brightness(const ImageFrame& frame)`：仍是你会的const引用，只是类型从vector换成自己定义的ImageFrame。空像素平均值返回-1，这次先判断再做除法。

多个帧可以放进`std::vector<ImageFrame>`，与vector<int>一样使用push_back。容器元素从整数变为一份完整记录。访问frames[0].camera_id，先取第0份记录，再取编号；空容器仍不能取第0项。

本例结构体只含数字与vector，可以复制为另一份独立记录，例如`ImageFrame changed = original;`。其中vector按自己的值语义复制；改变changed.pixels不会改original.pixels。复制含裸指针的复杂结构不能据此照搬，DAY37再专门讲区别。

### 4. 两项相连实践（45分钟手敲＋10分钟检查）

**02：建立一张完整帧记录**

文件：`02_C++核心_结构体图像帧.cpp`。

自行定义ImageFrame，包含前面五项成员；数字成员给默认值，pixels使用vector。读入顺序为camera_id、timestamp、width、height，接着width×height个0—255像素。尺寸0—4，空帧允许width=height=0；输入保证合法，不考文本解析。

实现mean_brightness(const ImageFrame& frame)，空像素返回-1，否则返回平均值。不修改帧，不在函数里打印。

main三行输出：第一行四项元信息；第二行像素数量和平均值；第三行原像素列表。

输入0 1.5 2 2 0 20 120 250：前两行为0 1.5 2 2、4 97.5；第三行0 20 120 250。
输入1 2.0 0 0：前两行1 2 0 0、0 -1，第三行为空。
输入2 3.0 1 1 0：像素数量1、平均0，不能把黑像素误当空帧。

**03：处理两张帧记录，说明信息与像素一起保留**

文件：`03_C++应用_多帧亮度处理.cpp`。

复用自己02的ImageFrame与均值函数，以及DAY33的亮度副本函数。自行实现`ImageFrame brighten_frame(const ImageFrame& source, int delta)`：返回新记录，编号、时刻、宽高保持；只有像素按加delta并限制255的规则改变，原帧不改。

main依次读两张帧（每张按02输入格式），放入vector<ImageFrame>，最后读取delta（0—30）。对每张帧输出三行：编号、时刻、原均值、新均值；原像素；新像素。两张共六行，空像素对应空行。只读遍历多帧时可以用`const ImageFrame&`作为循环元素类型，含义仍是“借来读，不改它”。

组合输入：
```text
0 1.0 2 2 0 20 120 250
1 1.5 0 0
20
```
第一帧四个统计值为0、1、97.5、113.75，原/新像素与昨日相同；第二帧统计为1、1.5、-1、-1，原/新像素为空。自行再测delta=0与像素250、255，验证上限和原数据保留。

老师不预填两份struct实现。先讲清接口再自己组织代码，已有正确处理函数直接复用。

```bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY34/02_C++核心_结构体图像帧.cpp" -o /tmp/day34-frame
/tmp/day34-frame
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY34/03_C++应用_多帧亮度处理.cpp" -o /tmp/day34-frames
/tmp/day34-frames
```

## 六、模型：训练误差降了，为什么还要看没参加训练的数据（65分钟）

教材接《神经网络与深度学习》2.4，先解释拟合、噪声、偏差与方差的关系，不要求现在推完整期望公式。今天复用正确fit和评估器，不再增加新框架。

### 1. 从你已完成的学习率实验接起

DAY33说明步长改变会影响训练是否下降。现在假设步长正常、代码也正确，是否训练误差越低就说明模型越可靠？

训练集是模型据以修改参数的样本。一直盯训练误差，可能只说明它更贴合这几份记录。**泛化（generalization）**指模型在没参加训练的数据上是否仍能处理好。人话：不是只会做课堂原题，还要看换一份输入能不能行。

因此今天保留一份独立数据，只拿来评估，绝不送入求梯度的训练器。它只检验这次小实验，不用它反复调出最好学习率。

### 2. 数据也会有误差，模型可能把误差一起学进去

原训练关系是y=2x+1，样本[-1,0,1,2]对应[-1,1,3,5]。

现在假设最后一条记录出现测量或录入误差，把5记成11。输入没变，训练目标变了：
```text
干净标签：[-1,1,3,5]
有误标签：[-1,1,3,11]
```

**噪声（noise）**泛指观测中的随机扰动等误差；今天人为改一条标签模拟数据错误，不把它当作严格的零均值随机噪声实验。

原本该预测5的地方，训练现在要求预测11。优化器不知道哪一条是错的，只按目标减少平均损失。于是参数可能朝另一条直线移动。这不等于梯度公式错了，训练目标本身已经改变。

### 3. 模型能力与数据敏感性，各指什么

**拟合**是模型贴合已给样本的能力。直线模型无法表达所有关系：例如x为-1、0、1时，若目标是1、0、1，一条直线无法同时穿过三点，练再久也不能三项都零误差。这是表达能力限制，不只是学习率问题。

**欠拟合**是模型对主要关系都没学好；**过拟合**是过度适应有限训练样本的细节、误差，换数据表现反而不好。不能只看到一次留出误差大，就宣称已经证明过拟合。

教材的**偏差（bias）**讨论不同训练集所得模型的平均预测离理想关系有多远；**方差（variance）**讨论换一批训练数据后预测会波动多少。人话：一种是长期偏离目标，另一种是太容易随样本改变。这里的统计偏差不是模型参数bias那个偏置b，两者名字相近、含义不同。

今天不计算这两个统计量，只通过更换一条记录观察参数敏感性和留出误差。是否过拟合、偏差方差如何估计，需要更多训练集与模型对照，后续逐步验证。

### 4. 一份固定留出数据，让比较站在同一把尺上

保留输入[-2,3]，标签[-3,7]，不参与训练。分别训练干净组和有误组，各自初始w=b=0、α=0.1、100步，再用同一留出集评估。

预期数值（都是平均半平方损失）：

| 训练用的数据 | 自己的训练损失前→后 | 最终(w,b)约值 | 同一留出集损失约值 |
|---|---|---|---:|
| 干净标签 | 4.5→8.41e-9 | (1.999918,1.000133) | 2.52e-8 |
| 最后一项改为11 | 16.5→1.35000008 | (3.799740,1.600421) | 11.2475 |

两组训练目标不同，不能只比各自训练损失的绝对大小判“哪个优化器更好”。它们使用同一优化器；我们是在同一个留出标准上比较数据变化造成的结果。

有误组的训练误差确实下降，但x=3的预测约13，离正确标签7很远。这个例子说明“优化能工作”与“数据和模型能解决任务”需要分别检查。它不构成所有复杂模型的过拟合实验。

### 5. 独立实践（25分钟）与手算（10分钟）

文件：`04_模型实践_训练误差与留出误差.py`。

复用已有六类及梯度函数，不要求改train/fit命名；调用区自己组织：
- 两份训练数据与上表一致，同一份留出数据。
- 每组建立自己的模型、学习率0.1优化器和Trainer，从(0,0)跑100步。
- 保存训练前后损失、最终参数、留出损失以及x=3预测。评估留出集用另一个LossEvaluator，不把留出数据放进Trainer。
- 评估前后比较参数，确认evaluate没有修改模型；原数据也保持。
- 核对干净组留出损失小于0.001，有误组留出损失明显更大。解释原因时不要只写“学习率不好”。

手算一个最小例子：模型w=2、b=1，输入x=2，正确标签5时损失多少，标签错误成11时损失多少？在同一旧参数点，两种标签对应梯度各是什么？用数值说明“标签改变会改变模型往哪边走”。

你只需把真实卡点或结论写一句，不新建评估报告模板。下一课沿教材继续训练与评估数据的用途，不同时引入多套统计工具。

## 七、今天完成标准

算法看“学过905后能否自己恢复读写职责，并在27改变保留条件”；C++看“一份帧记录是否把像素和说明一起保存、空帧是否先判断”；模型看“数据不参与训练却能独立评估、改变标签后能解释结果”。

每天仍两道算法题、两项C++练习、一项模型实践。新题可先看完整示范；复习题关闭答案先练。看到答案后重写的完成方式如实说明即可，不为了追求全独立耗上一整天。

## 八、DAY33五份完整示范与逐项对照

这里是前一天示范，算法部分88尚未通过，DAY36才安排完整复写。今日两题是905与27，不因答案已给就自动加第三份作业。


<details>
<summary>00｜349：未完成，参考留给后续哈希专题，今天不用另做</summary>

```python
class Solution:
    def intersection(self, nums1, nums2):
        available = set(nums1)
        common = set()
        for value in nums2:
            if value in available:
                common.add(value)
        return list(common)

solver = Solution()
assert set(solver.intersection([1, 2, 2, 1], [2, 2])) == {2}
result = solver.intersection([4, 9, 5], [9, 4, 9, 8, 4])
assert set(result) == {4, 9} and len(result) == 2
```

nums1做“出现过”的名单，第二个集合负责避免答案重复。平均O(m+n)时间、O(m+n)空间以内。原提交为空，因此没有可对比的算法错误；后续哈希专题再精讲，不要求今天把这份代码当第三道题去刷。

</details>

<details>
<summary>01｜88：下标必须永远访问它所属的数组</summary>

```python
class Solution:
    def merge(self, nums1, m, nums2, n):
        first = m - 1
        second = n - 1
        write = m + n - 1
        while second >= 0:
            if first >= 0 and nums1[first] > nums2[second]:
                nums1[write] = nums1[first]
                first -= 1
            else:
                nums1[write] = nums2[second]
                second -= 1
            write -= 1

solver = Solution()
for first_values, m, other, expected in [
    ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], [1, 2, 2, 3, 5, 6]),
    ([1], 1, [], [1]),
    ([0], 0, [1], [1]),
    ([2, 4, 0, 0], 2, [1, 3], [1, 2, 3, 4]),
    ([0, 0], 1, [-1], [-1, 0]),
]:
    a = first_values.copy()
    saved_other = other.copy()
    returned = solver.merge(a, m, other, len(other))
    assert returned is None and a == expected and other == saved_other
```

| 角色 | 只能读取谁 | 放入这一侧的值以后做什么 |
|---|---|---|
| first | nums1[first] | first减1 |
| second | nums2[second] | second减1 |
| write | 不负责选来源，只指向nums1的下一个写入格 | 每轮减1 |

你的初始化说明first属于nums1，但后面用nums2[first]，角色与代码不一致。这比背“把条件改成while second>=0”更需要先理解。

为什么while只要求second还有值？nums2用完，nums1剩下的前缀就在原位置；nums1用完而nums2未完，继续把nums2放入预留位置。边界检查first>=0必须先于nums1[first]读取，避免拿Python负下标意外读尾部。

时间O(m+n)，额外空间O(1)，无返回列表。这个参考不代表你已独立掌握；DAY36两路扫描时再关掉它重写。

</details>

<details>
<summary>02｜图像缓冲区：保留非空计算与正确释放，补空图平均值</summary>

```cpp
#include <iostream>
int main() {
    int n;
    std::cin >> n;
    int* pixels = new int[n]{};
    double total = 0;
    int dark_count = 0;
    for (int i = 0; i < n; ++i) {
        std::cin >> pixels[i];
        total += pixels[i];
        if (pixels[i] < 50) {
            ++dark_count;
        }
    }
    delete[] pixels;
    pixels = nullptr;

    std::cout << n << "\n";
    if (n == 0) {
        std::cout << -1 << "\n";
    } else {
        std::cout << total / n << "\n";
    }
    std::cout << dark_count << "\n";
    return 0;
}
```

与你相比，只增加除法前的空图分支，其他计算等价。统计值已是独立变量，释放像素后打印它们合法。n=0的数组没有元素，循环执行0次，释放也合法；不能因此认为0/0是有效平均值。

你的“房间号”类比有帮助，需修正nullptr只是清空本地指针，释放动作在delete[]处。教材里“堆/栈”可帮助理解常见实现，但这课只需准确掌握哪些数据随作用域结束、哪些需要对应释放，不用先背所有存储术语。

</details>

<details>
<summary>03｜图像亮度副本：函数计算正确，补直接头文件与空图分支</summary>

```cpp
#include <iostream>
#include <vector>
std::vector<int> brighten_copy(const std::vector<int>& pixels, int delta);

int main() {
    int n;
    std::cin >> n;
    std::vector<int> pixels;
    for (int i = 0; i < n; ++i) {
        int pixel;
        std::cin >> pixel;
        pixels.push_back(pixel);
    }
    int delta;
    std::cin >> delta;
    std::vector<int> results = brighten_copy(pixels, delta);

    for (int pixel : pixels) {
        std::cout << pixel << " ";
    }
    std::cout << "\n";
    double total = 0;
    for (int pixel : results) {
        total += pixel;
        std::cout << pixel << " ";
    }
    std::cout << "\n";
    if (results.empty()) {
        std::cout << -1 << "\n";
    } else {
        std::cout << total / results.size() << "\n";
    }
    return 0;
}

std::vector<int> brighten_copy(const std::vector<int>& pixels, int delta) {
    std::vector<int> result = pixels;
    for (int& pixel : result) {
        pixel += delta;
        if (pixel > 255) {
            pixel = 255;
        }
    }
    return result;
}
```

你函数中的复制、引用遍历、亮度上限均正确。参考直接包含<vector>，不依赖其他头文件；当前本机碰巧能编译，不应据此把头文件缺失当成通用写法。empty()是已学的容器空判断；均值先判断后相除。

这份brighten_copy可以继续用于今天的帧结构，不要求再次手写同一循环。新实践的重点是整份记录中的元信息与像素一起保存。

</details>

<details>
<summary>04｜学习率对照：保留你正确的六类，整理调用与结果核对</summary>

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
        error = prediction - target
        return (error**2)/2
    def mean(self,predictions,targets):
        total = 0
        for i in range(len(predictions)):
            total += self.forward(predictions[i],targets[i])
        return total/len(predictions)
        
class LossEvaluator:
    def __init__(self,data,loss):
        self.data = data
        self.loss = loss
    def evaluate(self,model):
        predictions = []
        for i in range(self.data.size()):
            single_xs,single_ys = self.data.get_item(i)
            prediction = model.forward(single_xs)
            predictions.append(prediction)
        mse = self.loss.mean(predictions,self.data.ys)
        return mse

class GradientDescent:
    def __init__(self,learning_rate):
        self.learning_rate = learning_rate
    def step(self,model,g_w,g_b):
        model.weight -= self.learning_rate * g_w
        model.bias -= self.learning_rate * g_b

def batch_gradient(model,data):
    g_w,g_b = 0,0
    for i in range(data.size()):
        single_xs,single_ys = data.get_item(i)
        error = model.forward(single_xs) - single_ys
        g_w += error * single_xs
        g_b += error * 1
    return g_w/data.size(),g_b/data.size()

class Trainer:
    def __init__(self,model,data,loss,optimizer):
        self.model = model
        self.data = data
        self.loss = loss
        self.optimizer = optimizer

        self.evaluator = LossEvaluator(self.data,self.loss)
    
    def train(self):
        old_loss = self.evaluator.evaluate(self.model)

        mean_g_w,mean_g_b = batch_gradient(self.model,self.data)

        self.optimizer.step(self.model,mean_g_w,mean_g_b)

        new_loss = self.evaluator.evaluate(self.model)

        return new_loss
    
    def fit(self,epochs):
        loss_list = []
        loss_list.append(self.evaluator.evaluate(self.model))
        for i in range(epochs):
            loss_list.append(self.train())
        return loss_list

data = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
loss = SquaredLoss()
histories = {}
models = {}

for rate in [0, 0.1, 2]:
    model = LinearNeuron(0, 0)
    trainer = Trainer(model, data, loss, GradientDescent(rate))
    history = trainer.fit(20)
    histories[rate] = history
    models[rate] = model
    assert len(history) == 21
    assert history[0] == 4.5
    print(rate, history[0], history[1], history[-1], model.weight, model.bias)

assert histories[0] == [4.5] * 21
assert models[0].weight == 0 and models[0].bias == 0
assert abs(histories[0.1][1] - 3.021875) < 1e-9
assert histories[0.1][-1] < histories[0.1][0]
assert abs(histories[2][1] - 30.75) < 1e-9
assert histories[2][-1] > histories[2][0]

fresh = LinearNeuron(0, 0)
fresh_trainer = Trainer(fresh, data, loss, GradientDescent(0.1))
fresh_history = fresh_trainer.fit(100)
assert len(fresh_history) == 101
assert fresh_history[-1] < 0.001
assert abs(fresh.forward(3) - 7) < 0.01
assert abs(fresh.forward(4) - 9) < 0.01
print("DAY33学习率与独立100步验证通过")
```

六类和batch_gradient沿用你自己的接口，epochs在本课全批量训练时与更新步数对应，变量名不同不算错。原三场都用了不同对象，这一点正确。

参考用同一个小循环组织三场，是减少重复；你分别写三个对象并没有计算错误。参考增加完整损失字典、参数输出与独立100步预测，不把你已经完成的学习率对照判成没做。

</details>

### DAY33理论示范回答

- 动态数组的指针保存首地址；delete[]释放对应存储；nullptr只改变指针变量，不代替释放。
- 空图没有平均亮度，本课约定-1；黑像素0是合法亮度，不能混成空图。
- 原图const引用供函数读取；复制得到的vector按值拥有独立元素，修改副本不改原图。亮度超过255需按本课规则限制。
- 公平比较学习率，必须固定数据、初始参数、损失定义和更新次数。模型需各自独立，数据对象若只读可以共享。
- 旧梯度(-3.5,-2)从(0,0)出发：α=0.1一步得(0.35,0.2)，损失3.021875；α=2得(7,4)，损失30.75。损失不降还可能因为没有真正更新、反复重置、已经接近最优或数据/模型限制，不能只有“学习率错了”一个解释。

### 本课参考位置

- [905官方题目](https://leetcode.com/problems/sort-array-by-parity/description/)核对输出要求与边界；本课读写双指针是选定教学方法，代码由课程独立组织。
- [C++ Primer Plus中文版](../../学习资料/C++/C++%20Primer%20Plus：中文版（第六版）%20(Stephen%20Prata).pdf)4.4，书内88—90页（PDF106—108页）：结构类型、实例与点号成员访问。
- [神经网络与深度学习](../../学习资料/AI%20agent/神经网络与深度学习%20(邱锡鹏).pdf)2.4，书内37—39页（PDF52—54页）：偏差、方差与数据变化。今天使用连贯小实验解释，不要求背完整推导。


