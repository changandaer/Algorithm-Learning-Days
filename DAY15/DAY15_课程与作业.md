# DAY15：开始C++，复习LeetCode，用真实神经元学习类

> 今天仍只读这一份课程。包含DAY14的评语、全部题目的示范与对比、新理论和作业。预计180分钟；示范答案按需要查阅，不要求全部重抄。
>
> 主线：Python复习LC217，开始C++17的编译、函数和容器。支线：用纯Python实现单输入神经元，理解参数为什么属于对象。只在Mac本地运行，不安装GPU软件、PyTorch、CMake或Docker。
>
> 顺序：先读第一节；第二、三节是昨天的答案；第四节补两个概念；第五节C++；第六节神经元；第七节统一领取今天作业。所有作答文件只有一句说明，三步分析、实现、测试都由你写。

## 一、DAY14评语：85/100，具备开始C++的条件

最重要的进步是：你把“参数传进来→完整处理→返回结果”真正用到了岗位项目里，之前只返回两条数据的问题也已经修复。`try/except`代码与理论回答表明，你已能区分自动关闭文件和处理报错。

本次检查了6个Python文件、课程内回答区、`课后作业.md`、代码注释及本地Git记录。理论回答写在`课后作业.md`，我没有因为文件名不同而漏掉；课程末尾留白无需重复填写。

| 项目 | 检查结果 | 证据与解释 |
|---|---|---|
| 00 完整读取 | 通过；242补写未见 | 6/3/1/0条输入全部正确，函数不再返回`None`；文件中没有242平台版本 |
| 01 LC1两数之和 | 算法通过 | 7029组输入与目标组合通过，包括负数、重复值、无解扩展；多解时接受任意合法索引对 |
| 02 LC387 | 算法通过 | `a/b/c`组成长度0～7的3280个字符串全部通过，另测`loveleetcode`和十万次重复字符；连续调用同一个对象也正确 |
| 03 岗位项目 | 功能通过 | 四份文件×七个阈值，共28组通过；直接传入新嵌套列表也正确 |
| 04 异常选练 | 通过 | 四个存在路径及一个缺失路径结果正确，不把文件缺失伪装成成功 |
| 05 计数器支线 | 未实现，不计主线扣分 | 文件只有说明。你的反馈是题意不清、与模型目标脱节；今天换成真实神经元，不要求补回计数器 |
| 理论 | 有进步，仍需校准 | 第1～4题基本理解；第5题误把哈希值当作唯一编号，第7题混淆输入长度与字符种类；第6题未答，8～9题支线未答 |

评分：概念19/25，代码29/30，分析与调试17/20，测试与复杂度11/15，Git记录与表达9/10，共85分。这是基于提交材料的教学评估，不是一个精确测量能力的客观仪器。支线未做单独记录为“未验收”，不因我之前题意设计不合适而扣主线分。

暂不能声称你已通过限时闭卷阶段验收：未见机试用时、提示使用情况；额外测试是我补的，不能算成你已经独立写过这些测试。但核心代码已足够支持开始C++，不需要为了补写记录停在原地。今天的一题短复习继续验证独立性。

### 接下来最值得练的内容

- 解释自己的代码为什么正确。例如387的第二个字典不断覆盖索引，为什么仍不影响答案？这不是错误，下面会讲清楚。
- 让测试自动检查答案。你已经会写`assert`，岗位项目却仍以打印为主；今天只要求少量有用断言，不增加记录表格。
- 先讲准已用到的概念，不急着猜哈希表底层机制。今天不学哈希冲突的实现算法，也不加去重、排序任务。

你的三步注释有一处沿用了LC1的文字，和387代码不一致。无需重写长流程，只把它当成提醒：注释应帮助你表达真实思路，不必为填满“三步”写无用内容。

## 二、DAY14代码示范与逐题对比

下面是昨天题目的答案，不是今天作答文件。每个小节可单独阅读；文件路径按仓库根目录运行。

### 00：完整读取，以及尚未补写的242入口

```python
def load_job_skills(file_path):
    jobs = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()
            if clean_line != "":
                skills = []
                for part in clean_line.split(","):
                    skills.append(part.strip().lower())
                jobs.append(skills)
    return jobs


assert len(load_job_skills("DAY13/岗位技能样例.txt")) == 6
assert len(load_job_skills("DAY14/岗位样例A_三条岗位.txt")) == 3
assert load_job_skills("DAY14/岗位样例B_一条岗位.txt") == [["docker", "linux"]]
assert load_job_skills("DAY14/岗位样例C_仅空白行.txt") == []
```

你的第36行在循环外返回，已正确修复核心问题。你先拆分再排除`['']`，示范先判断空行再拆分；在题目保证的数据范围内，两种都对。示范只是少做空白行的无用处理，不要求为了风格改写已完成文件。

下面补全昨天要求的242平台入口。今天不重复增加一整道242作业，DAY16到期复习时再闭卷补上。

```python
class Solution:
    def isAnagram(self, s, t):
        if len(s) != len(t):
            return False
        left_counts = {}
        right_counts = {}
        for letter in s:
            left_counts[letter] = left_counts.get(letter, 0) + 1
        for letter in t:
            right_counts[letter] = right_counts.get(letter, 0) + 1
        return left_counts == right_counts


solution = Solution()
assert solution.isAnagram("aab", "aba") == True
assert solution.isAnagram("aab", "abb") == False
```

算法沿用你DAY13已写对的字符计数，只是平台要调用`isAnagram`这个名称。未见这部分提交，不能说“已修复”，也不把它当作算法不会。

### 01：两数之和

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for index in range(len(nums)):
            needed = target - nums[index]
            if needed in seen:
                return [seen[needed], index]
            seen[nums[index]] = index
        return []


solution = Solution()
assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]
assert solution.twoSum([3, 3], 6) == [0, 1]
assert solution.twoSum([3], 6) == []
assert solution.twoSum([-4, 1, 5], 1) == [0, 2]
```

你的实现与此核心一致，不需要修改。检查当前数之前，`seen`只保存之前见过的数，所以不会使用同一位置两次。`[3,3]`成功不是巧合：第一轮记下第一个3，第二轮找到它。

平均时间O(n)，额外空间最坏O(n)。今天这里没有固定26种字母的条件。无解返回`[]`是本地练习扩展，不是说LeetCode原题不保证有解。

### 02：字符串中的第一个唯一字符

普通函数示范：

```python
def first_unique_index(s):
    counts = {}
    for letter in s:
        counts[letter] = counts.get(letter, 0) + 1
    for index in range(len(s)):
        if counts[s[index]] == 1:
            return index
    return -1


assert first_unique_index("leetcode") == 0
assert first_unique_index("loveleetcode") == 2
assert first_unique_index("aabb") == -1
assert first_unique_index("aabc") == 2
assert first_unique_index("z") == 0
assert first_unique_index("") == -1
```

平台版本（单独提交即可，不依赖上面的普通函数）：

```python
class Solution:
    def firstUniqChar(self, s):
        counts = {}
        for letter in s:
            counts[letter] = counts.get(letter, 0) + 1
        for index in range(len(s)):
            if counts[s[index]] == 1:
                return index
        return -1


solution = Solution()
assert solution.firstUniqChar("loveleetcode") == 2
assert solution.firstUniqChar("aabc") == 2
assert solution.firstUniqChar("aabb") == -1
```

你的版本使用`letters`计数、`word`存索引，再遍历`letters.items()`；它正确，不强迫换成示范。

为什么正确：字典保持键首次插入的顺序，更新旧键的值不会把键移到末尾。`word`实际保存每个字符的最后一次索引，但只有次数等于1的字符才会被返回；这样的字符只有一次出现，首次和最后一次索引本来就相同。因此你找到的是最靠左的唯一字符。

示范的区别是再遍历一次原字符串，自然按原索引从小到大找；不需要第二个索引字典，也少依赖一条字典顺序规则。两者时间复杂度都为平均O(n)，固定小写字母时额外空间都是O(1)，不是一个O(n)另一个O(1)。少一个容器是常数上的简化。

你未另写普通函数，但平台方法已经能证明主要算法能力，不要求为形式重复抄一遍。三步注释里的“需要数字”来自两数之和，建议口述时改成你实际做的字符统计；不按注释篇幅扣分。

### 03：岗位共同技能分析器

这是能单独运行的完整示范，读取函数也包含在内：

```python
def load_job_skills(file_path):
    jobs = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()
            if clean_line != "":
                skills = []
                for part in clean_line.split(","):
                    skills.append(part.strip().lower())
                jobs.append(skills)
    return jobs


def analyze_jobs(job_skills, min_jobs):
    counts = {}
    for skills in job_skills:
        for skill in skills:
            counts[skill] = counts.get(skill, 0) + 1
    common = []
    for skill, count in counts.items():
        if count >= min_jobs:
            common.append(skill)
    return {
        "job_count": len(job_skills),
        "skill_counts": counts,
        "common_skills": common,
    }


def run_report(file_path, min_jobs):
    jobs = load_job_skills(file_path)
    return analyze_jobs(jobs, min_jobs)


assert run_report("DAY14/岗位样例B_一条岗位.txt", 1) == {
    "job_count": 1,
    "skill_counts": {"docker": 1, "linux": 1},
    "common_skills": ["docker", "linux"],
}
assert run_report("DAY14/岗位样例A_三条岗位.txt", 2) == {
    "job_count": 3,
    "skill_counts": {"python": 2, "linux": 3, "git": 2, "c++": 1, "pytorch": 1},
    "common_skills": ["python", "linux", "git"],
}
assert run_report("DAY14/岗位样例A_三条岗位.txt", 3)["common_skills"] == ["linux"]
assert run_report("DAY14/岗位样例A_三条岗位.txt", 4)["common_skills"] == []
assert run_report("DAY14/岗位样例C_仅空白行.txt", 1) == {
    "job_count": 0, "skill_counts": {}, "common_skills": [],
}
assert analyze_jobs([["docker"], ["docker", "linux"]], 2) == {
    "job_count": 2,
    "skill_counts": {"docker": 2, "linux": 1},
    "common_skills": ["docker"],
}
```

你的三个函数职责和数据传递都正确。示范直接遍历技能，你通过索引取技能；本题都可用。你保留`analyze_results`中间变量也有助于调试，不是必须删掉的“多余代码”。

真正有价值的差异在测试：示范会主动比较预期结果，错误时停止；你的代码打印报告，需要人逐项看。上面特意展示同一份A文件改阈值和直接传列表两种测试，帮助确认参数真正起作用。

这里沿用原题保证：单个岗位内没有重复技能。不是临时加入去重要求。若把所有字符与技能处理的总规模记作N，读取加统计平均O(N)，保留完整岗位和计数表所占内存随数据增长，不是O(1)。

### 04：区分空内容与读取失败

```python
def try_read_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return {"ok": True, "text": content}
    except FileNotFoundError:
        return {"ok": False, "error": "找不到文件"}


assert try_read_text("DAY14/岗位样例C_仅空白行.txt") == {
    "ok": True, "text": "\n\n",
}
assert try_read_text("DAY14/岗位样例D_不存在.txt") == {
    "ok": False, "error": "找不到文件",
}
print("缺失路径已处理，后面的语句仍能执行")
```

你把成功的`return`写在`with`里面，这也是正确的：离开`with`返回之前仍会清理文件。示范写在外面只是方便看清“读取”和“返回”。未设置的其他错误仍会向外报告，不能把这个函数理解成能处理所有文件故障。

### 05：原计数器题的存档答案，不要求回补

你没有提交实现，因此这里不能进行代码差异评价。保留示范是为了满足“前一天所有题有答案”的约定；今天的支线已替换，下面不作为必读或作业。

<details>
<summary>需要时展开原题示范</summary>

```python
class StudyCounter:
    def __init__(self, name):
        self.name = name
        self.solved = 0

    def record_success(self):
        self.solved += 1
        return self.solved

    def reset(self):
        self.solved = 0


first = StudyCounter("小陈")
second = StudyCounter("小李")
assert first.record_success() == 1
assert first.record_success() == 2
assert second.solved == 0
assert second.record_success() == 1
assert first.reset() is None
assert first.solved == 0
assert second.solved == 1
assert first.name == "小陈"
```

`is None`是判断结果是否就是`None`对象的常用写法；`reset`没有提供具体返回值，因此返回`None`。这段只供原题参考，今天不增加新的计数器任务。

</details>

## 三、DAY14理论题示范与反馈

1. **返回时机：** 两数之和需要一对合法索引，找到就已完成要求；收集全部岗位需要把文件处理完。你的解释正确，提前返回不是永远好或永远坏，取决于要求是否已经满足。
2. **空列表与None：** `[]`是有类型、可遍历、长度为0的列表；`None`是一个特殊值，经常表示没有提供结果，不是“这个变量不存在”。0条岗位返回`[]`，调用者仍能正常统计。你的实际代码已做对，口述补准即可。
3. **额外空间：** `s/t`是已给输入；字符计数字典是新建辅助空间；布尔返回值是固定大小输出。你对“输入以外新使用的空间”的方向正确，不必联想到硬件寄存器；这些数据通常是程序管理的内存。
4. **with与except：** `with`清理已打开文件；`except`匹配某种异常并执行处理代码，而不是“制造或设定错误原因”。你的回答和代码已能表达这一分工。
5. **字典相等：** 比较的是键值对应关系，不是插入先后。哈希值不是每个数据独有的身份证，下面补充；你当前理由不正确，但结论可用。
6. **换输入测试：** `analyze_jobs([["docker"], ["docker", "linux"]], 2)`应只筛出`docker`，频率为`docker:2, linux:1`。如果仍得到原文件里的Python/C++报告，就可能忽略了参数。你本题留白，项目实际已正确使用参数，不要求另写长篇补交。
7. **387变量与复杂度：** `letters`保存次数，`word`保存每个字符最后一次出现的位置；平均时间O(n)，辅助空间O(k)。只允许26种小写字母时k上限固定，所以O(1)。你的时间分析正确，空间解释需要修正。
8. **原支线：** 类规定状态与操作，对象是具体实例；普通实例方法通过对象调用时自动收到该对象作为`self`，`__init__`负责实例初始化。未答，今天改在神经元上学习，不记为已经掌握。
9. **封装：** 把相关状态和操作组织起来，提供清楚的使用方式；不等于所有数据在语言层面都不能被外部访问。神经元中就是把参数和前向计算放在一起。未答，今天结合代码理解。

## 四、只补两个会影响算法表达的概念

### 1. 哈希值不保证唯一

哈希（hash）把键转换为便于定位的数值；哈希冲突（collision）是不同键可能得到相同哈希值。人话：先按编号找一个柜子，不等于同一个柜子里永远只能放一件东西。字典还要区分真正的键，不能只看编号是否相同。[Python可哈希对象定义](https://docs.python.org/3.11/glossary.html#term-hashable)

所以解释字典相等，直接说“拥有相同键及对应值”，就准确且够用。无需猜“唯一哈希编码”。字典迭代顺序与相等比较是两套规则；更新已存在键的值不会改变该键原来的插入位置。[Python字典规则](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)

### 2. 字符串变长，不一定出现更多种字符

`"aaaa"`长度4，`"a" * 100000`长度十万，但两者只需保存键`a`及一个计数。遍历次数增加，字典键数没有增加。

设n为字符总数、k为不同字符数。你的两个字典各至多k项，合起来O(2k)，简写O(k)。若固定小写英文字母，k不超过26，写O(1)。若字符种类不固定，O(k)最坏可写O(n)。不能说“所有字典题都是O(1)”或“输入变长种类必定变多”。

这是同一段代码在不同输入约束下的分析，不要求背两套答案；计数按通常机试的固定大小存储单位估算即可。

## 五、C++第一课：把已有的计算思路交给另一种语言

今天不学习新算法套路。函数、判断、遍历的思路你已会，变化的是C++怎样表达，以及怎样把源代码变成可运行程序。

### 1. 编译不是运行，VS Code也不是编译器

源代码（source code）是你写的`.cpp`文字。编译器（compiler）检查并翻译代码；链接（linking）把需要的程序部分组合起来；最终得到可执行文件（executable）。今天一条`clang++`命令会替你完成这些步骤，不分别操作中间文件。[Clang官方说明](https://clang.llvm.org/docs/CommandGuide/clang.html)

人话：`.cpp`是做菜说明，编译得到能执行这套说明的程序，再启动它。修改了说明，必须重新编译；直接运行旧程序不会自动包含刚刚改过的代码。Python也有内部编译过程，不能简单理解为“Python完全不编译”；区别是你当前通常用`python3 文件.py`一次完成运行。

已只读检查本机环境：Apple Clang 21.0.0，arm64；今天使用`clang++ -std=c++17`，不改变系统Python。你无需再装一个编译器。

### 2. 一个最小可运行示例，逐行认识外壳

这是理论示例，不是预算或耗时统计作业的答案。

```cpp
#include <iostream>

int main() {
    int completed = 4;
    std::cout << completed << '\n';
    return 0;
}
```

- `#include <iostream>`让这份源代码能使用标准输入输出库的声明。当前可理解为“告诉编译器我要用哪些工具”，不是Python的`import`原封不动换名。
- `main`是这个独立程序的入口，运行时从这里开始执行我们的代码。它前面的`int`说明返回整数；这里`return 0;`向系统表示成功结束，不是在屏幕打印0。[main入口说明](https://learn.microsoft.com/en-us/cpp/cpp/main-function-command-line-args?view=msvc-170)
- `{`和`}`围住代码块，作用类似Python冒号后的缩进区域；缩进仍应清楚，但C++主要按大括号判断范围。
- `int completed = 4;`声明一个整数变量，并给初始值。普通语句末尾需要分号；`#include`行不加分号。
- `std`是标准库的命名空间（namespace），像一个工具所属的名称范围；`::`表示在该范围里找`cout`。今天保留`std::`，不增加省略它的另一套写法。
- `std::cout << completed`把值送到标准输出，通常就是终端。后面的`<< '\n'`再输出换行；这里单引号包住一个换行字符。

程序入口、分号和括号可以查，不把第一次记不住标成不会编程。目标是自己写出、编译并理解它。

### 3. 类型：先说这个变量要装哪类值

类型（type）规定值的类别和允许的操作。C++里今天写出的局部变量和参数在编译时就有确定类型，不能像Python变量那样随意重新绑定成完全不同类型。

| 写法 | 作用 | 与已学Python的联系 |
|---|---|---|
| `int count = 0;` | 整数计数 | 类似`count = 0`，但C++的`int`范围有限 |
| `double loss = 0.5;` | 近似表示小数 | 类似用浮点数表示loss，今天只认识、不做精度实验 |
| `bool found = false;` | 真或假 | C++写`true/false`，不是`True/False` |

整数除法要小心：C++的`5 / 2`得到2，`5.0 / 2`得到2.5；不要把Python的`/`习惯直接搬过来。今天作业不涉及平均数，避免同时处理除零与小数误差。

`int`不是无限大整数，越界不能当作自动变成Python大整数。今天限定输入规模，使总和在本机`int`范围内；之后学`long long`与溢出判断，不背所有类型字节数。[C++基本类型](https://learn.microsoft.com/en-us/cpp/cpp/fundamental-types-cpp?view=msvc-170)

### 4. 函数：返回类型、名称、参数、函数体

先看一个标量例子：

```cpp
int triple(int value) {
    return value * 3;
}
```

左侧第一个`int`说返回整数，括号里的`int value`说接收一个整数。`return`仍结束当前函数，把结果交给调用者。把这段放在`main`前，`main`内就可以写`int result = triple(4);`。

今天统一“先定义函数，再写main调用”，不同时教函数前置声明。普通返回`int`的计算函数，所有正常走到结束的路径都应该提供结果；不能沿用Python遗漏`return`后得到`None`的想法。`main`的特殊规则不推广给其他函数。[C++函数说明](https://learn.microsoft.com/en-us/cpp/cpp/functions-cpp?view=msvc-170)

### 5. vector：先把它看作装同类元素的可变长列表

`std::vector<int>`是存放整数的顺序容器（container）。容器就是帮你保存一组数据的工具。现在只需要会建立和遍历它，不学习模板原理；`<int>`说明元素是整数。

```cpp
#include <vector>
#include <iostream>

int main() {
    std::vector<int> values = {6, 9};
    values.push_back(12);
    int first = values[0];
    std::cout << first << '\n';
    return 0;
}
```

这里的三个新动作分别是：`{6,9}`建立两个元素，`push_back(12)`在末尾追加，`[0]`取第一个元素。输出仍然是6；下一段再学习如何遍历它们。

索引仍从0开始，不能访问长度以外的位置；`vector`的`[]`不保证像Python那样抛出越界异常。`values.size()`可以读元素个数，`values.empty()`判断是否为空。今天遍历直接取元素，不需要索引类型转换。[vector官方库文档](https://learn.microsoft.com/en-us/cpp/standard-library/vector-class?view=msvc-170)

### 6. 遍历与判断：一项一项看，再决定是否处理

下面是放在`main`内部的局部示例，需要文件顶部有`#include <vector>`和`#include <iostream>`：

```cpp
std::vector<int> values = {3, -2, 0};
for (int value : values) {
    if (value > 0) {
        std::cout << value << '\n';
    }
}
```

`for (int value : values)`叫基于范围的循环（range-based for）：依次取出每个元素，交给本轮`value`；这里的冒号不是Python的“开始代码块”，而是分隔元素变量与容器。它对应你熟悉的`for value in values`。空容器就执行0轮。[范围循环说明](https://learn.microsoft.com/en-us/cpp/cpp/range-based-for-statement-cpp?view=msvc-170)

`if (value > 0)`把判断放在括号里，为真才进入大括号。`==`比较是否相等，`=`赋值；`count += 1;`仍是增加1。循环结束后再返回统计结果，继续用你已经修复的返回时机知识。

### 7. 用assert检查，而不只是看打印

在文件顶部加入`#include <cassert>`，在`main`内写`assert(triple(4) == 12);`即可检查结果。C++的`assert`条件放括号中，末尾有分号；正确时不输出，错误时报告并终止。今天编译不设置`NDEBUG`，保留断言检查。[assert说明](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/assert-macro-assert-wassert?view=msvc-170)

`triple`例子与这里的测试只教语法。今天你自己决定作业如何实现，并将规定数据写成自己的断言。

### 8. 今天暂用值传参，明确它的代价

普通整数参数例如`int value`得到一个值副本，修改它不改调用者的整数。今天的容器函数也先写`std::vector<int> times_ms`：传入一个现有vector时通常复制其中元素，所以即使函数只用一个累计变量，也要算这份O(n)的副本。

因此今天可以说“遍历只需O(1)辅助状态，但当前值传参版本含O(n)的输入副本”。下一课学引用与`const`，再解释怎样避免复制；不提前塞一个看不懂的`const ... &`让你机械照抄。

## 六、神经网络支线：一个神经元到底算了什么

这节替换计数器练习。教材已核对：本地《神经网络与深度学习（邱锡鹏）》4.1，书内页79～80（PDF阅读器第94～95页），以及4.1.2，书内页83（PDF第98页）。只取神经元公式、图4.1所表达的关系和ReLU定义；不要求今天读后面的导数、变体或整章。

来源：:codex-file-citation{path="/Users/chen/CCY/学习资料/AI agent/神经网络与深度学习 (邱锡鹏).pdf" purpose="source"}。本节数值例子与教学拆分为重新设计，不复制教材图页，不把书放进GitHub。

### 1. 先认识一个真实计算单元，不急着整个网络

人工神经元（artificial neuron）是神经网络的一种基本计算单元。今天只给它一个数x，先计算`z = w * x + b`，再计算`a = ReLU(z)`。这是真实的神经元前向运算，只是输入维度为1，不是把普通计数器换个名字。

| 符号 | 名称 | 人话与代码角色 |
|---|---|---|
| x | 输入（input） | 这次交给神经元的一个数，每次调用可以不同 |
| w | 权重（weight） | 乘在输入上的参数；正负与大小决定这项贡献怎样改变 |
| b | 偏置（bias） | 乘完后再整体加的参数，让x为0时也能有非零的z |
| z | 激活前的值 | `w*x+b`这一小步的临时结果 |
| a | 输出/激活值（activation） | 经过激活函数后返回的数 |

参数（parameter）是模型保留、之后可以学习调整的值。先把w和b理解成两个调节旋钮：同样的x，旋钮不同，结果可能不同。w不总是“重要程度越大越好”，它也可以是负数；b不是报错补偿，而是公式本来就包含的一项。

严格说`w*x+b`是仿射变换（affine transformation）；很多模型资料把含偏置的这种层叫线性层。今天只要算对，不必背术语差别。

### 2. ReLU只做一个明确的规则

ReLU（Rectified Linear Unit，修正线性单元）是一种激活函数：z大于等于0就原样输出，小于0就输出0。数学写作`max(0,z)`，今天代码可以用你已学的`if`实现，不需要任何库。

注意截断的是算完后的z，不是看x正负就直接决定。举例w为-2、b为1、x为-3，z等于7，尽管输入是负数，输出仍是7。

为什么需要激活函数？仅把“乘一下、加一下”的层连续堆起来，仍能合成一次这样的计算。例如`2*(3*x+1)+4 = 6*x+6`。ReLU在0两侧遵循不同规则，使整个函数不再是一条直线，为后续网络表达更复杂关系提供基础。它的输出也不是概率，可能大于1。

### 3. 手算一次，区分计算和学习

先设w=3、b=-2，算下面的小例子：

| x | z=3x-2 | a=ReLU(z) |
|---:|---:|---:|
| 2 | 4 | 4 |
| 0 | -2 | 0 |
| -1 | -5 | 0 |

从输入算到输出叫前向计算（forward computation）。训练（training）还需要目标答案、误差评价和调整参数的方法。今天w、b由我们手动指定，只验证前向；重复调用`forward`不会自动学习，不声称已训练模型或得到有实际预测价值的参数。

后续路线会逐步添加多个输入、多个神经元、一层、多层、损失和梯度。数学只按当前计算所需来补，不会下一课突然要求会矩阵微分。

### 4. 为什么这时用类：一组参数和使用它的运算放在一起

类（class）规定同类对象的状态和行为，对象/实例（object/instance）是具体的一份。我们希望神经元A与B拥有自己的w和b，都能执行前向；因此参数属于实例，输入x属于这次调用。

先看一个更小的网络参数示例，只演示初始化，不给出今天神经元的完整实现：

```python
class BiasParameter:
    def __init__(self, value):
        self.value = value


left_bias = BiasParameter(-2)
right_bias = BiasParameter(1)
assert left_bias.value == -2
assert right_bias.value == 1
```

`BiasParameter`这里只保存真实的偏置参数，还不是一个会计算的神经元。逐行拆开：

- `class BiasParameter:`定义类；类名不是变量值，直到调用它才得到实例。
- `def __init__(self, value):`定义初始化方法，前后各两个下划线。创建实例时用它设置初始状态，不用手动调用它；它不应返回一个具体计算结果。
- `self`按惯例表示“当前这个实例”，通过对象调用普通实例方法时自动传入，不是关键字，也不是全局变量。
- 右侧`value`是创建时传入的参数；左侧`self.value`把值保存在当前实例的属性（attribute）里。初始化结束后仍能通过这个实例访问它。
- 两次创建得到两份实例，分别保存-2和1。这里的数值参数各自绑定；以后用列表参数时还会专门检查是否共享同一可变列表，不把“用了类”误解为自动深拷贝所有数据。

方法（method）是定义在类里的函数。今天作业的前向入口约定为`forward(self, x)`：调用`neuron.forward(3)`时，Python自动把`neuron`交给`self`，你写的3交给x。方法内部可以读取`self.weight`、`self.bias`，z则可以是本次调用的局部变量，不必把所有中间结果都存为属性。[Python类与实例方法](https://docs.python.org/3.11/tutorial/classes.html)

`forward`在普通Python类里只是我们约定的方法名，Python不会因为它叫这个名字而自动执行神经网络。今天用`neuron.forward(x)`明确调用；之后学PyTorch再讲`model(x)`的机制。

### 5. 今天的封装边界

封装（encapsulation）是把相关状态与操作组织起来并提供清楚的接口。在这里，调用者创建神经元时给参数，计算时给x并取回a，无需每次在外面重写公式。

这不等于强制隐藏所有属性。今天允许通过`neuron.weight`和`neuron.bias`检查参数；不学私有属性、继承或装饰器。先让类真的完成一次正确的神经元计算，再在有需要时学习参数检查和层的组合。

## 七、今天作业：只新增四个作答文件

### 时间预算

| 时间 | 做什么 |
|---:|---|
| 15分钟 | 读DAY14反馈，口述哈希与空间两点，昨天答案按需对照 |
| 25分钟 | 任务0：Python闭卷复习LC217，并口述387 |
| 45分钟 | 第五节C++理论，理解编译、函数、vector和断言 |
| 20分钟 | 任务1：独立写第一个C++计算程序，编译与测试 |
| 35分钟 | 任务2：C++训练耗时统计 |
| 30分钟 | 第六节神经元理论与任务3，约15分钟阅读＋15分钟实践 |
| 10分钟 | 简短理论回答、保存运行结果与有意义的Git提交 |

共180分钟。第一次配置或理解超时很正常；优先保留LC217和C++基础，支线可以分两次完成，不为赶课复制答案。不添加额外TODO或一堆日志。每天三步由你写，不预填算法阶段。

### 任务0：LC217存在重复元素，Python复习

文件：`00_Python复习_LeetCode217_存在重复元素.py`。

[LeetCode 217官方题目](https://leetcode.com/problems/contains-duplicate/)，简单：整数列表中只要某个数出现至少两次，返回`True`，否则返回`False`。入口`Solution.containsDuplicate(self, nums)`。今天是DAY12后的第3课复习，先关闭旧答案独立做；沿用已学字典，不为这一题额外学新容器。

测试数据与结果：`[1,2,3,1]→True`、`[1,2,3,4]→False`、`[-2,0,-2]→True`、`[7]→False`。本地扩展`[]→False`，平台输入本身至少一项。自己再设计一组测试，写时间与额外空间复杂度。

目标20分钟左右独立编码；剩余约5分钟口述DAY14的387：两个字典各存什么？索引被覆盖为什么仍正确？不要求再重抄387。

如需提示，先提交你的分析、现有代码与卡住的输入。今天不给217完整答案；DAY16再提供示范。

### 任务1：C++函数与编译

文件：`01_C++入门_函数与编译.cpp`。

实现普通函数`int remaining_budget(int total, int used)`，返回总预算减去已使用量；结果允许为负数，表示超额。今日输入均在0～1000，不涉及溢出。再写自己的`main`和断言：`(10,3)→7`、`(5,5)→0`、`(3,7)→-4`，自己加一组。

你必须亲手写出所需头文件、函数定义、main和测试，不提供填空外壳。若想打印其中一个结果，可以使用已教的`std::cout`，不是必选。

再做一次小调试：先让正确版本跑通，临时删除一条普通语句末尾的分号，重新编译，读第一条错误提示；修复后再次编译并运行。只在本题自己的文件里操作，最后保留修好的版本。记录“错误提示中哪个词或位置帮助了我”一句话即可。

### 任务2：C++训练耗时统计，项目02的第一个计算部件

文件：`02_C++实践_训练耗时统计.cpp`。

输入是一组已读出的训练步耗时，单位毫秒。训练步（training step）暂理解为模型训练的一次更新；今天不训练模型，只分析耗时数据。后面会把文件解析接到这两个函数前面，发展成C++日志分析器。

从空白实现两个普通函数：

- `int total_time_ms(std::vector<int> times_ms)`：返回总耗时。
- `int count_slow_steps(std::vector<int> times_ms, int threshold)`：返回耗时大于或等于阈值的步数。

输入保证：最多1000项，每项0～10000，阈值为0～10000；不需要处理字符串、不需要读取文件、不需要排序。总和最大一千万，在本机`int`范围内。

| 耗时输入 | 阈值 | 总耗时 | 慢步骤数量 |
|---|---:|---:|---:|
| `[80,120,100,90]` | 100 | 390 | 2 |
| `[80,120,100,90]` | 121 | 390 | 0 |
| `[]` | 100 | 0 | 0 |
| `[100]` | 100 | 100 | 1 |
| `[0,0]` | 0 | 0 | 2 |

表中用方括号是为了方便读数据；C++建立vector时用本课教过的写法。自己写`main`，构造数据并断言；再加一组自己的数据。连续换不同数据调用，确认结果没有沿用上次累计值。

口述两点：空列表为什么仍有结果？你的遍历状态占多少空间，当前vector值传参还多了什么开销？不要求打印一份长报告。

### 任务3：真实的单输入ReLU神经元

文件：`03_神经网络支线_单输入神经元.py`。

目标说清楚：你要做一个能保留w、b的对象。每次输入一个x，返回`ReLU(w*x+b)`这个数。它不是分类器、不返回字符串，也不修改w和b；今天没有训练步骤。

外部接口约定：类名`SingleNeuron`，初始化接收`weight`、`bias`；能读取同名实例属性；计算方法`forward(self, x)`返回数值。不得在方法里固定使用样例的权重，必须使用当前对象自己的参数。

先在注释中自己手算z和输出，再写类及断言：

| 实例 | weight | bias | 输入x | 应返回 |
|---|---:|---:|---:|---:|
| A | 2 | -1 | 3 | 5 |
| A | 2 | -1 | 0 | 0 |
| A | 2 | -1 | 0.5 | 0 |
| B | -1 | 2 | 3 | 0 |
| B | -1 | 2 | -1 | 3 |

同一个A连续接收不同输入，再调用B，再回到A输入3，仍应得到5。检查两个对象的参数没有在计算中改变。自己增加一个测试并写出手算依据。

今日只允许你已学的类、函数、普通数值运算、判断和断言；无新库、无张量、无自动求导。不预填初始化或前向实现，卡住时告诉我具体哪一个概念或哪一行不会。

## 八、在Mac本地运行：先编译成功，再启动程序

从仓库根目录运行：

```bash
cd /Users/chen/CCY/Algorithm-Learning-Days
python3 DAY15/00_Python复习_LeetCode217_存在重复元素.py
```

沿用你当前Python环境，`python3`无需替换系统版本。先写完C++任务1，再执行：

```bash
mkdir -p .build/DAY15
clang++ -std=c++17 -Wall -Wextra -pedantic DAY15/01_C++入门_函数与编译.cpp -o .build/DAY15/budget
```

确认上一条命令没有编译错误，再运行：

```bash
./.build/DAY15/budget
```

任务2同理：

```bash
clang++ -std=c++17 -Wall -Wextra -pedantic DAY15/02_C++实践_训练耗时统计.cpp -o .build/DAY15/timing
```

成功后：

```bash
./.build/DAY15/timing
python3 DAY15/03_神经网络支线_单输入神经元.py
```

`mkdir -p`在不存在时建立输出目录；`.build`是本地编译产物，不是作业源代码。`-std=c++17`选语言标准；`-Wall -Wextra -pedantic`开启常用警告及标准相关诊断，不代表能抓住所有逻辑错误；`-o`指定输出文件。路径前的`./`表示从当前目录启动该文件。

不要把`.cpp`交给`python3`，也不要把本地`main`直接贴到LeetCode的方法答题区。今天C++先做本地程序；后面专门讲C++的`Solution`外壳，不在第一天顺带加入另一套类语法。

如果编译失败，旧可执行文件可能仍在，因此不能用“旧程序还能运行”证明新代码正确。按第一条错误定位并重新编译。如果只有空白说明，Python可能安静退出，但C++因缺少main不能链接；这都不代表作业已完成。

仓库原来没有根目录`.gitignore`，本次添加了一份，用于忽略`.build`、缓存和虚拟环境，不复制到各DAY。已有Git历史里的`.DS_Store`不会因新增忽略规则自动消失，本次没有修改或移除它。教师没有替你提交或推送。

## 九、今日理论回答与验收

只回答下面6项，写在这里或你自己的课后文件，选一处即可。可以简短，但要结合自己代码。

1. C++修改源码后为什么要重新编译？`main`中的`return 0`和输出0有什么不同？
2. 用自己的函数解释返回类型、参数类型；为什么耗时累加器要初始化为0？
3. 用`vector`和Python列表比较今日遍历写法；当前值传参为什么会有输入副本？
4. LC217最重要的状态是什么？它的空间分析为什么不能照搬LC387的“26种字母”？顺带用一句话修正“哈希值一定唯一”。
5. 神经元的输入、参数、中间值、输出分别是什么？手算一组自己增加的数据。
6. `self.weight`与输入x分别属于谁？创建两个实例为何需要分别测试？只调用forward为什么还不叫训练？

再留一行：LC217用了多久、是否查过答案或获得提示，以及今天最不明白的一个点。无需写流水账或重复TODO。

主线验收看能否独立写出LC217、编译并运行自己的C++函数、对不同数据做有效测试；支线看手算与代码是否一致、参数是否属于各自实例。评分继续25/30/20/15/10，不按代码行数、注释长度或是否一次编译成功评价能力。

### 下一步由今天反馈决定

- DAY16：若C++基本程序能独立运行，讲引用与`const`，解决本课vector复制，再用索引循环准备C++简单题；Python复习242并补平台入口。
- 神经元：若能解释并手写单输入版本，再扩展到多个输入的加权和与权重列表；若还混淆self和局部变量，就在真实神经元上换数据练，不换回计数器。
- DAY17复习387，DAY18复习LC1，DAY19复习217，DAY20复习242，DAY21复习387；多个复习撞车时一题编码，其余口述。DAY32～35分别回访LC1/217/242/387。
- C++第一天不要求高效写出哈希题；先跑通基本程序，再学对应容器。同一算法后续用两种语言迁移，不同时背两套解法。

今天的耗时统计与神经元会继续长成项目，不一次性生成新仓库或大量空目录。此前所有DAY和你的代码保持原样。课程参考以本文链接的官方文档及已核对本地教材为主，今天不要求额外通读任何书。

C++阶段的开源对照选用[TheAlgorithms/C-Plus-Plus](https://github.com/TheAlgorithms/C-Plus-Plus)，代码采用[MIT许可证](https://github.com/TheAlgorithms/C-Plus-Plus/blob/master/LICENSE)。本次借鉴范围是“独立函数＋可运行程序＋自测”的组织方式，耗时统计题和数据是围绕训练日志重新设计的，并未搬入仓库实现。先完成自己的版本，再按当天所学选看局部代码；今天不克隆、不安装、不要求读整仓，后续学会索引查找再看对应实现。

## 十、我的DAY15回答（也可写在自己的课后文件）

1.

2.

3.

4.

5.

6.

LC217用时、提示使用情况、今天最不明白的地方：
