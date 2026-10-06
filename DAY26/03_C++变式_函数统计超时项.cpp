// DAY26 C++变式：函数接收vector和阈值，统计严格超时项；自己实现与测试，要求见课程。
#include<iostream>
#include<vector>

int count_over_limit(std::vector<int> durations, int limit){
    if(durations.empty()){
        return 0;
    }
    int total = 0;
    for(int value: durations){
        if(value > limit){
            total += 1;
        }
    }
    return total;
}

int main(){

    int n;
    std::cin>> n;
    std::vector<int> durations;
    for(int i=0;i<n;i++){
        int value;
        std::cin>> value;
        durations.push_back(value);
    }
    int limit;
    std::cin>> limit;

    int total = count_over_limit(durations,limit);
    std::cout<< total << '\n';

    return 0;
}