// DAY35：自己实现图像处理器的配置、处理与计数；复用已正确图像函数，要求见同目录课程。
#include<iostream>

struct ImageFrame{
    int camera_id = 0;
    double times_stamp = 0;
    int width = 1;
    int height = 1;
    std::vector<int> pixels = std::vector<int> (width * height);
};

double mean_brightness(const ImageFrame& frame){
    if(frame.pixels.empty()){
        return -1;
    }
    else{
        double total = 0;
        for(const int& pixel:frame.pixels){
            total += pixel;
        }
        return total/frame.pixels.size();
    }

}

std::vector<int> brighten_copy(const std::vector<int>& pixels,int delta){

    std::vector<int> result = pixels;
    for(int& pixel:result){
        pixel += delta;
        if(pixel > 255){
            pixel = 255;
        }
    }
    return result;
}

ImageFrame brighten_frame(const ImageFrame& frame,int delta){
    ImageFrame new_frame = frame;
    new_frame.pixels = brighten_copy(new_frame.pixels,delta);
    return new_frame;
}

class BrightnessProcessor{

    private:
        int delta_ = 0;
        int count_ = 0;

     public:
        bool configure(int delta){
            if(delta>=0 && delta<=30){
                delta_ = delta;
                return true;
            }
            else{
                return false;
            }

        }

        int delta() const{
            return this->delta_;
        }

        int count() const{
            return this->count_;
        }

        ImageFrame process(const ImageFrame& source){
            ImageFrame new_frame = brighten_frame(source,delta_);
            count_ += 1;
            return new_frame;
        }


};
int main(){

    ImageFrame frame;

    std::cin >> frame.camera_id >> frame.times_stamp >> frame.width >> frame.height;
    frame.pixels.resize(frame.width * frame.height);
    for(int& pixel:frame.pixels){
        std::cin >> pixel;
    }

    int delta;
    std::cin >> delta;

    BrightnessProcessor processor;
    bool conf_ok = processor.configure(delta);
    ImageFrame frame_1 = processor.process(frame);
    ImageFrame frame_2 = processor.process(frame);

    std::cout << conf_ok << '\n';
    std::cout << processor.delta() << ' ' << processor.count() << '\n';
    std::cout << mean_brightness(frame) << ' ' << mean_brightness(frame_2) << '\n';

    for(int& pixel:frame_2.pixels){
        std::cout << pixel << ' ';
    }
    std::cout << '\n';

    std::cout << processor.configure(31) << ' ' << processor.delta() << '\n';

    return 0;
}