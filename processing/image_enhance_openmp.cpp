#include <omp.h>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <algorithm>

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <in.jpg> <out.jpg>\n";
        return 1;
    }
    cv::Mat img = cv::imread(argv[1]);
    if (img.empty()) { std::cerr << "Cannot open " << argv[1] << "\n"; return 1; }
    cv::Mat out = img.clone();

    #pragma omp parallel for collapse(2)
    for (int r = 0; r < img.rows; ++r)
        for (int c = 0; c < img.cols; ++c)
            for (int ch = 0; ch < 3; ++ch)
                out.at<cv::Vec3b>(r, c)[ch] =
                    std::min(255, img.at<cv::Vec3b>(r, c)[ch] + 20);

    cv::imwrite(argv[2], out);
    return 0;
}
