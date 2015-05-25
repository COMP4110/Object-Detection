cmake_minimum_required(VERSION 2.8)
project(Object_Detection)

# Compiler settings
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# Shared libraries
FIND_PACKAGE(OpenCV REQUIRED)
FIND_PACKAGE(Boost COMPONENTS system filesystem REQUIRED)

INCLUDE_DIRECTORIES({$OpenCV_INCLUDE_DIRS} REQUIRED)
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR} REQUIRED)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

FILE(GLOB src_files "*.cpp" "*.h")

ADD_EXECUTABLE(Object_Detection ${src_files})
SET_TARGET_PROPERTIES(Object_Detection PROPERTIES LINKER_LANGUAGE CXX)
TARGET_LINK_LIBRARIES(Object_Detection
    ${OpenCV_LIBS}
    ${Boost_FILESYSTEM_LIBRARY}
    ${Boost_SYSTEM_LIBRARY}
    )