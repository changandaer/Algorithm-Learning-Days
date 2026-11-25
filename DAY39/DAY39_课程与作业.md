# DAY39｜把拆图配置放进 C++ 对象，让 Python 模型学会多个输入

2026-11-14。C++ 先修复你记录的段错误，再接《C++ Primer Plus》第 10 章，把已学的类、分文件和重载串起来。Python 从 DAY38 已经写对的训练部件继续，扩展成能学习多个特征权重的线性模型。

| 内容 | 时间 |
|---|---:|
| C++ 修复 30 分钟，教材讲解 35 分钟，D2SLAM 与 ROS 理论 15 分钟，类的实践 50 分钟，C++ 短答 10 分钟 | 140 分钟 |
| 模型现状回顾 5 分钟，多输入讲解 20 分钟，梯度手算 15 分钟，模型实践 25 分钟，模型短答 5 分钟 | 70 分钟 |
| 阶段核验 20 分钟，保存结果与反馈 10 分钟 | 30 分钟 |

[总约定](../学习与授课总约定.md) · [阶段计划](../DAY29-DAY39_阶段计划.md) · [理论作答](课后总结.md)

<a id="day38-review"></a>
## 一、DAY38 讲评，先回答你遇到的段错误

### 这次程序按什么顺序出错？

你记录了编译成功、运行时 `segmentation fault`。它表示程序在运行中访问了无效的内存位置。教师重新编译原文件，用内存检查定位到空列表的下标访问。先看这次实际输入的 8 列、4 块。

~~~text
source.width / num_views = 8 / 4 = 2
你写的拒绝条件是 2 != 0，结果为真
split_views 返回空列表
main 随后读取 views_four_one[1]
空列表没有第 2 项，运行出错
~~~

这里 `/` 求商，`%` 求余数。判断是否能均分，要看余数是否为 0。例如 8 除以 4 的商是 2、余数是 0。修复顺序如下，先在 DAY39 练习中完成这一段，再让新类调用它。

| 提交中的位置 | 会发生什么 | 怎样改、怎样验证 |
|---|---|---|
| `source.width/num_views != 0` | 8×2 的正常图也被拒绝，教师单独调用两种入口都得到大小 0 | 检查正块数后，用 `%` 判断余数。取 `views[1]` 前先断言 `views.size()==4`，错误会停在更容易读懂的位置。 |
| `std::vector<Image> views;` 后直接写 `views[i]` | 上一处修好后，这个列表仍没有元素。教师只修 `%` 再运行，在这一行又发现无效访问 | 采用你 DAY37 的 `std::vector<Image> views(num_views)` 先建好各项，再按下标写；也可以用空列表逐次追加。 |
| `i < part_with` | `part_with` 是每块有多少列；8 列拆 4 块时它等于 2，循环只做两次 | 循环需要做 `num_views` 次。每轮的起始列仍是 `i * part_width`。 |
| 创建 `source_2` 后，两次调用还传 `source_1` | 实际仍在切旧的 8×2 图，却拿三行图的结果来比较 | 将这两次实参换成 `source_2`，先检查结果尺寸，再检查像素。 |
| 缺像素数量与尺寸上限检查 | 理论第 1 题说会拒绝缺像素的图，代码尚未实现这个检查 | 在切图前检查宽高 1—4096，像素数等于宽乘高。用 8×2、只有 15 个数的输入验证。 |

你的 `crop_colum` 行列计算仍然正确，一参数重载也正确地调用了两参数版，`#pragma once` 已加入，重复包含检查通过。问题集中在函数内部的容器、条件和测试实参。本课保留你使用的 `crop_colum` 名字。

### 理论和 Python 分别怎样评价？

- 第 1 题的防重复包含解释正确，“缺一个像素时会拒绝”尚缺代码支持。实际报错已记录，漏链接日志还待补。
- 第 2、3 题的重载判断正确。一次调用写了多少个实参，由源代码中的调用表达式决定；运行时把 `parts` 从 2 改成 4，两个实参的调用仍匹配同一版本。
- 第 4 题关于 `ImageConstPtr`、重载与 `encoding` 的解释正确，可以继续读成员函数。
- 第 5 题写的是课程反馈。你要求推进模型能力、保持逐日连续性，本课已据此调整。计算参考仍收在文末，供核对。
- 第 6 题留白。教师调用验证了当前评价方法保持模型参数，但这项补测只证明实现行为，口述解释按你后续回答记录。

Python 文件已写出六类和批梯度函数，`sample_losses` 的列表在每次调用时重新建立，循环结束后返回，计算正确。教师运行了规定的四次固定模型调用，追加 36 组预测、逐条损失与均值组合，都通过且参数、数据保持；再用你现有的训练器组装 100 步实验，末损失为 `8.4097e-9`。文件里尚未留下实际实验调用，这部分在 DAY39 的模型项目里补运行证据。

有一处接口改进供查阅。`sample_losses` 当前把半平方公式直接写在里面，如果换损失对象，它会与 `evaluate` 的结果含义不同。文末示范改为调用 `self.loss.forward`，本课练习的重点继续推进多输入模型与训练。

## 二、C++ 教材主课，把“函数＋配置”放进一个对象（35 分钟）

### 接着哪一天，今天新增什么？

DAY35 你已经写过保存配置与次数的类；DAY37 学会声明与定义分文件；DAY38 学会同名函数根据实参匹配。今天把这些写法放在一起，让一个对象记住自己每次要切几块。

原来的 `split_views(source,4)` 每次都传 4。现在创建 `ImageSplitter four(4)`，后面写 `four.split(source)`。这一次调用的图像是 `source`，持续保存在对象里的配置是 4。类似 Python 模型将 `weight` 存在 `self`，而每次 `forward(x)` 传入新的 `x`。

教材对应第 10 章的类接口与实现，书内第 510—518 页，特别是第 514 页 Implementing Class Member Functions；构造函数从第 524 页起，const Member Functions 在第 537 页。分别对应 PDF 第 525—533、539、552 页。 [《C++ Primer Plus》第 6 版](<../../学习资料/C++/C++ Primer Plus, 6th edition (Stephen Prata).pdf>)

### 用一个更小的配置类逐行看

先看头文件里的类型定义。

~~~cpp
class CutConfig {
private:
    int parts;
public:
    CutConfig(int value);
    int count() const;
};
~~~

`parts` 是每个对象自己的整数。`private` 限制外部怎样访问它，`public` 列出允许外部调用的接口。每个对象保存各自的字段，独立性来自对象本身。`CutConfig(int value)` 与类同名、没有返回类型，是构造函数，创建对象时负责准备好初始状态。

在 `.cpp` 中写定义，可以一小段一小段看。

~~~cpp
CutConfig::CutConfig(int value) {
    parts = value;
}

int CutConfig::count() const {
    return parts;
}
~~~

第一个 `CutConfig::` 指归属，后面的 `CutConfig` 是构造函数名。`parts=value` 把传入值存进正在创建的这个对象。第二段开头的 `int` 才是普通成员函数的返回类型。类内声明和类外定义，都要保留参数后面的 `const`。

~~~cpp
const CutConfig four(4);
const CutConfig two(2);
int first = four.count(); // 得到 4
int second = two.count(); // 得到 2
~~~

定义时的 `CutConfig::count` 告诉编译器它属于哪个类。调用时的 `four.count()` 还指定了这一次使用哪个对象的数据。`four` 和 `two` 走相同的方法代码，读的是各自的 `parts`。

### 两个 const 分别管哪一个对象？

正式作业会用这个接口。

~~~cpp
std::vector<Image> split(const Image& source) const;
~~~

参数中的 `const Image&` 表示借看传进来的图，通过 `source` 读取它。末尾的 `const` 表示这个成员函数以只读方式访问当前处理器，在本课中它会读取块数，不能通过当前对象修改普通数据成员 `num_views`。

一个是这次输入的图像，一个是接收方法调用的处理器对象。它们属于不同位置，所以需要分别表达。末尾的 `const` 也使 `const ImageSplitter four(4)` 可以调用该方法。

如果头文件声明 `int count() const;`，实现却写 `int CutConfig::count()`，编译器会认为它没有对应上声明。今天故意试一次这个错误，再恢复一致，以后在 D2SLAM 中看到长函数头也能分辨要核对哪里。

## 三、再回 D2SLAM，认出同一组写法（15 分钟，含 ROS 理论）

`d2estimator.hpp` 中的 `D2Estimator` 类里有两条声明。

~~~cpp
Swarm::Odometry getOdometry() const;
Swarm::Odometry getOdometry(int drone_id) const;
~~~

这是 DAY38 的重载，加上今天的只读成员函数写法。`Swarm::Odometry` 是返回类型，可以先读作一份运动估计结果。`drone_id` 表示要查询哪架无人机。

在 `.cpp` 中，第一份定义很短。

~~~cpp
Swarm::Odometry D2Estimator::getOdometry() const {
    return getOdometry(self_id);
}
~~~

`D2Estimator::` 写明归属。调用时没有显式传入编号，就用当前对象保存的 `self_id`，转交给同名的一个参数版本。这里的 `self_id` 是无人机编号这个数据成员，与 Python 的 `self` 含义分别看待。 [头文件第 85—86 行](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2vins/src/estimator/d2estimator.hpp) · [实现第 908—917 行](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2vins/src/estimator/d2estimator.cpp)

另一条能直接读完的实际定义是 `bool D2Estimator::isInitialized() const { return solve_count > 0; }`。它从当前对象读取求解次数，返回是否大于 0。这可以与刚才的配置查询方法对照。 [声明第 103 行](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2vins/src/estimator/d2estimator.hpp) · [定义第 1003 行](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2vins/src/estimator/d2estimator.cpp)

ROS 这次只补一个连接。DAY38 的回调把图像信息交给前端，估计器结合图像与惯性读数得到运动状态；查询函数从现有状态取结果。节点里的 `estimator` 指针通过 `->` 调用对象的方法，例如 `estimator->getMotionPredict(stamp)`。点号用于对象，箭头用于通过指针访问对象的成员。 [节点第 70—72 行](../../学习资料/C++/OmniNxt_具备全向视觉感知能力的紧凑型空中机器人/D2SLAM-main/d2vins/src/d2vins_node.cpp)

## 四、C++ 实践，先修再接类（修复 30 分钟＋实践 50 分钟）

在 [DAY39 三文件练习](C++练习/frame_input.h) 复用 DAY38 的代码。文末收有修正后的完整 DAY38 参考，按卡点查阅。

**第一步，修复普通函数。** 保留 `Image`、`crop_colum` 和两个 `split_views` 重载，按第一节的错误链逐一修复。给每个 `views[i]` 测试先加大小断言，再跑 8×2、12×3、缺像素、不可均分和块数 0。

**第二步，给同一个工具加类接口。** 在头文件定义 `ImageSplitter`，私有字段 `int num_views` 保存配置；公开声明下面三项，在 `.cpp` 分别实现。

| 接口 | 接收与返回什么 |
|---|---|
| `ImageSplitter(int parts)` | 构造时把传入块数存入当前对象 |
| `int view_count() const` | 返回当前对象保存的块数 |
| `std::vector<Image> split(const Image& source) const` | 用保存的块数调用已有的两参数 `split_views`，返回图像列表 |

成员方法复用已经修好的函数。块数 0 等无效配置交给原函数按已有约定返回空列表。

**第三步，比较三个对象。** `const ImageSplitter four(4)` 和 `const ImageSplitter two(2)` 对同一张 8×2 图分别返回 4 张 2×2、2 张 4×2。再建块数 0 的对象，结果为空。连续调用两次 `four.split` 后，`four.view_count()` 仍为 4，`two.view_count()` 仍为 2，原图像素保持原样。

先编译正确版本，再临时删掉 `.cpp` 中 `view_count` 定义末尾的 `const`，观察哪一行报错并恢复。从仓库根目录编译运行。

~~~bash
cd DAY39/C++练习
c++ -std=c++17 -Wall -Wextra -Wpedantic main.cpp frame_input.cpp -o /tmp/day39_splitter
/tmp/day39_splitter
~~~

想复查越界时，可在同一条编译命令中加入 `-g -fsanitize=address,undefined`。这会给运行程序加上内存访问检查。报错时先读自己代码中的文件名和行号，再核对当时列表的大小。

## 五、Python 模型，接着原训练器学会多个特征（70 分钟）

### 你已经可以继续到哪里？（5 分钟）

你已经写出了前向、数据集、损失、评价器、梯度更新和训练器。DAY38 的方法补测正确，现有训练器也能在教师组装的调用下训练单输入模型。现在继续学习模型表达与参数学习，把一份输入从一个数扩展为多个数。

教材第 2.3 节本来就用 `wᵀx+b` 表达多元线性回归，第 3.1 节沿用这个打分函数进入线性分类。今天把第 2.3 节的向量公式落实到可训练代码，再用第 3.1 节认识“分数怎样用于分类”的入口。 [书内第 32—33 页，PDF 第 47—48 页；第 54—55 页，PDF 第 69—70 页](<../../学习资料/AI agent/神经网络与深度学习 (邱锡鹏).pdf>)

### 为什么旧的一个输入不够？（10 分钟）

先保留 DAY35 的关系 `y=2*x+1`。如果 `x` 代表亮度，两张图亮度相同，模型收到的是同一个数，算出的结果也相同。现在我们想把噪声程度也交给它。亮度相同、噪声不同的图，输入就能不同，模型有了区分它们的依据。

给每张图的简化记录约定两个特征，按固定顺序排成列表 `[亮度,噪声]`。特征就是描述一个样本的某项数字。用一份列表保存多个特征，数学中称为向量。教学数据已缩放，-1 表示较低、1 表示较高，0 表示中间水平。

旧模型的一个权重变成 `[w1,w2]`，计算仍是“各乘各的权重，加起来，再加偏置”。

~~~text
旧：y_hat = w*x + b
新：y_hat = w1*x1 + w2*x2 + b
    features = [x1,x2]，weights = [w1,w2]
~~~

在这次人工任务中用 `y=2*x1-x2+1` 造目标分数。把第二项特征设为 0，它正好回到 DAY35 的 `y=2*x+1`。例子里 `[1,-1]` 的目标是 4，`[1,1]` 的目标是 2，两者亮度相同、噪声不同。

### 从手算写到类的接口（10 分钟）

多输入模型命名为 `MultiInputNeuron`，属性是 `weights` 列表与一个 `bias`，`forward(features)` 返回一个预测数。数学中的 `wᵀx` 叫点积，就是两排数按位置相乘再相加。例如 `[2,-1]` 与 `[1,-1]` 得到 `2*1+(-1)*(-1)=3`，加偏置 1 后是 4。上标 T 表示把向量转成便于做这种乘法的排布，在这次 Python 列表实现中直接按下标计算即可。

先看相邻的三特征手算，避免把做法记成只能写两个乘积。

~~~text
weights=[1,2,-1]，features=[2,3,4]，bias=0.5
结果 = 1*2 + 2*3 + (-1)*4 + 0.5 = 4.5
~~~

写前向时，先让结果从偏置开始，再按特征个数累加每个乘积。构造函数使用 `weights.copy()` 保存各实例自己的列表，后续训练修改这个对象的权重。

数据集也能沿用。`xs` 从 `[-1,0,1,2]` 变成 `[[x11,x12],[x21,x22],...]`，外层每一项仍是一条样本。`get_item(i)` 依旧返回“这一条的输入、这一条的目标”。评价器继续调用 `model.forward(x)`，只是此时 `x` 是一整份特征列表。

### 原来一个梯度，怎样对应一排权重？（15 分钟）

仍用已有半平方损失。设一条样本的误差 `error=prediction-target`，旧版权重梯度是 `error*x`，偏置梯度是 `error`。现在每个权重各负责一项特征，所以第 j 个权重的梯度是 `error*features[j]`，偏置梯度保持同样的计算。批量梯度仍然逐样本相加后取平均。

用四条对称的训练样本看一次更新，初值权重 `[0,0]`、偏置 0。

| 特征 | 目标 | 初始预测 | error | 对 w1 的贡献 | 对 w2 的贡献 |
|---|---:|---:|---:|---:|---:|
| `[-1,-1]` | 0 | 0 | 0 | 0 | 0 |
| `[-1,1]` | -2 | 0 | 2 | -2 | 2 |
| `[1,-1]` | 4 | 0 | -4 | -4 | 4 |
| `[1,1]` | 2 | 0 | -2 | -2 | -2 |

平均后权重梯度为 `[-2,1]`，偏置梯度为 -1。学习率 0.1 的一次更新，把权重变为 `[0.2,-0.1]`，偏置变为 0.1。初始平均半平方损失是 3，更新后是 2.43。

计算两项梯度时都使用本轮同一个旧模型。求完全部平均梯度，再交给更新器逐项修改权重。你 DAY38 的“先求梯度、再 step”顺序可以保留。

### 只改需要支持多输入的部件，跑一次训练（25 分钟）

在 [模型练习](04_模型实践_多输入模型与训练.py) 复用 DAY38 的 `RegressionDataset`、`SquaredLoss`、`LossEvaluator`、`Trainer`。`Trainer` 的 `train` 与 `fit` 调用顺序继续使用原来的版本。新增或调整三处。

| 部件 | 本次要实现的约定 |
|---|---|
| `MultiInputNeuron(weights,bias)` | 保存非空权重列表的副本。`forward(features)` 支持与权重等长的特征列表，返回点积加偏置。用长度断言检查特征个数。 |
| `batch_gradient(model,data)` | 接口顺序沿用你的 DAY38 版本。返回 `(g_weights,g_bias)`，前者是每个权重对应的平均梯度列表。 |
| `VectorGradientDescent(learning_rate)` | `step(model,g_weights,g_bias)` 逐项更新 `model.weights`，再更新 `model.bias`。它与原更新器承担同一职责，接收的权重梯度现在是一组数。 |

使用 `len(model.weights)` 确定有几项权重，零梯度列表可用 `[0.0] * len(model.weights)` 创建。每个列表位置装一个梯度累加值。输入每条样本时，先计算一个 `error`，再让它乘到每项特征上。

训练数据如下，标签来自上面的教学关系。

~~~python
xs_train = [[-1,-1], [-1,1], [1,-1], [1,1]]
ys_train = [0,-2,4,2]
~~~

按下面顺序验证。第一次只跑一步，把手算接到程序，再新建模型从零跑 100 步。

| 验收 | 预期结果 |
|---|---|
| 前向，权重 `[2,-1]`、偏置 1 | `[1,-1]` 得 4，`[1,1]` 得 2；三特征手算例子得 4.5 |
| 零初值的批梯度 | 权重梯度 `[-2,1]`，偏置梯度 -1 |
| 从零 `fit(1)` | 记录长度为 2，损失从 3 到 2.43；权重 `[0.2,-0.1]`、偏置 0.1 |
| 另建零初值模型，学习率 0.1，`fit(100)` | 记录长度为 101；权重接近 `[2,-1]`、偏置接近 1；末损失小于 `1e-6` |
| 验证，`xs=[[0,0],[1,0],[0,1]]`、`ys=[1,3,0]` | 每项预测与目标误差小于 0.01 |
| 最后测试，`xs=[[0.5,-0.5],[-0.5,0.5]]`、`ys=[2.5,-0.5]` | 每项预测误差小于 0.01；评价前后权重和偏置保持 |

这是固定学习率的一次模型扩展实验。训练用训练集更新参数，验证与最终测试沿用已学职责。检查浮点值用 `abs(actual-expected)<1e-10` 等容差，参数训练后的“接近”按表中标准。

这次训练是在已知规则的人工数据上验证实现。你应能交出一个输入、参数、训练和测试都接通的多输入模型。

### 接到真正的神经网络，还差哪一步？（并入短答前回顾）

第 3.1 节把同样的线性分数 `wᵀx+b` 接到类别决策。例如分数大于 0 时判为一类，小于 0 时判为另一类。接下来的第 3.2 节会把分数通过 Sigmoid 转成 0 到 1 之间的量，学习二分类；第 3.3 节再接多个类别。随后进入第 4 章，学习激活函数、多个神经元和层的组合。

后续每课会增加一个能运行的模型能力，理论继续说明前一个部件为什么需要扩展。当前这个多输入、可训练的加权和，将被这些模型反复复用。

## 六、阶段核验（20 分钟，另留 10 分钟保存）

关闭示范代码与 AI，选择已经练过的内容完成下面三项，记录是否用了提示。

1. 从空白写一个短的 const 成员函数定义，说明 `类名::` 和末尾 `const` 分别指什么。
2. 给一张 8×2 图和两个配置对象，先预测结果的数量与尺寸，再用已有程序验证。解释 `views[1]` 为什么要在确认大小后使用。
3. 用一条两特征样本说明输入、模型参数、前向和每项权重梯度怎样对应。展示训练前后参数与最终测试输出。

C++ 的修复、模型新实现和闭卷解释分别记录。DAY39 的阶段结果依据实际证据，在下一次评阅时确认。

<a id="day38-answers"></a>
## 七、DAY38 示范答案与理论参考

下面对应 DAY38，供你核对原提交。完整示范折叠保存，当天的类和多输入模型由你自己完成。

<details>
<summary>DAY38 C++ 三文件完整示范，按错误链修复</summary>

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
std::vector<Image> split_views(const Image& source);
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

std::vector<Image> split_views(const Image& source) {
    return split_views(source, 4);
}
~~~

直接调用 `crop_colum` 时，输入约定是图像有效、裁剪范围有效。对外的 `split_views` 先检查这些前提所需的尺寸、像素数量与块数，再发起裁剪。你的一参数版本保存到局部列表再返回，结果同样正确，这里简写为直接返回。

`main.cpp`

~~~cpp
#include "frame_input.h"

#include <cassert>
#include <iostream>

int main() {
    const Image source_1{8, 2, {10, 11, 20, 21, 30, 31, 40, 41,
                                12, 13, 22, 23, 32, 33, 42, 43}};
    const auto saved = source_1.pixels;
    const auto four_default = split_views(source_1);
    const auto four_explicit = split_views(source_1, 4);
    assert(four_default.size() == 4 && four_explicit.size() == 4);
    const std::vector<std::vector<int>> expected{
        {10, 11, 12, 13}, {20, 21, 22, 23},
        {30, 31, 32, 33}, {40, 41, 42, 43}
    };
    for (int i = 0; i < 4; ++i) {
        assert(four_default[i].width == 2 && four_default[i].height == 2);
        assert(four_default[i].pixels == expected[i]);
        assert(four_explicit[i].pixels == expected[i]);
    }

    const auto two = split_views(source_1, 2);
    assert(two.size() == 2);
    assert(two[0].width == 4 && two[0].height == 2);
    assert((two[0].pixels == std::vector<int>{10, 11, 20, 21, 12, 13, 22, 23}));

    Image source_2{12, 3, {}};
    for (int pixel = 0; pixel < 36; ++pixel) {
        source_2.pixels.push_back(pixel);
    }
    const auto tall_default = split_views(source_2);
    const auto tall_explicit = split_views(source_2, 4);
    assert(tall_default.size() == 4 && tall_explicit.size() == 4);
    for (int i = 0; i < 4; ++i) {
        assert(tall_default[i].width == 3 && tall_default[i].height == 3);
        assert(tall_default[i].pixels == tall_explicit[i].pixels);
    }
    assert((tall_default[1].pixels ==
            std::vector<int>{3, 4, 5, 15, 16, 17, 27, 28, 29}));

    Image missing_pixel = source_1;
    missing_pixel.pixels.pop_back();
    assert(split_views(missing_pixel).empty());
    assert(split_views({6, 1, {0, 1, 2, 3, 4, 5}}).empty());
    assert(split_views(source_1, 0).empty());
    assert(split_views({0, 0, {}}).empty());
    assert(split_views({4097, 1, {}}).empty());
    assert(source_1.pixels == saved);
    std::cout << "four views, two views, three rows and invalid inputs passed\n";
}
~~~

先检查大小，再读第几项。三行图的两次调用都传 `source_2`，这样断言实际测试的是你刚创建的新输入。

</details>

<details>
<summary>DAY38 Python 六类、逐条损失和训练验证调用示范</summary>

与你提交的代码相比，主体保留，`sample_losses` 调用持有的损失对象，末尾补固定参数与训练验证的实际调用。`batch_gradient(model,data)` 的顺序沿用你的实现。

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
        for i in range(self.data.size()):
            x, y = self.data.get_item(i)
            predictions.append(model.forward(x))
        return self.loss.mean(predictions, self.data.ys)

    def sample_losses(self, model):
        values = []
        for i in range(self.data.size()):
            x, y = self.data.get_item(i)
            prediction = model.forward(x)
            values.append(self.loss.forward(prediction, y))
        return values


class GradientDescent:
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate

    def step(self, model, g_w, g_b):
        model.weight -= self.learning_rate * g_w
        model.bias -= self.learning_rate * g_b


def batch_gradient(model, data):
    g_w, g_b = 0, 0
    for i in range(data.size()):
        x, y = data.get_item(i)
        error = model.forward(x) - y
        g_w += error * x
        g_b += error
    return g_w / data.size(), g_b / data.size()


class Trainer:
    def __init__(self, model, data, loss, optimizer):
        self.model = model
        self.data = data
        self.loss = loss
        self.optimizer = optimizer
        self.evaluator = LossEvaluator(data, loss)

    def train(self):
        g_w, g_b = batch_gradient(self.model, self.data)
        self.optimizer.step(self.model, g_w, g_b)
        return self.evaluator.evaluate(self.model)

    def fit(self, epochs):
        history = [self.evaluator.evaluate(self.model)]
        for i in range(epochs):
            history.append(self.train())
        return history


loss = SquaredLoss()
data_val = RegressionDataset([-2, 3], [-3, 7])
val_evaluator = LossEvaluator(data_val, loss)
saved_xs, saved_ys = data_val.xs.copy(), data_val.ys.copy()
for weight, bias, expected in (
    (1, 0, [0.5, 8.0]),
    (0, 0, [4.5, 24.5]),
    (1, 0, [0.5, 8.0]),
    (2, 1, [0.0, 0.0]),
):
    model = LinearNeuron(weight, bias)
    before = (model.weight, model.bias)
    values = val_evaluator.sample_losses(model)
    assert values == expected
    assert abs(sum(values) / len(values) - val_evaluator.evaluate(model)) < 1e-12
    assert (model.weight, model.bias) == before
assert data_val.xs == saved_xs and data_val.ys == saved_ys

data_train = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
models = {}
val_scores = {}
for rate in (0, 0.1):
    model = LinearNeuron(0, 0)
    trainer = Trainer(model, data_train, loss, GradientDescent(rate))
    history = trainer.fit(100)
    assert len(history) == 101
    before = (model.weight, model.bias)
    values = val_evaluator.sample_losses(model)
    score = val_evaluator.evaluate(model)
    assert abs(sum(values) / len(values) - score) < 1e-12
    assert (model.weight, model.bias) == before
    models[rate] = model
    val_scores[rate] = score
    print(rate, values, score)

best_rate = min(val_scores, key=val_scores.get)
assert best_rate == 0.1
best_model = models[best_rate]
data_test = RegressionDataset([4, 5], [9, 11])
test_evaluator = LossEvaluator(data_test, loss)
before = (best_model.weight, best_model.bias)
print("test", test_evaluator.evaluate(best_model))
assert abs(best_model.forward(4) - 9) < 0.01
assert abs(best_model.forward(5) - 11) < 0.01
assert (best_model.weight, best_model.bias) == before
~~~

你原来的 `train` 先计算一次 `old_loss` 但没有使用，结果仍然正确。示范直接保留更新后的评价，`fit` 继续单独记录初始损失。

</details>

<details>
<summary>DAY38 六道理论参考与提交对照</summary>

1. `#pragma once` 已正确加入。有效的输入校验应在 `split_views` 中完成，但你的提交还没有像素数检查。编译能生成程序，运行时仍可能发生越界。直接报错来自正常图被错误拒绝后访问空结果，再往下还要修空容器写入与循环上限。
2. 一参数调用选一参数版本，两参数调用选两参数版本。`parts` 的值变了，调用表达式仍有两个实参。你的判断正确，参数数量从调用表达式来数。
3. 一参数版能接 `source`，两参数版也能凭默认值补成完整调用，因此二者都成为可用候选。仅改变返回类型无法让这次调用作出选择。你的解释正确。
4. `image` 是 `sensor_msgs::ImageConstPtr`，调用匹配借看该指针的重载。`encoding` 改变的是函数进入后的数据分支。你的解释正确。
5. 固定模型的两项预测为 `[-2,3]`，差值 `[1,-4]`，半平方损失 `[0.5,8]`，平均 4.25。数据集提供样本，模型做前向，损失对象打分。你的回答提出了课程推进需求，本课据此从评价部件转向多输入参数学习。
6. 同一个验证评价器持有的数据和损失对象相同，传入的模型及其参数不同，预测与分数就会不同。`evaluate` 中的 `self` 是评价器，进入 `model.forward` 后的 `self` 是该模型。评价前后两份模型的参数均保持。你的实现由教师补测验证了这一行为，理论作答仍可用自己的话补充。

</details>
