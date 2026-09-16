// DAY18 C++基础：毫秒换算为秒；要求见当天课程，自己写三步分析、小程序与测试。

#include <iostream>
#include <cassert>

int main(){

    int duration_ms = 2500;
    double seconds = duration_ms / 1000.0;
    std::cout << seconds << "\n";

    duration_ms = 750;
    seconds = duration_ms / 1000.0; // 重新计算！
    assert(seconds==0.75);

    duration_ms = 1;
    seconds = duration_ms / 1000.0;
    assert(seconds== 0.001);

    return 0;
}