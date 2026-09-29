// DAY24 C++变式：复制vector后只修改副本，输出并比较两份数据；格式见课程，自己分析和实现。
#include<iostream>
#include<vector>

int main(){

    int n,value;
    std::cin>> n;
    
    std::vector<int> values;

    for(int i=0;n>i;i+=1){

        std::cin>> value;
        values.push_back(value);
        
    }

    std::cout<< n << "\n";
    for(int value:values){
        std::cout<< value << "\n";
    }

    int index,new_value;
    std::cin>> index >> new_value;
    values[index] = new_value;

    std::cout<< n << "\n";
    for(int value:values){
        std::cout<< value << "\n";
    }

    return 0;
}