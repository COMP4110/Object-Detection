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
# TODO: Add options to only use a (deterministic) fraction of the samples.
pos_img_dir = classifier_yaml['dataset']['positive']['directory']
positive_image_files = glob.glob("{}/{}/*.jpg".format(base_dir, pos_img_dir))

positive_info_file_name = '{}/positive.txt'.format(output_dir)
with open('{}/{}'.format(base_dir, positive_info_file_name), 'w') as dat_file:
	for img in sorted(positive_image_files):
		dat_file.write("{}\n".format(img))
	
	dat_file.flush()

print positive_info_file_name


print '\n## Creating samples...'
samplesCommand = [ 'opencv_createsamples'
	, '-info', positive_info_file_name # classifier_yaml['dataset']['info']
	, '-vec',  classifier_yaml['dataset']['vec']
	, '-num',  classifier_yaml['dataset']['num'] # TODO: calculate from file contents.
	]
subprocess.call(samplesCommand, cwd=base_dir)


# print '\n## Training classifier...'
# samplesCommand = [ 'opencv_traincascade'
# 	, '-vec',               classifier_yaml['dataset']['vec']
# 	, '-data',              classifier_yaml['training']['basic']['data']
# 	, '-bg',                classifier_yaml['training']['basic']['bg']
# 	, '-numPos',            classifier_yaml['training']['basic']['numPos']
# 	, '-numNeg',            classifier_yaml['training']['basic']['numNeg']
# 	, '-numStages',         classifier_yaml['training']['basic']['numStages']
# 	, '-featureType',       classifier_yaml['training']['cascade']['featureType']
# 	, '-minHitRate',        classifier_yaml['training']['boost']['minHitRate']
# 	, '-maxFalseAlarmRate', classifier_yaml['training']['boost']['maxFalseAlarmRate']
# 	, '-weightTrimRate',    classifier_yaml['training']['boost']['weightTrimRate']
# 	, '-maxDepth',          classifier_yaml['training']['boost']['maxDepth']
# 	, '-maxWeakCount',      classifier_yaml['training']['boost']['maxWeakCount']
# 	]
# subprocess.call(samplesCommand, cwd=base_dir)


# print '\n## Running classifier...'
# runCommand = [ './build/Object_Detection'
# 	, classifier_yaml['training']['basic']['data'] + '/cascade.xml'
# 	, classifier_yaml['testing']['detectionsFile']
# 	, classifier_yaml['testing']['inputDir']
# 	, classifier_yaml['testing']['outputDir']
# 	]
# subprocess.call(runCommand, cwd=base_dir)


# print '\n## Calculating statistics...'
# statsCommand = [ 'python detection_stats.py'
# 	, classifier_yaml['testing']['detectionsFile']
# 	, classifier_yaml['dataset']['info']
# 	]
# subprocess.call(statsCommand, cwd=base_dir)

# # subprocess.check_output(['ls'], cwd=base_dir)
