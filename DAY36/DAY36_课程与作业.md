# DAY36｜按顺序找字母、读D2SLAM的四相机拆图、用两个数给图片打分

> 2026-11-09 修订。每个模块先看小例子，再动手。Python 65分钟，C++ 100分钟，模型 65分钟，整理 10分钟。[课后总结.md](课后总结.md)约10–15分钟，计入这240分钟。
>
> 课程依据见[学习与授课总约定](../学习与授课总约定.md)和[阶段计划](../DAY29-DAY39_阶段计划.md)。DAY35的五份代码示范和六道理论参考在[本课后半部分](#day35-answers)。

## DAY35评阅

| 提交 | 实际检查 | 评语 |
|---|---|---|
| Python 922 | 原脚本通过，另测19,304组合法输入 | 两个下标都只访问自己负责的奇偶位置，推进和停止正确。断言锁定了一种排列，另一种合法排列也应通过。 |
| Python 905 | 原脚本通过，另测21,844组输入 | 读位置扫描，写位置只在发现偶数后推进。DAY34会中断程序的断言已修正。接着用分区和元素次数来测试。 |
| C++ 02 | 本机 C++17 编译通过，120组整程序输入和类级断言通过 | 配置有效范围、失败后保留旧值、两次处理、空帧计数都正确。显式包含 `<vector>`，让文件直接声明自己的依赖。 |
| C++ 03 | 120组整程序输入和类级断言通过 | 两个实例各自维护配置和计数。两条警告来自保存后未使用的配置结果。图像处理过程可以省去中间副本。 |
| 模型 | 脚本通过，验证和测试求值前后参数一致 | 用验证集选出0.1，独立测试只评估选中模型。最终预测约8.99980和10.99972。省去未使用的 `old_loss`，每步可少遍历一遍训练数据。 |
| 理论六题 | 逐题读过 | 第4、5题完整正确，第1、2、6题各补一处解释，第3题修正对象计数和访问权限的关系。 |

905与922的断言要检查题目真正要求的性质。C++里“属于哪个对象”和“外部能否访问”是两个维度，具体对照见文末DAY35评语。今天用你已经会的结构体和像素列表，读D2SLAM实际怎么拆图。

本轮检查到DAY36，905、922已有实现正确的证据，88仍待今天重写后验证。模型三份数据的分工已经跑通，今天补双特征和Embedding接入。349排在后续专题，905与88的限时独立验收安排在DAY39。

## Python 新题 392｜用两根手指找字母（35分钟）

### 第一步　先在纸上做一遍

纸上有两行字母。上面是要找的 `s="ac"`，下面是给你挑字的 `t="baxcc"`。

~~~text
要找 s      a c
从 t 里挑   b a x c c
~~~

从下面一行左往右看。先找 `a`，看见 `b` 就跳过，找到 `a` 后接着往右找 `c`。最后能按顺序挑出 `a、c`，所以答案是 `True`。这些字母可以隔着几格，中间的 `x` 可以不要。题目把这样挑出来的字符串叫**子序列**。

如果要找的是 `"ba"`，而下面只有 `"ab"`，找到 `b` 时已经走到末尾，右边没有 `a` 了。尽管两个字母都出现过，答案仍是 `False`。题目只要真假，不用返回挑中的字母或它们的位置。[LeetCode 392 原题](https://leetcode.com/problems/is-subsequence/description/)

### 第二步　每根手指只做一件事

- 上面的手指指着**还缺哪个字母**。它在 `s` 上，位置记为 `need`。
- 下面的手指指着**现在看哪个字母**。它在 `t` 上，位置记为 `scan`。

下面这一格看完就走，匹配上时，上面的手指也往右一格。没匹配上时，上面的手指继续等同一个字母。

| 现在看 `t[scan]` | 还缺 `s[need]` | 看完这一格后的动作 |
|---|---|---|
| 下标0的 `b` | `a` | 跳过 `b`，还在等 `a` |
| 下标1的 `a` | `a` | 找到 `a`，接下来等 `c` |
| 下标2的 `x` | `c` | 跳过 `x`，还在等 `c` |
| 下标3的 `c` | `c` | 找到 `c`，上面已经找完，可以停 |

为什么遇到第一个合适的字母就能选？假设两个 `c` 都能接在刚找到的 `a` 后。选前面的 `c`，它右边保留的格子更多，后续需要的字母仍可以从那里找。每找到一个字母，我们都可以用同样的理由往下做。用两个位置分别记进度，这就是本题的**双指针**。

### 第三步　把两根手指写成代码

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
~~~

逐段对应刚才的动作。

1. 两个位置从 `0` 起，代表各自那一行的第一格。
2. `while` 先确认两根手指都有格子可指。比如 `s` 有两格，合法位置是 `0` 和 `1`，`need` 到 `2` 时就不能再读 `s[need]`。
3. `need += 1` 在 `if` 里面，只有找到了才移动。`scan += 1` 在 `if` 外面，不管这格有没有匹配，下面都换到下一格。
4. 最后只问上面找完了吗。`need` 从 `0` 起，每匹配一个字母加 `1`，等于 `len(s)` 时就找齐了。空串没有要找的字母，所以 `need` 一开始就等于 `len(s)`。如果下面先走完、上面还有字母没找到，比较结果就是 `False`。

下面每一格最多看一次，最多看 `len(t)` 格，所以时间是 `O(len(t))`。除了两个位置，没建一份随输入变长的新列表，额外空间是 `O(1)`。

关掉示范，把它重写到 `00_Python精讲重写_LeetCode392_判断子序列.py`。先跑表里这几组，再试 `("abc", "ahbgdc")` 应为真、`("axc", "ahbgdc")` 应为假。

| `s` | `t` | 预期 | 主要检查 |
|---|---|---|---|
| `"ac"` | `"baxcc"` | `True` | 可以跳过不需要的字母 |
| `"ba"` | `"ab"` | `False` | 有这些字母也要看顺序 |
| `"aaa"` | `"aa"` | `False` | `t` 的一格只能用一次 |
| `""` | `"abc"` 或 `""` | `True` | 没有要找的字母 |
| `"a"` | `""` | `False` | 没有格子可供查找 |

## Python 复习题 88｜把结果写回第一排（20分钟做，10分钟检查）

两排数都已经从小到大排好，允许相等。`nums1` 的前 `m` 格是真正要合并的数，后 `n` 格是留给结果的空位。程序里空位也写成0，所以要用 `m` 区分。比如 `nums1=[0,2,0]`、`m=2` 时，开头的0是数，末尾的0是空位。`nums2` 的 `n` 格全是要合并的数。

合并后，要让传进来的 `nums1` 本身变成排好的结果。这叫**原地修改**。函数完成修改后返回 `None`。目标是最多走过两排数各一遍，且不用一份新列表存整批结果。[LeetCode 88 原题](https://leetcode.com/problems/merge-sorted-array/description/)

写在 `01_Python专题复习_LeetCode88_原地合并.py`。先用原来的三步自己想。上一版有一个从第一排算出的下标，用去读了第二排。这次像392那样，把每个位置和它要读的那一排绑在一起，优先测两排长度不同的例子。

| 原来的 `nums1`、`m` | `nums2`、`n` | 改过的 `nums1` |
|---|---|---|
| `[4,5,6,0]`、3 | `[2]`、1 | `[2,4,5,6]` |
| `[2,0,0,0]`、1 | `[1,3,4]`、3 | `[1,2,3,4]` |
| `[0]`、0 | `[1]`、1 | `[1]` |
| `[1]`、1 | `[]`、0 | `[1]` |
| `[-1,0,2,0,0]`、3 | `[0,2]`、2 | `[-1,0,0,2,2]` |

也检查返回值是 `None`，并确认 `nums2` 的内容没变。

<details>
<summary>卡住约10分钟再看起步提示</summary>

在纸上把第一排画成 `[3,4,_]`，第二排画成 `[1]`。如果先把最小的1写进第一格，还没处理的3就被盖掉了。从最后的空格写就有地方放。第一轮看第一排最后一个真数4和第二排最后一个真数1，最大的4正好该放到第一排最后一格。之后只移动刚用掉的那一排的读位置，同时把写位置往左挪一格。

</details>

<details>
<summary>约20分钟仍卡住再看收尾提示</summary>

用只有一排还有数的情况检查。只剩第一排的数时，它们已经在第一排前面。只剩第二排的数时，它们还没写进第一排。读任何一排前，都先确认那一排还有数。Python 的 `-1` 也能读到末项，不能用它来试探是否读完。

</details>

<a id="day36-cpp"></a>

## C++｜D2SLAM 怎么把一张宽图拆回四张（100分钟）

### 1. 先在纸上切一张图

四个相机各给出一张两列宽、两行高的小图。传到程序里时，这四张图已经从左到右拼成了一张宽图。每个数字代表一个小格的亮度，也就是一个**像素**。十位数用来帮我们认出它来自哪一张图。

~~~text
列号        0   1 │  2   3 │  4   5 │  6   7
第 0 行    10  11 │ 20  21 │ 30  31 │ 40  41
第 1 行    12  13 │ 22  23 │ 32  33 │ 42  43
拼接顺序      0   │    1   │    2   │    3
~~~

整张图有8列、2行。四张图一样宽，所以每张占 `8 / 4 = 2` 列。要取第1块（从0数起，也就是第二张），就从第2列开始，每一行都取第2和第3列。

~~~text
20 21
22 23
~~~

想象盖一个长方形框，只留下框内的格子，这个操作叫**裁剪**。画框要知道四个数字，按顺序是起始列、起始行、宽度、高度。第二块就是 `(2, 0, 2, 2)`。

| 拼接顺序 `i` | 起始列 | 每一行取哪些列 |
|---|---|---|
| 0 | 0 | 0、1 |
| 1 | 2 | 2、3 |
| 2 | 4 | 4、5 |
| 3 | 6 | 6、7 |

取第 `i` 块之前跨过了 `i` 个小图宽，起始列就是 `i * 2`。四块都从第0行开始，都取原图的两行，因为图是左右并排的。

### 2. 把纸上的格子换成 C++ 列表里的位置

昨天用过 `std::vector<int>` 存像素。先抄完整的第0行，再抄完整的第1行，宽图在列表里就是下面这样。

~~~text
列表下标    0   1   2   3   4   5   6   7   8   9  10  11 ...
像素值     10  11  20  21  30  31  40  41  12  13  22  23 ...
~~~

怎么取第1行、第2列的22？先跨过前面完整的一行8格，再向右走2格，得到下标10。于是 **列表下标 = 行号 × 原图宽度 + 列号**。写成 C++ 时，`pixels[1 * 8 + 2]` 就是22。

取第二块时，先从下标2、3取20、21，再从下标10、11取22、23。若从下标2连续取四项，会拿到20、21、30、31，混进了下一块。写代码时，外层循环每次处理一行，内层循环取那一行中框住的几列。用已会的 `push_back` 把读到的数字放进小图自己的像素列表。

### 3. 回到 D2SLAM，读懂这五行

系统收到图像消息，就调用 `monoImageCallback`。这种由收到消息触发的函数叫**回调函数**。本地源码中，四路鱼眼相机配置 `FOURCORNER_FISHEYE`（鱼眼相机能拍到较宽的范围）把拼接图交给它。先看函数拿到宽图后做的这一步。 [d2frontend.cpp 第128–132行，接收入口在第384–388行](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2frontend/src/d2frontend.cpp)

~~~cpp
std::vector<cv::Mat> imgs;
const int num_imgs = 4;
for (int i = 0; i < 4; i++) {
  imgs.emplace_back(img(
      cv::Rect(i * img.cols / num_imgs, 0, img.cols / num_imgs, img.rows)));
~~~

1. `img` 是宽图。OpenCV 是源码里处理图像用的工具库，`cv::Mat` 是它表示图像用的类型。`img.cols` 读列数8，`img.rows` 读行数2。
2. `cv::Rect(x, y, width, height)` 就是刚才的框。把 `i=1` 代入，`i * img.cols / num_imgs` 得到2。四个参数正好是 `(2, 0, 2, 2)`。
3. `img(框)` 取出框里的小图。OpenCV 允许在图像对象后面这样加括号。今天读成“在 `img` 上取这一块”即可。
4. `imgs` 是存小图的列表，尖括号里的 `cv::Mat` 表示里面每项是一张图。`emplace_back` 在这里把刚取的小图加到末尾。所以 `imgs[1]` 对应从左数第二块。作业里用已经会的 `push_back` 追加。

取出框内区域的那一刻，OpenCV 只是让新图指向原图的那部分像素，像盖好框后透过框看。练习会把这些像素的值抄进另一个 `vector`，所以之后改小图的数字，原图不变。两者框选的位置一样。 [OpenCV 的 Mat 区域操作](https://docs.opencv.org/4.x/d3/d63/classcv_1_1Mat.html)

源码接下来会按需把彩色小图转为灰度图，再把小图和拍摄时刻等信息装成一个数据包，代码里叫 `StereoFrame`。下一课从这个包里装了什么开始。今天的0到3表示拼接图从左到右的顺序，项目后续另有字段记录相机编号。 [本地 StereoFrame 四图构造，第71–82行](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2common/include/d2common/d2frontend_types.h)

### 4. 实践02，裁出一张小图（约20分钟）

写在 `02_C++核心_D2SLAM按列裁剪.cpp`。沿用昨天结构体的写法，让 `Image` 存 `int width`、`int height` 和 `std::vector<int> pixels`。像素按行排列。实现 `Image crop_columns(const Image& source, int start_col, int crop_width)`。`const Image&` 表示借来读原图。从指定列开始，每行取 `crop_width` 列，返回与原图等高的小图。这个函数负责源码中 `img(cv::Rect(...))` 做的框选工作。

用本课开头的宽图，`crop_columns(source, 2, 2)` 应返回宽2、高2，像素 `[20, 21, 22, 23]`。再取最后两列，期望 `[40, 41, 42, 43]`。打印小图宽高和像素，再确认原图像素没变。本题传入有效的小图数据和裁剪范围，起始列至少为0，裁剪宽度大于0，框的右边不超出原图。

### 5. 实践03，把宽图拆成四张（约25分钟）

写在 `03_C++应用_D2SLAM拆分四相机图像.cpp`。复用02的 `Image` 和 `crop_columns`，实现 `std::vector<Image> split_views(const Image& source, int num_views)`。它对应源码的循环和 `imgs` 列表。先算一小块有多宽，再从左到右调用裁剪函数，依次把结果加进列表。

用同一张8列2行的宽图，按真实分支传入 `num_views=4`。期望四张都宽2、高2，顺序如下。

~~~text
第 0 块   [10, 11, 12, 13]
第 1 块   [20, 21, 22, 23]
第 2 块   [30, 31, 32, 33]
第 3 块   [40, 41, 42, 43]
~~~

再传 `num_views=2`，第二块应从第4列开始，像素为 `[30, 31, 40, 41, 32, 33, 42, 43]`。作业允许改变份数，这样可以检查公式是否真的随份数变。**练习约定**在计算块宽前检查份数为正、原图宽高为正、宽度能整除份数。份数为0、宽为6却要切成4块、空图这三种情况都返回空列表。用 `%` 看余数，先确认除数大于0再算。

从学习仓库根目录分别编译运行。两份程序各有一个 `main`。

~~~bash
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY36/02_C++核心_D2SLAM按列裁剪.cpp" -o /tmp/day36-crop
/tmp/day36-crop
clang++ -std=c++17 -Wall -Wextra -pedantic "DAY36/03_C++应用_D2SLAM拆分四相机图像.cpp" -o /tmp/day36-split
/tmp/day36-split
~~~

写完再打开源码，自己指出哪一段算起始列、哪一段取图、哪一段追加小图。C++ 两道理论题在[课后总结.md](课后总结.md)。

## 模型｜两张图一样亮，为什么分数可以不同（65分钟）

### 先用昨天的办法算

给两张图打分。它们的亮度都是4，其中一张有些杂点，噪声记为3，另一张干净些，噪声记为0。这些数字是这次练习给定的。

假设沿用昨天一个输入的计算，把亮度乘2，再加1。两张图都只给模型数字4，两次都得到 `2×4+1=9`。图里的杂点有差别，但模型拿到的数字一模一样，所以算出的结果也一样。

要让模型把这个差别算进去，就再给它一个数字。约定列表的第一格放亮度，第二格放噪声。两张图现在分别写成 `[4,3]` 和 `[4,0]`。亮度和噪声是这道题选出来的两项**特征**，就是拿去参与计算的数据。用这样一份有固定顺序的数字列表描述一张图，叫**特征表示**。这里“向量”先理解成这份按顺序排好的数字。[《神经网络与深度学习》第2.6节](../../学习资料/AI%20agent/神经网络与深度学习%20(邱锡鹏).pdf)

### 给两格数字分别定规则

还是拿刚才的评分做例子。我们规定亮度每增加1就加2分，噪声每增加1就扣1分，最后每张图再加1分。这三个数对应 `weight1=2`、`weight2=-1`、`bias=1`。乘在输入上的数叫**权重**，最后固定加上的数叫**偏置**。

| 图片 | 第一格的亮度贡献 | 第二格的噪声贡献 | 合起来加1 |
|---|---|---|---|
| `[4,3]` | `4×2=8` | `3×(-1)=-3` | `8-3+1=6` |
| `[4,0]` | `4×2=8` | `0×(-1)=0` | `8+0+1=9` |

先分别乘再相加，这一步叫**加权和**。公式只是把表里的步骤写短一点。

~~~text
预测分数 = 亮度 × 亮度权重 + 噪声 × 噪声权重 + 偏置
       = x₁ × w₁ + x₂ × w₂ + b
~~~

数学里的第一项 `x₁`，在 Python 列表里是 `features[0]`。第二项 `x₂` 是 `features[1]`。如果把 `[4,3]` 传成 `[3,4]`，模型就会按“亮度3、噪声4”来算，变成 `3×2-4+1=3`。程序只看位置，所以调用者和模型都得遵守同一顺序。

以后看到**点积**，可以回想表里“按位置分别乘，再相加”的部分。输入 `[4,3]` 和权重 `[2,-1]` 的点积是 `8-3=5`，算分数时再加偏置1。

昨天的类已经会用 `self.weight` 取出对象里保存的权重。今天把它扩展成两个权重属性，`forward(features)` 每次从传入列表取两个值，按位置和两个权重配对，算完返回一个数。这个“从输入算出结果”的动作就是**前向计算**。本课的权重由我们给定，调用时直接算分数。

### 手上只有档位名字时，先翻成两格数字

有时相机配置只给我们一个名称，比如“常规档”，而刚才的计算需要两个数。用一组数字代表一个名称，这组数字就是它的 **Embedding（嵌入向量）**。DAY19 的 `EmbeddingTable` 可以当一本小字典用。查“常规档”得到我们预先填好的 `[4,3]`，查“低噪档”得到 `[4,0]`。

两次 `forward` 分别找两个对象做事。先让查表对象读名字并给出列表，再让神经元读列表并给出分数。以常规档为例。

~~~text
"常规档" → 查表对象 → [4, 3] → 神经元 → 6
~~~

得到的整个 `[4,3]` 都交给神经元，第一格和第二格各有用途。本练习的表项是手填的示例值。以后遇到可训练的 Embedding，表里也是“一个名字对应一组数字”，那些数字可以在训练过程中调整。今天先跑通名字到分数这条路。

### 实践04｜先直接给数字，再接上查表（约25分钟）

写在 `04_模型实践_双特征与Embedding接入.py`。沿用 DAY19 的 `EmbeddingTable` 和它的 `forward(token)`。新建 `LinearNeuron2D(weight1, weight2, bias)`，让对象记住这三个数。它的 `forward(features)` 收到一个恰好有两项的列表，算出一个分数。

先只测神经元，确认 `[4,3]` 得到6、`[4,0]` 得到9。两组都对后，再加入查表。这样如果直接输入算对了、接表以后出错，可以先打印查出来的列表，看看是不是传错了。

| 自测 | 应看到什么 |
|---|---|
| 直接传入 `[4,3]`、`[4,0]` | 依次得6、9 |
| 分别查“常规档”“低噪档”，把查到的列表交给神经元 | 同样依次得6、9 |
| 传入 `[0,0]`、`[3,4]` | 依次得1、3 |
| 算完再看原输入 `[4,3]` 及对象的三个参数 | 仍为 `[4,3]` 和 `(2,-1,1)` |

<a id="day35-answers"></a>

## DAY35示范答案与逐题对照

以下示范保留你已做对的解法，主要改进断言、图像复制和损失记录。可以按需要展开。

<details>
<summary>00｜922 按奇偶位置排列</summary>

~~~python
class Solution:
    def sortArrayByParityII(self, nums):
        even_index = 0
        odd_index = 1

        while even_index < len(nums) and odd_index < len(nums):
            if nums[even_index] % 2 == 0:
                even_index += 2
            elif nums[odd_index] % 2 == 1:
                odd_index += 2
            else:
                nums[even_index], nums[odd_index] = nums[odd_index], nums[even_index]
                even_index += 2
                odd_index += 2
        return nums


solver = Solution()
for original in ([4, 2, 5, 7], [2, 3], [3, 2], [0, 1, 2, 3],
                 [2, 0, 3, 1], [2, 2, 1, 1]):
    working = original.copy()
    result = solver.sortArrayByParityII(working)

    assert result is working
    assert sorted(result) == sorted(original)
    for index, value in enumerate(result):
        assert index % 2 == value % 2
~~~

你的交换与推进逻辑和示范一致。比如对 `[4,2,5,7]`，`[4,5,2,7]` 和 `[2,7,4,5]` 都符合题意。参考先核对对象身份和元素次数，再逐格检查奇偶。测试里的 `sorted` 用于对照，算法自身仍为 O(n) 时间、O(1) 额外空间。

</details>

<details>
<summary>01｜905 按奇偶分区</summary>

~~~python
class Solution:
    def sortArrayByParity(self, nums):
        write = 0
        for read in range(len(nums)):
            if nums[read] % 2 == 0:
                nums[write], nums[read] = nums[read], nums[write]
                write += 1
        return nums


solver = Solution()
for original in ([3, 1, 2, 4], [0], [1, 3, 5], [2, 4, 6], [2, 1, 2, 1]):
    working = original.copy()
    assert working == original
    assert working is not original

    result = solver.sortArrayByParity(working)
    assert result is working
    assert sorted(result) == sorted(original)

    seen_odd = False
    for value in result:
        if value % 2 == 1:
            seen_odd = True
        else:
            assert not seen_odd
~~~

你的代码注释准确写出了读写职责。示范在见到第一个奇数后要求再也不出现偶数，同时验证元素次数。即使算法把某一组的顺序调整了，只要这两项成立就通过。`[2,4]` 中会发生自己与自己交换，最终内容仍相等。

</details>

<details>
<summary>02与03｜C++ 两份完整程序的公共部分</summary>

把下面公共部分与对应题的 `main` 放在同一文件。公共部分只需在各自文件开头放一次，每份程序都可单独编译。

~~~cpp
#include <iostream>
#include <vector>

struct ImageFrame {
    int camera_id = 0;
    double timestamp = 0.0;
    int width = 0;
    int height = 0;
    std::vector<int> pixels;
};

ImageFrame read_frame() {
    ImageFrame frame;
    std::cin >> frame.camera_id >> frame.timestamp >> frame.width >> frame.height;
    frame.pixels.resize(frame.width * frame.height);
    for (int& pixel : frame.pixels) {
        std::cin >> pixel;
    }
    return frame;
}

double mean_brightness(const ImageFrame& frame) {
    if (frame.pixels.empty()) {
        return -1.0;
    }
    double total = 0.0;
    for (int pixel : frame.pixels) {
        total += pixel;
    }
    return total / frame.pixels.size();
}

ImageFrame brighten_frame(const ImageFrame& source, int delta) {
    ImageFrame result = source;
    for (int& pixel : result.pixels) {
        pixel += delta;
        if (pixel > 255) {
            pixel = 255;
        }
    }
    return result;
}

class BrightnessProcessor {
private:
    int delta_ = 0;
    int count_ = 0;

public:
    bool configure(int delta) {
        if (delta < 0 || delta > 30) {
            return false;
        }
        delta_ = delta;
        return true;
    }

    int delta() const {
        return delta_;
    }

    int count() const {
        return count_;
    }

    ImageFrame process(const ImageFrame& source) {
        ImageFrame result = brighten_frame(source, delta_);
        ++count_;
        return result;
    }
};

void print_pixels(const ImageFrame& frame) {
    bool first = true;
    for (int pixel : frame.pixels) {
        if (!first) {
            std::cout << ' ';
        }
        std::cout << pixel;
        first = false;
    }
    std::cout << '\n';
}
~~~

你在02用 `const std::vector<int>&` 借入像素做得对。03改成 `const std::vector<int> pixels` 时，参数已经按值复制，`const` 只限制这个局部副本的写入。随后再拷贝 `pixels_copy` 就多复制一次。示范让 `brighten_frame` 只建立一份结果帧，再直接修改其中的像素。`times_stamp` 与 `timestamp` 只是命名差异。

**02的入口**

~~~cpp
int main() {
    const ImageFrame frame = read_frame();
    int delta = 0;
    std::cin >> delta;

    BrightnessProcessor processor;
    const bool configured = processor.configure(delta);
    processor.process(frame);
    const ImageFrame second = processor.process(frame);

    std::cout << configured << '\n';
    std::cout << processor.delta() << ' ' << processor.count() << '\n';
    std::cout << mean_brightness(frame) << ' ' << mean_brightness(second) << '\n';
    print_pixels(second);
    const bool invalid_configured = processor.configure(31);
    std::cout << invalid_configured << ' ' << processor.delta() << '\n';
}
~~~

你正确用同一原帧调用两次，也保护了非法配置后的状态。第一次只需要触发处理并增加计数，可以直接调用，避免持有一份之后不用的图像。最后一次配置返回0，旧增量仍为20。

**03的入口**

~~~cpp
int main() {
    const ImageFrame frame1 = read_frame();
    const ImageFrame frame2 = read_frame();
    int delta_a = 0;
    int delta_b = 0;
    std::cin >> delta_a >> delta_b;

    BrightnessProcessor a;
    BrightnessProcessor b;
    if (!a.configure(delta_a) || !b.configure(delta_b)) {
        return 1;
    }

    const ImageFrame a1 = a.process(frame1);
    const ImageFrame b1 = b.process(frame1);
    const ImageFrame a2 = a.process(frame2);

    std::cout << a.delta() << ' ' << a.count() << ' '
              << b.delta() << ' ' << b.count() << '\n';
    std::cout << mean_brightness(frame1) << ' ' << mean_brightness(a1)
              << ' ' << mean_brightness(b1) << '\n';
    std::cout << a2.camera_id << ' ' << a2.timestamp << ' '
              << mean_brightness(a2) << '\n';
    print_pixels(frame1);
}
~~~

你正确得到A计数2、B计数1，因为这题B确实处理了一帧。示范在配置失败时停止，直接使用返回值，避免 `conf_A` 与 `conf_B` 的两条未使用警告。题面保证合法增量，两种写法对规定输入的输出一致。

</details>

<details>
<summary>04｜模型 三份数据与学习率选择</summary>

~~~python
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


class LossEvaluator:
    def __init__(self, data, loss):
        self.data = data
        self.loss = loss

    def evaluate(self, model):
        total = 0.0
        for index in range(self.data.size()):
            x, y = self.data.get_item(index)
            total += self.loss.forward(model.forward(x), y)
        return total / self.data.size()


class GradientDescent:
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate

    def step(self, model, grad_weight, grad_bias):
        model.weight -= self.learning_rate * grad_weight
        model.bias -= self.learning_rate * grad_bias


def batch_gradient(data, model):
    grad_weight = 0.0
    grad_bias = 0.0
    for index in range(data.size()):
        x, y = data.get_item(index)
        error = model.forward(x) - y
        grad_weight += error * x
        grad_bias += error
    return grad_weight / data.size(), grad_bias / data.size()


class Trainer:
    def __init__(self, model, data, loss, optimizer):
        self.model = model
        self.data = data
        self.optimizer = optimizer
        self.evaluator = LossEvaluator(data, loss)

    def train(self):
        grad_weight, grad_bias = batch_gradient(self.data, self.model)
        self.optimizer.step(self.model, grad_weight, grad_bias)
        return self.evaluator.evaluate(self.model)

    def fit(self, epochs):
        history = [self.evaluator.evaluate(self.model)]
        for _ in range(epochs):
            history.append(self.train())
        return history


train = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
validation = RegressionDataset([-2, 3], [-3, 7])
test = RegressionDataset([4, 5], [9, 11])
loss = SquaredLoss()
validation_evaluator = LossEvaluator(validation, loss)
models = {}
validation_losses = {}

for rate in (0.0, 0.1):
    model = LinearNeuron(0, 0)
    trainer = Trainer(model, train, loss, GradientDescent(rate))
    history = trainer.fit(100)
    models[rate] = model

    before = model.weight, model.bias
    validation_losses[rate] = validation_evaluator.evaluate(model)
    assert (model.weight, model.bias) == before
    print(rate, history[0], history[-1], validation_losses[rate])

best_rate = min(validation_losses, key=validation_losses.get)
assert best_rate == 0.1
best_model = models[best_rate]
before = best_model.weight, best_model.bias
test_loss = LossEvaluator(test, loss).evaluate(best_model)
assert (best_model.weight, best_model.bias) == before
print("chosen", best_rate, "test loss", test_loss)
for index in range(test.size()):
    x, target = test.get_item(index)
    prediction = best_model.forward(x)
    assert abs(prediction - target) < 0.01
    print(x, prediction)
~~~

你用的 `min(val_losses, key=val_losses.get)` 正确。字典迭代给出学习率，`key` 让 `min` 按对应的验证损失比较，最后返回学习率这个键。示范延续你的数据流，在同一次遍历累加损失，并省去未使用的 `old_loss`。你已经检查了验证阶段的参数，参考也给测试阶段加上同一检查。验证损失约为14.5和2.52e-8，最终测试损失约为2.88e-8。

</details>

### 六道理论参考

1. **922下标**　`nums[2]=5` 放错了，偶数下标应放偶数。0与1分别加2可遍历各自那类位置，你的解释正确。905的 `write` 指向下一个应放**偶数值**的位置，`read` 读到偶数才推进 `write`。922是两个指定位置各自扫描，两格放错时才交换。
2. **905测试**　复制前提下，排序前后 `==` 都是 `True`，`is` 都是 `False`。这个结论正确。现有算法在 `[2,4]` 上执行的是同一位置交换，判断内容是否相等取决于最终结果。
3. **实例状态**　只有A调用两次时计数为2和0，和编程题中A、B均调用的情境不同。`this` 指向A，你答对了。即使计数改成 `public`，它仍是各自对象的成员，只是外部可以直接写，例如 `a.count_ = 99`，绕过计数规则。`private` 管访问权限。
4. **vector**　圆括号形式给4个0，大括号形式给元素4和0。`resize(4)` 后再追加7，长度是5，下标4为7。宽高字段修改后，程序需要主动同步容器长度。这题完整正确。
5. **数据职责**　你把三份数据的职责和数据值都对应对了。用测试误差反复选学习率，会让测试数据参与选择，最后报出的测试误差失去独立性，即使它没有直接参与梯度计算。
6. **评估手算**　预测3，半平方损失 `(3-7)²/2=8`，评估后仍是 `w=1、b=0`。你答对了数值与状态。再补原因，若在评估中执行 `step`，这条验证样本就参与了拟合，用它继续评价便混淆了训练和验证的职责。
