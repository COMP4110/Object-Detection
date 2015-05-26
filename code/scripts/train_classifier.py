import urllib2
import tarfile
from PIL import Image
import io
import os.path
import yaml
import argparse
import subprocess
import glob

base_dir = ".."

# Parse arguments:
parser = argparse.ArgumentParser(description='Train classifier')
parser.add_argument('classifier_yaml', type=str, nargs='?', default='../classifiers/classifier.yaml', help='Filename of the YAML file describing the classifier to train.')
args = parser.parse_args()

# Read classifier training file:
file = open(args.classifier_yaml, 'r')
classifier_yaml = yaml.load(file)
file.close()

# Create directories:
classifier_name = args.classifier_yaml.split('/')[-1].split('.yaml')[0]
output_dir = '{}/{}'.format(classifier_yaml['training']['basic']['data'], classifier_name)
output_dir_relative = '{}/{}'.format(base_dir, output_dir)

if not os.path.isdir(output_dir_relative):
	print '\n## Creating output directory: {}'.format(output_dir_relative)
	os.makedirs(output_dir_relative)
else:
	print '\n## Using existing output directory: {}'.format(output_dir_relative)


print '\n## Creating dataset...'

# Load the global info file with bounding boxes for all positive images:
global_info_fname = 'info.dat'
global_info = {}
with open(global_info_fname, 'r') as dat_file:
	for line in dat_file.readlines():
		parts = line.strip().partition(' ')
		image_path = parts[0].split('/')[-1]
		details = parts[2]
		global_info[image_path] = details

# TODO: Add options to only use a (deterministic) fraction of the samples.
pos_img_dir = classifier_yaml['dataset']['positive']['directory']
positive_image_files = glob.glob("{}/{}/*.jpg".format(base_dir, pos_img_dir))

pos_info_fname = '{}/positive.txt'.format(output_dir)
pos_info_fname_depth = len(pos_info_fname.split('/')) - 1
# Note: image paths in the data file have to be relative to the file itself.
pos_info_entry_prefix = '../' * pos_info_fname_depth
with open('{}/{}'.format(base_dir, pos_info_fname), 'w') as dat_file:
	for img in sorted(positive_image_files):
		# Use the bounding boxes from the global info file:
		key = img.split('/')[-1]
		details = global_info[key]
		dat_file.write("{}{} {}\n".format(pos_info_entry_prefix, img.strip('../'), details))
	
	dat_file.flush()

print pos_info_fname


print '\n## Creating samples...'
balls_vec_fname = '{}/balls.vec'.format(output_dir)

samplesCommand = [ 'opencv_createsamples'
	, '-info', pos_info_fname # classifier_yaml['dataset']['info']
	, '-vec',  balls_vec_fname
	, '-num',  classifier_yaml['dataset']['num'] # TODO: calculate from file contents.
	]
subprocess.call(samplesCommand, cwd=base_dir)


print '\n## Training classifier...'
traincascade_data_dir = '{}/data'.format(output_dir)
traincascade_data_dir_relative = '{}/{}'.format(base_dir, traincascade_data_dir)
if not os.path.isdir(traincascade_data_dir_relative):
	print '\n## Creating training data directory: {}'.format(traincascade_data_dir_relative)
	os.makedirs(traincascade_data_dir_relative)
else:
	print '\n## Using existing training data directory: {}'.format(traincascade_data_dir_relative)

samplesCommand = [ 'opencv_traincascade'
	, '-vec',               balls_vec_fname
	, '-data',              traincascade_data_dir
	, '-bg',                classifier_yaml['training']['basic']['bg']
	, '-numPos',            classifier_yaml['training']['basic']['numPos']
	, '-numNeg',            classifier_yaml['training']['basic']['numNeg']
	, '-numStages',         classifier_yaml['training']['basic']['numStages']
	, '-featureType',       classifier_yaml['training']['cascade']['featureType']
	, '-minHitRate',        classifier_yaml['training']['boost']['minHitRate']
	, '-maxFalseAlarmRate', classifier_yaml['training']['boost']['maxFalseAlarmRate']
	, '-weightTrimRate',    classifier_yaml['training']['boost']['weightTrimRate']
	, '-maxDepth',          classifier_yaml['training']['boost']['maxDepth']
	, '-maxWeakCount',      classifier_yaml['training']['boost']['maxWeakCount']
	]
subprocess.call(samplesCommand, cwd=base_dir)


print '\n## Running classifier...'
detections_fname = '{}/detections.dat'.format(output_dir)

results_dir = '{}/results'.format(output_dir)
results_dir_relative = '{}/{}'.format(base_dir, results_dir)
if not os.path.isdir(results_dir_relative):
	print '\n## Creating results directory: {}'.format(results_dir_relative)
	os.makedirs(results_dir_relative)
else:
	print '\n## Using existing results directory: {}'.format(results_dir_relative)

runCommand = [ './build/Object_Detection'
	, traincascade_data_dir + '/cascade.xml'
	, detections_fname
	, classifier_yaml['testing']['inputDir']
	, results_dir
	]
subprocess.call(runCommand, cwd=base_dir)


print '\n## Calculating statistics...'
# Note: Need to use the global data file because
#       pos_info_fname doesn't have bounding boxes for the test set.
statsCommand = [ 'python', 'scripts/detection_stats.py'
	, detections_fname
	, 'scripts/{}'.format(global_info_fname)
	]
subprocess.call(statsCommand, cwd=base_dir)

# # subprocess.check_output(['ls'], cwd=base_dir)
