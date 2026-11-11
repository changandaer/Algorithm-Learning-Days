// 包含同一个头文件，用两种尺寸的图和坏输入验证结果。按课件做一次漏链接实验。
#include "frame_input.h"
#include<cassert>
#include<iostream>

int main(){
    Image source{8,2,{10,11,20,21,30,31,40,41,
                      12,13,22,23,32,33,42,43}};

    std::vector<Image> views_four = split_views(source,4);
    assert(views_four.size() == 4);
    assert((views_four[0].pixels == std::vector<int>{10, 11, 12, 13}));
    assert((views_four[1].pixels == std::vector<int>{20, 21, 22, 23}));
    assert((views_four[2].pixels == std::vector<int>{30, 31, 32, 33}));
    assert((views_four[3].pixels == std::vector<int>{40, 41, 42, 43}));
}