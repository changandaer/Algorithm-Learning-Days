// DAY20 C++基础：用普通for循环输出指定范围；自己写三步分析、小程序和测试。

#include<iostream>


int main(){

    int start;
    int end;
    std::cin >> start >> end;


    for(int value = start; value<= end and value >= start; value = value +1){

        std::cout << value << "\n";
    }

    return 0;
}