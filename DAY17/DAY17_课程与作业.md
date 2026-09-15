# DAY17：把C++求和写成函数，复习LC387，理解模型怎样接收输入

> 今天只读这一份课程。包含DAY16全部示范答案、逐题评语和DAY17理论与作业。约3小时，三份作答文件均留白；三步分析仍由你自己写，没有额外TODO。
>
> 阅读顺序：第一节看评价；第二、三节按需要对照昨天答案；第四节回答“辅助数据”；第五节学习C++函数；第六节回答“对象不也是自己调用吗”；第七节领取作业。
>
> 今天只把你已经会的C++求和封装成一个函数，不同时教引用、const、指针和类。神经网络不升级数学结构，也不要求你再机械抄一遍相同的类。全部在Mac本地完成，无新依赖。

## 一、DAY16评语：86/100，可以向前推进一个小台阶

你的C++已经不只是“看过vector”：能建立容器、追加元素、读取长度、区分空与零，并在循环外保留累计值。Python的242平台入口已补齐；神经元换输入、换参数的代码正确。这些都是实际进步。

这次完整检查了三份代码、代码注释、`课后总结.md`和本地Git记录；运行Python，编译C++，并用额外输入验证。旧课程与代码保持原样。

| 项目 | 实际证据 | 结论 |
|---|---|---|
| LC242 | 6条自写断言通过；补测14641组短字符串组合、2组长字符串通过；已记录7分钟 | 算法与平台入口正确，速度记录是有价值的反馈 |
| C++容器与求和 | 原程序无警告编译，输出2、3、0、1、0；50的求和断言通过；额外换6组数据均正确 | 已具备把这段计算放进一个函数的基础 |
| 神经元 | 原场景输出4、0、0、5、4、0、5；补测90组参数/输入及实例独立性通过 | 计算和各实例参数使用正确；对“谁调用、谁供数据”仍有疑问 |
| 理论与心得 | 容器、累计、固定字母表已有理解；明确提出“辅助数据是什么”和调用疑问 | 需要用你的代码解释，不再仅重复概念定义 |

评分：概念20/25，代码30/30，分析与调试17/20，测试与复杂度10/15，Git记录与表达9/10，共86分。它是基于提交材料的教学估分，不是平台成绩，也不是全部闭卷面试能力的证明。

这里没有把命名、空行或三步分析篇幅作为主要扣分项。你记录了242用时，但没说明是否查答案或使用提示，因此不能把“7分钟”直接认定为全程无辅助。额外测试由我执行，也不算成你已经独立写过。

### 尚未保留的验证，不等于你不会

- C++作业中的单元素与空容器求和测试，未见你保留；我在内存中的测试副本里换输入后验证通过，没有改你的文件。
- C++有些观察只打印了结果，没有断言；神经元场景则全用打印，未保留规定的断言及B参数检查。
- 理论第一题说清了头文件用途，但还没回答“assert与打印的区别”。这次补一句实际用途即可，不补长篇报告。

下一步重点是“同一段计算，换输入仍能独立调用和检查”。不需要再来一天空容器教学，也不因一个术语疑问暂停整个主线。

## 二、DAY16全部示范答案与对比

这些是昨天题目的答案。按需要查阅，不要求全部抄写；DAY17的新任务没有预填实现。

### 00：LC242有效的字母异位词

```python
class Solution:
    def isAnagram(self, s, t):
        if len(s) != len(t):
            return False

        s_counts = {}
        t_counts = {}
        for letter in s:
            s_counts[letter] = s_counts.get(letter, 0) + 1
        for letter in t:
            t_counts[letter] = t_counts.get(letter, 0) + 1
        return s_counts == t_counts


solution = Solution()
assert solution.isAnagram("anagram", "nagaram") == True
assert solution.isAnagram("aab", "aba") == True
assert solution.isAnagram("", "") == True
assert solution.isAnagram("rat", "car") == False
assert solution.isAnagram("aab", "abb") == False
assert solution.isAnagram("a", "aa") == False
assert solution.isAnagram("abca", "caba") == True
```

你的实现完全正确。你在长度相同时进入计数、相等时返回True，否则在最后返回False；示范在长度不等时先退出，最终直接返回字典比较结果。两种算法一致，示范只是少一层缩进，不要求为了写法重做。

你的`isAnagram`名称符合平台入口，之前待补的部分可以标记完成。测试覆盖了字符次数、不同长度和空串扩展；“字符种类相同但次数不同”也没有漏判。

### 01：C++的vector观察与求和

下面按DAY16要求，仍只用main，不提前用函数答案替代昨天的任务：

```cpp
#include <vector>
#include <cassert>

int main() {
    std::vector<int> values{8, 13};
    assert(values.size() == 2);
    assert(values.empty() == false);
    assert(values[0] == 8);

    values.push_back(5);
    assert(values.size() == 3);
    assert(values[0] == 8);
    assert(values[1] == 13);
    assert(values[2] == 5);

    std::vector<int> empty_values{};
    assert(empty_values.size() == 0);
    assert(empty_values.empty() == true);
    empty_values.push_back(0);
    assert(empty_values.size() == 1);
    assert(empty_values.empty() == false);
    assert(empty_values[0] == 0);

    std::vector<int> times{15, 25, 10};
    int total = 0;
    for (int value : times) {
        total += value;
    }
    assert(total == 50);

    std::vector<int> one_time{7};
    int one_total = 0;
    for (int value : one_time) {
        one_total += value;
    }
    assert(one_total == 7);

    std::vector<int> no_times{};
    int empty_total = 0;
    for (int value : no_times) {
        empty_total += value;
    }
    assert(empty_total == 0);
    return 0;
}
```

你的第27～33行正确：累计变量在循环外建立，所有元素都参与求和。额外测试还确认了空输入也能得到0，因此不把“没保留空输入测试”误说成“空输入会算错”。

示范与主要差异是测试更完整，而不是算法更高级。DAY16允许用三个短区域测试，所以这里重复写循环没有违反要求；DAY17学函数后，就能让这三份测试调用同一段计算代码。

你用`int is_empty`接收布尔结果，本题会转成0或1，输出并没有错。若要保存真假，更贴切的写法是`bool is_empty = empty_values.empty();`。这属于类型表达建议，不是阻碍学习的错误。

`int len_vector = values.size();`在本题很小的容器上正常；`size()`本身返回容器的计数类型，不保证任意大容器都能放进int。今天可以直接比较或输出`values.size()`，暂不加类型转换练习。[vector计数与empty说明](https://learn.microsoft.com/en-us/cpp/standard-library/vector-class?view=msvc-170)

### 02：神经元的输入与实例参数

```python
class SingleNeuron:
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias

    def forward(self, x):
        z = self.weight * x + self.bias
        if z > 0:
            return z
        return 0


neuron_a = SingleNeuron(3, -2)
neuron_b = SingleNeuron(-2, 1)
assert neuron_a.forward(2) == 4
assert neuron_a.forward(0) == 0
assert neuron_b.forward(2) == 0
assert neuron_b.forward(-2) == 5
assert neuron_a.forward(2) == 4

neuron_a.weight = 1
assert neuron_a.forward(2) == 0
assert neuron_b.forward(-2) == 5
assert neuron_b.weight == -2
assert neuron_b.bias == 1
```

你的类与计算都正确，改A之后没有影响B。再次赋值`neuron_A.bias = -2`与原值相同，可以保留，不影响结果；示范只修改本次要求改变的weight。

主要差别仍是断言：打印结果需要人对照，断言把已经手算好的期望留给程序检查。无需为了多一行断言写新的记录表。

你在主程序用`z`接住forward返回值时，这个变量实际保存的是经过ReLU后的输出；函数内部的`z`则是激活前的值。两个变量处在不同范围，代码不会因此冲突。解释模型时区分两者即可，外部变量改叫`output`只是可读性建议。

## 三、DAY16五道理论题的参考回答

1. **头文件和检查：** `iostream`提供标准输入输出相关对象，`cassert`提供assert检查宏，`vector`提供顺序容器。打印展示一个结果；断言检查结果是否符合预期，失败时报告。你前半部分正确，“输出输出”视为笔误，不据此扣分；后半部分尚需补充。
2. **空容器与0：** 加入0后有一个元素，size是1，empty是false；默认输出bool时显示0。你的回答正确。
3. **累计值：** 还没处理任何数据时总和为0；每次把当前项加到已有结果上。如果每轮重置，之前的和被丢掉，例如4与6最终只剩6而不是10。你的解释方向正确。
4. **辅助数据和复杂度：** 本题辅助数据就是自己建立的两个计数字典等工作数据。时间O(m+k)的写法可以，m、k表示两串长度；不必为符号改名重写。空间更直接由两个字典的键数决定；不限字符集时O(m+k)是一个最坏上界，限定26个小写字母时两个字典合计最多52项，仍为O(1)。你最后的固定字母表结论正确，不是整道复杂度答错。
5. **模型与调用：** 通过对象调用方法，确实会把这个对象传给self，所以你说“对象调用”并不离谱。还要看括号里显式提供了什么：那是本次x。参数可以由人指定、初始化或加载已有模型，并非只有训练后才存在；训练是根据数据误差更新参数。下面用你能运行的具体表达式讲清楚，不要求背“来自谁”这句话。

## 四、直接回答：什么是“辅助数据”

它不是今天又增加的一种数据结构，也不是另一个算法术语体系。只是给“为这次计算另外准备的数据”起的统称。

在你的242里：

| 代码里的内容 | 在算法中做什么 | 空间分析时怎样看 |
|---|---|---|
| `s`、`t` | 已经传进来的原字符串 | 输入数据 |
| `s_dict`、`t_dict` | 为了比较字符次数而新建的字典 | 主要辅助数据 |
| 循环中的字符变量 | 暂时处理当前字符 | 固定数量的工作变量 |
| 返回的True或False | 把判断结果交给调用者 | 固定大小的输出 |

比如`s = "aaaaa"`，字典只需要一个键a和计数5，不是五个键。换成更长的全a字符串，遍历次数增加，键数仍然是1。

所以问“用了多少额外空间”，就是问这些工作数据最多同时保存多少内容。在本题固定小写字母的约束下，不能只按输入每多一个字符就给字典多算一项；但你写的O(m+k)可以作为字符种类不受限制时的宽松上界。

不要把“辅助数据”与CPU寄存器、缓存等硬件名词绑定。本阶段分析的是代码为了计算保留了哪些值和容器，按通常机试的常量大小计数单位估算。

## 五、C++今天只学一件事：让同一段计算可以被多次调用

你在main里已经会求和。现在希望第一组数据算50，第二组算7，第三组空数据算0，而不复制三份循环。函数（function）就是把这个计算单独命名，接收输入并返回结果。

今天的新增重点不是求和算法，而是“定义、调用、返回”之间如何交接数据。

### 1. 先用很小的函数观察程序怎么走

下面的示例给金额加2，不是今天求和作业的答案：

```cpp
#include <cassert>

int add_fee(int amount) {
    int result = amount + 2;
    return result;
}

int main() {
    int price = 6;
    int first = add_fee(price);
    int second = add_fee(10);
    assert(first == 8);
    assert(second == 12);
    assert(price == 6);
    return 0;
}
```

从main看：先有price=6；执行到调用时进入add_fee，本次amount收到6，算出8返回；main把8存入first，再执行下一条语句。第二次调用提供10，重新算出12。只定义add_fee并不会把函数体提前运行一次。

定义里的`amount`叫形参（parameter），是函数接收输入时使用的名字；调用里的`price`或`10`叫实参（argument），是这次实际给出的值。人话：一个是“接收口的名字”，一个是“这次送进去的东西”。不要背两套词，能在自己的代码里指出即可。[C++函数定义、参数与返回值](https://learn.microsoft.com/en-us/cpp/cpp/functions-cpp?view=msvc-170)

### 2. 拆开今天需要读懂的函数入口

本次接口约定为`int total_time_ms(std::vector<int> times_ms)`，不在作答文件中预填。

| 片段 | 意思 |
|---|---|
| 第一个`int` | 计算结果是一个整数，即总耗时 |
| `total_time_ms` | 给这段计算起的名字，调用时要用同一名字 |
| `std::vector<int>` | 接收一组整数，不再只是单个int |
| `times_ms` | 函数内部称呼这组数据的名字 |
| 后面的`{ ... }` | 定义这段计算具体做什么 |

调用时可以传`training_times`，函数里叫`times_ms`；两边不必同名。关键是把这次传入的容器当作输入，而不是在函数里另建写死的样例。

类型后面跟名字是声明接收的变量，不能把定义写成`total_time_ms({15,25,10})`来代替函数参数。花括号里的具体数据应由调用方建立。

### 3. 先用另一个容器函数理解“接收一组数据”

这段示例只返回最后一项；没有元素就返回0。它使用的是你已认识的empty、size和索引，不引入新容器API：

```cpp
#include <vector>
#include <cassert>

int last_or_zero(std::vector<int> numbers) {
    if (numbers.empty()) {
        return 0;
    }
    return numbers[numbers.size() - 1];
}

int main() {
    std::vector<int> first{4, 9};
    std::vector<int> second{7};
    std::vector<int> no_numbers{};
    assert(last_or_zero(first) == 9);
    assert(last_or_zero(second) == 7);
    assert(last_or_zero(no_numbers) == 0);
    return 0;
}
```

同一个函数收到不同的vector，结果跟着数据改变。`if (numbers.empty())`使用empty返回的真假：真就执行里面的return；返回后整个函数结束，所以空容器不会继续读“最后一项”。它与`if (numbers.empty() == true)`表达同一个判断。

你可以看这个示例理解函数的外壳，然后关闭示例，自己把已会的求和放进作业函数；不需要抄last_or_zero作为额外练习。

### 4. 函数里的变量为什么不会与main混在一起

作用域（scope）指一个名字在代码中能被使用的范围。普通函数里的局部变量只在相应范围内使用，main不能直接读取另一个函数内部的累计变量。C++的大括号也会形成块作用域，不完全等同于Python的缩进规则。[C++作用域说明](https://learn.microsoft.com/en-us/cpp/cpp/scope-visual-cpp?view=msvc-170)

本课把累计值建立在函数里，每次调用都从0开始。返回整数时，交给调用方的是计算结果；局部变量结束使用，不会把已经返回给调用者的这个整数结果顺便删掉。

调用方可以写`int answer = total_time_ms(training_times);`接住结果，也可以把调用放进自己的断言里检查。返回和输出不同：只写cout会显示数字，却没有按函数约定把整数交回去。

计算函数里不要用`return 0`表示“我运行成功”，那会把答案变成0；main最后的`return 0`才是我们约定的程序退出状态。函数应该返回本次算出的总耗时。

今天继续把计算函数定义在main之前，两个函数并列，不把一个普通函数定义写进main内部。不学习函数前置声明、重载或静态变量。

### 5. 值传参：本次版本会收到一份vector副本

今天写的`std::vector<int> times_ms`是值传参（pass by value）。把一个已有vector传进来时，函数接收它的值副本；不是因为两边起了相同名字就能共用一个变量。

这能让本次调用独立处理，但复制n个整数需要O(n)的存储和复制工作。求和本身只需要一个固定大小的累计值，因此可以说“计算工作变量O(1)，当前值传参版本计入容器副本后额外空间O(n)”。总时间仍是O(n)。

这是明确当前版本的代价，不是要求今天立刻优化。下一阶段再用已经理解的例子解释引用与const，而不是先把`&`加进接口让你照抄。也不要把这种C++规则原封不动套到Python对象传参上。

## 六、神经网络支线：你说“对象调用”并没有错，还需要区分两个位置

你问：“这个调用不也是实例对象去调用的吗，说到底不都是实例对象自己吗？”

日常说“neuron调用forward”可以。更具体地说，是程序运行到`neuron.forward(sample)`这行，选定neuron这个对象的forward方法，再给它本次sample。点号前后与括号里承担的是不同角色，不需要在“谁主动调用”上抠字眼。

### 1. 把本次输入放进一个看得见的变量

下面的片段使用第二节已经解释过的SingleNeuron定义；放在同一个Python文件、类定义之后即可，不需要导入新库：

```python
neuron = SingleNeuron(2, 1)
sample = 3
output = neuron.forward(sample)
assert output == 7

sample = 5
assert neuron.forward(sample) == 11
assert neuron.weight == 2
assert neuron.bias == 1
```

同一个neuron没有重新创建，也没有调整参数，只是本次sample从3变成5，所以结果从7变成11。

| 表达式的一部分 | 这次提供什么 |
|---|---|
| `neuron.` | 指定使用哪一个对象，它会作为self传给普通实例方法 |
| `forward` | 指定执行哪一个方法 |
| `(sample)` | 显式提供这次输入值，交给x |
| `self.weight`、`self.bias` | 方法执行时，从当前对象读取持续保存的模型参数 |

所以不是“都用了同一个对象，因此所有输入都等于对象自身”。对象是neuron，本次x是一个数，二者同时交给方法，各自承担不同角色。

### 2. 用等价调用拆开这个过程

对于这里普通的Python实例方法，下面两行得到相同结果：

```python
first = neuron.forward(sample)
second = SingleNeuron.forward(neuron, sample)
assert first == second
```

第二种写法显式展示了两个输入位置：neuron交给self，sample交给x。第一种写法把第一个位置自动补上了。它只用于帮助理解，日常仍用第一种，不要求改成另一套代码风格。[Python方法对象与参数传递](https://docs.python.org/3.11/tutorial/classes.html#method-objects)

你也可以在某个对象的方法里发起另一个调用，输入甚至可以取自一个对象属性；所以“输入绝不能来自对象”不是正确规则，我之前对“来源”的说法过于简化。需要识别的是这一次到底传了什么，以及方法是否把它保存成长期状态。

本课的x没有存成`self.x`，每次forward收到不同值；weight和bias保留在对象上，用于后续调用。这才是现在要理解的区别。

### 3. “函数参数”和“模型参数”不是同一层含义

定义`forward(self, x)`时，self和x是Python函数的接收参数；讨论神经网络时，模型参数是weight和bias这些决定模型计算的值。两个场景都使用“参数”这个词，不代表x也是本课要学习调整的模型权重。

权重在训练前也存在，可以由人指定、随机初始化，或从已训练的模型加载。本课`SingleNeuron(2,1)`就是人为给初始参数，完全是有效的模型参数；forward只按它们计算。训练则进一步根据样本、目标与误差调整这些参数，不是只靠多调用几次自动发生。

### 4. 今天增加的实践：从外部给同一模型送入几条样本

实际使用模型时，经常希望把几条数据交给同一个模型，按相同规则得到几条输出。今天写一个普通函数接收“模型对象”和“样本列表”，使用你已会的列表、循环和方法调用即可。

先只给一条样本，看看普通函数接收对象是否需要神秘的新语法。接着上面的neuron定义运行：

```python
def predict_one(model, sample):
    return model.forward(sample)


assert predict_one(neuron, 3) == 7
```

`model`是函数内部称呼传入对象的名字，`sample`接收本次的3。这不会自动新建或复制一份SingleNeuron，也没有把神经元的类定义放进函数；函数只是使用收到的对象完成计算。这个示例只处理一个数，今天的样本列表由你自己组织遍历与返回结果。

这不会把一个神经元扩展成多个输入特征：列表里每个数是一条独立样本，每次forward仍只接收一个数。例如输入列表有三个数，输出也有三个数，不是先把三项相加再交给神经元。

这是串行完成多次单输入预测，不是PyTorch的张量批处理，也没有新模型公式。目的在于让你亲手看到：外部函数持有样本，模型保存参数，两者通过方法调用合作。具体实现步骤仍由你写。

## 七、今天的三份作业

### 时间安排

| 时间 | 做什么 |
|---:|---|
| 15分钟 | DAY16反馈与“辅助数据”解释，昨天答案按需查 |
| 25分钟 | 任务0：闭卷复习LC387 |
| 45分钟 | C++函数理论：调用、参数、局部变量、返回值 |
| 45分钟 | 任务1：只封装一个求和函数，换输入测试 |
| 35分钟 | 神经元调用讲解与任务2；理论约15分钟、实践约20分钟 |
| 10分钟 | 简短回答、保存测试与Git提交 |
| 5分钟 | 缓冲，提前完成可收工 |

共180分钟。支线时间略长是为了回答你的实际疑问，不再另外布置神经元数学题。若超时，优先保留LeetCode和C++函数，支线可顺延；不以抄完代码赶进度。

### 任务0：Python复习LeetCode 387

文件：`00_Python复习_LeetCode387_第一个唯一字符.py`。

[LeetCode 387官方题目](https://leetcode.com/problems/first-unique-character-in-a-string/)，简单；这是DAY14后的第3课复习。返回在整个字符串里只出现一次、且位置最靠左的字符索引；没有则返回-1。限定小写英文字母，先闭卷尝试。

入口`Solution.firstUniqChar(self, s)`。不要求重复写普通函数，不要求固定用一个还是两个字典，只要能解释并正确处理输入。

| s | 应返回 |
|---|---:|
| `"leetcode"` | 0 |
| `"loveleetcode"` | 2 |
| `"aabb"` | -1 |
| `"aabc"` | 2 |
| `"z"` | 0 |
| `""` | -1，本地扩展 |

自己增加一组，写断言、时间和额外空间，并说明关键变量保存什么。时间目标是20分钟左右，但不是超过就失败；记录真实用时及是否查过答案。今天不预给387答案，DAY18再评讲。

### 任务1：把耗时求和写成一个C++函数

文件：`01_C++实践_把耗时求和写成函数.cpp`。

要求独立实现`int total_time_ms(std::vector<int> times_ms)`，返回这次提供的全部耗时之和。函数内部不打印、不写死样例、不读取全局容器。main负责创建样例、调用函数、检查结果。

输入保证为非负整数，单次总和不超过10000；不用处理文件、非法类型或溢出。沿用本课值传参，不需要自行猜引用语法。

| 输入 | 预期总耗时 |
|---|---:|
| `{15,25,10}` | 50 |
| `{7}` | 7 |
| `{}` | 0 |
| `{0,0}` | 0 |
| `{12,8}` | 20 |

自己写头文件、函数、main和断言。按7→50→0→20→50的次序连续调用，再检查原始50那份vector仍有3项且元素为15、25、10。它用于判断计算是否正确使用了本次参数，有没有错误残留前次累计结果。

只需要一个求和函数，不增加慢步骤函数。完成后用自己的话说明：调用方的数据叫什么、函数内部叫什么；返回值在哪里被接住；每次累计值为什么重新从0开始。三步由你自己写，接口说明不等于替你预填算法步骤。

### 任务2：给模型传入一组样本，每次仍然只输入一个数

文件：`02_神经网络支线_给模型传入一组样本.py`。

可以复用你自己DAY16已经写正确的SingleNeuron类，放在这份文件里；不必每次把同样的类再抄一遍，也不需要跨文件import。复用自己的已理解代码与复制AI新题答案不是一回事。

本次真正独立编写的是普通函数`predict_samples(model, samples)`：

- model是一个SingleNeuron实例；samples是由数值组成的列表。
- 返回一个新列表，按输入顺序保存每条样本的神经元输出；不是只打印，也不是返回一个总和。
- 每次给forward的是一个数。输入为空时返回空列表。
- 不修改samples，也不修改模型的weight与bias；不使用固定的全局neuron_A或固定样本代替参数。

用这些预期验证，断言由你写：

| 模型参数 | samples | 预期结果 |
|---|---|---|
| A：weight=2，bias=1 | `[-1,0,2]` | `[0,1,5]` |
| B：weight=-1，bias=3 | `[-1,0,2]` | `[4,3,1]` |
| A | `[]` | `[]` |
| A | `[4]` | `[9]` |

先分别调用A、B，再回到A处理原来三条样本，结果仍应是`[0,1,5]`。检查样本内容与两份模型参数没有被函数改动。自己再设计一条样本，先手算，再写断言。

只针对一条实际调用解释：model是谁，sample的值是什么，forward中的self与x分别收到什么。不要求提交长篇“数据来源”定义。

三步仍由你自己写；我不预填循环或调用骨架。如果卡住，发已有代码、预期和实际结果，先给你引导问题，再根据需要逐级提示。

## 八、怎样运行与检查

继续使用当前Python环境，在仓库根目录运行：

```bash
cd /Users/chen/CCY/Algorithm-Learning-Days
python3 DAY17/00_Python复习_LeetCode387_第一个唯一字符.py
python3 DAY17/02_神经网络支线_给模型传入一组样本.py
```

写完C++后先编译：

```bash
mkdir -p .build/DAY17
clang++ -std=c++17 -Wall -Wextra -pedantic DAY17/01_C++实践_把耗时求和写成函数.cpp -o .build/DAY17/total_time
```

确认编译成功，再运行：

```bash
./.build/DAY17/total_time
```

编译失败时不要直接运行旧文件来判断新代码。断言通过时可以没有输出，但要确保main或主程序真的调用了需要检查的函数。不要把“程序能退出”与“功能已验证”混为一谈。

沿用根目录忽略规则，编译结果放在`.build`，不提交可执行文件。没有新增GPU、依赖、编辑器插件或重复的公共目录。

## 九、今天只写五个简短回答

写在下方或自己的课后文件，二选一，代码旁的心得也会读取。

1. 用自己387代码中的具体变量解释“辅助数据”，并说时间和额外空间。
2. 用一次C++调用指出返回类型、形参和实参；它们的变量名必须相同吗？
3. 为什么main不能直接读取计算函数内部的累计变量？返回结果以后，调用方如何继续使用它？
4. 对自己的`model.forward(sample)`，分别说model、self、sample、x代表什么。用一个具体数字回答即可。
5. `predict_samples`处理三条样本，是三次单输入预测还是一个三输入神经元？如何验证它真的使用了传入的模型而不是固定A？

记录一行：LC387用时、是否查过答案或获得提示、今天最卡的一处。三步分析仍是思考工具，不是按字数验收的表格。

### DAY18及之后怎样推进

- 如果能独立换输入调用C++函数，接下来1～2课开始vector类简单算法题，优先[LC1480一维数组的动态和](https://leetcode.com/problems/running-sum-of-1d-array/)；先教必要的“返回容器”和题目含义，再讲C++平台外壳，不等整门C++学完才刷题。
- 如果仍混淆函数定义与调用，先只补这个环节，Python每日LeetCode不暂停。引用、const和性能改进按实际需要逐个加入。
- 神经元的模型与样本关系验证稳定后，再学多个输入特征的加权和及权重列表。不会把今天的“样本列表”直接冒充“多输入神经元已经学会”。
- 原复习到期安排保留：DAY18 LC1，DAY19 LC217，DAY20 LC242，DAY21 LC387；若当天开启新题，旧题可先口述，忘了再重写。DAY32～35分别回访LC1/217/242/387。

项目继续沿既定方向：C++求和将成为训练日志分析器的一个可测试函数；预测样本函数将成为小型神经网络的数据调用入口。本阶段不重新寻找一套路线图或添加整仓阅读任务，已有GitHub参考只在完成自己的版本后按小模块对照。

## 十、我的DAY17回答

1.

2.

3.

4.

5.

LC387用时、提示使用情况、今天最卡的地方：
