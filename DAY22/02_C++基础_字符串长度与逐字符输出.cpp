// DAY22 C++基础：读取一个英文字符串，输出长度并逐字符输出；三步、小程序与测试自己写。
#include<iostream>

int main(){

    std::string word;
    std::cin>> word;
    int len = word.size();
    std::cout<< len <<"\n";
    int i = 0;
    while(i<len){
        std::cout<< word[i]<<"\n";
        i += 1;
    }

    return 0;
}