// DAY21 C++基础：用while输出包含0的倒计时；输入输出见课程，三步、实现和测试自己写。

#include<iostream>

int main(){

    int n = 0;
    std::cin >> n;

    while(n>=0){

        std::cout << n <<"\n";
        n -= 1;
    }

    return 0;
}