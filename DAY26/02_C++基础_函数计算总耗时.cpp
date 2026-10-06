// DAY26 C++基础：函数接收vector并返回总耗时，完成副本短检查；自己实现与测试，要求见课程。
#include<iostream>
#include<vector>

int total_duration(std::vector<int> duration){

    int total = 0;
    if(duration.empty()){
        return 0;
    }
    else{

        for(int value : duration){
            
            total += value;
    }
    }
    return total;
}

int main(){

    int n;
    std::cin>> n;
    std::vector<int> duration;
    for(int i=0;n>i;i++){

        int value;
        std::cin>> value;
        duration.push_back(value);

    }
    for(int value : duration){
            
            std::cout<<value<<'\n';
    }
    int total = total_duration(duration);

    std::cout << total<<'\n';

    return 0;
}