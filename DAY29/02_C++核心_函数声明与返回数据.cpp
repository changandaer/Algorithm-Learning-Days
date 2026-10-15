// DAY29：独立完成函数声明与筛选数据实验；要求见同目录课程，自写三步分析。

#include<iostream>
#include<vector>

std::vector<int> over_limit(std::vector<int> container,int threshold);

int main(){

    int n;
    std::cin>> n;

    int i=0;
    std::vector<int> values;
    while(i<n){

        int value;
        std::cin>> value;
        values.push_back(value);
        i+=1;
    }

    int limit;
    std::cin>> limit;

    std::vector<int> result;
    result = over_limit(values,limit);

    std::cout<< result.size() << '\n';
    for(int value:result){
        std::cout<< value <<'\n';
    }
    
    return 0;
}

std::vector<int> over_limit(std::vector<int> container,int threshold){

    std::vector<int> exceed_limit;
    for(int value:container){
        if(value > threshold){
            exceed_limit.push_back(value);
        }
    }

    return exceed_limit;

}

/* 为什么数量由main读取size()，而不是塞进数据列表？
因为如果塞进数据列表就会破坏原有函数预定的接口，反而破坏函数的逻辑性和整体性

函数内是否能直接读取main里声明的局部阈值变量？
不可以直接读取，必须在调用函数时值传递传给函数
*/