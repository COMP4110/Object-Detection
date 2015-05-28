#include <opencv2/core/core.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/objdetect/objdetect.hpp>

#include <iostream>

int main(int argc, char* argv[]) {

	const struct {
		const double angle;
		const double startAngle;
		const double endAngle;
		const cv::Scalar color;
		const int thickness;
		const int lineType;
		const int shift;
	} Draw = {0, 0, 360, cv::Scalar(40, 40, 200), 3, 8, 0};

	cv::CascadeClassifier classifier;
	if (argc == 2) {
		classifier.load("../../classifiers/" + std::string(argv[1]) + "/data/cascade.xml");
	} else {
		classifier.load("../../classifiers/scheme_4/data/cascade.xml");
	}

	cv::VideoCapture cap(0);

	if (!cap.isOpened()) {
		std::cout << "Error: Could not open webcam" << std::endl;
	}

	cap.set(CV_CAP_PROP_FRAME_WIDTH, 1024);
    cap.set(CV_CAP_PROP_FRAME_HEIGHT, 768);

	cv::Mat frame;
	cv::Mat image;
	cv::Mat down_image;
	cv::namedWindow("Detections", CV_WINDOW_NORMAL);
//	cvSetWindowProperty("Detections", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);


	double scale = 0.50;
	while (true) {
		cap >> frame;

		cvtColor(frame, image, CV_BGR2GRAY);
		//cv::equalizeHist(image, image);
		cv::resize(image, down_image, cv::Size(), scale, scale, 0);

		cv::Size minSize = cv::Size();
		cv::Size maxSize = cv::Size();
		double scaleFactor = 1.1;
		int minNeighbours = 3;
		int flags = 0;
		std::vector<cv::Rect> objects;
		classifier.detectMultiScale(down_image, objects, scaleFactor, minNeighbours, flags, minSize, maxSize);

		for (size_t i = 0, len = objects.size(); i < len; i++) {
			// Get the current object.
			cv::Rect object = objects[i];
			// Calculate the size and center of the object.
			cv::Point center((int) ((object.x + object.width * 0.5) / scale), (int) ((object.y + object.height * 0.5) / scale));
			cv::Size size((int) ((object.width * 0.5) / scale), (int) ((object.height * 0.5) / scale));
			// Display the detection on the coloured frame.
			cv::ellipse(frame, center, size, Draw.angle, Draw.startAngle, Draw.endAngle, Draw.color, Draw.thickness, Draw.lineType, Draw.shift);

//			cv::Point center2((int) (object.x + object.width * 0.5), (int) (object.y + object.height * 0.5));
//			cv::Size size2((int) (object.width * 0.5), (int) (object.height * 0.5));
			// Display the detection on the coloured frame.
//			cv::ellipse(down_image, center2, size2, Draw.angle, Draw.startAngle, Draw.endAngle, Draw.color, Draw.thickness, Draw.lineType, Draw.shift);
		}

		cv::imshow("Detections", frame);
//		cv::imshow("Detections", down_image);

        cv::waitKey(30);
    }

	return 0;

}
