// DAY28：独立完成读取、求和、超时筛选及规定输出，具体接口和测试见当天课程。
#include<iostream>
#include<vector>

int total_duration(std::vector<int> values){

    int total = 0;
    for(int value:values){
        total += value;
    }
    return total;

}

int main(){

    int n,total,limit;
    std::vector<int> durations;

    int i=0;
    std::cin>> n;
    while(i<n){
        int duration;
        std::cin>> duration;
        durations.push_back(duration);
        i+=1;

    }
    total = total_duration(durations);
    std::cout<< total << '\n';

    std::cin>> limit; 
    std::vector<int> exceed_limit;
    int count = 0;
    for(int value:durations){
        if(value>limit){
            exceed_limit.push_back(value);
            count += 1;
        }
    }
    std::cout<< count <<'\n';

    for(int i:exceed_limit){
        std::cout<< i << '\n';
    }

    return 0;
}