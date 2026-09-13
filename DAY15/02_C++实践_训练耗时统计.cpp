// DAY15任务2：用vector和函数实现训练耗时统计；自己写三步分析、实现和测试。

#include <iostream>
#include <vector>


int main() {

    // std::vector<int> values = {6, 9};
    // values.push_back(12);
    // int first = values[values.size() - 1];
    // std::cout << first << '\n';

    std::vector<int> values = {-3, -2, 0, 1, 2, 3};
    for (int value : values){
        if (value > 0){
            std::cout << value << "\n";
        }
    }
    return 0;
}

int total_time_ms(std::vector<int> time_ms){

    
}

int count_slow_steps(std::vector<int> times_ms, int threshold){}