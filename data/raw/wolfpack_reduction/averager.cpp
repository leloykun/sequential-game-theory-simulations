#include <iostream>
#include <string>

double ar[4][2];
    
int main() {
    std::string temp1, temp2;
    int runs = 10;
    for (int r = 0; r < runs; ++r) {
        std::cin>>temp1>>temp2;
        for (int i = 0; i < 4; ++i) {
            double x, y;
            std::cin>>temp1>>temp2>>x>>y;
            ar[i][0] += x / runs;
            ar[i][1] += y / runs;
        }
    }
    
    std::cout<<"NOTE TO SELF:\n";
    std::cout<<"take the average of the\n";
    std::cout<<"second and third lines\n\n";
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 2; ++j)
            std::cout<<ar[i][j]/14469.4<<" ";
        std::cout<<"\n";
    }
    
    return 0;
}
