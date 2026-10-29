// DAY33：按输入数量保存图像像素、统计并正确释放；自己写三步、实现与测试，要求见同目录课程。

/* 固定数组：int pixels[4] = {}; //编译时确定大小，在栈内存，大小不能改，生命周期随作用域结束自动销毁。
   动态数组(C风格)：
                int n = 4; //运行时指定大小 n
                int* pixels = new int[n];  // 在堆上分配n个int，未初始化
                int* pixels2 = new int[n]{}; // 全部初始化为 0，等价于静态数组 ={} 的效果
                pixels[0] = 5; // 使用，和数组一样下标访问
                delete[] pixels; //必须手动释放！不然内存泄漏
                pixels = nullptr; // 置空，防止野指针
*/

#include<iostream>

int main(){

    int n;
    double total = 0;
    int counts = 0;
    std::cin >> n;
    int* pixels = new int[n]{};
    for(int i=0;i<n;i++){
        int pixel;
        std::cin >> pixel;
        if(pixel<50){
            counts += 1;
        }
        total += pixel;
        pixels[i] = pixel;
    }

    delete[] pixels;
    pixels = nullptr;

    std::cout << n << '\n';
    std::cout << total/n << '\n';
    std::cout << counts << '\n';

    return 0;
}

/*
pixels本身存什么？new建出的数据何时结束？只写pixels=nullptr但漏掉释放，会发生什么？

pixels这个指针变量本身存储的是动态数组的第一个元素的地址
new[] 就相当于问操作系统借一间房间(堆内存)
pixels 就相当于存储了借的这间房的房间号
delete[] 就相当于将房间清理之后退还给操作系统
nullptr 就相当于将借来的房间的房间号设置为空，这样操作系统可以收回这个空房间便于后续分配

只写delete[] pixels; 就相当于将房间清理之后还给了操作系统，但是房间号却依旧存在，再想通过这个房间号访问房间就会产生 使用已释放内存 的bug
只写pixels=nullptr但漏掉释放就相当于将房间号设置为空，再也找不到借的房间在哪里，导致房间一直显示被占用，也就是内存泄漏

*/