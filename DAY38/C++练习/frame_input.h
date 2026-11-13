// 复用 DAY37 的 Image 和函数声明，加防重复包含，再声明固定切四块的一参数重载。
#include<vector>
#pragma once

struct Image{
    int width;
    int height;
    std::vector<int> pixels;
};

Image crop_colum(const Image& source,int start_col,int crop_width);

std::vector<Image> split_views(const Image& source,int num_views);
std::vector<Image> split_views(const Image& source);