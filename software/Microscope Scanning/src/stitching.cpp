/*
 * Stitching test, extracted from: http://study.marearts.com/2013/11/opencv-stitching-example-stitcher-class.html
 *
 */

#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <opencv2/stitching/stitcher.hpp>

using namespace cv;
using namespace std;


int main()
{
    vector< Mat > vImg;
    Mat rImg;

    vImg.push_back( imread("../../images/scan01.jpg") );
    vImg.push_back( imread("../../images/scan02.jpg") );

    Stitcher stitcher = Stitcher::createDefault();


    unsigned long AAtime=0, BBtime=0; //check processing time
    AAtime = getTickCount(); //check processing time

    Stitcher::Status status = stitcher.stitch(vImg, rImg);

    BBtime = getTickCount(); //check processing time
    printf("%.2lf sec \n",  (BBtime - AAtime)/getTickFrequency() ); //check processing time

    if (Stitcher::OK == status)
        imshow("Stitching Result",rImg);
    else
        printf("Stitching fail.");

    waitKey(0);

    return 0;
}
