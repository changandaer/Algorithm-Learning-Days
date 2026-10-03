// DAY25 C++变式：把指定范围内的筛选求和写成普通函数；自己分析、实现及验证连续调用，要求见当天课程。

#include<iostream>

int sum_at_least(int start, int end, int threshold){

    int value = start;
    int total = 0;
    while(value<=end){

        if(value>=threshold){

            total += value;
            value += 1;
        }
        else{
            value += 1;
        }

    }

    return total;

}

int main(){

    int start,end,threshold;
    std::cin>> start >> end >> threshold;
    int result = sum_at_least(start,end,threshold);
    std::cout<< result << "\n";

    return 0;
}