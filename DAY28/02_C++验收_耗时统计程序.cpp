// DAY28：独立完成读取、求和、超时筛选及规定输出，具体接口和测试见当天课程。
#include<iostream>
#include<vector>

int total_duration(std::vector<int> durations){

    int total = 0;
    for(int value:durations){
        total += value;
    }
    return total;

}

std::vector<int> over_limit(std::vector<int> durations, int limit){

    std::vector<int> exceed_limit;
    int count = 0;
    for(int value:durations){
        if(value>limit){
            count += 1;
        }
    }
    exceed_limit.push_back(count);

    for(int value:durations){
        if(value>limit){
            exceed_limit.push_back(value);
        }
    }
    return exceed_limit;

}


int main(){

    int n,duration,total,limit;
    int i=0;
    std::cin>> n;
    std::vector<int> durations;
    std::vector<int> exceed_limit;
    while(i<n){
        std::cin>> duration;
        durations.push_back(duration);
        i++;
    }

    std::cin>> limit;

    total = total_duration(durations);
    exceed_limit = over_limit(durations,limit);

    std::cout<< total << '\n';

    for(int duration : exceed_limit){
        std::cout<< duration << '\n';
    }


    return 0;
}