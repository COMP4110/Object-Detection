import os.path

info = {}
with open('info.dat', 'r') as dat_file:
	for line in dat_file.readlines():
		parts = line.strip().partition(' ')
		image_path = parts[0]
		details = parts[2]
		info[image_path] = details

with open('info_filtered.dat', 'w') as dat_filtered_file:
	for image_path, details in info.iteritems():
		if os.path.isfile(image_path):
			dat_filtered_file.write('{} {}\n'.format(image_path, details))
