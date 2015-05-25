from PIL import Image
import os.path
import argparse
import glob

parser = argparse.ArgumentParser(description='Resize all images in a directory')
parser.add_argument('-i', type=str, nargs='?', default='../images/tests/', help='Input folder for images to resize')
parser.add_argument('-o', type=str, nargs='?', default='../images/tests/processed/', help='Output folder for resized image windows')
parser.add_argument('-s', type=int, nargs='?', default=500, help='Maximum resized dinemsion')

args = parser.parse_args()

files = glob.glob("{}/*.jpg".format(args.i))

for f_in in files:
	try:
		f_out = "{}/{}".format(args.o, f_in.split('/')[-1])
		im = Image.open(f_in)
		print "{} -> {}".format(f_in, f_out)
		im.thumbnail((args.s, args.s), Image.ANTIALIAS)
		im.save(f_out)
	except IOError:
		print "Error opening {}".format(f_in)
