# DAY35｜双指针专题②：位置与数值的奇偶；图像处理类；训练、验证和测试

> 2026-11-03。当前依据：[学习与授课总约定](../学习与授课总约定.md)、[阶段计划](../DAY29-DAY39_阶段计划.md)。约4小时，仍在Mac本地运行。
>
> **今天全部需要作答的理论题集中在[课后总结.md](课后总结.md)**，共6个短题，已留作答位置。课程正文负责讲解，不再让你在长文里寻找理论作业。DAY34没有单独列清理论题，不能算你漏交；你自建的《问答DAY34.md》已阅读并纳入反馈。

## 一、DAY34评阅：算法已经有迁移证据，主要补好测试判断

| 项目 | 实际验证 | 评语 |
|---|---|---|
| 905 | 原脚本第一组在断言处停止；单独核验方法，21,844组输入全部正确 | 算法与原地修改正确，错误在测试要求“修改后副本仍等于原列表” |
| 27 | 原脚本通过，13,120组输入核对k、有效前缀与整数返回均通过 | 能把读写角色用于不同条件，之前返回元组的缺口已修复 |
| C++02 | C++17编译无警告，100组合法帧输入输出通过，含空图 | struct字段、resize后下标写入、空图均值均正确 |
| C++03 | 100组两帧输入通过，原图保持、亮度上限与元信息正确；编译有一条int与size类型比较警告 | 核心计算正确，范围for可避免这条警告，不为格式停课 |
| 模型 | 干净/有误两组100步结果与课堂数值一致；额外核对评估重复调用和参数保持 | 数据分开、独立模型、统一留出评估正确；可继续数据用途与选择模型 |
| 学习反馈 | 已读《问答DAY34.md》全部八部分 | 有实际调试记录；下面纠正几条过度概括，保留你的原笔记 |

这说明你在算法上并非没有推进：27已经能使用905相同的读写关系并返回正确接口。测试用时与提示范围未记录，所以这里不把补测通过等同闭卷机试已经达标。

### 1. assert不会把“预计False”自动当成通过

你在排序后的副本上写了assert nums == nums_copy，旁边注释“False”。assert的含义是**要求条件为真，否则中断程序**；注释不会改变这个要求。

复制后、排序前，两个列表是不同对象但内容相等。排序后可能内容不等，也可能仍然相等：例如原本[2,4]已经符合要求，算法可以不改变内容。因此不能机械地把这条断言换成assert nums != nums_copy。

真正应检查的是：原输入若特意保留作基准就仍保持原值；被处理的那份列表元素及次数未丢；偶数整体在奇数前；方法返回的就是约定结果。文末参考给出相应测试。

**==比较内容，is比较是否同一个对象。** 两份不同列表完全可能相等；一个列表被重排后也仍是原来的那个对象。

### 2. 你的C++初始化与resize问题已经在代码中解决

在02里默认宽高10×10，pixels先建成100项；之后读入2×2，再resize(4)，长度会变4。改width不会自动让已经创建的pixels跟着变，这正是resize要单独执行的原因。

笔记里“vector必须圆括号、不能大括号”应改为“含义不同，要选对”：

- std::vector<int>(4,0)：4个0；
- std::vector<int>{4,0}：两个元素4和0；
- std::vector<int>{}：合法的空vector。

你已先resize再按下标输入，这样正确。若resize到4后再push_back输入4项，长度就会成8，前面4项原来已有的值不会自动被覆盖。

均值函数不需要先复制整份pixels；直接只读遍历即可。你当前复制仍算对，只是多用O(n)空间。times_stamp这个名字能在全文件保持一致就不影响计算，不因它不同于示范改判。

### 3. 另外两条笔记需要校准

范围for正在遍历一个vector时，再向同一个vector追加元素，会影响遍历所依赖的位置；可能重新分配，也可能使保存的结束位置失效。不要把“这次没有重新分配”当作一定安全。你提交的最终两帧代码没有这个问题，不把已修复尝试继续当错误。

“100步难以收敛，必须1000步”不适用于本次固定实验。你当前干净组100步已达到训练损失约8.41e-9；有误组的非零损失主要因为四个目标无法被同一直线全部满足，增加步数也不保证变0。先确认梯度与数据，再判断是否需要更多更新；旧笔记中曾把标签y写成x的问题在最终代码已修复。

共享optimizer也不自动算错：你目前GradientDescent只保存学习率，没有跨更新的额外历史，所以两组共享它仍得到正确结果。以后更新器若保存历史状态，比较独立实验就要另外检查。今天为调用关系清楚，各候选仍建立自己的更新器。

## 二、算法新题922精讲：沿同一个专题，先分清“位置”与“数值”（约35分钟）

[LeetCode922：按奇偶排序数组II](https://leetcode.com/problems/sort-array-by-parity-ii/description/)，简单。数组长度为偶数，偶数值和奇数值各占一半。要求偶数下标放偶数值、奇数下标放奇数值，返回任意合法结果。本课实现原地版本，O(n)时间、O(1)额外空间。

仍按昨天三步：输入输出→执行阶段→状态与检查。新题看完完整示范再关闭重写，复习905先自己完成。

### 第一步：输入输出，说清与905的区别

905要求“偶数整体在前”，922要求“偶数、奇数按位置交替”。[2,4,5,7]符合905，却不符合922：下标1是奇数位置，里面4却是偶数值。

**下标的奇偶与元素值的奇偶是两回事。** 例如下标2是偶数位置，nums[2]=5是奇数值，这一格就放错了。0号位置属于偶数位置。

[4,2,5,7]的一份合法结果是[4,5,2,7]。重复值保留，组内不要求数值排序。题目保证各占一半，今天不处理违反这一前提的输入。

### 第二步：从能做对的方法，走到两个位置的互补交换

直观办法：新建结果列表，用一个位置从0开始每次加2放偶数，用另一个从1开始每次加2放奇数。能做对，但需要额外列表。

想原地完成，就不必搬已经放对的格子。只找两类错误：

- 某个偶数位置里放了奇数值；
- 某个奇数位置里放了偶数值。

把这两个值交换，两个位置同时修好。为什么能找到对应错误？因为题目保证奇偶值各占一半；一个偶数位置被奇数占用，就会有另一个奇数位置被偶数占用。

它与905共享“给下标明确职责，修好一个范围就向前推进”。但922的两个下标分别负责两类位置，不再是普通read/write，不能只把905条件换一下就照抄。

### 第三步：状态、推进与停止，逐轮看

even从0开始，负责检查0、2、4……；odd从1开始，负责检查1、3、5……。每次加2，就是只访问自己负责的那类位置。

| 条件 | 说明 | 动作 |
|---|---|---|
| nums[even]已经是偶数 | 这一个偶数位置不用改 | even加2 |
| 否则，nums[odd]已经是奇数 | 这一个奇数位置不用改 | odd加2 |
| 否则 | 两边位置都放错，正好互补 | 交换两项，两个下标各加2 |

while同时保证even和odd仍在范围内，再读取元素，避免先读越界再判断。

用[4,2,5,7]：

1. even=0，值4放对，even到2；
2. even=2值5放错，odd=1值2也放错，交换成[4,5,2,7]；
3. even到4、odd到3，even已到边界，结束。

这里even一侧全部排好后，剩余奇数位置也必须正确，否则偶数值的总数就与题目前提矛盾。另一侧先结束同理。不是凭“看起来差不多”提前停。

**完整参考：**
```python
class Solution:
    def sortArrayByParityII(self, nums):
        even = 0
        odd = 1
        while even < len(nums) and odd < len(nums):
            if nums[even] % 2 == 0:
                even += 2
            elif nums[odd] % 2 == 1:
                odd += 2
            else:
                nums[even], nums[odd] = nums[odd], nums[even]
                even += 2
                odd += 2
        return nums
```

每次推进的是已经确认正确的位置；各下标只向前，每个位置检查常数次。相同奇偶值不需要特判成多次写入，交换后一次推进两侧是因为真的同时修好了两格。

文件：`00_Python精讲重写_LeetCode922_按奇偶位置排列.py`。看完后关闭答案重写，检查[4,2,5,7]、[2,3]、[3,2]、[0,1,2,3]、[2,0,3,1]、[2,2,1,1]。先核对元素次数，再逐项检查nums[i]%2==i%2，不与某一个完整排列硬比。

## 三、算法复习905：独立练原来的读写位置（约20分钟＋检查10分钟）

文件：`01_Python专题复习_LeetCode905_按奇偶排序.py`。

原地把偶数整体移到奇数前，返回列表。输入[3,1,2,4]可以得到[2,4,3,1]，但没有要求偶数必须放在偶数下标。目标O(n)、O(1)。

先关闭昨日代码和本课文末参考，自己简述读写职责并实现。测试[3,1,2,4]、[2,4]、[1,3]、[0]、[2,1,2,1]。特别检查：已经符合条件的列表，不改变内容也是合法答案。

卡住10分钟可看这句提示：读位置检查每项，写位置只在放入一个偶数后推进。约20分钟仍卡住就对照905示范，再关闭重写，不取消今天922学习。

两个题的规律对照：905维护“偶数前缀”，922维护“已经正确的偶数位置、奇数位置”；变量职责变了，推进步长也跟着变，不能把所有双指针都背成同一个循环。

## 四、C++与图像：从一份帧记录，到一个会持续工作的处理器（100分钟）

继续昨天的ImageFrame，不重新从像素开始。帧记录说明“这一张图是什么”，普通函数处理“这一次的图”。现在相机持续送图，我们希望同一个处理器记住亮度增量与已经处理的帧数，这才有了使用类保存状态的实际理由。

### 1. 类、对象与方法怎样接到已有代码

**类（class）**描述一种对象应保存哪些数据、提供哪些操作；**对象（object）**是按这个类型创建的具体实例；**成员函数/方法（member function/method）**是通过对象调用的操作。你Python里的模型和Trainer已在做同一件事。

小例子只计处理次数，展示语法，不是作业完整实现：

```cpp
#include <iostream>
class FrameCounter {
private:
    int count_ = 0;

public:
    void record() {
        this->count_ += 1;
    }

    int count() const {
        return this->count_;
    }
};

int main() {
    FrameCounter first;
    FrameCounter second;
    first.record();
    first.record();
    second.record();
    std::cout << first.count() << " " << second.count() << "\n";
    return 0;
}
```

输出2 1。两份对象分别有自己的count_，调用first.record不会增加second那一份。count_末尾下划线只是命名习惯，不是新运算符。

### 2. public/private解决的是怎样正确使用对象

**public**表示外部可以通过这个名字使用；**private**表示外部不能直接访问，只能由类的成员操作。人话：让调用者使用规定的按钮，不随意改内部计数和配置。

例子中main可以调用first.record()，但不能写first.count_=999。不是数据神秘消失，而是编译器按访问约定限制直接操作。

**封装（encapsulation）**在这里就是把状态与相关操作放在一起，并规定外面怎样使用。本课处理器应通过方法设置0—30的亮度增量；输入31时拒绝并保持原配置，避免外部绕开检查。

struct和class都能包含数据与方法，主要语法区别之一是默认访问权限：struct默认public，class默认private。不是“struct只能放数据、class才能写函数”；我们当前用struct保存帧，用class管理持续处理状态，方便分工。

### 3. this是什么，为什么不用像Python那样手写self参数

调用first.record()时，**this指针**指向当前这一个first对象。this->count_访问这个对象的成员。箭头`->`用来通过对象指针访问成员，this->count_与(*this).count_在这里等价；日常只需读懂前一种。

Python方法把self写在参数列表里；C++普通成员函数的当前对象通过this隐含提供，不用写成record(self)。record里直接写count_，在本例也表示当前对象的成员。

所以this不是“全班所有对象共用一个状态”。先找到调用句中的对象，再解释方法里的this，和解释Python的self一样。

count()末尾的const表示这个成员函数不修改普通成员状态，给“读计数”一个只读约定；record会修改计数，不能也按此写成只读。它与const ImageFrame&参数限制输入修改有关联，但所在位置和约束对象不同。

今天的方法直接写在class内部，省去多文件与作用域写法。构造、初始化列表和析构明天再讲，不一起堆进本课。

### 4. 旧的图像处理函数继续复用

保留你已经写对的ImageFrame、mean_brightness、brighten_copy、brighten_frame。处理器的方法只需调用已有brighten_frame，并更新自己的计数；不要为“用类”把原来的正确亮度循环又写一份。

ImageFrame负责一帧的内容；BrightnessProcessor负责跨多帧持续使用的配置和计数。处理器不是图像本身，delta不是相机的拍摄时刻。

bool用来表达真或假，C++写true/false。下面configure成功返回true，失败返回false；cout打印时默认显示1或0。

### 5. 两项相连实践，约45分钟手敲＋10分钟检查

**02：一个处理器保存配置与次数**

文件：`02_C++核心_图像处理类与封装.cpp`。

自行写BrightnessProcessor，私有保存亮度增量delta_与处理次数count_，默认均为0。提供这些公开接口：

| 接口 | 行为 |
|---|---|
| bool configure(int delta) | 0—30时保存并返回true；否则返回false，旧配置和计数不变 |
| int delta() const | 返回当前增量 |
| int count() const | 返回处理次数 |
| ImageFrame process(const ImageFrame& source) | 返回按当前增量处理的新帧；输入不改，次数加1 |

空帧也算接收并处理了一次请求，因此count也加1；只是结果仍为空，均值-1。configure不清零计数，也不处理图像。

main读取一帧（camera_id、timestamp、width、height，再读width×height像素），再读合法delta。用同一个处理器对同一原帧连续process两次，结果都从原帧出发，不是在第一次结果上再加亮。

输出五行：configure结果；当前增量和计数；原均值和第二次结果均值；第二次结果像素；尝试configure(31)后的返回值和仍保存的增量。

输入0 1.0 2 2 0 20 120 250 20，五行应为：
```text
1
20 2
97.5 113.75
20 40 140 255
0 20
```
空帧0 1.0 0 0 20：原/新均值都-1，像素行空，处理次数仍2。自行检查原帧的编号、时刻、宽高、像素未被修改。

**03：两份对象的状态各归各**

文件：`03_C++应用_双处理器与连续帧.cpp`。

直接复用02已经写对的类与旧函数，不重复发明另一套接口。main读两帧，然后读deltaA、deltaB（都0—30）。创建A与B，分别配置；A处理第一帧，B也处理同一第一帧，随后只有A处理第二帧。

输出四行：

1. A增量、A次数、B增量、B次数；
2. 第一原帧均值、A的第一结果均值、B的第一结果均值；
3. A第二结果的相机编号、时刻、平均亮度；
4. 第一原帧像素，验证输入保留。

输入：
```text
0 1.0 2 2 0 20 120 250
1 1.5 0 0
20 0
```
四行分别为20 2 0 1、97.5 113.75 97.5、1 1.5 -1、0 20 120 250。再测非空第二帧与deltaA=deltaB，结果可能相同，但两对象仍各自计数，不因为输出相同就成同一个对象。

```bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY35/02_C++核心_图像处理类与封装.cpp" -o /tmp/day35-processor
/tmp/day35-processor
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY35/03_C++应用_双处理器与连续帧.cpp" -o /tmp/day35-processors
/tmp/day35-processors
```

今天相当于为未来每次收到图像后要调用的处理功能建立对象状态，还没有接真实ROS通信。二维位置估计放到后续空间计算，不为了追表格日期额外开一套新状态。

## 五、模型：同样是留出数据，验证集与测试集为什么分工不同（65分钟）

教材沿2.5理解学习类型，结合已学2.2.3.2补训练/验证/测试边界。今天继续用线性神经元，不新增神经网络层。

### 1. 你现在做的是哪种学习

**监督学习（supervised learning）**是训练时有输入x与目标标签y，利用预测与标签之间的差学习关系。你当前的线性回归输出一个数，属于监督学习中的回归；“识别图中是哪类物体”则是输出类别的分类。分类模型后面才实现，不因为知道名字就算会了。

没有给目标标签、从数据寻找结构，属于另一类无监督学习；通过行动、反馈奖励学习行为属于强化学习。今天只需知道它们与当前成对(x,y)任务的区别，不增加三套算法。

### 2. 昨天的留出集已经做对，今天再分清“选择”和“最终报告”

训练集参与求梯度和改参数。昨天你把data_test只传给LossEvaluator，没有送进Trainer，这个边界正确。

现在要从学习率0、0.1两种候选里挑一个。如果用某份数据的误差做选择，那份数据就在承担**验证集（validation set）**职责。选定之后，另外保留一份**测试集（test set）**，只用于最终评价。

人话：训练是练习，验证帮助选择练法，测试留到决定完成后检查。名字写成data_test并不能自动保证它没被用于选择，关键看代码怎样使用它。

如果看了测试误差，再反复选择学习率、步数或模型，就相当于把测试集也拿来指导决定；即使没有直接对它求梯度，最终成绩也不再是完全独立的评价。

### 3. 接到你已有的对象，哪里传哪份数据

- Trainer接训练数据，更新模型；
- 每个候选训练完，用验证数据的LossEvaluator评价，选较小验证损失；
- 选完只把选中模型交给测试数据的LossEvaluator；
- evaluate仍不得修改模型、数据或学习率。

验证可以影响最终选择，不能把这说成“验证集完全不影响模型决策”；它影响的是选择哪一个候选，不直接参与本课的梯度更新。测试集保留到最后。

### 4. 独立实践（约25分钟）

文件：`04_模型实践_训练验证测试分工.py`。

复用已正确的六类与batch_gradient，建立：

- 训练：x=[-1,0,1,2]，y=[-1,1,3,5]；
- 验证：x=[-2,3]，y=[-3,7]；
- 测试：x=[4,5]，y=[9,11]。

候选学习率为0与0.1，都用各自w=b=0的模型、各自更新器，训练100步。记录训练前后损失、验证损失；根据验证损失选择候选，最后只报告选中模型的测试损失与两项预测。

可以用已会字典分别保存“学习率→模型”和“学习率→验证损失”，不用未教的自动选参库。比较两个数后保存best_rate即可，测试数据不参加这次比较。

预期：学习率0的模型不动，验证损失14.5；0.1组验证损失约2.52e-8，应选0.1；最终预测4、5分别接近9、11，绝对误差各小于0.01。评估前后保存参数并对比，确认没有被评价改动。

本实验人工数据非常简单，重在组织正确的数据路径，不据此证明某个学习率对所有问题最佳。理论题中的小手算也放在独立总结文件，不再藏在这段实践要求里。

## 六、今天要交什么

两道算法、两份C++、一份模型代码；理论题在[课后总结.md](课后总结.md)直接作答。完整旧题示范在后面，新题922精讲在正文，练习文件都留白。

时间仍为Python65、C++100、模型65、反馈保存10分钟；理论短答计入相应模块检查和最后整理，不额外追加一小时。保留真实卡点和参考范围即可。

## 七、DAY34五份示范答案与逐题比较

已正确的算法与类不要求全部重抄；以下参考主要修905的测试、简化图像记录，并完整展示原模型实验。原代码与自建问答笔记保持不动。


<details>
<summary>00｜905：方法保留，测试分别检查身份、内容与分区</summary>

```python
class Solution:
    def sortArrayByParity(self, nums):
        write = 0
        for read in range(len(nums)):
            if nums[read] % 2 == 0:
                nums[write], nums[read] = nums[read], nums[write]
                write += 1
        return nums

solver = Solution()
for original in [[3, 1, 2, 4], [0], [1, 3, 5], [2, 4, 6], [2, 1, 2, 1]]:
    saved = original.copy()
    working = original.copy()
    assert working == original
    assert working is not original

    result = solver.sortArrayByParity(working)
    assert result is working
    assert original == saved
    assert sorted(result) == sorted(saved)
    seen_odd = False
    for value in result:
        if value % 2 == 1:
            seen_odd = True
        else:
            assert not seen_odd
```

方法与你一致。原脚本在第一组assert original==working失败，不代表方法错误；参考把测试改成验证真正需要的性质。sorted在这里仅是教师测试对照，不属于O(n)算法。

当原输入已经满足分区时，working可能内容没变。is检查同一对象不要求值改变，==检查值不要求同一对象；这两句话可以用今天独立理论题的小例子验证。

</details>

<details>
<summary>01｜27：你的返回与状态已正确，参考增加有效前缀检查</summary>

```python
class Solution:
    def removeElement(self, nums, val):
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write], nums[read] = nums[read], nums[write]
                write += 1
        return write

solver = Solution()
for original, val, expected in [
    ([4, 1, 4, 2, 1], 4, [1, 2, 1]),
    ([2, 2], 2, []),
    ([], 0, []),
    ([1, 1, 3], 2, [1, 1, 3]),
]:
    values = original.copy()
    k = solver.removeElement(values, val)
    assert isinstance(k, int)
    assert k == len(expected)
    assert values[:k] == expected
```

核心与你相同，O(n)时间、O(1)额外空间。你原测试主要核对返回长度；参考同时看保留内容，避免长度正确但元素错误。注释里“等于4交换”与最终代码!=val不一致，改注释即可，不因此否定正确实现。

</details>

<details>
<summary>02｜结构体图像帧：数据计算正确，参考去掉多余副本</summary>

```cpp
#include <iostream>
#include <vector>

struct ImageFrame {
    int camera_id = 0;
    double timestamp = 0.0;
    int width = 0;
    int height = 0;
    std::vector<int> pixels;
};

double mean_brightness(const ImageFrame& frame) {
    if (frame.pixels.empty()) {
        return -1;
    }
    double total = 0;
    for (int pixel : frame.pixels) {
        total += pixel;
    }
    return total / frame.pixels.size();
}

int main() {
    ImageFrame frame;
    std::cin >> frame.camera_id >> frame.timestamp >> frame.width >> frame.height;
    frame.pixels.resize(frame.width * frame.height);
    for (int& pixel : frame.pixels) {
        std::cin >> pixel;
    }

    std::cout << frame.camera_id << " " << frame.timestamp << " "
              << frame.width << " " << frame.height << "\n";
    std::cout << frame.pixels.size() << " " << mean_brightness(frame) << "\n";
    for (int pixel : frame.pixels) {
        std::cout << pixel << " ";
    }
    std::cout << "\n";
    return 0;
}
```

你的times_stamp命名合法，参考只统一timestamp。默认宽高先设0、像素为空，读入后再resize，不必先创建100格。你先复制copy_image_frame但后来没用，可整理去掉；它在读入之前形成，不会自动随原记录后面的输入变化。

你的均值函数先复制pixels再统计，结果正确；参考直接只读遍历，避免额外空间。空图返回-1的旧缺口已经修好。直接包含<vector>更清楚，不依赖iostream间接带入。

</details>

<details>
<summary>03｜两帧处理：你逐项复制元信息与返回新像素都正确</summary>

```cpp
#include <iostream>
#include <vector>

struct ImageFrame {
    int camera_id = 0;
    double timestamp = 0.0;
    int width = 0;
    int height = 0;
    std::vector<int> pixels;
};

double mean_brightness(const ImageFrame& frame) {
    if (frame.pixels.empty()) {
        return -1;
    }
    double total = 0;
    for (int pixel : frame.pixels) {
        total += pixel;
    }
    return total / frame.pixels.size();
}

std::vector<int> brighten_copy(std::vector<int> pixels, int delta) {
    for (int& pixel : pixels) {
        pixel += delta;
        if (pixel > 255) {
            pixel = 255;
        }
    }
    return pixels;
}

ImageFrame brighten_frame(const ImageFrame& source, int delta) {
    ImageFrame result = source;
    result.pixels = brighten_copy(source.pixels, delta);
    return result;
}

int main() {
    std::vector<ImageFrame> frames(2);
    for (ImageFrame& frame : frames) {
        std::cin >> frame.camera_id >> frame.timestamp >> frame.width >> frame.height;
        frame.pixels.resize(frame.width * frame.height);
        for (int& pixel : frame.pixels) {
            std::cin >> pixel;
        }
    }
    int delta;
    std::cin >> delta;

    for (const ImageFrame& frame : frames) {
        ImageFrame result = brighten_frame(frame, delta);
        std::cout << frame.camera_id << " " << frame.timestamp << " "
                  << mean_brightness(frame) << " " << mean_brightness(result) << "\n";
        for (int pixel : frame.pixels) {
            std::cout << pixel << " ";
        }
        std::cout << "\n";
        for (int pixel : result.pixels) {
            std::cout << pixel << " ";
        }
        std::cout << "\n";
    }
    return 0;
}
```

你的brighten_copy按值接收vector，修改本地副本再返回，正确；不强迫一定改成const引用加内部副本。逐项写camera_id、时刻、宽高也正确，参考用已有值语义整体复制，少写几行。

把下标循环改为范围for不是修算法，只是避免int与size()的有符号/无符号比较警告。对int小值只读时复制一个整数足够，不必把const int&当成所有场景都唯一更好的写法；只读大型ImageFrame时const引用更有意义。

</details>

<details>
<summary>04｜训练与留出误差：你的计算与数据路径已正确</summary>

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
        mean_loss = self.loss.mean(predictions,self.data.ys)

        return mean_loss

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

loss = SquaredLoss()
held_out = RegressionDataset([-2, 3], [-3, 7])
held_evaluator = LossEvaluator(held_out, loss)

for name, labels in [
    ("clean", [-1, 1, 3, 5]),
    ("dirty", [-1, 1, 3, 11]),
]:
    model = LinearNeuron(0, 0)
    train_data = RegressionDataset([-1, 0, 1, 2], labels.copy())
    trainer = Trainer(model, train_data, loss, GradientDescent(0.1))
    history = trainer.fit(100)

    before = (model.weight, model.bias)
    held_loss = held_evaluator.evaluate(model)
    repeated = held_evaluator.evaluate(model)
    assert before == (model.weight, model.bias)
    assert held_loss == repeated
    assert held_out.xs == [-2, 3] and held_out.ys == [-3, 7]
    assert train_data.ys == labels

    print(name, history[0], history[-1], model.weight, model.bias,
          held_loss, model.forward(3))
    if name == "clean":
        assert held_loss < 0.001
        assert abs(model.forward(3) - 7) < 0.01
    else:
        assert held_loss > 10

print("DAY34训练与留出评估验证通过")
```

六类与batch_gradient沿用你的计算。你的两组分别建立model、Trainer，留出数据只评估，结果已正确。参考用循环减少重复、增加评估参数保持与数据不变核对，并补x=3预测；当前共享纯学习率更新器的写法不算错。

原笔记中曾有梯度把y写成x的错误，最终代码已经改对。教师不会继续据旧尝试判当前梯度错误。干净组100步已达阈值，有误组继续训练不保证变0，两组差别来自训练目标，不是统一加到1000步就能消除。

</details>

### DAY34理论示范与笔记对照

DAY34没有独立题单，下面作为解释与参考，不追溯算漏交：

- 905与27都能维护读位置和有效前缀；905要保留全部奇数，交换可同时保存它们；27只检查非val前缀，返回整数k。
- 默认宽高只参与对象创建时的像素初始化，随后改变宽高不会自动重建vector。resize改变元素个数，push_back在现有末尾新增一项。
- const输入不能通过非常量引用修改其元素；先形成可修改副本再处理合法。struct可有方法，class也可含公开数据，但本课程用它们分别组织记录与受控状态。
- 测试只要内容相同就可能==为真，无论是否同一对象；.copy()形成新列表，浅拷贝并不意味着所有层级的子对象都独立。当前仅含整数的列表可按本例验证。
- w=2、b=1、x=2时预测5。标签5对应半平方损失0、两个梯度0；标签错误为11时误差-6、损失18，w梯度-12、b梯度-6。这说明数据标签会改变更新方向。
- 数据改变使参数改变、留出表现变差，不能仅凭这一组实验正式估计偏差方差，也不能只看训练损失就宣称泛化可靠。

### 本课教材定位

- [922官方题目](https://leetcode.com/problems/sort-array-by-parity-ii/description/)：长度为偶数、奇偶值各半及下标要求。
- [C++ Primer Plus中文版](../../学习资料/C++/C++%20Primer%20Plus：中文版（第六版）%20(Stephen%20Prata).pdf)：10.2相关段落书内343—344、347页；10.4书内363—364页。今天只用访问权限、成员函数、只读方法与this，构造/析构下一课接入。
- [神经网络与深度学习](../../学习资料/AI%20agent/神经网络与深度学习%20(邱锡鹏).pdf)：2.5书内41页，结合2.2.3.2书内30页的验证集用途。不逐条堆学习算法名字，用当前已有模型说明数据路径。


