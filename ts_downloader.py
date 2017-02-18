#!/usr/bin/python
#########################################
# A generic TS downloader. It requires a text file input as the first argument which
# contains a list of the TS URLs. It then downloads/concatonates each in order to a single TS file
# Then converts them to an mp4 file
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

def update_progress(progress):
   print '\r[{0}] {1}%'.format('#'*(progress/50), progress)

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

if len(sys.argv) < 2:
   print "Specify input file"
   sys.exit()

output = sys.argv[1] + ".ts"
input = sys.argv[1]
fileOutput = open(output, 'w+')
fileInput = open(input, 'r')
lineList = fileInput.readlines()
fileInput.close()

print "Downloading TS to", output

lastTS = re.search('[0-9]{3}\.',lineList[len(lineList)-1]).group(0)
lastTS = lastTS.translate(None, string.punctuation)
lastTS = int(lastTS)

for line in lineList:
    line.strip()
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
mp4Output = output + ".mp4"
bashCommand = ["avconv", "-i", output, "-vcodec", "copy", "-acodec", "copy", mp4Output]
cwd = os.getcwd()
print "Converting to mp4. Output file -", mp4Output
conversion = subprocess.Popen(bashCommand, cwd=cwd)
conversion.communicate()

print ""
print "MP4 conversion completed with return code", conversion.returncode
print ""
