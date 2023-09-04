import os
import sys
import signal
import shutil
import imagesize

# Spotlight lockscreen images directory
SPOTLIGHT_PATH = os.getenv('LOCALAPPDATA') + '\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets\\'

# Save directory that might be set via environment variable
ENV_SAVE_PATH = os.getenv('WALLPAPERS_SAVE_PATH')

# Prefixes for file names
DESKTOP_PREFIX = 'Desktop_'
MOBILE_PREFIX = 'Mobile_'

# Minimum file size 150kB to filter out non wallpapers in Spotlight directory
MINIMUM_FILE_SIZE = 150000

# Image extension
IMAGE_EXT = '.jpg'

# Variables regarding what types of images should be saved
SAVE_DESKTOP = False
SAVE_MOBILE = False

# Handles Ctrl + C and Ctrl + System Break
def termination_handler(SignalNumber, Frame):
	print('')
	os.system('pause')
	sys.exit(1)

# Returns prefix based on image's aspect ratio
def horizontal_or_vertical(image_path):
	width, height = imagesize.get(image_path)

	if width < height:
		return MOBILE_PREFIX
	else:
		return DESKTOP_PREFIX

# Returns save path from user's input
def read_save_path():
	text = ''

	while True:
		text = input('Please enter where would you like to save Spotlight lockscreen images:\n')

		if not os.path.isdir(text):
			print('The path you entered does not lead to a directory. Please try again.')
			continue
		else:
			return text

# Sets what types of images should be saved based on user's input
def set_images_type():
	global SAVE_DESKTOP
	global SAVE_MOBILE
	num = 0

	print('Please choose which images would you like to save:')
	print('1. Desktop and Mobile')
	print('2. Desktop only')
	print('3. Mobile only')

	while True:
		try:
			num = int(input('Your choice: '))
		except ValueError:
			print('Please enter valid number (1-3)')
			continue

		if num == 1:
			SAVE_MOBILE = True
			SAVE_DESKTOP = True
			break
		elif num == 2:
			SAVE_DESKTOP = True
			break
		elif num == 3:
			SAVE_MOBILE = True
			break
		else:
			print('The number has to be in range 1-3')

# Looks for images in Spotlight lock screen images directory
def search_spotlight_dir():
	desktop_files = []
	mobile_files = []

	for path in os.listdir(SPOTLIGHT_PATH):
		current_path = os.path.join(SPOTLIGHT_PATH, path)
		
		if os.path.isfile(current_path):
			if os.path.getsize(current_path) > MINIMUM_FILE_SIZE:
				prefix = horizontal_or_vertical(current_path)

				if prefix == MOBILE_PREFIX and SAVE_MOBILE is True:
					mobile_files.append(path)
				elif prefix == DESKTOP_PREFIX and SAVE_DESKTOP is True:
					desktop_files.append(path)

	if SAVE_DESKTOP is True and SAVE_MOBILE is True:
		print('-----')
		print(f'Images found: {len(desktop_files) + len(mobile_files)}')
		print(f'Images found in Desktop aspect ratio: {len(desktop_files)}')
		print(f'Images found in Mobile aspect ratio: {len(mobile_files)}')
	elif SAVE_DESKTOP is True:
		print('-----')
		print(f'Images found in Desktop aspect ratio: {len(desktop_files)}')
	else:
		print('-----')
		print(f'Images found in Mobile aspect ratio: {len(mobile_files)}')

	return dict(mobile = mobile_files, desktop = desktop_files)

# Copies images to selected directory
def copy_images(save_dir):
	files = search_spotlight_dir()
	copy_count = 0
	duplicate_count = 0

	if SAVE_DESKTOP is True and len(files['desktop']) > 0:
		for file in files['desktop']:
			test_path = os.path.join(save_dir, DESKTOP_PREFIX + file) + IMAGE_EXT

			if os.path.isfile(test_path) is False:
				shutil.copy(
					os.path.join(SPOTLIGHT_PATH + file),
					test_path
				)
				copy_count += 1
			else:
				duplicate_count += 1

	if SAVE_MOBILE is True and len(files['mobile']) > 0:
		for file in files['mobile']:
			test_path = os.path.join(save_dir, MOBILE_PREFIX + file) + IMAGE_EXT

			if os.path.isfile(test_path) is False:
				shutil.copy(
					os.path.join(SPOTLIGHT_PATH + file),
					test_path
				)
				copy_count += 1
			else:
				duplicate_count += 1

	if copy_count > 0:
		print('-----')
		print(f'Images copied to target directory: {copy_count}')
	
	if duplicate_count > 0:
		print('-----')
		print(f'Images omitted as target directory already had them: {duplicate_count}')

# Main function of the script, runs other functions, checks environment variable
def main():
	global ENV_SAVE_PATH
	save_path = ENV_SAVE_PATH

	if save_path is None:
		save_path = read_save_path()

	if not os.path.isdir(save_path):
		print('Environment value WALLPAPERS_SAVE_PATH is set but it does not have valid path to a directory.')
		save_path = read_save_path()

	set_images_type()

	copy_images(save_path)

	os.system('pause')

# Runs the main function
if __name__ == "__main__":
	signal.signal(signal.SIGINT, termination_handler)
	signal.signal(signal.SIGBREAK, termination_handler)
	main()