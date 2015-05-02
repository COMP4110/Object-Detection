cmake_minimum_required(VERSION 3.1)
project(Object_Detection)

find_package(OpenCV REQUIRED)
include_directories($OpenCV_INCLUDE_DIRS} REQUIRED)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp)
add_executable(Object_Detection ${SOURCE_FILES} Adaboost.cpp Adaboost.h CascadeClassifier.h CascadeClassifier.cpp)
target_link_libraries(Object_Detection ${OpenCV_LIBS})
