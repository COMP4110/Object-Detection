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


# Load the global info file with bounding boxes for all positive images:
global_info_fname = 'info.dat'
global_info = {}
with open(global_info_fname, 'r') as dat_file:
	for line in dat_file.readlines():
		parts = line.strip().partition(' ')
		image_path = parts[0].split('/')[-1]
		details = parts[2]
		global_info[image_path] = details


print '\n## Creating datasets...'

pos_img_dir = classifier_yaml['dataset']['directory']['positive']
bak_img_dir = classifier_yaml['dataset']['directory']['background']
neg_img_dir = classifier_yaml['dataset']['directory']['negative']
pos_image_files = glob.glob("{}/{}/*.jpg".format(base_dir, pos_img_dir))
bak_image_files = glob.glob("{}/{}/*.jpg".format(base_dir, bak_img_dir))
neg_image_files = glob.glob("{}/{}/*.jpg".format(base_dir, neg_img_dir))

pos_info_fname = '{}/positive.txt'.format(output_dir)
neg_info_fname = '{}/negative.txt'.format(output_dir)

# Note: image paths in the data file have to be relative to the file itself.
pos_info_fname_depth = len(pos_info_fname.split('/')) - 1
info_entry_prefix = '../' * pos_info_fname_depth

# Filter image file lists to match sysnet specifications:
posSets = classifier_yaml['dataset']['description']['synsets']['pos']
negSets = classifier_yaml['dataset']['description']['synsets']['neg']
posProg = re.compile('.*({})_.*.jpg'.format('|'.join(posSets)))
negProg = re.compile('.*({})_.*.jpg'.format('|'.join(negSets)))
pos_image_files = filter(lambda x: posProg.match(x), pos_image_files)
bak_image_files = filter(lambda x: negProg.match(x), bak_image_files)
neg_image_files = filter(lambda x: negProg.match(x), neg_image_files)

# Truncate file lists to sample the correct number of images:
datasetSize = int(classifier_yaml['dataset']['description']['number'])
posFrac = float(classifier_yaml['dataset']['description']['posFrac'])
hardNegFrac = float(classifier_yaml['dataset']['description']['hardNegFrac'])
numPos = int(datasetSize * posFrac)
numNeg = int(datasetSize * (1 - posFrac) * hardNegFrac)
numBak = max(0, datasetSize - numPos - numNeg)
pos_image_files = random.sample(pos_image_files, min(numPos, len(pos_image_files)))
bak_image_files = random.sample(bak_image_files, min(numBak, len(bak_image_files)))
neg_image_files = random.sample(neg_image_files, min(numNeg, len(neg_image_files)))

# Complain if there aren't enough images:
if numPos != len(pos_image_files):
	print '  numPos:', numPos
	print '  len(pos_image_files):', len(pos_image_files)
	raise ValueError('Not enough positive images!')
if numNeg != len(neg_image_files):
	print '  numNeg:', numNeg
	print '  len(neg_image_files):', len(neg_image_files)
	raise ValueError('Not enough negitive images!')
if numBak != len(bak_image_files):
	print '  numBak:', numBak
	print '  len(bak_image_files):', len(bak_image_files)
	raise ValueError('Not enough background images!')

# Adjust numbers in case there weren't enough images:
datasetSize = numPos + numNeg + numBak
numPos = len(pos_image_files)
numBak = len(bak_image_files)
numNeg = len(neg_image_files)

print 'datasetSize:', datasetSize
print 'posFrac:', posFrac
print 'hardNegFrac:', hardNegFrac
print '  numPos:', numPos
print '  numNeg:', numNeg
print '  numBak:', numBak

def write_img(img, dat_file):
	key = img.split('/')[-1]
	details = global_info[key]
	dat_file.write("{}{} {}".format(info_entry_prefix, img.strip('../'), details))

# Write pos_image_files and bounding box info to pos_info_fname:
with open('{}/{}'.format(base_dir, pos_info_fname), 'w') as dat_file:
	images = sorted(pos_image_files)
	write_img(images[0], dat_file)
	for img in images[1:]:
		# Use the bounding boxes from the global info file:
		dat_file.write("\n")
		write_img(img, dat_file)
	dat_file.flush()

print pos_info_fname

# Write neg_image_files to neg_info_fname:
with open('{}/{}'.format(base_dir, neg_info_fname), 'w') as dat_file:
	images = sorted(bak_image_files + neg_image_files)
	dat_file.write("{}{}".format(info_entry_prefix, images[0].strip('../')))
	for img in images[1:]:
		dat_file.write("\n{}{}".format(info_entry_prefix, img.strip('../')))
	dat_file.flush()
print neg_info_fname


print '\n## Creating samples...'
balls_vec_fname = '{}/balls.vec'.format(output_dir)

samplesCommand = [ 'opencv_createsamples'
	, '-info', pos_info_fname
	, '-vec',  balls_vec_fname
	, '-num',  str(numPos)
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

# From the opencv_traincascade documentation:
#	-numPos <number_of_positive_samples>
#	-numNeg <number_of_negative_samples>
#		Number of positive/negative samples used in training for every classifier stage.
# The key word being 'every'. We need to ensure that we don't ask for so
# many samples that the last stages don't have enough.
# 
# We'll use the formula derived on the following page to decide how many
# samples to use, after solving for numPos:
# 	http://answers.opencv.org/question/4368/
# (the formula seems a little off to me - it seems like we should raise
#  to the power of numStages rather than multiplying? The latter is more
#  conservative though, so it shouldn't be a problem.)
skipFrac = float(classifier_yaml['training']['boost']['skipFrac']) # A count of all the skipped samples from vec-file (for all stages).
skippedSamples = numPos * skipFrac # A count of all the skipped samples from vec-file (for all stages).
minHitRate = float(classifier_yaml['training']['boost']['minHitRate'])
numStages = float(classifier_yaml['training']['basic']['numStages'])
numPosTraining = int((numPos - skippedSamples) / (1 + (1 - minHitRate) * (numStages - 1)))
# numPosTraining = int((numPos - skippedSamples) / (1 + (1 - minHitRate)**(numStages - 1))) # ??
numNegTraining = (numNeg + numBak)
print '## numPosTraining:', numPosTraining
samplesCommand = [ 'opencv_traincascade'
	, '-vec',               balls_vec_fname.split('/')[-1]
	, '-data',              'data'
	, '-bg',                neg_info_fname.split('/')[-1]
	, '-numPos',            str(numPosTraining)
	, '-numNeg',            str(numNegTraining)
	, '-numStages',         classifier_yaml['training']['basic']['numStages']
	, '-featureType',       classifier_yaml['training']['cascade']['featureType']
	, '-minHitRate',        classifier_yaml['training']['boost']['minHitRate']
	, '-maxFalseAlarmRate', classifier_yaml['training']['boost']['maxFalseAlarmRate']
	, '-weightTrimRate',    classifier_yaml['training']['boost']['weightTrimRate']
	, '-maxDepth',          classifier_yaml['training']['boost']['maxDepth']
	, '-maxWeakCount',      classifier_yaml['training']['boost']['maxWeakCount']
	]
subprocess.call(samplesCommand, cwd='{}/{}'.format(base_dir, output_dir))


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
