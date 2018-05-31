import argparse
import os
import sys
import datetime

import lib.time_util as time_util


# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument('source')
parser.add_argument('destination')
parser.add_argument('-t', '--time')
arguments = parser.parse_args()

# Argument Verification

# Source Dir
if(not os.path.exists(arguments.source)):
    print('Can\'t find source directory "%s"' % arguments.source)
    sys.exit()
# Destination Dir
if(not os.path.exists(arguments.destination)):
    print('Can\'t find destination directory "%s"' % arguments.destination)
    sys.exit()
# Time
time = time_util.parseTimeArgument(arguments.time)
if(time == None):
    print('Can\'t parse "%s" as a time argument' % arguments.time)
    print('Must be one of "today" or "yesterday" or of the format "YYYY-MM-DD"')
    sys.exit()
