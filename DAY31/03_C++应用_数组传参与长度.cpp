// DAY31：独立实现数组求和与原地平移；自己写三步与测试，接口见同目录课程。
#include<iostream>

int sum_values(int* values,int length);
void shift_values(int* values,int length,int delta);

int main(){

    int array_in_built[6] = {};
    int n;
    std::cin >> n;

    for(int i=0;i<n;i++){
        int value;
        std::cin >> value;
        array_in_built[i] = value;
    }

    int delta;
    std::cin>> delta;

    //int* location = array_in_built; 
    int* location = &array_in_built[0];
    // 这两种写法等价！

    int old_result = sum_values(location,n);
    std::cout << old_result << '\n';

    shift_values(location,n,delta);
    int shifted_result = sum_values(location,n);
    std::cout << shifted_result << '\n';

    for(int i=0;i<n;i++){
        std::cout << array_in_built[i];
        std::cout << ' ';
    }

    std::cout << '\n';

    return 0;
}

int sum_values(int* values,int length){

    int total = 0;
    for(int i=0;i<length;i++){
        total += values[i]; 
        //values[i] 本身就是在底层执行了指针偏移和解引用（它等价于 *(values + i)）
    }
    return total;

}

void shift_values(int* values,int length,int delta){
    for(int i=0;i<length;i++){
        values[i] += delta;
    }
}