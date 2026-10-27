// DAY32：独立对比修改副本与原容器，自己写三步、实现与测试；要求见同目录课程。
#include<iostream>
#include<vector>

std::vector<int> shifted_copy(std::vector<int>values,int delta);
void shift_original(std::vector<int>& values,int delta);

int main(){

    int n;
    std::cin >> n;
    std::vector<int> values;
    int i = 0;
    int value;
    while(i<n){
        std::cin >> value;
        values.push_back(value);
        i++;
    }

    int delta;
    std::cin >> delta;

    std::vector<int> copy;
    copy = shifted_copy(values,delta);
    for(int value:values){
        std::cout << value << ' ';
    }
    std::cout<< '\n';

    for(int value:copy){
        std::cout << value << ' ';
    }
    std::cout<< '\n';

    shift_original(values,delta);
    for(int value:values){
        std::cout << value << ' ';
    }
    std::cout<< '\n';


    return 0;
}

std::vector<int> shifted_copy(std::vector<int>values,int delta){
    for(int &value:values){
        value += delta;
    }
    return values;
}

void shift_original(std::vector<int>& values,int delta){
    for(int &value:values){
        value += delta;
    }
}