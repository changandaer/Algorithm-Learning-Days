// 定义 Image，声明 crop_columns 和 split_views。写法和函数约定见课程第 4 节。
#include<vector>

struct Image{
    int width;
    int height;
    std::vector<int> pixels;
};

Image crop_colum(const Image& source, int start_col, int crop_width);

std::vector<Image> split_views(const Image& source, int num_views);