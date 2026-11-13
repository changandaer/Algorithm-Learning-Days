// 复用 DAY37 裁剪和拆分，补尺寸与像素数量检查，再让一参数重载调用两参数版。
#include "frame_input.h"

Image crop_colum(const Image& source,int start_col,int crop_width){

    Image result = {crop_width, source.height, {}};
    for(int row=0;row<source.height;row++){
        for(int offset=0;offset<crop_width;offset++){
            const int col = start_col + offset;
            const int index = row * source.width + col;
            result.pixels.push_back(source.pixels[index]);
        }
    }
    return result;
}

std::vector<Image> split_views(const Image& source,int num_views){
    std::vector<Image> views;
    if(source.height <= 0 || source.width <= 0 || num_views <= 0 || source.width/num_views != 0){
        return {};
    }
    const int part_with = source.width / num_views;
    for(int i=0;i<part_with;i++){
        views[i] = crop_colum(source,i*part_with,part_with);
    }
    return views;

}

std::vector<Image> split_views(const Image& source){
    std::vector<Image> views = split_views(source,4);
    return views;
}