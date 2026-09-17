// DAY19 C++基础：读取耗时和限制，判断是否超时；自己写三步分析、小程序和测试。
#include<iostream>
#include<cassert>

int main(){

    int duration_ms = 0,limit_ms = 0;

    // std::cin >> duration_ms;
    // std::cin >> limit_ms;

    std::cin >> duration_ms >> limit_ms;

    // std::cout << duration_ms << "\n";
    // std::cout << limit_ms << "\n";

    if(duration_ms > limit_ms){

        std::cout << "超时" << "\n";
    }
    else{

        std::cout << "正常" << "\n";
    }

   
    return 0;
}