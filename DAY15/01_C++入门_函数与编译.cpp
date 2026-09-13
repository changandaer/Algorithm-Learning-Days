// DAY15任务1：从空白写预算差额函数、main和测试；要求见课程，不预填实现。
#include <iostream>
#include <cassert>


// int main() {
//     int completed = 4;
//     std::cout << completed << '\n';
//     return 0;
// }

// int triple(int value);

// int main(){

//     int result = triple(4);
//     std::cout << result << '\n';
//     return 0;
// }
// int triple(int value){

//     return value * 3;
// }


// #include <vector>

// int main() {
//     std::vector<int> values = {6, 9};
//     values.push_back(12);
//     int first = values[values.size() - 1];
//     std::cout << first << '\n';
//     return 0;
// }

int remaining_budget(int total, int used){

    return total - used;
}

int main(){

    int result = remaining_budget(10,3);
    std::cout << result << "\n";

    assert(remaining_budget(5,5) == 0);
    assert(remaining_budget(3,7) == -4);
    assert(remaining_budget(9,5) == 4);

    return 0;
}

