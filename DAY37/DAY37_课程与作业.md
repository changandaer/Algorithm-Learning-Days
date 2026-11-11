# DAY37｜C++ 分文件编译，拿 DAY36 的裁剪程序练手

今天的 C++ 主课是《C++ Primer Plus》第 9 章的分文件编译。先弄懂为什么要把类型、声明、实现和入口分开，再去 D2SLAM 找同一个写法。你会用已经写过的宽图做纯 C++ 练习，ROS 以读接口和口头解释为主。

| 学习内容 | 时间 |
|---|---:|
| 对照 DAY36 提交 15 分钟，C++ 教材与逐行小例子 50 分钟，D2SLAM 读码 20 分钟，ROS 理论 10 分钟，纯 C++ 实践 60 分钟，C++ 与 ROS 短答 10 分钟 | 165 分钟 |
| 恢复查表与前向 10 分钟，手算误差 20 分钟，独立实践 25 分钟，模型短答与复查 10 分钟 | 65 分钟 |
| 查看 Git 差异，保存运行结果 | 10 分钟 |

[学习总约定](../学习与授课总约定.md) · [阶段计划](../DAY29-DAY39_阶段计划.md) · [课后总结](课后总结.md)

## 1. 先看你 DAY36 的程序做了什么

| 提交 | 检查结果 | 这次怎样接着做 |
|---|---|---|
| C++ 02 裁一块 | 原样运行得到 `2 2` 和 `40 41 42 43`。你已经能用 `const Image&` 读原图，用结构体把结果交出来。 | `source.width` 应是 8。你的两段循环刚好能取两行。今天换成三行，验证能根据图的实际高度处理。 |
| C++ 03 拆四块 | 输入 4，第一块传入 0。原来的 `(start_col-1)*2` 会得出 -2，运行时读到像素列表外。 | 保留“先建四个位置，再用下标填”的思路。先求这一块从哪列开始，再把列号交给裁剪函数。 |
| 模型 04 | 三个属性已存进对象，两个乘积也写出来了。实测 `forward([4,3])` 在裸写的 `bias` 处报 `NameError`。查表与测试调用待补。 | 先在两个不同偏置的实例上验证 `self.bias`，再加查表和误差计算。 |
| 392、88 和理论短答 | 两份 Python 文件只有题意注释，理论作答区空白。 | 参考答案放在文末，等你通知恢复算法时再用。 |

想找 DAY32 的检查、五项代码示范和六道理论参考，可以回到 [DAY33 课件第六节](../DAY33/DAY33_课程与作业.md)。今天直接用其中的 `const&`，借原图和消息来读，再单独创建结果。

## 2. 教材精讲｜把一个文件里的程序拆开（50 分钟）

**先修。** DAY29 已见过函数声明和定义，DAY32 用 `const&` 借看数据，DAY34 用结构体和 `vector` 放图像。DAY36 这些东西都在同一个 `.cpp`。今天学会把它们分到几个文件里，再一起编译运行。

《C++ Primer Plus》第 9 章用 `coordin.h`、`file1.cpp`、`file2.cpp` 把坐标的数据类型、计算函数和程序入口分开。先看书内第 447–453 页（PDF 第 462–468 页），特别是第 450 页图 9.1。下面用你熟悉的图像宽高做一个更小的同类例子。 [指定教材](<../../学习资料/C++/C++ Primer Plus, 6th edition (Stephen Prata).pdf>)

### 第一份文件告诉两边，函数应该怎样用

`shape.h`

~~~cpp
#pragma once

struct Shape {
    int width;
    int height;
};

int pixel_count(const Shape& shape);
~~~

- `struct Shape { ... };` 定义一种数据长什么样。以后写 `Shape small{8, 2};` 才创建一份具体的数据。这里两份 `.cpp` 都需要认识 `Shape`，所以放在共用的头文件。
- `int pixel_count(const Shape& shape);` 以分号结尾，是**函数声明**。从右边往回看，`const Shape&` 借一份尺寸来读，`shape` 是函数里用的名字，左边的 `int` 是计算结果的类型。你在 DAY32 见过这类传参。
- `#pragma once` 是本地 D2SLAM 常见的防重复包含写法。编译同一份 `.cpp` 时，如果通过两条路径遇到同一个头文件，就只处理一遍。教材第 451 页用 `#ifndef`、`#define`、`#endif` 达到同样目的。今天认得这两种写法即可。

### 第二份文件给出计算步骤

`shape.cpp`

~~~cpp
#include "shape.h"

int pixel_count(const Shape& shape) {
    return shape.width * shape.height;
}
~~~

`#include "shape.h"` 让这一份 `.cpp` 也读同一套类型和接口。带花括号、写出计算步骤的这段是**函数定义**。左边的返回类型和参数类型要与声明对应。只在这一份 `.cpp` 里给普通函数写实现，调用方通过头文件知道怎么用它。

### 第三份文件是入口，负责调用和观察结果

`main.cpp`

~~~cpp
#include <iostream>
#include "shape.h"

int main() {
    const Shape small{8, 2};
    std::cout << pixel_count(small) << '\n';
}
~~~

`<iostream>` 是标准库头，`"shape.h"` 是自己写的头。两行 `#include` 分别提供输出和函数调用需要的信息。运行时 `main` 把 `small` 交给 `pixel_count`，函数读到 8、2，返回 16。把输入改成 `{12, 3}`，应输出 36。先预测，再看程序。

### 编译过了，为什么还会找不到函数？

把三个小文件放在单独的临时目录后，可以跟着教材的图运行下面三步。这里用 `demo_main.o` 等名字区分示范的中间文件和当天作业。

~~~bash
c++ -std=c++17 -c main.cpp -o demo_main.o
c++ -std=c++17 -c shape.cpp -o demo_shape.o
c++ demo_main.o demo_shape.o -o shape_demo
./shape_demo
~~~

1. `-c` 表示先停在编译阶段。读头文件后，编译器知道 `main` 可以用一份 `Shape` 调用这个函数，于是生成 `demo_main.o`。可以把 `.o` 理解为一件已经翻译好的零件。
2. 另一份 `.cpp` 同样单独翻译。函数的计算步骤在 `demo_shape.o` 里。两次命令的 `-o` 都指定输出的文件名。
3. **链接**负责把两个零件合起来，给调用找到实现。如果只交 `demo_main.o`，Mac 上会看到 `Undefined symbols`，其中会提到 `pixel_count`。如果调用时把函数名拼错，通常第一步就会提示未声明。两个错误分别发生在不同环节。

今天练习的头文件会放图像类型和函数声明，实现文件会放裁剪函数体，入口会放测试。你写过的行列计算，搬到另一份文件后，计算本身仍然一样。

## 3. 到 D2SLAM 找出同一个写法（20 分钟）

看同一个函数 `processStereoframe` 的三处。今天只用这几行辨认声明、定义与调用。它接收的 `StereoFrame` 可以先理解成同一批图像的信息包。

| 在哪里 | 摘录 | 你现在能认出的写法 |
|---|---|---|
| `d2frontend.h` 第 72 行 | `void processStereoframe(const StereoFrame & stereoframe);` | 类里面的声明，`void` 表示没有返回值，`const StereoFrame&` 借来一批图供函数读取。 |
| `d2frontend.cpp` 第 200 行 | `void D2Frontend::processStereoframe(const StereoFrame &stereoframe) {` | 有函数体的是定义。前缀 `D2Frontend::` 标明这份定义属于哪个类。你 DAY35 把方法写在类里时，类的花括号已经交代了归属。 |
| 同一份 `.cpp` 第 163 行 | `processStereoframe(*sframe);` | 调用。这里先用 `*` 取出指针指向的帧对象，再交给函数的引用参数。智能指针的寿命问题后续再学。 |

回到 `d2frontend.cpp` 第 2 行，能找到它包含的头文件。再到这个包的 `CMakeLists.txt` 第 94–101 行，能看到它把 `src/d2frontend.cpp` 列为库的一份源文件。这里把库理解成给其他程序复用的编译产物即可。 [前端头文件](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2frontend/include/d2frontend/d2frontend.h) · [前端实现与调用](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2frontend/src/d2frontend.cpp) · [构建清单](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2frontend/CMakeLists.txt)

试着合上课件回到这两个文件，找到三处并用自己的话解释。DAY38 会沿用「先找声明，再找实现与调用」的方法，看同名的 `getImageFromMsg` 为什么有多个版本。

### ROS 只读一行，弄清谁收到什么（10 分钟）

在同一份 `d2frontend.cpp` 的四相机分支看第 386–388 行。这是现有源码，用来练读法。

~~~cpp
image_sub_single =
    it_->subscribe(params->image_topics[0], 10,
                   &D2Frontend::monoImageCallback, this, hints);
~~~

- **话题**是一个有名字的数据通道，**消息**是通道上传的一份数据。**节点**是 ROS 中负责具体工作的参与者。订阅就是告诉 ROS“我想接收这个通道上的数据”。此处通道名来自 `params->image_topics[0]`，10 是等待处理的接收队列大小。
- **回调**是收到消息时由 ROS 调用的函数。这里的 `&D2Frontend::monoImageCallback` 指定哪个成员函数，`this` 指当前前端对象。这个 `&` 是取地址，和 `const StereoFrame&` 里声明引用的 `&` 看位置区分。最后的 `hints` 是传输设置。
- `monoImageCallback` 先收到一张拼好的宽图。裁剪发生在这个回调里，四张图随后放进帧包，后面的 `processStereoframe` 接收的是这一批图。SLAM 前端可以利用连续画面中认得出的同一个点，为之后估计相机怎么动提供线索。 [前端回调，第 110–145 行](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2frontend/src/d2frontend.cpp) · [ROS 基础讲义，第 11 页](../../学习资料/C++/ROS/1.1_机器人操作系统.pdf)

## 4. 纯 C++ 实践｜给 DAY36 的裁剪程序分文件（60 分钟）

### A．把你写过的计算搬进三份文件（25 分钟）

| 文件 | 你要写的内容 |
|---|---|
| [frame_input.h](C++练习/frame_input.h) | 写 `Image`（字段为 `width`、`height`、`pixels`）和两个函数的声明。按教材小例子加上头文件防重复包含。 |
| [frame_input.cpp](C++练习/frame_input.cpp) | 先包含自己的头文件。把 DAY36 的裁剪和拆图函数搬过来，用实际宽高修好下标。 |
| [main.cpp](C++练习/main.cpp) | 包含同一份头文件，构造两份正常图与坏图，自己写调用、断言和简短输出。 |

先用这张 DAY36 宽图做一次纸面检查。列号从 0 开始。

~~~text
列     0  1 | 2  3 | 4  5 | 6  7
第0行 10 11 |20 21 |30 31 |40 41
第1行 12 13 |22 23 |32 33 |42 43
~~~

第 2 块的起始列为 2，输出宽也为 2。第 0 行读下标 2、3，第 1 行先跳过一整行 8 个数，再读下标 10、11。**原图宽用来找行的开头，裁剪宽用来决定每行读几个。** 换成三行时，第三行从 `2 * source.width` 找起。

- `Image crop_columns(const Image& source, int start_col, int crop_width)` 接收已经检查过的原图和有效范围，返回一张小图。保留 DAY36 的结构体和容器思路。先验 `crop_columns(source, 2, 2)` 得到 `[20,21,22,23]`。
- `std::vector<Image> split_views(const Image& source, int num_views)` 负责检查输入并复用裁剪。宽高各在 1 到 4096 之间，像素数等于宽乘高，块数大于 0，原图宽能整除块数时，从左到右返回小图。遇到坏图或无效块数，返回空列表。尺寸先检查再相乘，块数先检查再取余。比较像素数量时，可以把已经确认的正整数转成 `pixels.size()` 使用的数量类型，例如 `static_cast<std::size_t>(8 * 2)` 得到 16，使用时包含 `<cstddef>`。

### B．分开编译，故意少链接一份，再用不同图验证（35 分钟）

在仓库根目录进入练习目录，等 `main` 确实调用了 `split_views` 或 `crop_columns` 后再运行。第三条 `c++` 命令是故意少给一个 `.o` 的实验。

~~~bash
cd DAY37/C++练习
c++ -std=c++17 -Wall -Wextra -Wpedantic -c main.cpp -o /tmp/day37_main.o
c++ -std=c++17 -Wall -Wextra -Wpedantic -c frame_input.cpp -o /tmp/day37_frame.o
c++ /tmp/day37_main.o -o /tmp/day37_missing
c++ /tmp/day37_main.o /tmp/day37_frame.o -o /tmp/day37_frame_input
/tmp/day37_frame_input
~~~

先断言列表大小，再使用下标。比如先写 `assert(views.size() == 4);`，再检查 `views[1].pixels`。可以把预期值放进单独的 `std::vector<int> expected{20, 21, 22, 23};`，再做相等比较。使用 `assert` 时包含 `<cassert>`。用 `empty()` 检查坏图是否得到空列表。

| 测试数据 | 预期结果 |
|---|---|
| 上面的 8×2 宽图，切 4 块 | 四张 2×2，依次是 `[10,11,12,13]`、`[20,21,22,23]`、`[30,31,32,33]`、`[40,41,42,43]` |
| 12×3 宽图，像素从 0 到 35，切 4 块 | 四张 3×3，第二张是 `[3,4,5,15,16,17,27,28,29]` |
| 6×1 有 6 个数但切 4 块；8×2 只有 15 个数；有效图但块数传 0 | 各返回空列表，原图数据保持原样 |

留下漏链接的一行报错、补上文件后的结果和至少一条坏图的表现。若卡在旧下标，先展开文末 DAY36 的裁剪示范，对着两行数字走一遍，再回到自己的实现。

## 5. Python 模型｜同一批预测，怎样量出差多少？

### 先把 DAY19 的查表接回 DAY36

先用你已经写过的 `EmbeddingTable.forward(token)`。它用档位名查出两格数字。这里约定第一格表示亮度，第二格表示噪声。两个数字交给 `LinearNeuron2D.forward(features)`，按对应的权重相乘，再加偏置。表项是人为设置的，这一课做的是前向和评估。

~~~text
"常规档" → 查表 [4,3] → 2×4 + (-1)×3 + 1 → 6
"低噪档" → 查表 [4,0] → 2×4 + (-1)×0 + 1 → 9
~~~

`__init__(self, ..., bias)` 中的 `bias` 是创建对象那一刻传进来的值。`self.bias = bias` 把它保存到**当前对象**。`forward` 里的 `self.bias` 再从同一个对象取出来。换成偏置为 0 的另一个对象时，相同的 `[4,3]` 应得 5。这是判断当前实例是否用对的一个小测试。 [DAY19 作业](../DAY19/04_模型实践_Embedding输入表示.py) · [DAY36 双特征代码](../DAY36/04_模型实践_双特征与Embedding接入.py)

### 为什么报告两种误差？

用预测减真实值，知道差多少和偏哪边。若直接把有正有负的差值平均，大小相同的正负差会互相抵掉。**MAE（平均绝对误差）**先把每个差取绝对值再平均，回答“平均差几分”。**MSE（均方误差）**把差平方再平均，差距大的样本占得更重。

| 预测 | 真实 | 逐项差值 | MAE | MSE |
|---|---|---|---|---|
| `[6,9]` | `[7,6]` | `[-1,3]` | `(1+3)/2 = 2` | `(1+9)/2 = 5` |
| `[6,9]` | `[6,7]` | `[0,2]` | `1` | `2` |

DAY35 的平均半平方损失给每个平方乘了 0.5，同样的预测下是 MSE 的一半。这次模型只出分并算指标。将来评价机器人定位时，判断大偏差该占多重也是一个具体的工程选择。 [《神经网络与深度学习》第 2.7 节评价指标，书内第 45–47 页](<../../学习资料/AI agent/神经网络与深度学习 (邱锡鹏).pdf>)

### 实践 04

在 [模型练习文件](04_模型实践_从Embedding到MAE和MSE.py) 复用两类，先验证直接喂 `[4,3]` 得 6，再验证查表路径得到 `[6,9]`。自己写 `mean_absolute_error(predictions, targets)` 与 `mean_squared_error(predictions, targets)`，输入是两个非空、等长的数字列表，返回单个平均值。可用 `abs(-3)` 得 3，`(-3) ** 2` 得 9。沿用逐项累加、最后除以样本数的方法。断言表里两个样例都正确，预测完全一致时两指标为 0，计算前后模型权重和偏置仍是 `(2,-1,1)`。

## 6. 完成后留下什么

- 纯 C++ 三文件、两组正常图和坏输入的断言、漏链接与修复的实际输出。
- Python 的误差计算与断言，以及 [课后总结](课后总结.md)。ROS 只回答现有接口的读法。
- 在仓库根目录用 `git status --short` 查看改动。对于已经纳入 Git 的文件，用 `git diff -- DAY37` 核对；新文件直接在编辑器核对。

<a id="day36-answers"></a>

## DAY36 五项示范与理论参考

两道算法文件留白，以下是补练参考。C++示范集中解释原图宽、输出宽和起始列的区别，供核对已有实现。

<details>
<summary>00｜392 判断子序列</summary>

~~~python
class Solution:
    def isSubsequence(self, s, t):
        need = 0
        scan = 0
        while need < len(s) and scan < len(t):
            if s[need] == t[scan]:
                need += 1
            scan += 1
        return need == len(s)


solver = Solution()
assert solver.isSubsequence("ab", "axbb") is True
assert solver.isSubsequence("ba", "ab") is False
assert solver.isSubsequence("aaa", "aa") is False
assert solver.isSubsequence("", "") is True
assert solver.isSubsequence("a", "") is False
~~~

`scan` 读完一格必走。`need` 只在这格匹配时前进。以后补练时先在纸上标出这两个下标分别属于谁。

</details>

<details>
<summary>01｜88 合并两个有序数组</summary>

~~~python
class Solution:
    def merge(self, nums1, m, nums2, n):
        left = m - 1
        right = n - 1
        write = m + n - 1

        while right >= 0:
            if left >= 0 and nums1[left] > nums2[right]:
                nums1[write] = nums1[left]
                left -= 1
            else:
                nums1[write] = nums2[right]
                right -= 1
            write -= 1


solver = Solution()
for nums1, m, nums2, expected in (
    ([4, 5, 6, 0], 3, [2], [2, 4, 5, 6]),
    ([2, 0, 0, 0], 1, [1, 3, 4], [1, 2, 3, 4]),
    ([0], 0, [1], [1]),
    ([1], 1, [], [1]),
    ([-1, 0, 2, 0, 0], 3, [0, 2], [-1, 0, 0, 2, 2]),
):
    saved = nums2.copy()
    assert solver.merge(nums1, m, nums2, len(nums2)) is None
    assert nums1 == expected
    assert nums2 == saved
~~~

比两个未放的最大值，从尾部往前写。`left` 永远读 `nums1`，`right` 永远读 `nums2`，`write` 只写 `nums1`。第二排耗尽就结束，第一排还剩的数字已在正确的位置。这个状态对应 DAY33 尝试时混用的下标。

</details>

<details>
<summary>02 与 03｜两份 C++ 示范</summary>

把公共部分（含 `print_image`）放在相应的 `main` 前，能分别编译为两份程序。03 还需要下方的 `split_views`。裁剪函数接收尺寸正确、范围有效的图，DAY37 会在拆分函数入口补图像尺寸与像素数量的检查。

~~~cpp
#include <cassert>
#include <iostream>
#include <vector>

struct Image {
    int width;
    int height;
    std::vector<int> pixels;
};

Image crop_columns(const Image& source, int start_col, int crop_width) {
    Image result{crop_width, source.height, {}};
    for (int row = 0; row < source.height; ++row) {
        for (int offset = 0; offset < crop_width; ++offset) {
            const int col = start_col + offset;
            const int index = row * source.width + col;
            result.pixels.push_back(source.pixels[index]);
        }
    }
    return result;
}

void print_image(const Image& image) {
    std::cout << image.width << ' ' << image.height << '\n';
    for (int pixel : image.pixels) {
        std::cout << pixel << ' ';
    }
    std::cout << '\n';
}
~~~

**02 的入口**

~~~cpp
int main() {
    const Image source{8, 2, {10, 11, 20, 21, 30, 31, 40, 41,
                              12, 13, 22, 23, 32, 33, 42, 43}};
    const Image second = crop_columns(source, 2, 2);
    assert(second.width == 2 && second.height == 2);
    assert((second.pixels == std::vector<int>{20, 21, 22, 23}));
    const Image last = crop_columns(source, 6, 2);
    assert((last.pixels == std::vector<int>{40, 41, 42, 43}));
    assert(source.pixels[2] == 20 && source.pixels[10] == 22);
    print_image(second);
    print_image(last);
    const Image taller{3, 3, {10, 11, 12, 20, 21, 22, 30, 31, 32}};
    assert((crop_columns(taller, 1, 1).pixels == std::vector<int>{11, 21, 31}));
}
~~~

你的版本知道第二行要跨过8格，不过把行数和每行宽度都写死了。`source.width` 表示原图每行多长，`crop_width` 表示每行取多长，`start_col` 已经是列号。输入的像素列表长16且高2，源图宽8。用真实尺寸设置它后，还要让输出宽设成 `crop_width`。三行高的测试能检查是否每行都处理到了。

**03 的拆分函数和入口**

~~~cpp
std::vector<Image> split_views(const Image& source, int num_views) {
    if (num_views <= 0 || source.width <= 0 || source.height <= 0 ||
        source.width % num_views != 0) {
        return {};
    }
    const int part_width = source.width / num_views;
    std::vector<Image> views(num_views);
    for (int i = 0; i < num_views; ++i) {
        views[i] = crop_columns(source, i * part_width, part_width);
    }
    return views;
}

int main() {
    const Image source{8, 2, {10, 11, 20, 21, 30, 31, 40, 41,
                              12, 13, 22, 23, 32, 33, 42, 43}};
    const auto four = split_views(source, 4);
    assert(four.size() == 4);
    assert((four[0].pixels == std::vector<int>{10, 11, 12, 13}));
    assert((four[1].pixels == std::vector<int>{20, 21, 22, 23}));
    assert((four[2].pixels == std::vector<int>{30, 31, 32, 33}));
    assert((four[3].pixels == std::vector<int>{40, 41, 42, 43}));
    for (const Image& view : four) {
        print_image(view);
    }
    const auto two = split_views(source, 2);
    assert((two[1].pixels == std::vector<int>{30, 31, 40, 41, 32, 33, 42, 43}));
    assert(split_views(source, 0).empty());
    assert(split_views({6, 1, {0, 1, 2, 3, 4, 5}}, 4).empty());
    assert(split_views({0, 0, {}}, 4).empty());
}
~~~

预先开好 `views` 再按位置写可以保留。关键是把块号 `i` 换成起始列 `i * part_width` 后再传入，并使用原图宽算块宽。你的现版第一轮会用到负下标，编译成功也可能在运行时读出边界。

</details>

<details>
<summary>04｜双特征前向和查表</summary>

~~~python
class EmbeddingTable:
    def __init__(self, vectors):
        self.vectors = vectors

    def forward(self, token):
        return self.vectors[token]


class LinearNeuron2D:
    def __init__(self, weight1, weight2, bias):
        self.weight1 = weight1
        self.weight2 = weight2
        self.bias = bias

    def forward(self, features):
        return self.weight1 * features[0] + self.weight2 * features[1] + self.bias


table = EmbeddingTable({"常规档": [4, 3], "低噪档": [4, 0]})
model = LinearNeuron2D(2, -1, 1)
features = table.forward("常规档")
assert model.forward([4, 3]) == 6
assert model.forward([4, 0]) == 9
assert model.forward(features) == 6
assert model.forward(table.forward("低噪档")) == 9
assert model.forward([0, 0]) == 1
assert model.forward([3, 4]) == 3
assert features == [4, 3]
assert (model.weight1, model.weight2, model.bias) == (2, -1, 1)
~~~

你的两个乘积和三个属性都写对了。最后一项改成 `self.bias`，然后按“直接数字、查表结果”的顺序测试。构造时的形参 `bias` 只在那个方法调用内可用，后续方法读取对象的属性。

</details>

### DAY36 理论参考

1. 392已匹配 `a` 后，遇到 `x` 只移动 `scan`，因为仍在等 `b`。空 `s` 返回 `True`。
2. 88的两个读位置从2和0开始。读6与2，先把6写到 `nums1[3]`。第二排如果先用完，第一排余项已在前部。
3. `i=1` 时框参数是 `(2,0,2,2)`，`i * img.cols / num_imgs` 给出起始列2。小图存到 `imgs[1]`。
4. 第二块要读下标2、3、10、11。下标4和5在第一行的第三块，连续读会串到另一台相机。6列拆4块先检查能否整除，按练习约定返回空列表。
5. 只给相同亮度时，两张图给模型的输入相同，计算结果相同。查表得到整份列表后按亮度、噪声分别乘对应权重。这里的表项是人给的。
6. `[4,2]` 得 `8-2+1=7`。`[2,4]` 得 `4-4+1=1`。调换后每个值被当成另一项特征，乘到的权重也变了。
