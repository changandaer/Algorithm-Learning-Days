// DAY18 C++变式：计算完成比例；要求见当天课程，自己写三步分析、小程序与测试。

#include <iostream>
#include <cassert>

int main(){

    int total = 8, completed = 3;
    double ratio = completed * 1.0 / total;
    double percentage = ratio * 100;

    std::cout << ratio << "\n";
    std::cout << percentage << "%" << "\n";

    total = 8, completed = 0;
    ratio = completed * 1.0 / total;
    percentage = ratio * 100;
    assert(ratio==0);
    assert(percentage==0);

    total = 8, completed = 8;
    ratio = completed * 1.0 / total;
    percentage = ratio * 100;
    assert(ratio==1);
    assert(percentage==100);

    total = 4, completed = 1;
    ratio = completed * 1.0 / total;
    percentage = ratio * 100;
    assert(ratio==0.25);
    assert(percentage==25);

    return 0;
}