// DAY16任务1：在main中观察vector并计算总耗时；题意和测试数据见课程，自己写分析、实现和测试。
#include <iostream>
#include <vector>
#include <cassert>

int main(){

    std::vector<int> values{8,13};
    int len_vector = values.size();
    std::cout << len_vector << "\n";
    values.push_back(5);
    len_vector = values.size();
    std::cout << len_vector << "\n";

    std::vector<int> empty_values{};
    len_vector = empty_values.size();
    std::cout << len_vector << "\n";
    empty_values.push_back(0);
    len_vector = empty_values.size();
    std::cout << len_vector << "\n";
    // std::cout << empty_values[0] << "\n";
    int is_empty = empty_values.empty();
    std::cout << is_empty << "\n";
    assert(empty_values[0] == 0);

    std::vector<int> count_times{15,25,10};
    int count = 0;
    for (int count_time : count_times){

        count += count_time;

    }
    assert(count == 50);


    return 0;
}