import argparse
import json
import os
import shutil
import sys
import datetime

import lib.time_util as time_util
import lib.config as config

# config file
config_file = os.path.join(os.path.expanduser('~'), '.todaysphotos_config.json')

# Argument Parser
description = """
    By specifying a day the script will copy or move all images from your camera to the
    specified output directory. In the config.json file various options can be set for
    subfolders, date format and output naming options.
    The date will be added at the start of the output directory name and you can also include
    a type.
    Splits into JPG and RAW folder if JPG images are present.
"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-d', '--date',
                    help='Day from which the images should be copied. Either "today",\
                         "yesterday" or a date of the format YYYY-MM-DD',
                    default='today')
parser.add_argument('-n', '--name',
                    help='Name of the photoshoot. Will be added to export folder name')
parser.add_argument('-t', '--type',
                    help='Type of photography. Will be added to the export folder name')
parser.add_argument('-r', '--remove-orig',
                    help='If set the images will be deleted from the source directory',
                    action='store_true')
parser.add_argument('-o','--output',
                    help='Output directory that will overwrite the one from the configuration file')
parser.add_argument('-s', '--source',
                    help='Source directory that will overwrite the one from the configuration file')
arguments = parser.parse_args()



# ################## #
# Configuration File #
# ################## #

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
# Name
name = arguments.name if arguments.name else ""

# output directory
# command line specified one will overwrite the one from the config file
output_dir = arguments.output if arguments.output else cfg.destination_dir
if(not os.path.exists(output_dir)):
    print('Output directory "%s" does not exist' % output_dir)
    sys.exit()

# source directory
# command line specified one will overwrite the one from the config file
source_dir = arguments.source if arguments.source else cfg.source_dir
if(not os.path.exists(source_dir)):
    print('Source directory "%s" does not exist' % source_dir)
    sys.exit()

# determine the full output path
output_dir_name = cfg.delimiter.join(filter(None, [date.strftime(cfg.date_format), type, arguments.name]))
output_path     = os.path.join(output_dir, output_dir_name)

# ########## #
# Processing #
# ########## #

# jpeg images
images_jpg = [os.path.join(source_dir, image)
                for image
                in os.listdir(source_dir)
                if time_util.modTimestamp(os.path.join(source_dir, image)) == date
                # some hidden temporary files
                and image[0] != '.'
                # jpeg extensions
                and os.path.splitext(image)[1] in ['.JPG', '.jpg', '.JPEG', '.jpeg']
             ]

# RAW images
images_raw = [os.path.join(source_dir, image)
                for image
                in os.listdir(source_dir)
                if time_util.modTimestamp(os.path.join(source_dir, image)) == date
                # some hidden temporary files
                and image[0] != '.'
                # not jpeg => RAW
                and os.path.splitext(image)[1] not in ['.JPG', '.jpg', '.JPEG', '.jpeg']
             ]


# export images
if(len(images_jpg) > 0 or len(images_raw) > 0):
    # create the target directory
    os.makedirs(output_path, exist_ok=True)
    # create all the output subfolders
    for target_folder in cfg.target_folders:
        os.makedirs(os.path.join(output_path, target_folder), exist_ok=True)
    # create the export folder in case it was none of target folders
    os.makedirs(os.path.join(output_path, cfg.export_folder), exist_ok=True)
    # check if there are JPGs and create the folders accordingly
    if(len(images_jpg) > 0):
        os.makedirs(os.path.join(output_path, cfg.export_folder, 'JPG'))
        os.makedirs(os.path.join(output_path, cfg.export_folder, 'RAW'))

    # copy/move the images
    # store the correct function to move or copy the files
    process_func    = shutil.move if arguments.remove_orig else shutil.copy2
    process_verbose = "Moving" if arguments.remove_orig else "Copying"
    # RAW
    # If there are  JPGs copy/move them directly into the RAW subfolder
    print("%s RAW images" % process_verbose)
    print("")
    if(len(images_jpg) > 0):
        for index, raw_image in enumerate(images_raw, start=1):
            print("%s %s... (%d/%d)" % (process_verbose, os.path.basename(raw_image), index, len(images_raw)))
            process_func(raw_image, os.path.join(output_path, cfg.export_folder, 'RAW'))
    # Else copy/move them directly into the export folder
    else:
        for index, raw_image in enumerate(images_raw, start=1):
            print("%s %s... (%d/%d)" % (process_verbose, os.path.basename(raw_image), index, len(images_raw)))
            process_func(raw_image, os.path.join(output_path, cfg.export_folder))
    print("")

    # JPG
    print("%s JPG images" % process_verbose)
    print("")
    for index, jpg_image in enumerate(images_jpg, start=1):
        print("%s %s... (%d/%d)" % (process_verbose, os.path.basename(jpg_image), index, len(images_jpg)))
        process_func(jpg_image, os.path.join(output_path, cfg.export_folder, 'JPG'))

# no images found
else:
    print('No images from %s' % (date.strftime(cfg.date_format)))



# ############ #
# State Output #
# ############ #

print("")
print('Date: %s' % date.strftime(cfg.date_format))
print('Type: %s' % (type if type else "None"))
print('Name: %s' % (name if name else "None"))
print('Source Directory: %s' % source_dir)
print('Output Directory: %s' % output_path)
print('Delete Originals: %s' % ("Yes" if arguments.remove_orig else "No"))
print("")
print('RAW images: %d' % len(images_raw))
print('JPG images: %d' % len(images_jpg))
print("")
