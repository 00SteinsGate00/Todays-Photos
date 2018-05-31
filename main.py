import argparse
import os
import sys
import datetime

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
