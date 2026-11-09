// DAY36：按 D2SLAM 的裁剪范围，从宽图每一行取出指定的连续列。

#include<iostream>
#include<vector>

struct Image{
    int width;
    int height;
    std::vector<int> pixels;
};

Image crop_columns(const Image& source,int start_col,int crop_width){
    
    Image Rect_image;
    Rect_image.height = source.height;
    Rect_image.width = source.width;
    Rect_image.pixels = std::vector<int>{};
    for(int i=0;i<crop_width;i++){
        Rect_image.pixels.push_back(source.pixels[(start_col-1)*2 + i]);
    }
    for(int i=0;i<crop_width;i++){
        Rect_image.pixels.push_back(source.pixels[(start_col-1)*2 + 8 + i]);
    }
    return Rect_image;
}

int main(){

    Image source;
    source.height = 2;
    source.width = 2;
    source.pixels = std::vector<int>{10,11,20,21,30,31,40,41,12,13,22,23,32,33,42,43};

    Image Rect_image = crop_columns(source, 4, 2);
    std::cout << Rect_image.height << ' ' << Rect_image.width << '\n';
    for(const int& pixel:Rect_image.pixels){
        std::cout << pixel << ' ';
    }
    std::cout << '\n';

    return 0;
}