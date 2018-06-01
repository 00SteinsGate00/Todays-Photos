import argparse
import json
import os
import shutil
import sys
import datetime

import lib.time_util as time_util
import lib.config as config

# config file
config_file = os.path.join(os.path.dirname(__file__), 'config.json')

# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument('destination')
parser.add_argument('date')
parser.add_argument('-t', '--type')
arguments = parser.parse_args()



# ##################### #
# Argument Verification #
# ##################### #

# Time
date = time_util.parseTimeArgument(arguments.date)
if(date == None):
    print('Can\'t parse "%s" as a time argument' % arguments.date)
    print('Must be one of "today" or "yesterday" or of the format "YYYY-MM-DD"')
    sys.exit()

# Type
type = arguments.type if arguments.type else ""

# config reading and error parsing
try:
    cfg = config.Config(config_file)
# invalid JSON
except json.JSONDecodeError as e:
    print('Cannot parse configuration file. Invalid JSON')
    sys.exit()
# file does not exist
except FileNotFoundError as e:
    print('Configuration file "%s" not found' % (config_file))
    sys.exit()
# missing config option
except KeyError as e:
    print('%s missing in configuration file "%s"' % (e, config_file))
    sys.exit()



# ########## #
# Processing #
# ########## #

# jpeg images
images_jpg = [os.path.join(cfg.source_dir, image)
                for image
                in os.listdir(cfg.source_dir)
                if time_util.modTimestamp(os.path.join(cfg.source_dir, image)) == date
                # some hidden temporary files
                and image[0] != '.'
                # jpeg extensions
                and os.path.splitext(image)[1] in ['.JPG', '.jpg', '.JPEG', '.jpeg']
             ]

# RAW images
images_raw = [os.path.join(cfg.source_dir, image)
                for image
                in os.listdir(cfg.source_dir)
                if time_util.modTimestamp(os.path.join(cfg.source_dir, image)) == date
                # some hidden temporary files
                and image[0] != '.'
                # not jpeg => RAW
                and os.path.splitext(image)[1] not in ['.JPG', '.jpg', '.JPEG', '.jpeg']
             ]


# export images
if(len(images_jpg) > 0 or len(images_raw) > 0):
    # create the target directory
    output_dir = cfg.delimiter.join(filter(None, [date.strftime(cfg.date_format), type, arguments.destination]))
    os.makedirs(output_dir, exist_ok=True)
    # create all the output subfolders
    for target_folder in cfg.target_folders:
        os.makedirs(os.path.join(output_dir, target_folder), exist_ok=True)
    # create the export folder in case it was none of target folders
    os.makedirs(os.path.join(output_dir, cfg.export_folder), exist_ok=True)
    # check if there are JPGs and create the folders accordingly
    if(len(images_jpg) > 0):
        os.makedirs(os.path.join(output_dir, cfg.export_folder, 'JPG'))
        os.makedirs(os.path.join(output_dir, cfg.export_folder, 'RAW'))

    # copy the images
    # RAW
    # If there are  JPGs copy them directly into the RAW subfolder
    if(len(images_jpg) > 0):
        for raw_image in images_raw:
            shutil.copy2(raw_image, os.path.join(output_dir, cfg.export_folder, 'RAW'))
    # Else copy them directly into the export folder
    else:
        for raw_image in images_raw:
            shutil.copy2(raw_image, os.path.join(output_dir, cfg.export_folder))
    # JPG
    for jpg_image in images_jpg:
        shutil.copy2(jpg_image, os.path.join(output_dir, cfg.export_folder, 'JPG'))
# no images found
else:
    print('No images from %s' % (date.strftime(cfg.date_format)))
