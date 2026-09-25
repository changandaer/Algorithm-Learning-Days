// DAY23 C++基础：读入并保存一组耗时到vector，再输出长度与各项；输入输出见课程，自己实现。
#include<iostream>
#include<vector>

int main(){

    int n;
    std::cin>> n;
    std::vector<int> values;
    for(int i=0;n>i;i+=1){

        int value;
        std::cin>> value;
        values.push_back(value);

    }

    int len = values.size();
    for(int i=0; len>i; i+=1){

        std::cout<< values[i] << "\n";
    }


    return 0;
}