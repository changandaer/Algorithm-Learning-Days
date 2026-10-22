// DAY31：独立完成指针读写与空指针实验；自己写三步、实现和测试，要求见同目录课程。

 /* C++ 里有一条等价规则：p[i] 等价于 *(p + i),不管 p 是数组名，还是指针
    p[i] = *(p + i) 
    p 是首元素地址，p 也是指针变量，并不是地址常量，所以才可以对 p 进行操作
    p + i：指针加法，不是直接地址加 i 字节，是加 i × sizeof (int) 字节
*/


#include<iostream>

void add_to(int* target,int delta);

int main(){

    int origin;
    int add;
    std::cin >> origin >> add;
    int* origin_location = &origin;
    int* copy_location = origin_location;
    add_to(origin_location,add);
    std::cout << *origin_location << ' ' << *copy_location << '\n';

    int new_num = 100;
    origin_location = &new_num;
    *origin_location = 200;
    std::cout << origin << ' ' << new_num << ' ' << *copy_location << '\n';

    return 0;
}

void add_to(int* target,int delta){

    if(target!=nullptr){
        *target += delta;
    }
}

