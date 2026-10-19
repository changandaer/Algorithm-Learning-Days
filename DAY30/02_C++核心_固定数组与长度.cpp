// DAY30：固定数组与复制实验；自己写三步与实现，题意及测试见同目录课程。

#include<iostream>
#include<vector>

int main(){

    int built_in_array[5] = {};
    for(int i=0;i<5;i++){
        int value;
        std::cin>> value;
        built_in_array[i] = value;
    }

    int total = 0;
    int count = 0;
    for(int i=0;i<5;i++){
        
        total += built_in_array[i];

        if(built_in_array[i]>10){
            count += 1;
        }
    }

    int copy[5] = {};
    for(int i=0;i<5;i++){
        copy[i] = built_in_array[i];
    }
    copy[0] = 99;

    std::cout<< sizeof(built_in_array) / sizeof(built_in_array[0]) << ' ' << total << ' ' << count <<'\n';
    for(int i=0;i<5;i++){
        std::cout<< built_in_array[i];
        std::cout<< ' ';
    }
    std::cout<< '\n';
    for(int i=0;i<5;i++){
        std::cout<< copy[i];
        std::cout<< ' ';
    }

    return 0;
}

// 说明为什么不能访问下标5；程序不要实际访问它。
// 因为输入5个数字，下标是从0-4的，访问下标5会out of bounds