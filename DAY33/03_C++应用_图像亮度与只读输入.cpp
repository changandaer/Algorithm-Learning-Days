// DAY33：只读借用原图像素并返回调整亮度的副本；自己写三步、实现与测试，要求见同目录课程。
#include<iostream>

std::vector<int> brighten_copy(const std::vector<int>& pixels,int delta);

int main(){

    int n;
    std:: cin >> n;
    std:: vector<int> pixels;
    std:: vector<int> results;
    double total = 0;
    for(int i=0;i<n;i++){
        int pixel;
        std:: cin >> pixel;
        pixels.push_back(pixel);
    }
    int delta;
    std:: cin >> delta;

    results = brighten_copy(pixels,delta);

    for(int pixel:pixels){
        std:: cout << pixel << ' ';
    }

    std::cout << '\n';

    for(int pixel:results){
        total += pixel;
        std:: cout << pixel << ' ';
    }

    std::cout << '\n';
    
    std::cout << total/n << '\n';


    return 0;
}

std::vector<int> brighten_copy(const std::vector<int>& pixels,int delta){
    
    std::vector<int> copy_pixels = pixels;
    for(int& pixel:copy_pixels){
        pixel += delta;
        if(pixel>255){
            pixel = 255;
        }

    }
    return copy_pixels;
}