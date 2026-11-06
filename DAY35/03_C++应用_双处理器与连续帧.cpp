// DAY35：复用02的处理器，用两份对象和两帧验证配置与计数独立；要求见同目录课程。
#include<iostream>
#include<vector>

struct ImageFrame
{
    int camera_id = 0;
    double times_stamp = 1.0;
    int width = 1;
    int height = 1;
    std::vector<int> pixels;

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

std::vector<int> brighten_copy(const std::vector<int> pixels,int delta){

    std::vector<int> pixels_copy = pixels;
    for(int& pixel:pixels_copy){
        pixel += delta;
        if(pixel>255){
            pixel = 255;
        }
    }
    return pixels_copy;
}

ImageFrame brighten_frame(const ImageFrame& frame,int delta){
    ImageFrame copy_frame = frame;
    copy_frame.pixels = brighten_copy(copy_frame.pixels,delta);
    return copy_frame;
}

class BrightenProcessor{
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
        int delta()const{
            return delta_;
        }
        int count() const{
            return count_;
        }
        ImageFrame process(const ImageFrame& source){
            ImageFrame new_frame = source;
            new_frame = brighten_frame(new_frame,delta_);
            count_ += 1;
            return new_frame;
        }
};

int main(){

    std::vector<ImageFrame> frames(2);
    for(ImageFrame& frame:frames){
        std::cin >> frame.camera_id >> frame.times_stamp >> frame.width >> frame.height;
        frame.pixels.resize(frame.width * frame.height);

        for(int& pixel:frame.pixels){
            std::cin >> pixel;
        }
    }
    
    int delta_A;
    int delta_B;
    std::cin >> delta_A >> delta_B;

    BrightenProcessor processor_A;
    BrightenProcessor processor_B;

    bool conf_A = processor_A.configure(delta_A);
    bool conf_B = processor_B.configure(delta_B);

    ImageFrame frame_A_1 = processor_A.process(frames[0]);
    ImageFrame frame_B = processor_B.process(frames[0]);
    ImageFrame frame_A_2 = processor_A.process(frames[1]);

    int count_A = processor_A.count();
    int count_B = processor_B.count();

    std::cout << processor_A.delta() << ' ' << count_A << ' ' << processor_B.delta() << ' ' << count_B << '\n';
    
    double mean_frame_1 = mean_brightness(frames[0]);
    double mean_A_1 = mean_brightness(frame_A_1);
    double mean_B = mean_brightness(frame_B);
    std::cout << mean_frame_1 << ' ' << mean_A_1 << ' ' << mean_B << '\n';

    std::cout << frame_A_2.camera_id << ' ' << frame_A_2.times_stamp << ' ' << mean_brightness(frame_A_2) << '\n';
    
    for(const int& pixel:frames[0].pixels){
        std::cout << pixel << ' ';
    }
    std::cout << '\n';


    return 0;
}