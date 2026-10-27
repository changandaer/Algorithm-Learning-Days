// DAY32：独立实现const引用的只读统计接口，自己写三步和测试；要求见同目录课程。
#include<iostream>
#include<vector>

int total_duration(const std::vector<int>& values);
int count_over(const std::vector<int>& values,int threshold);

int main(){

    int n;
    std::cin >> n;
    std::vector<int> values;
    int i = 0;
    int value;
    while(i<n){
        std::cin >> value;
        values.push_back(value);
        i++;
    }

    values[0] = 100;

    int threshold;
    std::cin >> threshold;

    int total;
    total = total_duration(values);
    std::cout << total << '\n';

    int counts;
    counts = count_over(values,threshold);
    std::cout << counts << '\n';

    for(int value:values){
        std::cout << value << ' ';
    }
    std::cout<<'\n';

    const std::vector<int> const_values = {2,10,15};

    // const_values[0] = 100;
    int const_total;
    const_total = total_duration(const_values);
    std::cout << const_total  << '\n';

    int const_counts;
    const_counts = count_over(const_values,10);
    std::cout << const_counts << '\n';

    for(int value:const_values){
        std::cout << value << ' ';
    }
    std::cout<<'\n';

    return 0;
}

int total_duration(const std::vector<int>& values){
    // values[0] = 1;
    int total = 0;
    for(int value:values){
        total += value;
    }
    return total;
}
int count_over(const std::vector<int>& values,int threshold){
    int count = 0;
    for(int value:values){
        if(value>threshold){
            count += 1;
        }
    }
    return count;
}