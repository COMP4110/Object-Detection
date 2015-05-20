from PIL import Image
import os.path
import argparse

parser = argparse.ArgumentParser(description='ImageNet Gatherer')
parser.add_argument('output_folder', type=str, nargs='?', default='images', help='Output folder for cropped and resised image windows')
parser.add_argument('info_dat', type=str, nargs='?', default='info.dat', help='File containing image and bounding-box information')
parser.add_argument('w', type=str, nargs='?', default='parent_words.yaml', help='Width of the output window')
parser.add_argument('h', type=str, nargs='?', default='parent_words.yaml', help='Height of the output window')

args = parser.parse_args()

# Read the data file:
info = {}
with open(args.info_dat, 'r') as dat_file:
	for line in dat_file.readlines():
		parts = line.strip().partition(' ')
		image_path = parts[0]
		details = parts[2]
		info[image_path] = details


for image_path, details in info.iteritems():
	if os.path.isfile(image_path):
		print details
		# dat_filtered_file.write('{} {}\n'.format(image_path, details))
		# im = Image.open(image_path)
		# im.crop(details)
	 #    im.thumbnail(size, Image.ANTIALIAS)
	 #    im.save(file + ".thumbnail", "JPEG")
