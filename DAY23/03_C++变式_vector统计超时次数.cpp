// DAY23 C++变式：先保存耗时，再统计严格超过阈值的项数；输入输出见课程，自己分析和实现。
#include<iostream>
#include<vector>

int main(){

    int n,threshold,value;
    std::cin>> n >> threshold;
    std::vector<int> values;
 
    for(int i=0;i<n;i+=1){

        std::cin>> value;
        values.push_back(value);

    }

    int total = 0;

    for(int value:values){

        if(value > threshold){

            total += 1;
        }
    }

    std::cout<< total<<"\n";

    return 0;
}