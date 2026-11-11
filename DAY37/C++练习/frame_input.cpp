// 包含自己的头文件，迁移 DAY36 的裁剪、拆分，并补图像尺寸和像素数量检查。
#include "frame_input.h"

Image crop_colum(const Image& source, int start_col, int crop_width){

    Image result = {crop_width, source.height, {}};
    for(int row=0;row<source.height;row++){
        for(int offset=0;offset<crop_width;offset++){
            int col = start_col + offset;
            int index = row * source.width + col;
            result.pixels.push_back(source.pixels[index]);
        }
    }
    return result;
}

std::vector<Image>split_views(const Image& source, int num_views){
    if(num_views <= 0 || source.width <= 0 || source.height <= 0 || source.width % num_views != 0){
        return {};
    }
    const int part_width = source.width / num_views;
    std::vector<Image>views(num_views);
    for(int i=0;i<num_views;i++){
        views[i] = crop_colum(source,i * part_width,part_width);
    }
    return views;
}