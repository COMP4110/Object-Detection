#ifndef ADABOOST_H
#define ADABOOST_H

#include <string>

class Adaboost {

	private:

		const struct Image {
			std::string format = "jpg";
			// Load the image as grayscale
			int flag = 0;
		};

		const struct Draw {
			double angle = 0;
			double startAngle = 0;
			double endAngle = 360;
			cv::Scalar color(100, 100, 100);
			int thickness = 1;
			int lineType = 8;
			int shift = 0;
		};

		void processFrames(cv::VideoCapture frames);
		inline void displayDetection(cv::Mat& img, cv::Point center, cv::Size size);

	public:

		void readDirectory(const std::string& directory);

};

#endif
