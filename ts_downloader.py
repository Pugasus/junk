#!/usr/bin/python
#####################################################################################
# A TS video stream downloader script
# First argument: m3u8 link to video stream
# Second argument: Output filename
# The script will attempt to parse the m3u8 index file and find a 1080p version of the TS stream
# It then downloads each TS piece and writes these to the filename provided
# The resulting TS file is then converted to MP4
# Written for Debian, and requires ffmpeg to be installed for the mp4 conversion
#####################################################################################
import urllib
import socket
import time
import sys
import string
import re
import subprocess
import os
import requests

# Functions #########################################################################

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

# Main ##############################################################################

if len(sys.argv) < 3:
    print "Specify m3u8 link and output filename"
    sys.exit()

HQ_TS_INDEX_REGEX_MATCH = "(RESOLUTION=1920x1080.*\n)(^.*)"
socket.setdefaulttimeout(5)
tsIndex = sys.argv[1]
outputFile = sys.argv[2]

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
)

try:
    r = requests.get(tsIndex, headers=headers)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    print "Failed to fetch the m3u8 URL"
    print e
    sys.exit(1)

hqIndexSuffix = re.search(HQ_TS_INDEX_REGEX_MATCH, r.text, re.M).group(2)
tsBase = re.search("^.*\/(?!.*\/)", tsIndex).group(0)
hqIndex = tsBase + hqIndexSuffix

print "The 1080P stream I will try to download is", hqIndex

try:
    r = requests.get(hqIndex, headers=headers)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    print "Failed to fetch 1080P stream m3u8 URL"
    print e
    sys.exit(1)

tsPieces = re.findall("^.*\.ts", r.text, re.M)
lastTS = len(tsPieces)
print "The total number of TS pieces is", lastTS

tmpFile = outputFile + ".tmp"
fileOutput = open(tmpFile, 'w+')

print "Downloading TS to", tmpFile
print "Started at", time.strftime("%I:%M:%S")

currentTS = 0

while currentTS < lastTS:

    try:
        response = urllib.urlopen(tsBase + tsPieces[currentTS])
        fileOutput.write(response.read())
    except KeyboardInterrupt:
        print ""
        print "Cancelling download"
        fileOutput.close()
        sys.exit()
    except:
        print ""
        print "Timeout on part ", currentTS

    progress(currentTS, lastTS)
    currentTS = currentTS + 1

fileOutput.close()
print ""
mp4Output = outputFile + ".mp4"
bashCommand = ["ffmpeg", "-i", tmpFile, "-vcodec", "copy", "-acodec", "copy", mp4Output]
cwd = os.getcwd()
print "Converting to mp4. Output file -", mp4Output
conversion = subprocess.Popen(bashCommand, cwd=cwd)
conversion.communicate()

print ""
print "MP4 conversion completed with return code", conversion.returncode
print ""

if conversion.returncode == 0:
    #Delete the TS file upon successful MP4 conversion
    os.remove(tmpFile)
    print "Temp TS file deleted"
    print ""

sys.exit(0)
