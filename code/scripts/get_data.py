import urllib2
import tarfile
import Image
import io
import hashlib
import os.path
from bs4 import BeautifulSoup as Soup

blacklisted_images_sha1_hashes = [
	'10f3f7f79e6528aa9d828316248997568ac0d833'  # flickr 'photo not available' image
]

parent_words = [
	'n02778669',  # generic sporting equipment balls
	'n02779435',  # plaything/toy/ball
	'n03445777'  # golf balls
]

search_words = parent_words[:]

for parent_word in parent_words:
	hyponym_data_url = urllib2.urlopen('http://www.image-net.org/api/text/wordnet.structure.hyponym?wnid={}&full=1'.format(parent_word))
	for child_word in hyponym_data_url.readlines()[1:]:  # ignore first line as its the 'parent word'
		search_words.append(child_word[1:].strip())  # ignore proceeding dash and strip trailing newline

url_map = {}

cached_bbox = {}

output_dat_filename = 'info.dat'
with open(output_dat_filename, 'a+') as dat_file:
	for line in dat_file.read():
		image_path = line.strip().partition(' ')[2]
		cached_bbox[image_path] = True

	for search_word in search_words:
		mapping_data_url = urllib2.urlopen('http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid={}'.format(search_word))
		for map in mapping_data_url.readlines():
			parts = map.strip().partition(' ')
			url_map[parts[0]] = parts[2]

		bounding_boxes_url = urllib2.urlopen('http://image-net.org/downloads/bbox/bbox/{}.tar.gz'.format(search_word))
		with tarfile.open(fileobj=bounding_boxes_url, mode='r|*') as bounding_boxes_file:
			for fileinfo in bounding_boxes_file:
				if fileinfo.isreg():
					file = bounding_boxes_file.extractfile(fileinfo)
					xml = Soup(file)
					objects = xml.findAll('object')
					object_name = xml.annotation.filename.string
					object_url = url_map[object_name]

					output_image_filename = 'images/{}.jpg'.format(object_name)

					if not os.path.exists(output_image_filename):
						try:
							object_data = urllib2.urlopen(object_url)
							image_data = object_data.read()
							sha1hash = hashlib.sha1(image_data).hexdigest()
							print output_image_filename, str(sha1hash)
							if str(sha1hash) in blacklisted_images_sha1_hashes:
								print "Image blacklisted: {}".format(object_name)
								continue
							im = Image.open(io.BytesIO(image_data))
							im.save(output_image_filename, "JPEG")
							print "Saved to {}".format(output_image_filename)
						except Exception as e:
							print "Error retrieving for file {}: {}".format(object_name, e)
							continue
					else:
						print 'Image already exists: {}'.format(object_name)


					bounding_boxes = []
					for obj in objects:
						bbox = obj.bndbox
						bounding_boxes.append({
							'xmin': int(bbox.xmin.string),
							'ymin': int(bbox.ymin.string),
							'xmax': int(bbox.xmax.string),
							'ymax': int(bbox.ymax.string)
						})

					bbox_output = ['{} {} {} {}'.format(
						bb['xmin'],
						bb['ymin'],
						bb['xmax'] - bb['xmin'],
						bb['ymax'] - bb['ymin']
					) for bb in bounding_boxes]
					output = "{} {} {}".format(output_image_filename, len(bounding_boxes), " ".join(bbox_output))
					print "Writing: {}".format(output)
					dat_file.write("{}\n".format(output))
					dat_file.flush()
