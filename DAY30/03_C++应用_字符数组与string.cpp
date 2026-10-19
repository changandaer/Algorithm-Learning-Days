// DAY30：字符数组与string对照；自己写三步与实现，题意及测试见同目录课程。

#include<iostream>

int main(){

    char code[] = "LOSS";
    std::string text = "LOSS";
    std::cout<< sizeof(code) << ' ' << text.size() << '\n';

    int count = 0;
    for(int i=0;i<sizeof(code)-1;i++){
        if(code[i] == 'S'){
            count += 1;
        } 
    }
    std::cout<< count << '\n';

    code[0] = 'B';
    text += "_OK";
    std::cout<< code << ' ' << text << '\n';

    char empty[] = "";
    std::string empty_text = "";
    std::cout<< sizeof(empty) << ' ' << empty_text.size() << '\n';


    return 0;
}

/*

char、字符数组、C风格字符串、std::string之间的关系是什么？

char是单个字符；
字符数组是元素为字符的数组，char arr[N]，是连续存放 char 的一块内存；
C风格字符串是指以空字符`'\0'`标记文本结束，
我的问题是：char arr [5] = {'h','i','!','\0'}; 和 char arr [] = "hi"; 一样吗？都是 C 风格字符串吗？
std::string是C++为了字符串，新添加的一个类

*/