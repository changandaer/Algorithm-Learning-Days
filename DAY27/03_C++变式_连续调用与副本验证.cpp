// DAY27：复用自己的翻倍函数，连续调用并验证三个容器互不影响，要求见当天课程。

#include<iostream>
#include<vector>

std::vector<int> doubled(std::vector<int> original){

    std::vector<int> double_results;
    for(int i:original){
        double_results.push_back(i*2);
    }
    return double_results;
}

int main(){

    int i=0,n,element;
    std::vector<int> original,first,second;
    std::cin>> n;
    while(i<n){
        std::cin>> element;
        original.push_back(element);
        i++;
    }
    for(int o:original){
        std::cout<< o <<'\n';
    }
    first = doubled(original);
    second = doubled(first);

    if(first.size()>0){
        first[0] += 1;
    }
    for(int f:first){
        std::cout<< f <<'\n';
    }


    for(int s:second){
        std::cout<< s <<'\n';
    }

    return 0;
}