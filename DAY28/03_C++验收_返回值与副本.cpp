// DAY28：复用自己的筛选函数，验证返回值、原容器和连续调用互不串改，要求见当天课程。
#include<iostream>
#include<vector>

std::vector<int> over_limit(std::vector<int> durations, int limit){

    std::vector<int> exceed_limit;

    for(int value:durations){
        if(value>limit){
            exceed_limit.push_back(value);
        }
    }
    return exceed_limit;

}


int main(){

    
    std::vector<int> original{2,9,4};
    std::vector<int> first_exceed_limit;
    std::vector<int> second_exceed_limit;
    std::vector<int> third_exceed_limit;

    first_exceed_limit = over_limit(original,5);
    second_exceed_limit = over_limit(original,10);

    first_exceed_limit[0] = 99;
    third_exceed_limit = over_limit(original,5);


    for(int duration : original){
        std::cout<< duration<< ',';
    }
    std::cout<< '\n';

    for(int duration : first_exceed_limit){
        std::cout<< duration;
    }
    std::cout<< '\n';

    for(int duration : second_exceed_limit){
        std::cout<< duration;
    }
    std::cout<< '\n';

    for(int duration : third_exceed_limit){
        std::cout<< duration;
    }


    return 0;
}