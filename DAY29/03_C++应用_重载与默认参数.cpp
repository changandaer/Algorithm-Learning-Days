// DAY29：独立完成耗时统计的重载与默认参数实验；要求见同目录课程，自写三步分析。
// #include<iostream>
// #include<vector>

// int count_over(std::vector<int> container,int threshold = 10);
// int count_over(std::vector<int> container,int lower_bound,int upper_bound);

// int main(){

//     int n;
//     int i=0;
//     std::cin>> n;
//     std::vector<int> values;
//     while(i<n){
//         int value;
//         std::cin>> value;
//         values.push_back(value);
//         i+=1;
//     }

//     int threshold;
//     std::cin>> threshold;
//     std::cout<< count_over(values,threshold) <<'\n';

//     int lower_bound,upper_bound;
//     std::cin>> lower_bound >> upper_bound;
//     std::cout<< count_over(values,lower_bound,upper_bound);

//     return 0;
// }

// int count_over(std::vector<int> container,int threshold){

//     int count=0;
//     for(int value:container){
//         if(value>threshold){
//             count += 1;
//         }
//     }
//     return count;
// }

// int count_over(std::vector<int> container,int lower_bound,int upper_bound){
    
//     int count = 0;
//     for(int value:container){

//         if(value>lower_bound && value<=upper_bound){

//             count += 1;
//         } 
//     }
//     return count;

// }

/*
学习函数重载的时候，我遇到了一个问题，就是如果我输入 n=5 容器 values={4 10 12 20 20}, 接下来想分别进行以下操作：
只传容器；传容器和 20；传容器、10、20；传容器和 0
但是如果按照我上面这么写，在调用 count_over 函数的时候，必须给两个 count_over 函数都传递相应的参数，main 函数才会执行，
而不是我想要的 按照我输入的内容，main 函数自行决定我想要调用的是哪个 
count_over程序运行后，流程固定：读 n → 读 n 个元素 → 读 1 个 threshold → 调用 2 参版本 → 读 lower、upper 两个数 → 调用 3 参版本。
无法由用户动态选择本次调用哪一个函数。用户不能自由选择：只传容器 / 传容器 + 1 个数 / 传容器 + 2 个数。
C++程序不能 “根据输入参数数量自动选函数”吗？只能写判断语句判断用户输入什么数据然后给数据分配对应的函数执行吗？
*/


#include<iostream>
#include<vector>

int count_over(std::vector<int> values,int threshold = 10);
int count_over(std::vector<int> values,int lower,int upper);

int main(){

    int n;
    std::vector<int> values;
    std::cin>> n;

    for(int i=0;i<n;i++){
        int value;
        std::cin>> value;
        values.push_back(value);
    }

    std::cout<< count_over(values) << '\n';
    std::cout<< count_over(values,20) << '\n';
    std::cout<< count_over(values,10,20) << '\n';
    std::cout<< count_over(values,0) << '\n';

    return 0;
}

int count_over(std::vector<int> values,int threshold){

    int count = 0;
    for(int value:values){
        if(value>threshold){
            count += 1;
        }
    }

    return count;
}

int count_over(std::vector<int> values,int lower,int upper){

    int count = 0;
    for(int value:values){
        if(value>lower && value<=upper){
            count += 1;
        }
    }

    return count;
}