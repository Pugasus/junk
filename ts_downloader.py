#!/usr/bin/python
import urllib
import socket
import time
import sys
socket.setdefaulttimeout(5)
count = 1

if len(sys.argv) < 2:
   print "Specify input file"
   sys.exit()

output = sys.argv[1] + ".ts"
input = sys.argv[1]
file = open(output, 'w+')
with open(input, 'r') as f:
   for line in f:
       line.strip()
       try:
          response = urllib.urlopen(line)
          file.write(response.read())
       except:
          print "Timeout"
       print count
       count = count + 1
       time.sleep(1)
       if 'str' in line:
          break
       if line == '':
          break
