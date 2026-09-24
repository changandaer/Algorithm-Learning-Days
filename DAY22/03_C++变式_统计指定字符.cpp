// DAY22 C++变式：读取字符串和目标字符，统计出现次数；准确输入输出见课程，自己实现。
#include<iostream>
#include<cassert>

int main(){

    std::string word;
    char target;
    std::cin >> word;
    std::cin >> target;
    int total = 0,len = word.size();

    for(int i = 0;i<len;i+=1){

        if(word[i] == target){
            total += 1;
        } 
    }

    std::cout<< total <<"\n";


    return 0;
}