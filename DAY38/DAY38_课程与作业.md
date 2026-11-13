# DAY38｜同一个函数名怎样选版本，验证损失又是怎样算出来的？

C++ 接着 DAY37 的三文件程序，学习《C++ Primer Plus》第 8 章的函数重载，再到 D2SLAM 找同名函数的不同接口。Python 从 DAY35 的单输入模型和验证集继续，沿你自己的代码把“一条预测”走到“一份验证结果”。

| 内容 | 时间 |
|---|---:|
| DAY37 讲评 20 分钟，C++ 逐行讲解 40 分钟，D2SLAM 读码 20 分钟，纯 C++ 实践 65 分钟，ROS 理论 10 分钟，C++ 短答 10 分钟 | 165 分钟 |
| 重走 DAY35 数据与调用 15 分钟，逐条损失手算 10 分钟，解释评估与选模型 10 分钟，模型实践 25 分钟，模型短答 5 分钟 | 65 分钟 |
| 看运行结果与 Git 差异 | 10 分钟 |

[学习总约定](../学习与授课总约定.md) · [阶段计划](../DAY29-DAY39_阶段计划.md) · [理论作答位置](课后总结.md)

<a id="day37-review"></a>
## 一、DAY37 评阅

### 代码已经修好的地方

你的 `crop_colum` 已经按 `row * source.width + col` 读每一行，返回的小图也使用 `crop_width` 作为宽度。DAY36 的负下标和只处理两行的问题已经修好。`crop_colum` 这个名字在声明、定义、调用中一致，能正确工作，本课示范也沿用这个名字。

三份文件原样编译成功，你写在 `main` 中的四块像素断言全部通过。教师另外换宽度 1—24、高度 1—5、块数 0—8，共 1,080 组组合，合法图的拆分和无效块数处理均通过，输入像素保持原样。这是教师的正确性补测，闭卷组织程序和实际调试过程仍看你的提交记录。

### 还需要补的两处

| 位置 | 实际检查 | 下一步怎样补 |
|---|---|---|
| `frame_input.h` | 你能解释防重复包含，但文件里还没有写。教师让同一份 `.cpp` 包含它两次，编译报 `redefinition of 'Image'`。 | 在头文件顶部加 `#pragma once`，再试一次重复包含。它只解决同一份编译中的重复读取问题。 |
| `split_views` 的入口 | 你检查了块数、正尺寸和能否整除。教师传入 8×2、只有 15 个像素的图，内存检查报 `heap-buffer-overflow`。 | 补宽高 1—4096、像素数等于宽乘高的检查。先检查范围，再计算乘积，然后才能进入裁剪。 |
| `main.cpp` 的验证记录 | 提交只保留了 8×2 图的四项断言，三行图、坏图与漏链接日志待补。 | DAY38 继续用同一程序补这几种输入，再加重载。 |
| Python 模型文件 | 文件只有题目说明，尚无 DAY37 实现。 | 本课从你已写通的 DAY35 模型继续。DAY37 的示范放在末尾供查阅。 |

### 理论回答逐题看

1. **三文件分工和重复包含的路径解释正确。** 你举的 `a.h`、`b.h` 都包含同一个头的例子，说明理解了问题出现在哪里。接下来把这个理解落实到头文件。
2. **源码定位题留白。** 文末给声明、定义、调用的实际位置。DAY38 再用同样方式读重载。
3. **声明供编译、实现参与链接的主线正确。** “编译只看语法”需要补充。编译还会检查函数名是否可见、参数是否匹配、类型是否能使用。你没有在回答中写三行图的下标和实际报错日志，这两项保留待验。
4. **话题和当前对象的判断正确。** `monoImageCallback` 在这里是 `D2Frontend` 的成员函数。`&D2Frontend::monoImageCallback` 取它的地址，`this` 给出具体对象。`subscribe` 本身可以使用模板机制，回调在此处的身份是成员函数。
5. **两个偏置的计算留白。** 文末参考结果是 6 和 5。
6. **误差计算留白。** 参考结果和完整代码在文末。DAY38 先把 DAY35 已用过的半平方损失算透，再逐步接回其他指标。

当前结论是 C++ 的分文件与裁剪主体已有正确性证据，重点补入口检查和运行记录。模型的 DAY35 程序本次复跑正确，说明可以拿它作为继续讲解的起点。

## 二、C++ 主课｜同名函数，看调用处给了什么（40 分钟）

### 先接 DAY37 的头文件

昨天你给编译器看过这一条声明。

~~~cpp
std::vector<Image> split_views(const Image& source, int num_views);
~~~

调用 `split_views(source, 4)` 时，你明确说“把这张图切成四份”。现在想在最常用的四相机场景里直接写 `split_views(source)`，并保留切两份、切其他数量的入口。给同一种工作准备不同参数的入口，就会用到**函数重载**。

主教材第 8 章 Function Overloading，书内第 412—415 页，对应 PDF 第 427—430 页。先看第 412—414 页的参数匹配和返回类型规则。 [《C++ Primer Plus》第 6 版](<../../学习资料/C++/C++ Primer Plus, 6th edition (Stephen Prata).pdf>)

### 用一个小例子读清参数和调用

先看与图像有关、但更小的计算。假设头文件中已经声明下面两种用法。

~~~cpp
int pixel_count(int width, int height);
int pixel_count(const Image& source);
~~~

同名是因为两者都在算像素个数。第一种由调用者给宽高，第二种从已有图像里读宽高。实现可以这样逐行看。

~~~cpp
int pixel_count(int width, int height) {
    return width * height;
}

int pixel_count(const Image& source) {
    return pixel_count(source.width, source.height);
}
~~~

第一份函数体负责真正的乘法。第二份只读出两个字段，再交给第一份，乘法规则集中在一处。第二份里的调用有两个整数参数，所以会走到上面的两参数版本。

~~~cpp
Image source{8, 2, {}};
int first = pixel_count(8, 2);     // 两个 int，得到 16
int second = pixel_count(source); // 一个 Image，得到 16
~~~

这时 `source` 只用来演示读尺寸，正式裁剪还要检查它是否真的装了相应数量的像素。你在 DAY38 作业中要做同样的事，把“只传图”的拆分入口交给“传图与块数”的已有实现。

### 编译器靠什么分辨版本？

先看参数的数量、类型和顺序。教材把这些用于区分入口的信息称为函数签名。参数变量的名字不会让它变成另一个版本，例如把声明中的 `source` 改叫 `image`，仍是同一个接口。

D2SLAM 也会出现参数数量相同、类型不同的重载。例如一份参数是图像消息本身，另一份是指向只读图像消息的共享指针。两种东西类型不同，编译器可以据此选择。匹配过程中还可能发生类型转换，本课的调用先使用能直接匹配的类型。

如果只把返回类型从 `int` 改成 `double`，同时函数名、参数都一样，会在编译时报错。把结果存进 `double result` 也不能靠这个变量替调用挑选版本。先由调用处确定要调哪个函数，才能拿到它的结果。

### 你的 DAY29 提问，在这里再走一次

你当时问过，能否根据用户输入了多少数据，自动决定调哪个 `count_over`。编译器处理的是源代码里写好的调用，例如 `split_views(source)` 或 `split_views(source, parts)`。运行时读入 `parts=2` 或 `parts=4`，后一条调用始终有两个参数，只是第二个值改变了。

如果想让键盘输入决定走哪一种调用，可以先读入选择，再用 `if` 执行相应的调用语句。这和编译器判断一条调用匹配哪个版本，是两个相接的步骤。

### 给新重载加默认参数时，要想到候选是否冲突

若同时写一参数版本，以及两参数版本但第二项有默认值 `=4`，那么 `split_views(source)` 两边都能接，编译器会报调用有歧义。DAY38 使用两个明确的重载声明，两参数版的参数全部显式传入。默认参数的完整规则，等这两种调用能独立判断后再继续。

## 三、去 D2SLAM 对照真实重载（20 分钟）

打开 `d2frontend/include/d2frontend/utils.h` 第 14—17 行，可以看到三个声明。

~~~cpp
cv_bridge::CvImagePtr getImageFromMsg(const sensor_msgs::Image &img_msg);
cv_bridge::CvImagePtr getImageFromMsg(const sensor_msgs::ImageConstPtr &img_msg);
cv::Mat getImageFromMsg(const sensor_msgs::CompressedImageConstPtr &img_msg,
                       int flag);
~~~

先把很长的名字拆成这张表。`sensor_msgs::` 指这些消息类型所属的命名空间，`cv_bridge` 是连接 ROS 图像消息与 OpenCV 图像的工具，`cv::Mat` 是 OpenCV 使用的图像类型。

| 传入什么 | 参数数目 | 这里怎样读 |
|---|---:|---|
| `const sensor_msgs::Image&` | 1 | 借看一条图像消息对象 |
| `const sensor_msgs::ImageConstPtr&` | 1 | 借看一个指向只读图像消息的共享指针，访问所指消息时常见 `->` |
| `const sensor_msgs::CompressedImageConstPtr&`，再给一个 `int` | 2 | 接收压缩图像消息的共享指针，另传一个解码选项 |

顺着 DAY37 的办法找调用。`d2frontend.cpp` 第 110—112 行是实际源码。

~~~cpp
void D2Frontend::monoImageCallback(const sensor_msgs::ImageConstPtr &image) {
    auto _l = getImageFromMsg(image);
    auto img = _l->image;
~~~

调用处交进去的是 `image`，它的类型由函数参数声明给出，是 `sensor_msgs::ImageConstPtr`。所以调用第二个一参数重载。`auto` 让编译器从右侧结果推导变量类型，本课先认出 `_l` 接住了转换结果。

接着到 `d2frontend/src/loop_utils.cpp` 第 39—51 行找它的定义。下面摘出函数头和一个分支。

~~~cpp
cv_bridge::CvImagePtr getImageFromMsg(
    const sensor_msgs::ImageConstPtr &img_msg) {
    // 此处省略局部变量定义和其他分支
    if (img_msg->encoding == "8UC1" || img_msg->encoding == "mono8") {
        // 调用 cv_bridge 转换图像
    }
    // 后续分支见本地源码
}
~~~

这两处选择要分清。传入参数的类型决定使用哪个重载。已经进入这份实现后，程序才读取 `encoding` 字段，判断像素如何存放。即使这次消息写 `mono8`、下次写 `mono16`，只要调用处交的类型相同，仍进入同一份重载，再由内部 `if` 选择分支。 [声明所在头文件](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2frontend/include/d2frontend/utils.h) · [三个实现](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2frontend/src/loop_utils.cpp) · [实际调用](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2frontend/src/d2frontend.cpp)

## 四、ROS 理论｜接口类型与消息内容（10 分钟）

DAY37 的 `subscribe` 说明消息到达时调用当前对象的哪个成员函数。到了回调内部，消息类型又帮助 C++ 判断怎样调用后续工具函数。把调用连起来读，就是“订阅选定回调 → 回调接到图像消息指针 → 图像转换函数接收这种指针”。

`Image` 用于图像消息，`CompressedImage` 用于压缩图像消息。`encoding` 是消息内部描述像素存法的字段，例如 `mono8` 可以理解成每个灰度像素占 1 字节。读源码时先找变量的类型，再看函数进入后怎样解释字段。这里按现有 ROS 1 源码讲解，作答放在理论总结中。

## 五、C++ 实践｜补好检查，再给同一工具加入口（65 分钟）

在 [DAY38 的三份练习文件](C++练习/frame_input.h) 中复用你 DAY37 的结构体与函数。留白文件供你自己迁移代码。第 1 步约 20 分钟，第 2 步约 30 分钟，运行与对照约 15 分钟。

1. 头文件加防重复包含，在现有 `split_views(source, num_views)` 内补尺寸上限与像素数检查。保留 `crop_colum` 的正确下标。文末给 DAY37 的完整参考，可先尝试修，再按卡点展开。
2. 在头文件新增 `std::vector<Image> split_views(const Image& source);`，并在 `.cpp` 给它定义。它表示固定切四块，内部复用原来的两参数版本。不要再写一份行列循环。这里“固定切四块”是我们给工具设计的调用约定。
3. 在 `main` 中用一参数和两参数形式调用，并按下表测试。今天的正式源码保持两参数版无默认参数。理解后可临时加 `=4` 观察歧义，再去掉这个改动并重新编译。

| 用例 | 预期结果 |
|---|---|
| DAY37 的 8×2 宽图，`split_views(source)` 和 `split_views(source,4)` | 四块尺寸、像素逐一一致，第 2 块 `[20,21,22,23]` |
| 同图，`split_views(source,2)` | 两张 4×2 图，第 1 张 `[10,11,20,21,12,13,22,23]` |
| 12×3 图，按行存 0—35，调用一参数形式 | 四张 3×3 图，第 2 张 `[3,4,5,15,16,17,27,28,29]` |
| 8×2 只有 15 个像素；6×1 图调用一参数形式；正常图但块数为 0 | 返回空列表，输入保持原样 |

从仓库根目录执行。前两行生成两份 `.o`，第三条链接命令故意漏掉实现，第四条补齐。

~~~bash
cd DAY38/C++练习
c++ -std=c++17 -Wall -Wextra -Wpedantic -c main.cpp -o /tmp/day38_main.o
c++ -std=c++17 -Wall -Wextra -Wpedantic -c frame_input.cpp -o /tmp/day38_frame.o
c++ /tmp/day38_main.o -o /tmp/day38_missing
c++ /tmp/day38_main.o /tmp/day38_frame.o -o /tmp/day38_frame_input
/tmp/day38_frame_input
~~~

一参数与两参数版本各在头文件中声明，定义放在同一份实现文件。若链接时报缺某个版本，逐字对照头文件和定义的参数类型、个数，再确认实现文件参与了链接。

## 六、Python 模型｜从 DAY35 的一个验证结果拆回两条样本（65 分钟）

DAY36 同时换了输入数量、数据含义和模型接口，DAY37 又接上查表与新指标，讲解缺少从 DAY35 走过来的桥。本课从你已经写出的 `LinearNeuron`、`RegressionDataset`、`SquaredLoss`、`LossEvaluator`、`GradientDescent` 和 `Trainer` 继续，一起追踪一批数据怎样得到验证结果。

### 先找回 DAY35 做完的任务（15 分钟）

当时模型每次接收一个数 `x`，用 `w*x+b` 预测一个数 `y`。人工数据来自 `y=2*x+1`。现在用这些数据观察训练和评价的职责。

| 数据对象 | 数据 | 哪一步用它 |
|---|---|---|
| `data_train` | `x=[-1,0,1,2]`，`y=[-1,1,3,5]` | `Trainer.fit(100)` 反复用它计算梯度，更新模型的 `weight` 与 `bias` |
| `data_val` | `x=[-2,3]`，`y=[-3,7]` | 对两个训练好的候选分别评价，决定保留哪个学习率训练出的模型 |
| `data_test` | `x=[4,5]`，`y=[9,11]` | 选完以后，报告所选模型在这份数据上的结果 |

这里的 `x` 先保留为一个普通数。`forward(x)` 做一次预测，`train()` 用整批训练数据改一次参数，`fit(100)` 连续改 100 次。你用 0 和 0.1 两种学习率各创建一个从零开始的模型，得到两份候选。

本次复跑你的 DAY35 文件，学习率 0 的验证损失为 14.5，学习率 0.1 的验证损失约为 `2.5231e-8`，选中 0.1。这些输出下面会拆成具体的样本计算。 [你的 DAY35 程序](../DAY35/04_模型实践_训练验证测试分工.py)

### 拿一条样本，把三个方法接起来（10 分钟）

为了看清过程，先设 `model = LinearNeuron(1, 0)`，即权重 1、偏置 0。这是手算用的候选实例。验证集第一条样本是 `x=-2`、`y=-3`。沿你已经写过的方法走三行。

~~~python
x, y = data_val.get_item(0)    # 读到 -2 和 -3
prediction = model.forward(x) # 1 * (-2) + 0，得到 -2
one_loss = loss.forward(prediction, y) # (-2 - (-3)) ** 2 / 2，得到 0.5
~~~

`get_item` 只是取数据。`model.forward` 使用当前模型已经保存的参数算预测。`loss.forward` 比较预测和目标，给这一次预测算一个半平方损失。它们依次交接数值，所以调用顺序来自我们要做的事。

把第二条也算出来，就能看出你原来打印的平均数是怎么来的。

| 验证样本 | 预测 `w*x+b` | 预测减目标 | 半平方损失 |
|---|---:|---:|---:|
| `x=-2, y=-3` | -2 | 1 | 0.5 |
| `x=3, y=7` | 3 | -4 | 8 |
| 两条合在一起 | | | `(0.5+8)/2 = 4.25` |

半平方损失是每条差值先平方、再除以 2；平均损失是在所有样本损失加起来之后，再除以样本数。两个“除”分别来自两件事。本地教材第 2.2.2 节的式 (2.14) 定义平方损失，式 (2.22) 把样本损失取平均。 [《神经网络与深度学习》，书内第 27—28 页，PDF 第 42—43 页](<../../学习资料/AI agent/神经网络与深度学习 (邱锡鹏).pdf>)

### 再看 `self`，知道每次到底用了谁（10 分钟）

你在 DAY35 写过下面这一种调用。

~~~python
val_evaluator = LossEvaluator(data_val, loss)
val_loss = val_evaluator.evaluate(model)
~~~

构造时 `self.data = data` 把验证数据存给这个评价器，`self.loss = loss` 把计算损失的对象存给它。调用 `evaluate(model)` 时，方法中的 `self` 指 `val_evaluator`，显式参数 `model` 指这次要评价的那个模型。

所以 `self.data.get_item(i)` 表示“从这个评价器持有的验证集取样本”，`model.forward(x)` 表示“让传进来的模型预测”，`self.loss.forward(prediction,y)` 表示“让这个评价器持有的损失对象给预测打分”。每次调用方法，`self` 都指接收该次调用的对象，例如进入 `model.forward` 后，它的 `self` 就是模型。

同一个评价器可以依次接两个模型。模型为 `(w,b)=(0,0)` 时，验证预测是 `[0,0]`，逐条半平方损失是 `[4.5,24.5]`，平均 14.5。换成刚才的 `(1,0)`，逐条损失是 `[0.5,8]`，平均 4.25。验证数据保持同一份，结果差异来自传入模型的参数。

`evaluate` 中做的是预测、打分、汇总。真正的参数更新在 `GradientDescent.step`。DAY35 训练结束后再调用验证评价器，是为了比较已经得到的候选；用较低验证损失选择候选之后，再把所选模型交给测试评价器。教材第 2.2.3.2 节讲验证集用于模型选择，这一课继续用你原来的数据流程理解它。 [书内第 30 页，PDF 第 45 页](<../../学习资料/AI agent/神经网络与深度学习 (邱锡鹏).pdf>)

### 今天新增的实践，只把平均分拆开看（25 分钟）

在 [模型练习](04_模型实践_从逐条损失理解验证.py) 复用 DAY35 六个类、`batch_gradient` 和原实验调用。给现有 `LossEvaluator` 新增一个方法。

`sample_losses(self, model)` 使用这个评价器持有的数据与损失对象，按原样本顺序返回每条样本的半平方损失列表。它每次调用建立自己的结果列表，每条样本都经过“取一对数 → 预测 → 单条打分 → 放进列表”，遍历完才返回。

先自己实现，不增加新的类。原来的 `evaluate` 可以继续保留，让它的平均分与你返回的逐条损失核对。

| 验证调用 | 应看到什么 |
|---|---|
| 同一验证评价器，传 `LinearNeuron(1,0)` | 列表 `[0.5,8.0]`，列表平均值为 4.25，等于 `evaluate` |
| 接着传 `LinearNeuron(0,0)` | 列表 `[4.5,24.5]`，平均值 14.5 |
| 再传 `LinearNeuron(1,0)` | 再得到 `[0.5,8.0]`，结果不会累积成四项或六项 |
| 传 `LinearNeuron(2,1)` | `[0.0,0.0]`，当前人工关系被准确预测 |

用你已会的 `sum(values)/len(values)` 求列表平均值，浮点数比较用 `abs(actual-expected) < 1e-12`。每次评价前后都保存和比较模型的 `weight`、`bias`，再检查验证数据未被改变。

手算版本通过后，接到 DAY35 的实验里。在每个候选训练完、验证时，同时打印 `sample_losses(model)` 与 `evaluate(model)`，验证二者平均一致，按原有验证平均损失选择 0.1。最后评价一次选中模型的独立测试集。训练前已知的 `(1,0)` 手算能对上，再看训练后的很小数值，比较容易知道它从哪来。

如果时间只够先做一半，先交四个固定模型调用和参数不变的检查。下一节从这份证据继续接训练后的候选，按实际完成情况推进。原计划 2.8—2.9 的选读和双输入、查表、MAE/MSE 接续顺延到这条评价路径能独立解释之后。

## 七、今天怎样交与下一步

C++ 提交三文件、好坏输入的断言和实际编译输出。Python 提交复用后的程序及新增的逐条损失方法，写明做到固定模型还是也接好了训练候选。六道短答统一在 [课后总结](课后总结.md) 作答，计入当天预算。

DAY39 的 C++ 依据重载和入口检查结果，继续类的成员函数分文件。模型优先检查你能否自己追踪样本、预测与损失，再确定下一课的新增内容。

<a id="day37-answers"></a>
## 八、DAY37 示范答案与理论参考

下面对应 DAY37 的作业，用来核对已有提交。当天新任务的核心实现由你自己完成。

<details>
<summary>DAY37 C++ 三文件完整示范</summary>

这里沿用你已写对的 `crop_colum` 和预先建立 `views` 的方式。`crop_colum` 的输入约定是图像有效、裁剪范围有效。`split_views` 负责检查外部输入，再调用它。

`frame_input.h`

~~~cpp
#pragma once

#include <vector>

struct Image {
    int width;
    int height;
    std::vector<int> pixels;
};

Image crop_colum(const Image& source, int start_col, int crop_width);
std::vector<Image> split_views(const Image& source, int num_views);
~~~

`frame_input.cpp`

~~~cpp
#include "frame_input.h"

#include <cstddef>

Image crop_colum(const Image& source, int start_col, int crop_width) {
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

std::vector<Image> split_views(const Image& source, int num_views) {
    if (source.width <= 0 || source.width > 4096 ||
        source.height <= 0 || source.height > 4096 || num_views <= 0) {
        return {};
    }
    const std::size_t expected_size =
        static_cast<std::size_t>(source.width * source.height);
    if (source.pixels.size() != expected_size || source.width % num_views != 0) {
        return {};
    }

    const int part_width = source.width / num_views;
    std::vector<Image> views(num_views);
    for (int i = 0; i < num_views; ++i) {
        views[i] = crop_colum(source, i * part_width, part_width);
    }
    return views;
}
~~~

你的核心循环可以保留。变化主要在入口，正尺寸还要配上范围和像素数量的检查。约定宽高各最多 4096 后，在本机用 `int` 计算宽乘高是安全的，转成 `std::size_t` 再与列表长度比较。

`main.cpp`

~~~cpp
#include "frame_input.h"

#include <cassert>
#include <iostream>

int main() {
    const Image source{8, 2, {10, 11, 20, 21, 30, 31, 40, 41,
                              12, 13, 22, 23, 32, 33, 42, 43}};
    const auto saved = source.pixels;
    const auto views = split_views(source, 4);
    assert(views.size() == 4);
    const std::vector<std::vector<int>> expected{
        {10, 11, 12, 13}, {20, 21, 22, 23},
        {30, 31, 32, 33}, {40, 41, 42, 43}
    };
    for (int i = 0; i < 4; ++i) {
        assert(views[i].width == 2 && views[i].height == 2);
        assert(views[i].pixels == expected[i]);
    }

    Image taller{12, 3, {}};
    for (int pixel = 0; pixel < 36; ++pixel) {
        taller.pixels.push_back(pixel);
    }
    const auto tall_views = split_views(taller, 4);
    assert(tall_views.size() == 4);
    assert(tall_views[1].width == 3 && tall_views[1].height == 3);
    assert((tall_views[1].pixels ==
            std::vector<int>{3, 4, 5, 15, 16, 17, 27, 28, 29}));

    Image missing_pixel = source;
    missing_pixel.pixels.pop_back();
    assert(split_views(missing_pixel, 4).empty());
    assert(split_views({6, 1, {0, 1, 2, 3, 4, 5}}, 4).empty());
    assert(split_views(source, 0).empty());
    assert(split_views({0, 0, {}}, 4).empty());
    assert(split_views({4097, 1, {}}, 4).empty());
    assert(source.pixels == saved);
    std::cout << "8x2 and 12x3 passed; invalid inputs rejected\n";
}
~~~

将三份内容放到同一文件夹，用正文的两次编译、一次完整链接方式运行即可。`pop_back()` 在非空列表末尾移除一个元素，这里专门制造“尺寸写 8×2，实际缺一个像素”的输入。`std::vector<std::vector<int>>` 是装着多份整数列表的列表，这里按相机顺序保存四份预期像素。

</details>

<details>
<summary>DAY37 Python 模型完整示范，作为原题参考</summary>

DAY37 需要的是查表、双特征前向和误差指标的组合。表里的两格数字是人为给定的，模型参数也在调用时指定。下面只完成前向与评价。DAY38 的学习任务在第六节，从 DAY35 的单输入模型接起。

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
        return (self.weight1 * features[0]
                + self.weight2 * features[1]
                + self.bias)


def mean_absolute_error(predictions, targets):
    assert len(predictions) == len(targets) and len(predictions) > 0
    total = 0
    for i in range(len(predictions)):
        total += abs(predictions[i] - targets[i])
    return total / len(predictions)


def mean_squared_error(predictions, targets):
    assert len(predictions) == len(targets) and len(predictions) > 0
    total = 0
    for i in range(len(predictions)):
        total += (predictions[i] - targets[i]) ** 2
    return total / len(predictions)


table = EmbeddingTable({"常规档": [4, 3], "低噪档": [4, 0]})
model = LinearNeuron2D(2, -1, 1)
other_model = LinearNeuron2D(2, -1, 0)
assert model.forward([4, 3]) == 6
assert other_model.forward([4, 3]) == 5

predictions = []
for token in ["常规档", "低噪档"]:
    features = table.forward(token)
    predictions.append(model.forward(features))
assert predictions == [6, 9]

before = (model.weight1, model.weight2, model.bias)
assert mean_absolute_error(predictions, [7, 6]) == 2
assert mean_squared_error(predictions, [7, 6]) == 5
assert mean_absolute_error(predictions, [6, 7]) == 1
assert mean_squared_error(predictions, [6, 7]) == 2
assert mean_absolute_error(predictions, predictions) == 0
assert mean_squared_error(predictions, predictions) == 0
assert (model.weight1, model.weight2, model.bias) == before
~~~

</details>

<details>
<summary>DAY37 六道理论参考与逐题校准</summary>

1. `frame_input.h` 让调用方和实现方共用类型与函数声明，`frame_input.cpp` 写函数体，`main.cpp` 调用。`#pragma once` 避免同一份头文件在编译一个源文件时重复展开。你的多路径包含举例正确，实际提交需加上对应指令。
2. `d2frontend/include/d2frontend/d2frontend.h` 第 72 行是声明，`d2frontend/src/d2frontend.cpp` 第 200 行是定义，第 163 行是调用。类内已经有 `D2Frontend` 的上下文，类外需要 `D2Frontend::` 指明成员归属。源码位置与 DAY37 课件一致。
3. 12 列分四块，每块宽 3，第 2 块从列 3 开始。第 2 行对应行号 1，所以下标为 `1*12+3`、`1*12+4`、`1*12+5`，即 15、16、17。教师复现漏链接时提示 `Undefined symbols for architecture arm64`，并指出 `split_views(Image const&, int)`。编译会检查语法、名字和类型，单独编译调用方时可凭声明生成目标文件，链接时还要找到函数定义的目标代码。
4. 第一项 `params->image_topics[0]` 是话题名，`&D2Frontend::monoImageCallback` 指定成员函数，`this` 给当前前端对象。你的对象绑定解释正确，“模板函数”这一处应改成“成员函数”。
5. 权重固定 `(2,-1)`，输入 `[4,3]` 时加权和为 5。偏置 1 的对象输出 6，偏置 0 的对象输出 5。进入哪个模型的 `forward`，其中的 `self.bias` 就取哪个模型保存的偏置。
6. 逐项差为 `[-1,3]`，MAE 为 2，MSE 为 5，平均半平方损失为 2.5。MAE 中两项贡献为 1 和 3，MSE 中为 1 和 9，平方使较大差值的相对影响更强。

</details>
