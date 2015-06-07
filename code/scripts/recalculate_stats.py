import urllib2
import tarfile
from PIL import Image
import io
import os.path
import yaml
import argparse
import subprocess
import glob
import random
import re
random.seed(123454321) # Use deterministic samples.

base_dir = ".."

# Parse arguments:
parser = argparse.ArgumentParser(description='Train classifier')
parser.add_argument('classifier_dir', type=str, nargs='?', default='../classifiers/', help='Directory in which to find classifier YAML files.')
args = parser.parse_args()

files = glob.glob("{}/*.yaml".format(args.classifier_dir))

for classifier_yaml_fname in files:
	# Read classifier training file:
	file = open(classifier_yaml_fname, 'r')
	classifier_yaml = yaml.load(file)
	file.close()

	# Get directory names:
	classifier_name = classifier_yaml_fname.split('/')[-1].split('.yaml')[0]
	output_dir = '{}/{}'.format(classifier_yaml['training']['basic']['data'], classifier_name)

	# Construct file names:
	global_info_fname = 'info.dat'
	detections_fname = '{}/detections.dat'.format(output_dir)

	# print '\n## Calculating statistics...'
	# Note: Need to use the global data file because
	#       pos_info_fname doesn't have bounding boxes for the test set.
	statsCommand = [ 'python', 'scripts/detection_stats.py'
		, detections_fname
		, 'scripts/{}'.format(global_info_fname)
		, 'false'
		]
	subprocess.call(statsCommand, cwd=base_dir)

