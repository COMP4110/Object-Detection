#include <ostream>
#include <iostream>

#include "Adaboost.h"

/**
 * Reads the images in the specified directory and processes them.
 *
 * @param directory The relative path to the directory.
 */
void Adaboost::readDirectory(const std::string& directory) {
	// Capture the frames in the specified directory.
	cv::VideoCapture frames(directory + "/sphere_%03d." + Adaboost::Image.format);
	// Check if the video capture has been initialised.
	if (frames.isOpened()) {
		// Process the frames that were retrieved from the video capture.
		processFrames(frames);
	} else {
		std::cerr << "Could not read the frames in the specified directory." << std::endl;
	}
}

/**
 * Processes a VideoCapture object that contains a sequence of image frames. These frames are converted to grayscale
 * before being processed.
 *
 * @param capture The sequence of frames.
 */
void processFrames(cv::VideoCapture frames) {
	cv::Mat frame;// = cv::imread(file, Adaboost::Image.flag);
	for (int i = 1; frames.read(frame); i++) {
		std::cout << "Processing frame " << i << "." << std::endl;

	}
}

/**
 * Displays a detection on the specified image by drawing an ellipse in the given position.
 *
 * @param img An image container that stores the image that has found a detection.
 * @param center The center point of the detection.
 * @param size The size of the sphere.
 */
inline void Adaboost::displayDetection(cv::Mat& img, cv::Point center, cv::Size size) {
	Adaboost::Draw draw;
	cv::ellipse(img, center, size, draw.angle, draw.startAngle, draw.endAngle, draw.color, draw.thickness, draw.lineType, draw.shift);
}
