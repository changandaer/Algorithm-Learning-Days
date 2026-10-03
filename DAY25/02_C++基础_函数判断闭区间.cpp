// DAY25 C++基础：自己实现区间判断函数，并在main中完成副本短检查、输入与输出；要求见当天课程。

#include<iostream>
#include<cassert>
#include<vector>

bool in_closed_range(int value, int low, int high){

    if(value>= low and value <= high){
        return true;
    }
    else{
        return false;
    }

}

int main(){

    int value_1, low_1, high_1;
    std::cin>> value_1 >> low_1 >> high_1;

    bool result_1 = in_closed_range(value_1,low_1,high_1);
    std::cout<< result_1 << '\n';

    int value_2, low_2, high_2;
    std::cin>> value_2 >> low_2 >> high_2;

    bool result_2 = in_closed_range(value_2,low_2,high_2);
    std::cout<< result_2 << '\n';

    return 0;
}