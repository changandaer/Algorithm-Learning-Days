# DAY33｜集合交集、用一张图像学C++数据寿命、学习率对照

> 2026-10-28发布。当前约定：[学习与授课总约定](../学习与授课总约定.md)；执行表：[DAY29—DAY39阶段计划](../DAY29-DAY39_阶段计划.md)。
>
> C++从DAY32的vector、引用与const接到图像数据，长期目标是读懂OmniNxt论文与代码。为对齐目标源码，当前采用ROS 1语境，每天只讲本任务需要的概念。今天约4小时：Python65分钟、C++及机器人100分钟、模型65分钟、保存反馈10分钟。五份代码保持留白，三步由你自己写。DAY32全部参考与比较在文末。

## 一、DAY32评阅：先把已完成的能力记清楚

读取了五份代码及其中的注释，DAY32目录未见独立心得文件或单独理论回答。代码中的验证行为作为反馈；口述、手算、用时与提示范围没有记录的部分仍待验收，不直接认定不会。

| 项目 | 实际核对 | 评语与处理 |
|---|---|---|
| 88 | 原脚本在nums1=[1]、nums2=[]时IndexError；重新枚举399组小型有序组合，272组返回内容正确、127组越界 | 正向比较方向可用，但缺nums2耗尽分支；新建result并return也未完成原地接口。今天在复习位修正 |
| 977 | 长度1—8、值-2—2的1,286组有序输入全通过，输入未改变 | 相等分支与循环推进错误已修复，O(n)时间、结果O(n)空间，继续间隔复习 |
| C++02 | C++17编译无警告，100组完整输入通过，含空容器和负增量 | 副本与引用修改、范围for引用正确，无需重学 |
| C++03 | 函数单独核对7种长度、每种31个阈值，结果正确且不改输入；完整样例输出总和130而非34 | main先把首项改成100；这是调用方的修改，不是const失效。n=0时访问values[0]由AddressSanitizer确认越界 |
| 模型fit | 100组不同数据、初值、步数与学习率场景与独立公式一致；100步与10+90步终点一致 | 循环、steps+1条损失、原实例续训、fit(0)均正确。train只返回更新后损失也能支撑fit，不强迫改回模板 |
| 固定训练重跑 | 从(0,0)独立更新100次：末损失约8.41e-9，预测3约6.999887、预测4约8.999805 | 训练流程和指定数值条件有教师运行证据；原调用区尚未保留两次预测及相应断言 |

### 1. 88缺的是另一个“用完了”的判断

你的实现只检查left_1<m，却在该分支直接访问nums2[left_2]。当nums2先用完，left_2已等于n，就没有元素可读。

最小例子nums1=[1]、m=1、nums2=[]、n=0：left_1<m成立，但nums2[0]不存在，第一轮就出错。再看nums1=[2,4,0,0]、nums2=[1,3]，读完1和3后，剩下4本该保留，也不能再读取nums2。

这和今天存图像像素时的长度判断有共同点：**有地址或有容器，不代表当前位置一定有数据。**

先做出额外列表版也能帮助理解合并，但要完成本题仍需写回nums1。今天自己用从后填的思路修正，参考在文末，不改你的旧代码。

### 2. const引用约束的是哪一条访问路径

你的total_duration与count_over已经正确。main中values是普通容器，当然允许写values[0]=100；把它交给const引用函数，不会追溯性地禁止main之前修改。

若这行是为了观察外部仍可修改，可以作为实验保留在注释中；要按输入做正式统计就应去掉它。无论是否实验，空容器都没有第0项，需要先看长度再访问。今天图像练习会包括没有像素的输入，不为这一个问题取消新内容。

你的const_values[0]=100与函数内修改值都已注释，说明在探索只读限制。参考将“观察实验”和最终输入输出分开，计算函数无需推倒重写。输出27、1是否同一行只做格式整理。

### 3. 模型这次真的训练起来了

你把单步方法命名为train，只返回new_loss，fit调用它并收集每步结果，数学和状态连续性正确。接口名与示范不同，不影响当前实现；今天继续复用它。

原调用顺序是fit(0)、fit(1)、fit(2)、fit(10)、fit(50)、fit(100)，同一模型总更新0+1+2+10+50+100=163次。最后一份101条记录从第63步的模型开始，不能标成“从零100步”。这是实验初始条件的区别，不是fit循环错误。

SquaredLoss.forward保存self.prediction和self.target不影响当前损失数值，但它们只是最后一次样本的值，不是模型参数，也不是整个数据集的预测。若没有后续用途，可删这两个属性，局部参数已经足够；不要求为此重新抄类。

旧阶段“实现可训练线性神经元”的核心计算现已有代码与运行证据。独立口述、手算和限时能力继续分别验收，不把旧的“尚未实现训练”结论留作当前错误。

## 二、Python：349新题＋88修正（65分钟）

### 1. 先修88，20分钟

文件：`01_Python复习_LeetCode88_原地合并.py`。

实现merge(self, nums1, m, nums2, n)，结果写回nums1，返回None，nums2保持不变。目标O(m+n)时间、O(1)额外空间。题意沿用[官方题目](https://leetcode.com/problems/merge-sorted-array/description/)。

重点测试：[1]/m1与[]/n0；[0]/m0与[1]/n1；[2,4,0,0]/m2与[1,3]/n2；[0,0]/m1与[-1]/n1；[2,2,0,0]/m2与[2,2]/n2。前两个输入专门覆盖一边没有有效数据，0是否有效由m决定。

自己写三步，解释两个读位置各自是否仍有效，以及写入为何不覆盖未读取数据。卡住时按需看文末，关闭后重写；新题仍保留。

### 2. 新知识：集合不记录每次出现，只记录“有哪些”

**集合（set）**保存不重复的元素，适合回答“出现过没有”。人话：一张资格名单，同一个人登记五次也只占一个名字。

区别于昨天88：合并有序数组要保留每条记录；今天求交集只关心两个输入共同拥有的值，每个值输出一次。先读任务要不要保留次数，再选容器。

最小语法例子，与作业交集实现分开：

```python
seen = set([2, 2, 5])
print(len(seen))   # 2，重复的2只保留一个
seen.add(8)
print(2 in seen)   # True
print(3 in seen)   # False
items = list(seen) # 转成列表；不要依赖排列顺序
empty = set()     # 空集合；{}是空字典
```

集合里的整数查找和添加在通常哈希分布下平均O(1)，不是承诺任何情况下都常数时间；处理n个值平均O(n)。列表的in可能逐项搜索，长度n时一次查找最坏O(n)。

**交集（intersection）**指两边都出现的元素。例如A=[1,2,2,1]、B=[2,2]，共同值只有2，所以结果是[2]，不是[2,2]。无须给结果排序。

### 3. 新题349，约35分钟＋10分钟检查

文件：`00_Python新题_LeetCode349_两个数组的交集.py`。

[LeetCode349官方题目](https://leetcode.com/problems/intersection-of-two-arrays/description/)，简单。实现intersection(self, nums1, nums2)，返回只包含共同值且无重复的列表，顺序不限。输入长度均至少1，今天不额外考空输入。课程约定不修改输入。

你可以先用已学循环、in、集合add来组织，不要求一行写完。目标平均O(m+n)时间、O(m+n)额外空间以内；说清哪些集合负责查找、哪些信息负责避免重复，三步由你写，不预填算法流程。

| 输入 | 预期结果包含 |
|---|---|
| [1,2,2,1]， [2,2] | [2] |
| [4,9,5]， [9,4,9,8,4] | 4、9，各一次 |
| [1,2]， [3,4] | [] |
| [0,0]， [0] | [0] |
| [2]， [2,2,2] | [2] |

测试顺序不限，可用set(实际)==set(预期)比较内容，同时用len检查没有重复；否则实际[2,2]也可能被集合比较掩盖。不用新增测试框架。

## 三、C++与机器人：先让一张图像安全地交到下一段程序（100分钟）

今天只解决一个问题：**相机拍到一张图，下一段程序要用它时，那些数字还在不在？**

你DAY32已经会vector、引用、const。我们从这些熟悉的东西出发，用一个极小的图像实验学习数据的寿命。今天不要求安装ROS，也不先背一张工具名词表。

### 1. 从OmniNxt到底需要做什么说起

OmniNxt上的相机拍周围环境。后面的程序要利用照片判断机器人怎样移动、周围物体离它多远。论文把这两部分分别称为Omni-VINS和Omni-Depth：前者结合相机和运动测量估计运动，后者利用多相机图像估计远近。今天只先认识它们的用途，不解释内部算法。

先看一条能理解的链：

```text
相机拍照 → 一张图像的数据 → 处理图像的程序 → 后续估计位置、环境
                    ↑
             DAY33只做到这里的数据保存与处理
```

如果拍照程序与处理程序各自运行，它们需要约定怎样把图交给对方。**ROS（Robot Operating System）**是一套帮助机器人程序互相传数据、组织运行的工具。人话：让“负责拍照的程序”和“负责处理照片的程序”能配合工作。

ROS不会自动知道机器人在哪，也不会替你写图像处理算法。它负责把数据送到合适的程序；接收后怎样计算，仍需要你用C++实现。正式跨程序传输时，一份按约定格式装好的数据称为**消息（message）**，可以理解成写好内容和格式的数据包。今天先练数据包到达后那一小段计算，不写通信API。

你要求学习的**SLAM（同时定位与建图）**，可以先理解为：机器人一边估计自己移动到哪里、朝向哪里，一边把不同位置看到的东西放到同一张环境图里。如果不知道自己怎样移动，两次看到的同一面墙就可能被放错位置。这说明“处理图像”只是起点，后面还需要运动与空间关系的知识。

今天用一张图练C++；接下来才会从一张图走到连续多张图、运动与地图。每天增加一个能连上的能力。

### 2. 一张图片为什么能放进你熟悉的vector

先不看彩色照片。**灰度图像（grayscale image）**只记录明暗；本课约定一个像素的亮度用0—255的整数表示：0黑、255白，中间值是不同程度的灰。像素就是图像中的一个小格子。

假设一张极小图只有一行四格：

```text
第0格   第1格   第2格   第3格
  0      20     120     250
 黑色    较暗    中间灰   较亮
```

这行图可以先用你已经会的`std::vector<int>`保存为{0,20,120,250}。真实图像有宽、高，可能还有颜色；今天先取一行，是为了把注意力放在数据如何交给函数，不是让四个数字冒充完整相机驱动。

现在回到DAY32：一个函数只观察这张原图，参数可以是`const std::vector<int>& pixels`。它直接读原数据，不复制整个容器，也不能通过pixels去改原图。

如果希望让图整体亮一点，同时保留原始图作对比，就让函数返回一份新容器。原图用const引用借给函数读，函数自己建立处理结果。这与昨天“修改副本”和“修改原容器”的区别完全接上了。

### 3. 先做一次真实的像素计算，再谈新语法

把每个像素亮度加20：

```text
原图：  [0, 20, 120, 250]
先加20：[20, 40, 140, 270]
合法图：[20, 40, 140, 255]
```

为什么最后一项要变255？因为本课约定的图像亮度上限是255。超过上限时保留255，用你会的if判断就能实现。

这就是一个简单的**亮度调整（brightness adjustment）**：对真实的像素含义进行运算。它可用于观察输入变化，但把黑图加亮并不能恢复本来没拍到的细节，也不能保证后面的定位更准。

OmniNxt并没有因此要求你在它的流程中统一加20。今天借这个可手算的小操作，练“读原图、产生结果、保存两份数据”；是否对真实系统采用某种预处理，要之后通过效果对照决定。

平均亮度也能手算：原图总和390，除以4得到97.5；处理后总和455，平均113.75。平均值只是一个观察量，不等于图像质量的完整评价。

### 4. 原图在函数里创建，函数结束之后还在吗

这里才需要今天的新概念。

**作用域（scope）**说明一个名字在哪段代码里可用；**生命周期（lifetime）**说明那个对象从创建到结束的时间。人话：名字能不能叫到，与数据是否还存在，不能混为一件事。

你可以在main里创建vector，把它用const引用传给处理函数。函数运行时，main里的vector仍在，所以函数能正常读它；函数里的参数名字离开函数后不再可用，但main里的原图没有因此被删掉。

反过来，若函数在自己内部建一个普通局部数组，只把首地址返回，函数结束时这个局部数组就结束了。外面即使拿着那个地址，也不能再读原来的格子。

**保存地址不等于延长数据寿命。** 你DAY31学会了“地址能找到数据”，现在要再问一句：“读它时，这份数据还存在吗？”

普通局部数组本课先按“离开所属代码块后结束”理解。下面暂不运行错误例子，直接用时间顺序判断：

```text
函数里创建一排临时像素 → 把地址记给外面 → 函数结束
                                             ↓
                                那排局部像素已不能继续访问
```

返回vector结果是另一种做法：调用者得到自己的结果容器，容器负责保存其元素，函数内部局部名字结束不妨碍返回结果继续使用。今天先按这个接口使用，具体拷贝与移动机制以后再讲。

### 5. 想在运行时申请一排格子：new[]与delete[]

你已经会固定数组`int pixels[4] = {};`。它的大小预先写在代码里。如果n是运行时读入的数量，可以使用**动态数组（dynamic array）**，即运行时按所需数量申请的一排存储格子。

一个两格的小例子，只演示申请、使用、释放，不是作业实现：

```cpp
#include <iostream>
int main() {
    int count = 2;
    int* pixels = new int[count]{};
    pixels[0] = 30;
    pixels[1] = 90;
    std::cout << pixels[0] << " " << pixels[1] << "\n";
    delete[] pixels;
    pixels = nullptr;
    return 0;
}
```

按顺序看，不用一次背完名词：

1. `new int[count]{}`申请count个int格子；{}让它们初始为0。它把第一格地址交回来。
2. `int* pixels`保存这个地址，是你昨天已经理解的指针。
3. pixels[i]照常访问第i格，但仍必须保证i在范围内。
4. `delete[] pixels;`表示这些格子用完了，释放整排存储。
5. 再把pixels设为nullptr，表示这个名字现在不保存可继续访问的地址。

这里有两件不同的东西：pixels这个局部指针变量，和new申请的那排像素。指针自己离开代码块，不会自动替你释放new申请的数据，所以谁申请、谁释放要安排清楚。

new[]申请数组就配delete[]。教材也有申请单个对象的new与delete；今天先把数组配对用熟，单对象写法作为同一机制的选读，不加作业。

用完后不释放，存储可能越积越多，叫**内存泄漏（memory leak）**，人话是借来的空间一直不归还。释放后仍读旧地址，叫**使用已释放数据**，相当于用已失效的房间号找东西。两者都不能靠“这次好像正常”判断正确。

n=0可以申请零长度数组并释放，但里面没有任何可访问元素；不要用pixels[0]当作“先取一个初值”。这正好补上你昨天空vector仍写values[0]的问题。

### 6. 为什么已经会vector，还要做这个小实验

new[]让你亲手看见“申请、使用、释放”三个阶段，帮助之后读懂源码中资源从哪里来、什么时候结束。

真正写今天第二个图像处理函数时，继续用vector：容器会管理自己的元素存储，正常离开作用域时清理，无须你对vector写delete[]。这使我们能把精力放在图像计算上。以后学构造、析构时，再解释对象怎样帮你自动完成这些工作。

因此今天两项实验是同一条线：先看清一份像素数据的寿命，再用熟悉的容器把数据处理写得更直接。

### 7. 两份练习：各自新增什么、怎样确认做好了

**02：按输入数量保存一张极小图像，使用后释放**

文件：`02_C++核心_图像缓冲区与生命周期.cpp`。

“缓冲区（buffer）”就是暂时存放数据的一片空间，本题是存像素的一排格子；不用把它想成新算法。

main先读取n（0—8），再读取n个0—255的整数像素。用new int[n]{}保存它们，计算平均亮度与严格小于50的像素个数；main结束前正确释放数组，并把指针清空。

输出三行：像素数量、平均亮度、较暗像素数量。没有像素时平均值约定输出-1，较暗数量0。平均值用double累计和相除，避免整数除法丢失小数。不要先读第0项再判断空图。

| 输入 | 三行结果 |
|---|---|
| 4 0 20 120 250 | 4；97.5；2 |
| 0 | 0；-1；0 |
| 2 50 255 | 2；152.5；0 |
| 1 0 | 1；0；1 |

三步由你自己写，不给循环或初值。写完解释：pixels本身存什么？new建出的数据何时结束？只写pixels=nullptr但漏掉释放，会发生什么？

**03：只读借用原图，返回变亮的副本**

文件：`03_C++应用_图像亮度与只读输入.cpp`。

main读取n（0—8）、n个0—255整数、delta（0—30）。用vector保存原图，自行实现：

`std::vector<int> brighten_copy(const std::vector<int>& pixels, int delta)`

函数读取原像素，对每项加delta，超过255时保留255；返回新vector，不修改原图。main输出三行：原图、新图、新图平均亮度。空图前两行为空行，第三行-1。函数不打印，main负责展示。

输入4 0 20 120 250 20，前两行为0 20 120 250和20 40 140 255，第三行113.75。再测0 20、2 250 255 30、2 0 255 0，检查空图安全、上限与delta=0。

本题不再手工申请或释放vector的元素。你可以复用昨天循环、const引用、返回容器的写法，自己新增的是像素计算与状态验证。不是要求照抄一份老师已经写好的图像程序。

编译仍用现有Clang：

```bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY33/02_C++核心_图像缓冲区与生命周期.cpp" -o /tmp/day33-image-buffer
/tmp/day33-image-buffer
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY33/03_C++应用_图像亮度与只读输入.cpp" -o /tmp/day33-image-copy
/tmp/day33-image-copy
```

若要排查越界，可以在同一编译命令增加`-fsanitize=address -g`。AddressSanitizer是随编译器使用的内存错误检测工具；人话是运行时帮助指出“哪一行读写了不该访问的存储”。需要时再用，不为了形式增加一套记录，也不在最终代码中故意保留错误。

### 8. 今天与ROS、OmniNxt究竟接上了哪一部分

今天的程序用终端输入模拟一张图的少量像素，建立“原数据→只读借给处理函数→产生可继续使用的结果”关系。以后把输入端换成ROS传来的真实图像，处理函数仍需要明确谁保存原数据、谁能修改、结果由谁持有。

今天还没有在两个独立运行的程序之间传消息，也没有从图像算出机器人位置。明天围绕“多张图怎样区分拍摄时间、宽高与来自哪台相机”学习结构体，再解释ROS程序怎样约定传递的数据。术语随着这个问题出现，不再先摆一堆名字让你猜关系。

更远的OmniNxt路线见阶段计划：先掌握小图像和坐标计算，再接真实ROS数据，之后进入相机几何、连续图像中的点移动、运动估计和多相机深度。每一步都要有你能手算和实现的对应任务。

## 四、模型：同样的下降方向，步长为什么会让结果反过来（65分钟）

教材接《神经网络与深度学习》2.2.3.1。继续复用你正确的fit，今天只改变学习率，确保三场实验从同样初始参数开始。

### 1. 数据决定当前梯度，学习率决定实际走多远

固定数据x=[-1,0,1,2]、y=[-1,1,3,5]，w=b=0时平均梯度(-3.5,-2)。三个学习率面对相同旧模型时，梯度相同，更新幅度不同：

| 学习率 | 第一步(w,b) | 初始损失 | 一步后损失 |
|---|---|---|---|
| 0 | (0,0) | 4.5 | 4.5 |
| 0.1 | (0.35,0.2) | 4.5 | 3.021875 |
| 2 | (7,4) | 4.5 | 30.75 |

**收敛**先理解为迭代逐渐接近稳定解；**发散**是这里误差在更新中持续放大。方向取自局部变化，步子太大会跨过合适位置，后一步再从另一侧跨得更远。

学习率0让参数冻结，损失不下降不代表梯度为0；学习率过大损失上升，也不立刻说明求导公式错了。用对照把“实现错误”和“超参数不合适”分开。

### 2. 用一个样本看清“过大”的数学含义

对单样本，旧误差e=wx+b-y，梯度是ex、e。更新后：

```text
w_new = w - α*e*x
b_new = b - α*e
e_new = w_new*x + b_new - y
      = e * [1 - α*(x²+1)]
L_new = L_old * [1 - α*(x²+1)]²
```

若e非零，要让这一个样本的损失严格下降，需要括号的绝对值小于1。α为正时得到0<α<2/(x²+1)。

例如x=2：α=0.1时括号0.5，损失变原来的1/4；α=1时括号-4，误差换方向且放大4倍，损失放大16倍。

这是单样本、当前半平方损失、w和b都更新时的结论，**不能把这个上界直接当成所有数据集与深层网络的通用学习率公式**。多样本意见平均后的曲面不同，今天用公平实验验证实际行为，不要求推矩阵特征值。

### 3. 公平对照为什么要重新创建模型

你DAY32的连续fit是在续训。今天要比较三个学习率，就必须给每场创建各自w=b=0的模型、优化器与Trainer；数据可以共享，因为不被修改。

如果先α=0.1训好，再在同一个已训模型上测试α=2，起点变了，就不能把差别只归因于学习率。记录loss序列时，history[t]仍表示该场更新t次后的损失。

今天固定每场20次，不把发散场跑到数字溢出再猜原因。给定数据的20步结果都可用有限浮点数表示，不需新库。

### 4. 实践与手算

文件：`04_模型实践_学习率对照实验.py`。

允许直接复用自己的模型、数据、损失、评估器、优化器、Trainer与fit；train方法名也可沿用。今天独立写实验组织与检查，不重新定义一组新架构。

- 先用独立模型α=0.1、初值(0,0)跑100步，补上DAY32规定的预测3、4与误差阈值验证；这一小段关闭训练任务的证据缺口。
- 三场对照α为0、0.1、2，均从(0,0)出发，固定20步，返回21条损失。
- 用已有字典把“学习率→该场损失列表”对应保存；每场打印初始、一步后、最终损失，以及最终参数。
- α=0：损失始终4.5、参数不动；α=0.1：末损失小于初值；α=2：第一步30.75，末损失大于初值且总体放大。
- 三场数据、初值、步数、损失定义完全一致，只改变学习率。不要为了让结果好看改标签或手工设w=2、b=1。
- 手算同一批旧梯度(-3.5,-2)配α=0.1和2时的第一步参数与损失，核对上表。说明损失不降至少可能是哪两类原因。

不安装绘图库；数字序列就是今天的观察材料。DAY34再接“训练数据上变好，未见数据是否也变好”，不因学习率实验同时铺开所有优化器。

## 五、今天怎样继续与保存

五项代码：349新题、88修正、图像动态数组、只读借用原图并调整亮度、模型学习率对照。自己的三步分析与必要运行结果保留；自建心得随意，不强制新建记录文件。

三个口述检查：349为何只留一次而88保留重复；图像数组由谁释放、没有像素时为什么不能读第0项；学习率对照为何需要独立模型。

DAY33进度检查结论：C++进入生命周期有实现基础，模型训练已实现，可以推进对照；Python88原地与耗尽边界仍需在今天复习位完成。DAY36再检查积压，未掌握项分别记，不用一个总分掩盖差异。

真实ROS图像通信在C++核心、构建和Linux环境齐备后接入。今天先做好一张图像数据的保存与处理，之后的概念都要说明它在这条链上解决了哪一个问题。OmniNxt的具体学习里程碑已写进阶段计划。

## 六、DAY32五题示范与逐题比较

下面给出全部参考。88先尝试修正，再按需展开；其余按疑问选读，不要求把已正确类和循环全部重抄。


<details>
<summary>00｜88：从预留空间末端写回nums1</summary>

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
for initial, m, other, expected in [
    ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], [1, 2, 2, 3, 5, 6]),
    ([1], 1, [], [1]),
    ([0], 0, [1], [1]),
    ([2, 4, 0, 0], 2, [1, 3], [1, 2, 3, 4]),
    ([0, 0], 1, [-1], [-1, 0]),
    ([2, 2, 0, 0], 2, [2, 2], [2, 2, 2, 2]),
]:
    values = initial.copy()
    saved_other = other.copy()
    returned = solver.merge(values, m, other, len(other))
    assert returned is None
    assert values == expected
    assert other == saved_other
```

与你相比，参考改成从大到小写末端，避免覆盖nums1未读取数据；没有额外result列表，也不return新列表。只要nums2还有数据就继续，nums1先用完时直接搬nums2；nums2先用完时，nums1剩下的前缀原本就在正确位置，无须再搬。

为什么写入安全：尚有nums2元素时，末端写位置在nums1当前未读最大项之后，或读取值来自nums2；填好一格后只移动对应来源和写位置。用[2,4,0,0]、[1,3]逐步跟一次，比背三个变量名更有用。

算法O(m+n)、O(1)。你的额外列表版可作为理解合并的草稿，但正式版需要同时修“第二组耗尽”和“写回原输入”两件事。

</details>

<details>
<summary>01｜977：你已修正确，参考仅省去平方前多余abs</summary>

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
    ([0], [0]),
]:
    values = original.copy()
    assert solver.sortedSquares(values) == expected
    assert values == original
```

abs(x)**2与x**2在本题整数范围内结果相同，你原写法没有计算错误。每轮恰好处理一项、正确停止，旧错误关闭；参考增加输入不变的断言，不因原测试少这一条重学整题。

</details>

<details>
<summary>02｜值与引用传递：保留你正确的两个函数</summary>

```cpp
#include <iostream>
#include <vector>
std::vector<int> shifted_copy(std::vector<int> values, int delta);
void shift_original(std::vector<int>& values, int delta);

int main() {
    int n;
    std::cin >> n;
    std::vector<int> values;
    for (int i = 0; i < n; ++i) {
        int value;
        std::cin >> value;
        values.push_back(value);
    }
    int delta;
    std::cin >> delta;
    std::vector<int> copied = shifted_copy(values, delta);
    for (int value : values) {
        std::cout << value << " ";
    }
    std::cout << "\n";
    for (int value : copied) {
        std::cout << value << " ";
    }
    std::cout << "\n";
    shift_original(values, delta);
    for (int value : values) {
        std::cout << value << " ";
    }
    std::cout << "\n";
    return 0;
}

std::vector<int> shifted_copy(std::vector<int> values, int delta) {
    for (int& value : values) {
        value += delta;
    }
    return values;
}
void shift_original(std::vector<int>& values, int delta) {
    for (int& value : values) {
        value += delta;
    }
}
```

你的函数逻辑与此一致。范围for里的int&保证修改容器元素，而不是修改元素副本；外层参数是否有&决定容器本身是哪一份。参考只合并了一次声明与赋值，并简化输入布局，不要求换成唯一模板。

</details>

<details>
<summary>03｜const统计：函数正确，去掉main里改变输入的试验行</summary>

```cpp
#include <iostream>
#include <vector>
int total_duration(const std::vector<int>& values);
int count_over(const std::vector<int>& values, int threshold);

int main() {
    int n;
    std::cin >> n;
    std::vector<int> values;
    for (int i = 0; i < n; ++i) {
        int value;
        std::cin >> value;
        values.push_back(value);
    }
    int threshold;
    std::cin >> threshold;
    std::cout << total_duration(values) << "\n";
    std::cout << count_over(values, threshold) << "\n";
    for (int value : values) {
        std::cout << value << " ";
    }
    std::cout << "\n";
    const std::vector<int> fixed = {2, 10, 15};
    std::cout << total_duration(fixed) << " " << count_over(fixed, 10) << "\n";
    return 0;
}
int total_duration(const std::vector<int>& values) {
    int total = 0;
    for (int value : values) {
        total += value;
    }
    return total;
}
int count_over(const std::vector<int>& values, int threshold) {
    int count = 0;
    for (int value : values) {
        if (value > threshold) {
            ++count;
        }
    }
    return count;
}
```

保留你的两个计算函数。main不再写values[0]=100，因此空容器不会触发那次访问、正常样例的总和也保持34。对空容器循环自然执行0次，返回0，不需要借助第0项计算。

如果想单独验证“外部普通名字仍可修改”，先确认非空后再做实验，并明确改后的期望结果。const引用的承诺不能覆盖调用方自己的其他写入，这一点与参数理解有关，不能误判为const失败。

</details>

<details>
<summary>04｜fit：保留你的train与fit设计，用独立初值核验指定实验</summary>

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
        model.weight -= g_w * self.learning_rate
        model.bias -= g_b * self.learning_rate
        

def batch_gradients(model,data):
    g_w,g_b=0,0
    for i in range(data.size()):
        single_xs,single_ys = data.get_item(i)
        g_w += (model.forward(single_xs) - single_ys) * single_xs
        g_b += (model.forward(single_xs) - single_ys) * 1
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

        mean_g_w,mean_g_b = batch_gradients(self.model,self.data)

        self.optimizer.step(self.model,mean_g_w,mean_g_b)

        new_loss = self.evaluator.evaluate(self.model)

        return new_loss

    def fit(self,steps):
        loss_list = []
        loss_list.append(self.evaluator.evaluate(self.model))
        for i in range(steps):
            loss = self.train()
            loss_list.append(loss)
        return loss_list

data = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
loss = SquaredLoss()

model = LinearNeuron(0, 0)
alias = model
trainer = Trainer(model, data, loss, GradientDescent(0.1))
history = trainer.fit(100)
assert len(history) == 101
assert abs(history[0] - 4.5) < 1e-9
assert history[-1] < 0.001
assert model is alias and trainer.model is model
assert abs(model.forward(3) - 7) < 0.01
assert abs(model.forward(4) - 9) < 0.01
print(history[0], history[-1], model.weight, model.bias)
print(model.forward(3), model.forward(4))

continued_model = LinearNeuron(0, 0)
continued = Trainer(continued_model, data, loss, GradientDescent(0.1))
first = continued.fit(10)
second = continued.fit(90)
assert len(first) == 11 and len(second) == 91
assert abs(first[-1] - second[0]) < 1e-9
assert abs(continued_model.weight - model.weight) < 1e-9
assert abs(continued_model.bias - model.bias) < 1e-9

parameters_before = (model.weight, model.bias)
zero_steps = trainer.fit(0)
assert len(zero_steps) == 1
assert parameters_before == (model.weight, model.bias)
assert abs(zero_steps[0] - history[-1]) < 1e-9
assert data.xs == [-1, 0, 1, 2] and data.ys == [-1, 1, 3, 5]

small_model = LinearNeuron(0, 0)
small_data = RegressionDataset([0, 1], [1, 3])
small_trainer = Trainer(small_model, small_data, loss, GradientDescent(0.1))
small_history = small_trainer.fit(2)
assert abs(small_model.weight - 0.2825) < 1e-9
assert abs(small_model.bias - 0.3725) < 1e-9
print("DAY32 fit与续训验证通过")
```

你的fit主体正确，这里原样保留。参考只删去SquaredLoss里不需要的最后样本缓存，主调用区改成“独立100步”与“独立10+90步”两组对照，并补预测与fit(0)断言。

train里old_loss当前没有用到，保留不影响数值，也可后续整理去掉。一个方法返回更新后损失、fit先记初值再追加每步结果，是自洽设计，不要求为了命名改回train_step。

</details>

### DAY32理论与实验示范回答

1. 88从后写利用预留位置，避免把nums1前方尚未读取的值覆盖。nums2耗尽时已有nums1前缀无须再搬；nums1耗尽时继续搬nums2。
2. 引用绑定后赋值是修改原对象的值，不是换绑定。const引用限制通过该访问路径写入，普通外部名字仍可合法修改原对象。
3. 普通函数适合一次计算；类用于保存跨调用状态与相关操作。batch_gradients用model与data足够，Trainer保存训练所需对象，fit复用它们。
4. fit(10)再fit(90)在同样数据、算法和学习率下继续当前参数，等价于一次fit(100)；每次fit返回的是自己的损失记录，不会自动重置模型。
5. DAY32手算：x=[0,1]、y=[1,3]、初始(0,0)，第一步平均梯度(-1.5,-2)，参数(0.15,0.2)，损失由2.5变1.915625；第二步梯度(-1.325,-1.725)，参数(0.2825,0.3725)，损失约1.4731953125。
6. 训练损失下降与未见样本正确要分开验证；本次人工数据确为线性关系，验证通过也不等于任意现实任务能泛化。

### 今日资料定位与来源

- [ROS 1基础讲义](../../学习资料/C++/ROS/1.1_机器人操作系统.pdf)：PDF9—12页，Master、节点、话题、消息。
- [ROS 1实验手册](../../学习资料/C++/ROS/1.2_机器人操作系统实验手册.pdf)：PDF1、4—9页的概念与消息组织；具体运行命令等环境课实际使用。
- [OmniNxt英文论文](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/OmniNxt.pdf)：本次核对第1页系统图、III节与III-D/III-E；今天只解释图像输入、估计运动和估计远近的关系，公式后续逐步教。
- [视觉SLAM十四讲第2版](../../学习资料/C++/ROS/视觉SLAM十四讲从理论到实践%20第2版%20(高翔,张涛).pdf)：作为后续按章学习的主参考，先从整体问题与三维运动需要的基础接入，不要求先读完整本。
- [C++ Primer Plus中文版](../../学习资料/C++/C++%20Primer%20Plus：中文版（第六版）%20(Stephen%20Prata).pdf)：4.7.4—4.7.6，书内102—105页，动态对象与释放。
- [神经网络与深度学习](../../学习资料/AI%20agent/神经网络与深度学习%20(邱锡鹏).pdf)：2.2.3.1，学习率与梯度下降。

以上是选章与概念改写，练习独立设计。你提供的[ROS中文Wiki](https://wiki.ros.org/cn)本次访问受限；后续用已提供的中文讲义与官方源码交叉核对，不要求为读懂今天课程自行翻陌生API。目标系统入口以[OmniNxt官方README](https://github.com/HKUST-Aerial-Robotics/OmniNxt)与其指向的D2SLAM源码为准，今天不通读整仓。

