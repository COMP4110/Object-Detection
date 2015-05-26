import urllib2
import tarfile
from PIL import Image
import io
import os.path
import yaml
import argparse
import subprocess

base_dir = ".."

parser = argparse.ArgumentParser(description='Train classifier')
parser.add_argument('classifier_yaml', type=str, nargs='?', default='../classifiers/classifier.yaml', help='Filename of the YAML file describing the classifier to train.')

args = parser.parse_args()

file = open(args.classifier_yaml, 'r')
classifier_yaml = yaml.load(file)
file.close()

print 'Creating dataset...'


print 'Creating samples...'
samplesCommand = [ 'opencv_createsamples'
	, '-info', classifier_yaml['dataset']['info']
	, '-vec',  classifier_yaml['dataset']['vec']
	, '-num',  classifier_yaml['dataset']['num'] # TODO: calculate from file contents.
	]
subprocess.call(samplesCommand, cwd=base_dir)

print 'Training classifier...'
samplesCommand = [ 'opencv_traincascade'
	, '-vec',               classifier_yaml['dataset']['vec']
	, '-data',              classifier_yaml['training']['basic']['data']
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

print 'Running classifier...'
runCommand = [ './build/Object_Detection'
	, classifier_yaml['training']['basic']['data'] + '/cascade.xml'
	, classifier_yaml['testing']['detectionsFile']
	, classifier_yaml['testing']['inputDir']
	, classifier_yaml['testing']['outputDir']
	]
subprocess.call(runCommand, cwd=base_dir)

print 'Calculating statistics...'
statsCommand = [ 'python detection_stats.py'
	, classifier_yaml['testing']['detectionsFile']
	, classifier_yaml['dataset']['info']
	]
subprocess.call(statsCommand, cwd=base_dir)

# subprocess.check_output(['ls'], cwd=base_dir)
