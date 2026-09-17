// DAY19 C++变式：读取分数，按三个区间输出等级；自己写三步分析、小程序和测试。
#include<iostream>
#include<cassert>

int main(){

    int score = 0;
    std::cin >> score;

    if(score >= 85){

        std::cout << "A" << "\n";

    }
    else if(score >= 60){

        std::cout << "B" << "\n";
    }
    else{

        std::cout << "C" << "\n";
    }

}