cmake_minimum_required(VERSION 2.8)

project(stitch)

FIND_PACKAGE(OpenCV REQUIRED)

add_executable(stitching stitching.cpp)
target_link_libraries( stitching ${OpenCV_LIBS} )
