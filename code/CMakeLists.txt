cmake_minimum_required(VERSION 2.8)
project(Object_Detection)

find_package(OpenCV REQUIRED)
include_directories({$OpenCV_INCLUDE_DIRS} REQUIRED)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

file(GLOB SOURCE_FILES "*.cpp" "*.h")
add_executable(Object_Detection ${SOURCE_FILES})
target_link_libraries(Object_Detection ${OpenCV_LIBS})
