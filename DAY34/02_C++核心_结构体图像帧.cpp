// DAY34：用struct保存完整图像帧并只读求均值；自己写三步、实现与测试，要求见同目录课程。
#include<iostream>

struct ImageFrame{
    int camera_id = 0;
    double times_stamp = 0.0;
    int width = 10;
    int height = 10;
    std::vector<int> pixels = std::vector<int> (width * height,0);
};

double mean_brightness(const ImageFrame& frame);

int main(){

    ImageFrame image_frame;
    ImageFrame copy_image_frame = image_frame;
    std::cin >> image_frame.camera_id >> image_frame.times_stamp >> image_frame.width >> image_frame.height;

    std::cout << image_frame.camera_id << ' ' << image_frame.times_stamp << ' ' << image_frame.width << ' ' << image_frame.height;
    std::cout << '\n';

    int total_pixels = image_frame.width * image_frame.height;
    image_frame.pixels.resize(total_pixels); // 这里已经创建了 4 个 0
    

    for(int i=0;i<total_pixels;i++){
        int pixel;
        std::cin >> pixel;
        // image_frame.pixels.push_back(pixel); // 错误！push_back 是在4个0后面“追加”
        image_frame.pixels[i] = pixel;
    }
    
    double mean_pixels = mean_brightness(image_frame);
    std::cout << total_pixels << ' ' << mean_pixels;
    std::cout << '\n';

    for(int pixel:image_frame.pixels){
        std::cout << pixel << ' ';
    }
    std::cout << '\n';




    return 0;
}

double mean_brightness(const ImageFrame& frame){
    std::vector<int> copy_pixels = frame.pixels;
    if(frame.pixels.size() != 0){
        double total = 0;
        for(int pixel:copy_pixels){
            total += pixel;
        }

        return total/frame.pixels.size();
    }
    else{
        return -1;
    }

}