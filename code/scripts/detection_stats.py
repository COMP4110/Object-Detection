from PIL import Image
import os.path
import argparse

MAX_BB_CORNER_DISTANCE = 50

parser = argparse.ArgumentParser(description='ImageNet Gatherer')
parser.add_argument('detections_dat', type=str, nargs='?', default='../images/tests/detections.dat', help='File containing image and bounding-box information')
parser.add_argument('info_dat', type=str, nargs='?', default='info.dat', help='File containing image and bounding-box information')

args = parser.parse_args()

# From: http://stackoverflow.com/a/312464
# chunks :: [Int] -> [[Int]]
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# Read a bounding box data file:
# readDataFile :: String -> Map String [[Int]]
def readDataFile(file_name):
	data = {}
	with open(file_name, 'r') as dat_file:
		for line in dat_file.readlines():
			parts = line.strip().partition(' ')
			image_path = parts[0]
			num, unused_, objs_str = parts[2].partition(' ')

			objs = list(chunks(map(int, objs_str.split(' ')), 4))

			data[image_path] = objs
	return data

# corners :: [Int] -> [(Int, Int)]
def corners(obj):
	x = obj[0]
	y = obj[1]
	w = obj[2]
	h = obj[3]
	return [(x,y), (x+w,y), (x+w,y+h), (x,y+h)]

# sqrDist :: (Int, Int) -> (Int, Int) -> Float
def sqrDist(p1, p2):
	return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

# isNear :: (Int, Int) -> (Int, Int) -> Bool
def isNear(p1, p2):
	return sqrDist(p1, p2) < MAX_BB_CORNER_DISTANCE^2

# isDetection :: [Int] -> [Int] -> Bool
def isDetection(obj, actual):
	c_obj = corners(obj)
	c_act = corners(actual)

	return all(map(lambda (c1, c2): isNear(c1, c2), zip(c_obj, c_act)))


# Start script:
detections = readDataFile(args.detections_dat)
info = readDataFile(args.info_dat)

total_fp = 0
total_tp = 0
total_detected = 0

total_objects = 0
total_hit_count = 0

for key in detections:
	detected_objs = detections[key]
	actual_objs = info['images/{}'.format(key)]

	num_objects = len(actual_objs) + 0.0
	num_detected = len(detected_objs) + 0.0

	num_fp = 0
	num_tp = 0
	for d in detected_objs:
		if any(map(lambda a: isDetection(d, a), actual_objs)):
			num_tp += 1
		else:
			num_fp += 1

	total_fp += num_fp
	total_tp += num_tp

	# TODO: improve correctness of stats.
	total_detected += num_detected
	total_objects += num_objects

	if num_tp > 0:
		total_hit_count += 1 

	print "img {:19}, tp: {:6.2f}, fp: {:6.2f}, tp%: {:4.2f}, fp%: {:4.2f}".format(key, num_tp, num_fp, num_tp / num_detected, num_fp / num_detected)
	# print "img {}, tp: {:.2f}, fp: {:.2f}".format(key, num_tp, num_fp)
	# print "img {}, tp: {:.2f}, fp: {:.2f}".format(key, num_tp, num_fp)

# print "TOTAL, tp%: {:.3f}, fp%: {:.3f}".format(total_tp / total_detected, total_fp / total_detected)

# TODO: This should be: (num objects which had an associated true positive) / (num objects)
hit_rate = total_hit_count / total_objects
print "hit_rate:", hit_rate
