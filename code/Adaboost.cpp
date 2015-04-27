#include <ostream>
#include <iostream>

#include <opencv2/imgproc/imgproc.hpp>

#include "Adaboost.h"

/**
 * Reads the images in the specified directory and processes them.
 *
 * @param directory The relative path to the directory.
 */
void Adaboost::readDirectory(const std::string& directory) {
	// Specify the path as the directory being read.
	path = directory;
	cv::Mat frame;
	std::string file;
	for (int i = 1; !(frame = cv::imread(directory + "/" + (file = getFileName(i)), Image.flag)).empty(); i++) {
		processFrame(frame, file);
	}
}

inline std::string Adaboost::getFileName(int index) {
	return Image.prefix + std::to_string(index) + "." + Image.format;
}

/**
 * TODO
 * Processes a frame by first converting it to a grayscale image.
 *
 * @param frame The image frame.
 */
void Adaboost::processFrame(cv::Mat& frame, std::string file) {
	// Apply a histogram equalization to improve the image contrast.
	cv::equalizeHist(frame, frame);
	// Save the frame.
	saveFrame(frame, file);
}

/**
 * Saves a processed frame into a processed subdirectory.
 *
 * @param frame The frame that is being saved.
 * @param file The name of the frame.
 */
inline void Adaboost::saveFrame(cv::Mat& frame, std::string file) {
	cv::imwrite(getSaveDirectory() + "/" + file, frame);
}

/**
 * Returns the directory where saved images will be stored.
 */
inline std::string Adaboost::getSaveDirectory() {
	return path + "/processed";
}

/**
 * Displays a detection on the specified image by drawing an ellipse in the given position.
 *
 * @param img An image container that stores the image that has found a detection.
 * @param center The center point of the detection.
 * @param size The size of the sphere.
 */
inline void Adaboost::displayDetection(cv::Mat& img, cv::Point center, cv::Size size) {
	cv::ellipse(img, center, size, Draw.angle, Draw.startAngle, Draw.endAngle, Draw.color, Draw.thickness, Draw.lineType, Draw.shift);
}
