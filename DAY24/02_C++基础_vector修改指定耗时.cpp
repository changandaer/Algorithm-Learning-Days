// DAY24 C++基础：读入耗时并修改指定下标，输出长度与修改后的数据；格式见课程，自己实现。
#include<iostream>
#include<vector>

int main(){

    int n;
    std::cin>> n;

    int i = 0;
    int value;
    std::vector<int> values;
    while(n>i){
        std::cin>> value;
        values.push_back(value);
        i+=1;

    }

    int index,new_value;
    std::cin>> index >> new_value;
    values[index] = new_value;

    std::cout<< n << "\n";

    for(int value : values){

        std::cout<< value << "\n";
    }
    return 0;
}