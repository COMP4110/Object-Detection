from PIL import Image
import os.path
import argparse

parser = argparse.ArgumentParser(description='ImageNet Gatherer')
parser.add_argument('output_folder', type=str, nargs='?', default='cropped_negatives', help='Output folder for cropped and resised image windows')
parser.add_argument('info_dat', type=str, nargs='?', default='info_negative.dat', help='File containing image and bounding-box information')
parser.add_argument('w', type=int, nargs='?', default=24, help='Width of the output window')
parser.add_argument('h', type=int, nargs='?', default=24, help='Height of the output window')

args = parser.parse_args()

# Read the data file:
info = {}
with open(args.info_dat, 'r') as dat_file:
	for line in dat_file.readlines():
		parts = line.strip().partition(' ')
		image_path = parts[0]
		details = parts[2]
		info[image_path] = details

size = (args.w, args.h)

for image_path, details in info.iteritems():
	if os.path.isfile(image_path):
		file_name = image_path.rpartition('/')[2].partition('.')[0]
		out_path = '{}/{}.thumbnail.jpg'.format(args.output_folder, file_name)
		bboxes = [int(x) for x in details.split(' ')]
		try:
			im = Image.open(image_path)
			num_objects = bboxes[0]
			for i in range(1, 4 * num_objects, 4):
				bbox = bboxes[i:i+4]
				im_crop = im.crop((bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]))
				im_crop = im_crop.resize(size, Image.ANTIALIAS)
				im_crop.save(out_path, 'jpeg')
		except IOError:
			print "Error opening {}".format(image_path)
