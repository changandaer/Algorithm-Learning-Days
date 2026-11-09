// DAY36：复用按列裁剪，模拟 monoImageCallback 将横向拼接图拆成四张。

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

std::vector<Image> split_views(const Image& source,int num_views){

    std::vector<Image> views(num_views);
    for(int i=0;i<num_views;i++){
        views[i] = crop_columns(source,i,((source.pixels.size())/num_views)/2);
    }
    return views;
}


int main(){

    Image source;
    source.height = 2;
    source.width = 2;
    source.pixels = std::vector<int>{10,11,20,21,30,31,40,41,12,13,22,23,32,33,42,43};

    int num_views;
    std::cin >> num_views;

    std::vector<Image> views = split_views(source, num_views);

    for(int i=0;i<num_views;i++){
        for(int pixel:views[i].pixels){
            std::cout << pixel << ' ';
        }
        std::cout << '\n';

    }
    std::cout << '\n';

    return 0;
}