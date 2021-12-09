import json
import os

# list original file anotation
original_file_anotation = ['test-anotation.json', 'train-anotation.json', 'val-anotation.json']

# custom file anotation
for path in original_file_anotation:
	# new anotation 
	new_anotation = [] 

	# open file json
	original_file_anotation = open('Data/Original Anotation/' + path, 'r')

	# get data from file json
	dt_root = json.load(original_file_anotation)

	for item in dt_root:

		# print("error on: ", dt_root.index(item))

		# template dict item
		template_dict_item = {"image_file" : "", "image_size": [], "bbox": [], 'keypoints': []}

		# images file
		# if item["image"][24:]:
		template_dict_item['image_file'] = item["image"][24:]

		# image size
		# if item['kp-1'][0]['original_width'] and item['kp-1'][0]['original_height']: 
		template_dict_item['image_size'].append(item['kp-1'][0]['original_width'])
		template_dict_item['image_size'].append(item['kp-1'][0]['original_height'])

		# bbox
		# if item['label'][0]['x'] and item['label'][0]['y'] and item['label'][0]['width'] and item['label'][0]['height']:
		template_dict_item['bbox'].append(item['label'][0]['x'])
		template_dict_item['bbox'].append(item['label'][0]['y'])
		template_dict_item['bbox'].append(item['label'][0]['width'])
		template_dict_item['bbox'].append(item['label'][0]['height'])

		# keypoints
		# have total 51 values as 17 keypoints so we need to add 45 values as 0 to fix the total
		# if item['kp-1'][0]['x'] and item['kp-1'][0]['y'] and item['kp-1'][1]['x'] and item['kp-1'][1]['y']:
		template_dict_item['keypoints'].append(item['kp-1'][0]['x'])
		template_dict_item['keypoints'].append(item['kp-1'][0]['y'])
		template_dict_item['keypoints'].append(2)

		template_dict_item['keypoints'].append(item['kp-1'][1]['x'])
		template_dict_item['keypoints'].append(item['kp-1'][1]['y'])
		template_dict_item['keypoints'].append(2)

		template_dict_item['keypoints'] = template_dict_item['keypoints'] + [0]*45

		# add new item to new anotation
		new_anotation.append(template_dict_item)

		# break

	# print(new_anotation)
	# print(len(dt_root))


	# save new anotation
	result_file = open('Data/' + path, 'w')
	json.dump(new_anotation, result_file)
	result_file.close()





