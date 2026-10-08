// DAY27：编写返回翻倍后新vector的普通函数及调用程序，要求见当天课程。
#include<iostream>
#include<vector>


std::vector<int> doubled(std::vector<int> oringinal){

    std::vector<int> double_results;
    for(int i:oringinal){
        double_results.push_back(i*2);
    }
    return double_results;
}

int main(){

    int i=0;
    int n,element;
    std::vector<int> original;
    std::cin>> n;
    while(i<n){
        std::cin>> element;
        original.push_back(element);
        i++;
    }
    std::vector<int> double_results;
    double_results = doubled(original);
    for(int i:double_results){
        std::cout << i << '\n';
    }

    return 0;
}