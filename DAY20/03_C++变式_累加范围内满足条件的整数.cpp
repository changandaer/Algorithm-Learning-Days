// DAY20 C++变式：在范围内筛选并累加；要求见课程，自己写三步分析、小程序和测试。
#include<iostream>

int main(){

    int start,end,threshold;
    std::cin >> start >> end >> threshold;
    int total = 0;

    for(int value = threshold;value >= threshold and value <= end;value = value +1){

        total = total + value;

    }

    std::cout << total << "\n";

    return 0;
}