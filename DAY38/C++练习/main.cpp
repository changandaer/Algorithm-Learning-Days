// 用同一图像测试一参数、两参数重载，以及三行图和坏输入。保留断言与编译结果。
#include"frame_input.h"
#include<cassert>

int main(){

    Image source_1{8,2,{10,11,20,21,30,31,40,41,
                        12,13,22,23,32,33,42,43}};

    std::vector<Image> views_four_one = split_views(source_1);
    std::vector<Image> views_four_two = split_views(source_1,4);
    assert((views_four_one[1].pixels == std::vector<int>{20,21,22,23}));
    assert((views_four_two[1].pixels == std::vector<int>{20,21,22,23}));

    std::vector<Image> views_two_one = split_views(source_1);
    std::vector<Image> views_two_two = split_views(source_1,2);
    assert((views_two_one[0].pixels == std::vector<int>{10,11,12,13}));
    assert((views_two_two[0].pixels == std::vector<int>{10,11,20,21,12,13,22,23}));

    Image source_2{12,3,{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,
                         12,13,14,15,16,17,18,19,20,21,22,23,
                         24,25,26,27,28,29,30,31,32,33,34,35}};
    std::vector<Image> views2_four_one = split_views(source_1);
    std::vector<Image> views2_four_two = split_views(source_1,4);
    assert((views2_four_one[1].pixels == std::vector<int>{3,4,5,15,16,17,27,28,29}));
    assert((views2_four_two[1].pixels == std::vector<int>{3,4,5,15,16,17,27,28,29}));

    return 0;
}