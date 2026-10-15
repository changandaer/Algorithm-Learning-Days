# DAY29｜按条件保留元素、组织C++函数、第一次真正更新模型参数

> 当前阶段：[DAY29—DAY39阶段计划](../DAY29-DAY39_阶段计划.md)。规则：[学习与授课总约定](../学习与授课总约定.md)。今天约4小时，只用Mac本地Python与C++17，不安装新工具。
>
> 今天五个代码文件保持留白。你自己写三步分析，不写TODO；旧题先闭卷，新题先独立尝试。文末DAY28答案按需查看，不需要全部抄写。**今天的新题与新功能没有预填实现。**

## 一、承接DAY28：通过的继续前进，缺口放进真实任务

DAY28已有补测结论：704、121计算正确；C++统计程序与副本实验计算正确；四个模型类及调用正确。详细测试范围与逐题比较沿用[DAY28评阅](../DAY28/DAY28_课程与作业.md#day28-review)，不把历史补测说成今天重新跑过，也不把补测通过当作限时独立能力的证明。

今天只接住两个有实际意义的缺口：

- C++：筛选函数到底返回“数据”还是“数量＋数据”，需要固定下来。今天用函数接口、返回值与调用者职责解释，不为此重学循环。
- 模型：重新创建一个参数不同的模型，不等于更新原来的模型。今天让更新器真正改变原实例的参数，用更新前后的损失验证。

偏导手算与完整训练的证据仍待补齐。今天只做单样本一步更新；平均梯度在DAY30，训练器在DAY31，100次训练在DAY32。不提前堆在今天。

| 顺序 | 时间 | 完成什么 |
|---|---:|---|
| Python | 65分钟 | 26闭卷复习15分钟；27理论与实现40分钟；测试与解释10分钟 |
| C++ | 100分钟 | 理论45分钟；两项相连实践45分钟；编译检查10分钟 |
| 模型与数学 | 65分钟 | 连贯理论30分钟；手算10分钟；模型更新实践25分钟 |
| 反馈与保存 | 10分钟 | 留一个真实卡点、运行结果、保存代码；Git由你提交 |

如果超时，先减少重复测试和选读，不取消整块新内容。阅读量增加是为了讲透机制，不要求背下所有文字。

## 二、Python：从“只保留不同值”到“只保留符合条件的值”

### 1. 先闭卷复习26，15分钟

文件：`01_Python复习_LeetCode26_有序数组去重.py`。

[26：删除有序数组中的重复项](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/)。输入已经非递减排序，原地修改，让前k项为按原顺序排列的不重复元素，返回整数k。题目输入非空；今天不额外增加空输入要求。

| 原输入 | k | 修改后前k项 |
|---|---:|---|
| [0,0,2,2,5] | 3 | [0,2,5] |
| [7] | 1 | [7] |
| [3,3,3] | 1 | [3] |
| [-2,-2,0,4,4] | 3 | [-2,0,4] |

先自己写三步和代码，解释读位置与有效部分的关系。目标O(n)时间、O(1)额外空间。若卡住，记录卡在哪里，先进入新课；今天不因为一题遗忘整天停课。

### 2. 27究竟要解决什么问题

新题：[27：移除元素](https://leetcode.cn/problems/remove-element/)，简单。接口：`Solution.removeElement(self, nums, val)`。

给你一个列表和一个要排除的值val，把所有不等于val的元素放到原列表的前k个位置，并返回k。**列表不保证有序，允许改变剩余元素的顺序，不要求真的缩短列表。** 官方只检查k和前k项内容；后面的内容不算答案。

想象把一批耗时测量放在一排格子里，某个特定值代表无效记录。你需要留下有效记录，而不是消除相同的有效记录。

例如原数据为[4,1,4,2,1]，排除4：

- 两个4都不要；
- 两个1都要，因为它们是两条有效记录，不是要去重；
- k为3，前3项可以是[1,2,1]，也可以是[1,1,2]。

今天为了容易解释，可以采用保持原顺序的方法；**这不是官方对27的额外要求**。和26相比，最关键的变化不是循环语法，而是“什么元素值得留下”。

| 比较点 | 26 | 27 |
|---|---|---|
| 输入有序吗 | 是 | 不保证 |
| 保留条件 | 相同值只留一次 | 值不等于val |
| 非val的重复项 | 不适用这个规则 | 每一次出现都要保留 |
| 返回值 | 有效长度k | 有效长度k |
| 是否必须缩短列表 | 否 | 否 |

### 3. “原地”和“有效部分”到底是什么意思

**原地修改（in-place）**：在原来那份存储上修改。人话：在原来的纸上改，不是另写一张纸却只把自己的标签贴到新纸上。

已有语法的小对照：

```python
numbers = [8, 3, 8]
other_name = numbers
numbers[1] = 6
print(other_name)  # [8, 6, 8]：看到的是同一份列表
```

修改下标改变原列表。相反，在函数里只写`nums = another_list`，只是让局部名字改指向另一个列表，不会让调用者原来的列表自动变成答案。

**有效前缀（valid prefix）**：列表开头连续的、已经被认定有用的部分。人话：只有前k格交作业，后面不用擦干净。例如[1,2,1,2,1]配合k=3，答案只取前3格。

这意味着你不必不断删除元素，也不必费力把尾部填成0。反复从列表中间删除会移动后面的元素，最坏可能花O(n²)时间；使用少量位置状态，一次扫描就能做到O(n)。

今天不给完整循环和预填三步。你需要自己回答：查看一个元素后，什么情况下它应该进入有效部分？有效长度如何反映已经保留的个数？如果一个位置只被覆盖而没有删除，是否影响尚未处理的数据？

### 4. 新题实践与验收

文件：`00_Python新题_LeetCode27_移除元素.py`。

目标：O(n)时间、O(1)额外空间；不用新列表存全部答案。自写三步、平台方法、本地调用和测试。

| 原nums | val | 返回k | 前k项应包含 |
|---|---:|---:|---|
| [] | 7 | 0 | [] |
| [4,1,4,2,1] | 4 | 3 | 两个1、一个2 |
| [2,2] | 2 | 0 | [] |
| [1,1,3] | 2 | 3 | 两个1、一个3 |
| [5] | 5 | 0 | [] |
| [5] | 0 | 1 | [5] |

测试时保存方法返回的k，再看调用后的`nums[:k]`。切片用于观察测试结果，不要为了生成答案而额外复制整个输入。27允许顺序改变，所以不能只因前缀顺序不同判错；也不能只比较集合，因为集合会掩盖重复项丢失。

写完后口述：为什么返回的是整数，而不是列表？为什么看整个修改后的列表可能误判正确程序？

若仍有余力，用一分钟口述1047中“栈顶和当前字符相同”意味着什么，不另写第六份作业。

## 三、C++：函数不是把代码包起来，而是规定如何合作

教材对应[《C++ Primer Plus》中文版第六版](../../学习资料/C++/C++%20Primer%20Plus：中文版（第六版）%20(Stephen%20Prata).pdf)第7章7.1.2、7.2，第8章8.3、8.4；书内页205、207、274—278附近（PDF页码比书内页多18页）。今天不引入引用、指针、类或平台Solution外壳。

### 1. 先解决你已有程序的实际问题

DAY28的一个筛选函数返回“数量＋筛选结果”，另一个同名函数只返回“筛选结果”。两个程序可以各自算对，但调用者必须记住两套含义。

**函数接口（interface）**指别人使用函数时需要知道的输入、输出和约定。人话：这个小工具吃什么，交出什么，谁负责展示结果。

对耗时筛选统一成：

- 输入：一组耗时、阈值；
- 返回：所有严格超过阈值的耗时组成的新vector；
- 不往结果里塞数量，不负责打印；
- 调用者需要数量，就读取返回容器的size()；需要总耗时，就调用相应计算函数。

为什么把计算和打印分开？屏幕上的文字不能直接当作下一步计算的数据。返回的数据可以继续统计、测试，之后也可以写报告。你不是为了“代码好看”拆函数，而是为了让计算结果能被继续使用。

### 2. 声明、定义、调用：三件不同的事

**函数声明／原型（declaration/prototype）**告诉编译器：有这个函数，叫什么，收什么类型，返回什么类型。

**函数定义（definition）**给出函数体，说明具体怎么做。

**函数调用（call）**才让程序执行它。只有定义不会自动运行函数。

下面是独立小例子，不是今天筛选题的答案：

```cpp
#include <iostream>

double add_fee(double price, double fee);  // 声明，以分号结束

int main() {
    double price = 8.0;
    double result = add_fee(price, 0.5);  // 调用
    std::cout << result << "\n";
    std::cout << price << "\n";
    return 0;
}

double add_fee(double price, double fee) {  // 定义，有函数体
    double total = price + fee;
    return total;
}
```

输出8.5和8。编译器处理到main里的调用时，前面的声明已告诉它怎样检查参数与返回类型；后面的定义提供实际计算。将定义直接放在main之前也合法，但今天特意练习“声明在前、main居中、定义在后”，为以后的多文件程序做准备。

声明与定义要对应。同一个函数声明收两个double，定义却写成另一个参数列表，不是在“补完原函数”；可能变成另一个重载，导致原函数缺少定义。只声明却没有提供被调用函数的定义，通常到链接阶段会报错。今天仍是单文件，不需要学习新的构建工具。

### 3. 参数、返回值、局部变量怎样流动

**实参（argument）**：调用时交进去的值，例如price和0.5。
**形参（parameter）**：函数定义中接收值的名字，例如函数自己的price、fee。

例子中main的price与add_fee的price不是同一个变量，只是同名。今天的参数写法是**值传递（pass by value）**，用传入值初始化函数自己的参数。

人话：交给函数一份内容，让它在自己的工作区算。即使你在add_fee里面修改price，也不因此改掉main里的price。参数名不必与调用处变量名一致，位置与类型才影响对应关系。

`total`是**局部变量（local variable）**，名字只在函数对应的作用域内可用。main不能直接访问add_fee里的total；它通过返回值拿到计算结果，再保存为自己的result。

`return total;`不是把total这个局部变量搬进main，而是把它的值作为本次调用的结果交出去，然后结束函数。函数调用结束后，这个局部变量不再继续供main访问。

因此：

- `std::cout << total;`只输出文字，不代替返回值；
- `return total;`交回数据，不会自动打印；
- 非void计算函数的每条正常返回路径应交回约定类型的值。不要指望“最后算了一下就自动返回”。
- 花括号也形成作用域。在某个if块里声明的变量，不能任意跑到块外使用；需要块外继续用的累计结果，应在适当的外层先声明。

对于`std::vector<int> values`这种普通参数，同样按值传递：调用时形成容器副本。修改副本不改变调用者的原容器，但复制n项需要O(n)时间和空间。今天数据小，这个接口可用；DAY32学const引用后再减少不必要的复制，不提前塞陌生语法。

注意：C++这个按值vector参数，不能直接类比为Python对象传参后修改属性的行为，模型部分会用实际对象说明区别。

### 4. 函数重载：名字相同，接收方式不同

**函数重载（function overloading）**：同一作用域可以有同名函数，由不同的参数列表区分。人话：对外都叫“合并”，但接两个整数和接两个小数，用各自适用的版本。

```cpp
#include <iostream>

int combine(int a, int b);
double combine(double a, double b);

int main() {
    std::cout << combine(2, 3) << "\n";       // 整数版本：5
    std::cout << combine(2.5, 3.5) << "\n";   // 小数版本：6
    return 0;
}

int combine(int a, int b) {
    return a + b;
}

double combine(double a, double b) {
    return a + b;
}
```

编译器根据调用的参数，选择匹配的重载。参数个数、类型，或类型的排列顺序不同，可以构成不同版本。

但只把a改名为x，不是新版本；**只改返回类型也不能重载**。例如两个函数都接两个int，一个返回int、另一个返回double，调用`combine(2,3)`无法靠返回类型决定选谁。

上面的混合调用`combine(2,3.5)`会有歧义：一个版本要转换第二个参数，另一个要转换第一个，不能唯一选择。今天调用时使用明确匹配的类型，不要求背完复杂的重载解析规则。

什么时候用重载？当几个操作含义接近、只是输入方式不同。不要让同名函数一个筛选耗时、另一个删除文件，调用者会无法预测行为。

### 5. 默认参数：没写的实参怎样补齐

**默认参数（default argument）**是调用者省略某些末尾实参时使用的默认值。不是“传0时替换成默认值”，更不是在运行时猜用户想要什么。

```cpp
#include <iostream>

int add_margin(int value, int margin = 2);

int main() {
    std::cout << add_margin(9) << "\n";      // 11，省略margin，用2
    std::cout << add_margin(9, 5) << "\n";   // 14，明确传5
    std::cout << add_margin(9, 0) << "\n";   // 9，0是实际传入的值
    return 0;
}

int add_margin(int value, int margin) {
    return value + margin;
}
```

这里只有一个函数定义；默认参数只是减少调用时必须写的参数。重载则是提供不同参数列表的函数版本，两者不是同一机制。

本课采用固定写法：**默认值写在main之前的声明里，后面的定义不重复写默认值**。同一作用域重复指定已有默认值会报错，即使数值一样也不应重复。

默认值从右边连续安排。例如三个参数可以只给第三个默认值，也可以给第二、第三个；本课不写“第二个有默认值，第三个仍必填”的形式。

还要避免含糊：同时定义一个接一个int的函数，和另一个接两个int但第二个有默认值的同名函数，传一个int时两者都能调用，就可能产生歧义。今天实践使用“一/二参数调用对应一个版本，三参数调用对应另一个版本”，不会发生这个问题。

### 6. 两项实践：在同一个耗时任务上练接口

两个文件均独立编译；只用已学的vector、循环、判断、普通函数。不要复制一个完整筛选模板后只改函数名。

#### 02：函数声明、返回数据、调用者输出（约20分钟）

文件：`02_C++核心_函数声明与返回数据.cpp`。

你可以参考自己DAY28的筛选逻辑，不必推倒重写，但今天自行组织函数声明和调用关系。

要求：

- `over_limit`接收一个int容器与int阈值，按原顺序返回严格大于阈值的所有数据，返回类型为`std::vector<int>`。函数不打印、不在返回容器头部放数量。
- 声明在main前，定义在main后；参数按值传递。
- main读取n、接下来的n个非负整数、最后一个阈值。约定n为0—20，不考非法文本输入。
- main调用函数；第一行输出返回容器长度，之后每行输出一个筛选结果。空结果只输出一行0。
- 为了验证原容器没有变化，可以本地临时打印输入容器检查；最终规定输出不包含这些调试行。

输入一行`5 4 10 12 20 20 10`，输出：

```text
3
12
20
20
```

再测`0 10`，只输出0；测`3 10 10 10 10`，只输出0；测`3 4 12 20 0`，输出长度3与三项数据。

解释：为什么数量由main读取size()，而不是塞进数据列表？函数内是否能直接读取main里声明的局部阈值变量？请让参数承担传递作用，不改成全局变量。

#### 03：同一个统计任务的重载与默认值（约25分钟）

文件：`03_C++应用_重载与默认参数.cpp`。

写两个都叫`count_over`的函数，均返回int、不打印：

| 版本 | 接收什么 | 返回什么 |
|---|---|---|
| A | int容器、一个int阈值；阈值默认10 | 严格大于阈值的项数 |
| B | int容器、int下界、int上界；没有默认值 | 满足“下界 < 耗时 <= 上界”的项数 |

B保证下界不大于上界。两版本含义均为统计指定范围内的耗时；A的范围没有上限。重复数据按记录条数统计，不去重。可以复用已有筛选思路，也可以直接计数，不强制两份代码长得一样。

声明放在main前，定义在main后；默认值只在声明出现。main读取n及n个耗时，分别调用：

1. 只传容器；
2. 传容器和20；
3. 传容器、10、20；
4. 传容器和0。

输入`5 4 10 12 20 20`，四行输出应为3、0、3、5。再用空容器核对四次均为0。单独测试下界等于上界时B返回0。

这里第三种调用依据三个实参选择B；第一、二、四种选择A，只有第一种使用默认阈值。解释这一点即可，不背术语定义。

#### 编译与运行

在仓库根目录终端运行（生成物放临时目录，不放进Git）：

```bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY29/02_C++核心_函数声明与返回数据.cpp" -o /tmp/day29-core
/tmp/day29-core
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY29/03_C++应用_重载与默认参数.cpp" -o /tmp/day29-functions
/tmp/day29-functions
```

程序运行后输入上面的测试数据并按回车。若报错，先看第一条真正的错误：声明缺失、参数不匹配、默认值重复还是缺定义？不需要新建错误记录表，必要时把原报错和改法写在代码注释中。

## 四、模型与数学：让“知道错多少”变成“知道怎样改”

教材承接邱锡鹏[《神经网络与深度学习》](../../学习资料/AI%20agent/神经网络与深度学习%20(邱锡鹏).pdf)2.2.3.1梯度下降（书内第30页，PDF第45页，式2.27—2.28）。教材讨论经验风险；今天先把它缩小到一个样本，避免一次引入平均梯度和训练循环。

### 1. 为什么已经有评估器，还没有学会参数

已有四个部件可以完成：

数据集给出x和y → 神经元用w、b预测 → 损失对象计算误差代价 → 评估器汇总结果。

这回答“这个模型现在好不好”，但没有回答“下一步应该把参数改成什么”。如果一直手工试w=1、w=2，只是人替模型选参数。

**优化（optimization）**就是按照目标去寻找更合适的参数。今天使用**梯度下降（gradient descent）**：在当前参数处求损失的变化率，朝让损失局部下降的方向移动一小步。

人话：评估器像仪表，告诉你当前误差；梯度告诉你旋钮往哪边转；学习率决定转多大。仪表不会自己拧旋钮，所以需要新增一个负责更新的部件。

今天不是训练深层网络，也没有使用自动微分。我们为一个真实可学习的线性神经元手动求导、更新。未来神经网络虽然参数更多，仍然需要这一步。

### 2. 从预测到梯度，不跳过中间关系

对一个样本，输入x、标签y固定，模型参数为w、b：

```text
预测 p = w*x + b
误差 e = p - y
损失 L = e² / 2
```

偏导数的作用是衡量：其他自变量固定，只稍微改变一个参数，损失怎样变化。

先看对误差的导数：L=e²/2，所以dL/de=e。

再看参数怎样影响误差：

- w增加一点，预测与误差增加“这一点乘x”，所以∂e/∂w=x；
- b增加一点，预测与误差直接增加这一点，所以∂e/∂b=1。

通过**链式法则（chain rule）**把两段影响相乘：

```text
g_w = ∂L/∂w = e*x
g_b = ∂L/∂b = e
```

人话：w要先通过输入x影响预测，预测再影响损失，所以多乘一个x；b直接加到预测上，影响倍率为1。

“求w偏导时固定b”并不意味着计算出来的g_w与b无关。因为e=w*x+b-y，换一个b，当前误差就变了，g_w也可能改变。我们只是计算这一项变化率时不同时移动b。

### 3. 手算一次完整更新

使用新的小实验：x=2，y=5，初始w=0、b=1，学习率α=0.1。

| 环节 | 计算 | 结果 |
|---|---|---:|
| 旧预测 | 0×2＋1 | 1 |
| 旧误差 | 1−5 | −4 |
| 旧损失 | (−4)²÷2 | 8 |
| w梯度 | −4×2 | −8 |
| b梯度 | −4 | −4 |
| 新w | 0−0.1×(−8) | 0.8 |
| 新b | 1−0.1×(−4) | 1.4 |
| 新预测 | 0.8×2＋1.4 | 3 |
| 新损失 | (3−5)²÷2 | 2 |

更新规则：

```text
w_new = w_old - α*g_w
b_new = b_old - α*g_b
```

为什么是减？梯度正，局部增大参数会增加损失，就往小处走；梯度负，减去负值相当于增大参数。这个例子模型预测偏低，两个梯度都为负，两个参数就往能提高预测的方向调整。

**两个梯度必须先在同一份旧参数下算完，再一起用于更新。** 先改w再重新算b梯度，会把两个不同位置的信息混在一次更新里，不再是本课定义的标准梯度下降步骤。

可以依次执行两条属性赋值；关键不是计算机必须同时写两个值，而是右边使用的梯度都已由旧参数计算好。

### 4. 为什么不能承诺每次更新都变好

学习率（learning rate）α是人为选择的步长，属于**超参数（hyperparameter）**；w、b是从数据中调整的**参数（parameter）**。

对同一个旧模型与旧梯度：

- α=0：参数不动，损失仍为8；
- α=0.1：上表损失降到2；
- α=1：w变为8、b变为5，预测21，损失128，反而更糟。

方向有依据，不代表步子可以无限大。今天只要求正常步长和零步长的代码验证；过大学习率的系统实验安排在DAY33，不额外增加一份作业。

还要注意：仅靠x=2、y=5这个样本，只要2w+b=5就能零误差，有很多参数组合。一步损失下降说明更新流程有作用，不证明已经学到通用规律。DAY30会让多个样本共同决定更新方向，DAY32再检验未见样本。

### 5. 新增更新器，但不重新抄旧四类

今天新增`GradientDescent`类，中文就是“梯度下降更新器”。职责限定如下：

| 部件 | 保存什么 | 今天负责什么 |
|---|---|---|
| LinearNeuron | weight、bias | 按当前参数预测；参数可被更新 |
| RegressionDataset | 输入与标签 | 提供样本，不在更新时改数据 |
| SquaredLoss | 本课无需新增状态 | 计算半平方损失 |
| LossEvaluator | 数据集、损失对象 | 评估，不偷偷训练 |
| GradientDescent | learning_rate | 接收已经算好的梯度，修改模型参数 |

更新器提供：

- 构造方法接收learning_rate，将它保存为自己的实例属性。
- `step(self, model, grad_w, grad_b)`接收模型对象及两个数字梯度。
- 修改传入模型的weight、bias；不用重新创建LinearNeuron；不计算新梯度，不打印，也不返回一个新模型。
- 方法没有显式返回结果时得到None，今天要修改的是模型状态，而不是用返回值替换模型。

这里的self指更新器，不是神经元。学习率放在更新器上；权重和偏置放在传入的model上。grad_w、grad_b是本次调用的临时输入，不必全改成实例属性。

为什么Python这样可以修改原对象？传进去的是已有对象，局部名字model也指向它；修改它的属性会改变这个对象。若只让局部model指向一个新建对象，原来的对象不会自动被替换。

已有对象的小演示，**不是step的实现**：

```python
neuron = LinearNeuron(2, 1)
another_name = neuron
neuron.bias = 3
print(another_name.bias)    # 3
print(neuron is another_name)  # True
```

`is`检查两边是否为同一个对象，不是比较预测结果是否相等。两个分别创建的神经元即使参数相等，仍不是同一对象。这能验证今天是否在原模型上更新，不靠对象名字猜测。

### 6. 独立模型实践（25分钟）

文件：`04_模型实践_单样本梯度更新.py`。

**可以直接复用你DAY28已经写对的四个类定义**，不计为抄答案；不要整段复制旧调用区，因为旧调用中重新创建了模型。今天自己新增更新器、梯度计算与实际调用。不安装任何库。

先在注释中用自己的三步说明准备怎样做；不必抄上面的表格。

主实验：

1. 用单样本数据x=2、y=5，创建w=0、b=1的模型，以及已有损失、评估器。保留另一个指向该模型的名字，用于身份检查。
2. 先评估旧损失；用旧参数的预测算出两个梯度；调用一次step。
3. 用同一个评估器重新评估同一个模型。打印旧损失、两个梯度、新参数、新预测、新损失。
4. 检查仍是同一个模型对象，输入与标签没有被改变。结果应与上表一致。

两个短检查，不增加新类：

| 检查 | 初始条件 | 一次更新后应看到 |
|---|---|---|
| 零学习率 | 重新建立w=0、b=1的独立测试模型，x=2、y=5，α=0 | w、b、损失不变 |
| 输入为0 | 独立测试模型w=2、b=1，x=0、y=3，α=0.1 | w=2、b=1.2；新损失1.62 |

“同实例更新”约束针对一次实验的更新前后；不同测试场景可以新建独立模型，避免上一场参数污染下一场。

浮点数允许微小误差，可用已学的`abs(实际值 - 预期值) < 1e-9`检查，不用因为打印出1.2000000000000002纠结。

手算部分再独立完成x=1、y=4、w=2、b=1、α=0.1这一组，写出旧预测、旧损失、两个偏导和新参数。然后用自己的程序验证；不额外写心得长文。

今天不写batch_gradients、Trainer、fit，不做100次循环，也不重写整个深度网络。**新增能力是“从数据算方向，并在原模型上走一步”。**

## 五、今天怎样算完成

代码与运行结果足够，不新建教师记录表。重点检查：

- Python：27没有把非val的重复项误删；返回k，确实修改原输入；26能独立重写。
- C++：能解释声明、定义、调用；函数返回数据与main打印分开；重载与默认参数调用结果正确；没有用全局变量绕过参数。
- 模型：两个梯度来自同一旧参数点；step修改传入模型；正常学习率损失下降，零学习率不动；能解释为何x=0时w梯度为0。
- 知道什么是已证实、什么还未证实：一步更新正确不等于100次训练或泛化已经通过。

只需用自己的话回答三个问题（可以直接放相关代码注释）：

1. 27与26的“保留条件”分别是什么？为什么27保留下来的重复值不能删除？
2. “函数重载”与“默认参数”各解决什么问题？为什么返回类型不能单独区分重载？
3. 更新器里的self与model分别是谁？为什么梯度先算完，参数再修改？

遇到难点先独立尝试，再按“引导问题→伪代码→局部骨架→完整解释”请求帮助。无需为了每个小报错再等30分钟；已有尝试与报错足以说明卡点。看到完整答案后再关掉重写，诚实说明参考范围。

下次交DAY29时，我按实现、测试、理论与心得一起评阅，再在DAY30给出全部示范与逐题对照。当前不会代提交或推送Git。

## 六、DAY28完整示范与逐题比较（按需展开，不要求重抄）

以下承接DAY28现有评阅，集中放在今天这一份文档方便对照。它们是昨天的示范，不是今天独立题的预填代码。


以下代码可分别放入临时文件验证，**不要求覆盖原作业，也不要求全部再抄一遍**。示范保持DAY28已教范围，不提前使用引用、指针或新的模型类。

<details>
<summary>00｜704：你的实现已正确，示范仅使用较短变量名</summary>

```python
class Solution:
    def search(self, nums, target):
        left = 0
        right = len(nums) - 1
        while left <= right:
            middle = (left + right) // 2
            if nums[middle] < target:
                left = middle + 1
            elif nums[middle] > target:
                right = middle - 1
            else:
                return middle
        return -1

solver = Solution()
nums = [-8, -2, 1, 6, 11, 19]
for target, expected in [(-8, 0), (19, 5), (6, 3), (4, -1)]:
    assert solver.search(nums, target) == expected
assert solver.search([7], 7) == 0
assert solver.search([7], 6) == -1
assert solver.search([2, 8], 8) == 1
assert solver.search([2, 8], 3) == -1
```

你写的`right_index >= left_index`与示范条件等价，不需要修改。左右边界代表仍可能包含目标的闭区间；每次排除中间值及不可能的一侧。你已覆盖首尾和不存在的目标，补单元素、双元素测试即可。

</details>

<details>
<summary>01｜121：保留你“更新到前一天，再处理今天”的正确逻辑</summary>

```python
class Solution:
    def maxProfit(self, prices):
        lowest = prices[0]
        best = 0
        for day in range(1, len(prices)):
            if prices[day - 1] < lowest:
                lowest = prices[day - 1]
            profit = prices[day] - lowest
            if profit > best:
                best = profit
        return best

solver = Solution()
for prices, expected in [([6, 3, 3, 8, 2, 9], 7),
                         ([5, 5, 4, 4], 0), ([4], 0),
                         ([2, 7, 1, 4], 5), ([9, 1, 1, 2], 1),
                         ([0, 0, 3], 3), ([2, 8, 1], 6)]:
    assert solver.maxProfit(prices) == expected
```

这一版与前一天示范的更新位置不同，但等价：计算第day天利润时，lowest覆盖0到day−1天的最低价。你的新版本状态解释比上涨段筛选更直接，不要求改成另一套顺序。最后一天才出现最低价时，不会用它去“回到过去”卖出。

</details>

<details>
<summary>02｜C++统计：函数只返回筛选数据，main负责数量和格式</summary>

```cpp
#include <cassert>
#include <iostream>
#include <vector>

int total_duration(std::vector<int> durations) {
    int total = 0;
    for (int value : durations) {
        total += value;
    }
    return total;
}

std::vector<int> over_limit(std::vector<int> durations, int limit) {
    std::vector<int> result;
    for (int value : durations) {
        if (value > limit) {
            result.push_back(value);
        }
    }
    return result;
}

int main() {
    assert(total_duration({}) == 0);
    assert(total_duration({4, 10, 0, 7, 10}) == 31);
    assert(over_limit({}, 7).empty());
    assert(over_limit({7, 7}, 7).empty());
    std::vector<int> test = over_limit({4, 10, 0, 7, 10}, 7);
    assert(test.size() == 2);
    assert(test[0] == 10 && test[1] == 10);

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
    std::vector<int> filtered = over_limit(durations, limit);
    std::cout << total_duration(durations) << '\n';
    std::cout << filtered.size() << '\n';
    for (int value : filtered) {
        std::cout << value << '\n';
    }
    return 0;
}
```

合法输入前提与原题一致。`5 4 10 0 7 10 7`输出31、2、10、10，各一行；`0 7`输出两行0；`3 7 7 7 7`输出21、0；`2 8 9 7`输出17、2、8、9。断言成功不产生额外输出。

相比你的代码，筛选只遍历一次，也不把数量混入数据；你的两次遍历仍是O(n)，不是复杂度级别错误。这次修改的主要价值是接口稳定，而非少一轮循环就叫“算法升级”。

</details>

<details>
<summary>03｜C++副本：保留正确结果，补长度与统一分隔</summary>

```cpp
#include <cassert>
#include <iostream>
#include <vector>

std::vector<int> over_limit(std::vector<int> durations, int limit) {
    std::vector<int> result;
    for (int value : durations) {
        if (value > limit) {
            result.push_back(value);
        }
    }
    return result;
}

int main() {
    std::vector<int> original = {2, 9, 4};
    std::vector<int> first = over_limit(original, 5);
    std::vector<int> second = over_limit(original, 10);
    if (!first.empty()) {
        first[0] = 99;
    }
    std::vector<int> third = over_limit(original, 5);
    assert(original[0] == 2 && original[1] == 9 && original[2] == 4);
    assert(first.size() == 1 && first[0] == 99);
    assert(second.empty());
    assert(third.size() == 1 && third[0] == 9);

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
    std::cout << third.size() << '\n';
    for (int value : third) {
        std::cout << value << '\n';
    }
    return 0;
}
```

完整输出为3、2、9、4、1、99、0、1、9，各一行。你的数值内容已经正确，不因格式否定副本能力。固定输入下first确实非空；示范保留空判断，便于换输入。若误把original[0]改成99，后续筛选会读到原数据中的99，这是另一件事。

</details>

<details>
<summary>04｜模型：保留四类，补同实例修改、参数对照与断言</summary>

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
model_a = LinearNeuron(0, 1)
model_b = LinearNeuron(2, 1)
data_a = RegressionDataset([-2, 1, 3], [-3, 3, 7])
data_b = RegressionDataset([0, 2], [1, 5])
evaluator_a = LossEvaluator(data_a, loss)
evaluator_b = LossEvaluator(data_b, loss)

assert data_a.size() == 3
assert data_b.size() == 2
assert data_a.get_item(0) == (-2, -3)
assert abs(evaluator_a.evaluate(model_a) - 28 / 3) < 1e-9
assert evaluator_a.evaluate(model_b) == 0
assert evaluator_b.evaluate(model_a) == 4

# 修改原模型属性，不调用构造器，不重建评估器。
model_a.weight = 2
assert model_a.bias == 1
assert evaluator_a.evaluate(model_a) == 0
assert evaluator_b.evaluate(model_a) == 0
assert data_a.xs == [-2, 1, 3] and data_a.ys == [-3, 3, 7]
assert data_b.xs == [0, 2] and data_b.ys == [1, 5]

# B段：同一个评估器、同一个模型，改变参数再比较。
single_data = RegressionDataset([2], [5])
single_evaluator = LossEvaluator(single_data, loss)
probe = LinearNeuron(3, 0)
assert abs(single_evaluator.evaluate(probe) - 0.5) < 1e-9
probe.weight = 2.9
assert abs(single_evaluator.evaluate(probe) - 0.32) < 1e-9
probe.bias = 0.4
assert abs(single_evaluator.evaluate(probe) - 0.72) < 1e-9
print('DAY28模型评估与参数对照通过')
```

你的evaluate直接使用`self.data.ys`，在当前数据集定义下合法且结果正确。示范取样时一起收集y，是为了让输入与标签都通过同一接口配对，不是要求所有实现必须一样。你返回局部变量loss也合法，不强迫压成一行。拼写predicition不影响当前运行，属于日后整理项，不阻止新课。

你的原脚本输出28/3、0、4、0、0，数值正确；示范补上断言、保留同一对象及B段三组参数的验证。它依然只是评估与手动设参数，不声称已经训练。

</details>

### DAY28理论示范回答

- 实例属性能改变。你的咖啡机类比抓住了“根据结果调节”的意思；更贴近当前模型的是调节机器已有旋钮，而不是每次换一台机器。`model.weight = ...`修改当前对象，`model = LinearNeuron(...)`建立新对象并让名字指向它。
- evaluate没有return时返回None；Python不会自动把最后一次计算结果交给调用者。`model.forward`是方法，`model.forward(2)`才是一次调用的结果。
- 手算x=1、y=4、w=2、b=1：预测3、误差−1、半平方损失0.5；对w的偏导为`(w*x+b-y)*x=-1`，固定b、x、y；对b的偏导为`w*x+b-y=-1`，固定w、x、y。
- x=2、y=5时，(3,0)到(2.9,0)只减小w，损失从0.5降至0.32；再把b改成0.4，损失升为0.72。单个偏导只描述其他自变量固定时的局部变化，同时改变多个参数必须整体考虑。
- 先在同一旧参数点计算所有偏导，再更新参数；否则后算的偏导已不对应原来的点。梯度给出局部方向，学习率决定步长，不能保证任意大步子都下降。

本次不要求为补这几项重做DAY28。DAY29在真实参数更新中验证同实例修改与偏导；之后完成平均梯度、训练器和100次训练。C++转向函数体系、数组、指针、引用、内存、结构体和类，不把格式问题升级为重复基础课。

