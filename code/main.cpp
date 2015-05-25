#include <iostream>
#include <ostream>
#include <fstream>

#include "Adaboost.h"

int main(int argc, char** argv) {

	// Parse command line arguments:
	std::string classifier_file = "classifiers/cascade.xml";
	std::string detections_file = "images/tests/detections.dat";
	std::string input_dir = "images/tests";
	if (argc >= 2) {
		classifier_file = argv[1];
	}
	if (argc >= 3){
		detections_file = argv[2];
	}
	if (argc >= 4){
		input_dir = argv[3];
	}

	// Truncate the detections file:
	std::ofstream fs(detections_file, std::ios::out | std::ios::trunc);
	fs.close();

	std::cout << "classifier_file: " << classifier_file << std::endl;
	std::cout << "detections_file: " << detections_file << std::endl;
	std::cout << "input_dir: " << input_dir << std::endl;

	Adaboost adaboost;
	adaboost.readDirectory(input_dir, detections_file, classifier_file);

	return 0;
}
