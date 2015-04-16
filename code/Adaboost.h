#ifndef ADABOOST_H
#define ADABOOST_H

#include <string>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

class Adaboost {

	private:

		const struct {
			std::string prefix;
			const std::string format;
			// Load the image as grayscale
			int flag;
		} Image = {"sphere_", "jpg", CV_LOAD_IMAGE_GRAYSCALE};

		const struct {
			const double angle;
			const double startAngle;
			const double endAngle;
			const cv::Scalar color;
			const int thickness;
			const int lineType;
			const int shift;
		} Draw = {0, 0, 360, (100, 100, 100), 1, 8, 0};

		void processFrame(cv::Mat& frame, std::string file);

		inline std::string getFileName(int index);
		inline void saveFrame(cv::Mat& frame, std::string file);
		inline std::string getSaveDirectory();
		inline void displayDetection(cv::Mat& img, cv::Point center, cv::Size size);

		std::string path;

	public:

		void readDirectory(const std::string& directory);

};

#endif
