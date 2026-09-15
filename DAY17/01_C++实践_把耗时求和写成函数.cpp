// DAY17任务1：独立写一个vector求和函数与main测试；要求见课程，不预填实现。

#include <iostream>
#include <cassert>
#include <vector>

int total_time_ms(std::vector<int> times_ms){

    int total = 0;

    for(int time : times_ms){
        total += time;
        
    }
    return total;

}

int main(){

    std::vector<int>arr{15,25,10};
    int total = total_time_ms(arr);
    std::cout << total << "\n";

    assert(total_time_ms({7}) == 7);
    assert(total_time_ms({}) == 0);
    assert(total_time_ms({0,0}) == 0);
    assert(total_time_ms({12,8}) == 20);

    return 0;
}