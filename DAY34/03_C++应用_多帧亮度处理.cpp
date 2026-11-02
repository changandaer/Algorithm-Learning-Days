// DAY34：复用图像处理函数，保存并处理两份帧记录；自己写三步与测试，要求见同目录课程。
#include<iostream>
#include<vector>

struct ImageFrame{
    int camera_id = 0;
    double times_stamp = 0;
    int width = 1;
    int height = 1;
    std::vector<int> pixels;

};

double mean_brightness(const ImageFrame& source){

    if(source.pixels.empty()){
        return -1;
    }
    else{
        double total = 0;
        for(const int& pixel:source.pixels){
            total += pixel;
        }
        return total/source.pixels.size();

    }

};

std::vector<int> brighten_copy(std::vector<int> pixels,int delta){
    for(int i=0;i<pixels.size();i++){
        pixels[i] += delta;
        if(pixels[i]>255){
            pixels[i] = 255;
        }
    }
    return pixels;
}

ImageFrame brighten_frame(const ImageFrame& source,int delta){

    ImageFrame new_frame;
    new_frame.camera_id = source.camera_id;
    new_frame.times_stamp = source.times_stamp;
    new_frame.width = source.width;
    new_frame.height = source.height;

    new_frame.pixels = brighten_copy(source.pixels,delta);

    return new_frame;

}

int main(){

    std::vector<ImageFrame>frames(2);

    for(int i=0;i<2;i++){
        std::cin >> frames[i].camera_id >> frames[i].times_stamp >> frames[i].width >> frames[i].height;
        int total_pixels = frames[i].width * frames[i].height;
        frames[i].pixels.resize(total_pixels);
        for(int j=0;j<total_pixels;j++){
            
            std::cin >> frames[i].pixels[j];
        }

    }

    int delta;
    std::cin >> delta;

    for(const ImageFrame& frame:frames){

        double orig_mean = mean_brightness(frame);

        ImageFrame new_frame = brighten_frame(frame,delta);
        double new_mean = mean_brightness(new_frame);

        // 第一行：编号、时刻、原均值、新均值
        std::cout<< new_frame.camera_id << ' '
                << new_frame.times_stamp << ' '
                << orig_mean << ' '
                << new_mean << '\n';
        
        // 第二行：原像素（空像素则直接换行打印空行）
        for(const int& pixel:frame.pixels){
            std::cout << pixel <<' ';
        }

        std::cout << '\n';

        // 第三行：新像素（空像素则直接换行打印空行）
        for(const int& pixel:new_frame.pixels){
            std::cout << pixel << ' ';
        }
        std::cout << '\n';
    }


    return 0;
}