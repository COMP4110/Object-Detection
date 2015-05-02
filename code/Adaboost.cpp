/**
 * Implementation example:
 * 		http://docs.opencv.org/doc/tutorials/objdetect/cascade_classifier/cascade_classifier.html#cascade-classifier
 * Cascade Classification documentation:
 * 		http://docs.opencv.org/modules/objdetect/doc/cascade_classification.html#haar-feature-based-cascade-classifier-for-object-detection
 * 	Cascade Classifier Training:
 * 		http://docs.opencv.org/doc/user_guide/ug_traincascade.html
 */
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
	// Create variables to store the image and file name.
	cv::Mat frame;
	std::string file;
	// Attempt to load the specified classifier.
	if (cascadeClassifier.load("classifiers/cascade.xml")) {
		// Iterate through every image in the directory. It attempts to read the file and exits the loop if no image
		// was read. This is an alternative to using the boost library.
		for (int i = 1; !(frame = cv::imread(directory + "/" + (file = getFileName(i)), Image.flag)).empty(); i++) {
			// Process the current frame.
			processFrame(frame, file);
		}
	} else {
		std::cerr << "Unable to load the cascade classifier." << std::endl;
	}
}

/**
 * Retrieves the file name based on the index within the sequence of images.
 *
 * @param index The current frame within the sequence.
 */
inline std::string Adaboost::getFileName(int index) {
	return Image.prefix + std::to_string(index) + "." + Image.format;
}

/**
 * Processes a frame by converting it to grayscale and applying an equalizing histogram. Objects are then detected in
 * the frame and the processed image is saved.
 *
 * @param frame The current image.
 * @param file The name of the file.
 */
void Adaboost::processFrame(cv::Mat& frame, std::string file) {
	// Create an image container to store the processed frame.
	cv::Mat processedFrame;
	// Convert the frame to grayscale and store it in the new container so it can be processed more efficiently.
	cvtColor(frame, processedFrame, CV_BGR2GRAY);
	// Apply a histogram equalization to improve the image contrast.
	cv::equalizeHist(processedFrame, processedFrame);
	// Detect the objects in the frame.
	detectObjects(frame, processedFrame);
	// Save the frame.
	saveFrame(frame, file);
}

/**
 * Detects objects using the cascade classifier and the processed frame. This method also outputs the detection on
 * the original image.
 *
 * @param frame The original image.
 * @param processedFrame The processed image used with the classifier.
 */
void Adaboost::detectObjects(cv::Mat& frame, cv::Mat& processedFrame) {
	// Create a vector of rectangles to store the detected objects.
	std::vector<cv::Rect> objects;
	// Detect the objects using the processed frame and store the results in objects.
	cascadeClassifier.detect(processedFrame, objects);
	// Iterate through every detection.
	for (size_t i = 0, size = objects.size(); i < size; i++) {
		//Point center(faces[i].x + faces[i].width * 0.5, faces[i].y + faces[i].height * 0.5);
		//ellipse(frame, center, Size(faces[i].width * 0.5, faces[i].height * 0.5), 0, 0, 360, Scalar(255, 0, 255), 4, 8, 0);
		// TODO get the correct point and size
		// Display the detection on the coloured frame.
		displayDetection(frame, cv::Point(50, 50), cv::Size(100, 100));
	}
}

/**
 * Saves a processed frame into a subdirectory.
 *
 * @param frame The image that is being saved.
 * @param file The file name of the image.
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
 * @param frame An image container that stores the image that has found a detection.
 * @param center The center point of the detection.
 * @param size The size of the sphere.
 */
inline void Adaboost::displayDetection(cv::Mat& frame, cv::Point center, cv::Size size) {
	cv::ellipse(frame, center, size, Draw.angle, Draw.startAngle, Draw.endAngle, Draw.color, Draw.thickness, Draw.lineType, Draw.shift);
}
