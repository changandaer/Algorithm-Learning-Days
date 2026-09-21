// DAY21 C++变式：连续读取整数，遇0停止并输出此前总和；三步、实现和测试自己写。

#include<iostream>

int main(){

    int n = 0;
    int total = 0;

    while(true){

        std::cin >> n;
        if(n==0){
            break;
        }
        total += n;
    }
    std::cout << total << "\n";

    return 0;
}