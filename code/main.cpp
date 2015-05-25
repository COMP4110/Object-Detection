#include <iostream>
#include <ostream>
#include <fstream>

#include "Adaboost.h"

int main(int argc, char** argv) {

	// Parse command line arguments:
	std::string input_dir = "images/tests";
	std::string detections_file = "images/tests/detections.dat";
	if (argc >= 2) {
		input_dir = argv[1];
	}
	if (argc >= 3){
		detections_file = argv[2];
	}

	// Truncate the detections file:
	std::ofstream fs(detections_file, std::ios::out | std::ios::trunc);
	fs.close();

	Adaboost adaboost;
	adaboost.readDirectory(input_dir, detections_file);
	
	return 0;
}
