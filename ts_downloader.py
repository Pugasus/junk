#!/usr/bin/python
#########################################
# A generic TS downloader which downloads/concatonates each TS piece in order into a single TS file
# It then converts this to an mp4 file
# It requires the first argument to be the URL to the first TS file
# Second argument should be your output filename
# Third argument is the number of TS pieces to download
# The script expects each TS url to end in the format 00000.ts, 00001.ts etc
# Written for Debian, and requires avconv to be installed for the mp4 conversion
#########################################
import urllib
import socket
import time
import sys
import string
import re
import subprocess
import os

socket.setdefaulttimeout(5)
count = 0
curr_progress = 0

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

if len(sys.argv) < 4:
   print "Specify TS URL, output name, and number of TS pieces"
   sys.exit()

output = sys.argv[2] + ".ts"
input = sys.argv[1]
fileOutput = open(output, 'w+')

print "Downloading TS to", output

lastTS = int(sys.argv[3])
input = input[:-8]

while count <= lastTS:
    current_ts = str(count)
    line = input + current_ts.zfill(5) + ".ts"
    try:
       response = urllib.urlopen(line)
       fileOutput.write(response.read())
    except KeyboardInterrupt:
       print ""
       print "Cancelling download"
       fileOutput.close()
       sys.exit()
    except:
       print ""
       print "Timeout on part ", count
       
    progress(count, lastTS)
    count = count + 1
    if 'str' in line:
       break
    if line == '':
       break

fileOutput.close()
print ""
mp4Output = output[:-3] + ".mp4"
bashCommand = ["avconv", "-i", output, "-vcodec", "copy", "-acodec", "copy", mp4Output]
cwd = os.getcwd()
print "Converting to mp4. Output file -", mp4Output
conversion = subprocess.Popen(bashCommand, cwd=cwd)
conversion.communicate()

print ""
print "MP4 conversion completed with return code", conversion.returncode
print ""
