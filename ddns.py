import requests
import sys
import json
import socket
import re
from cpanelapi import client
import datetime

print datetime.datetime.now()

#First setup requests headers so it has a valid User-Agent
#This prevents ModSecurity blocks

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
)

#Get our current IP
try:
    r = requests.get("http://alexperusco.com/ip.php", headers=headers) 
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    print "Failed to get our current IP"
    print e
    sys.exit(1)

myIP = r.text
print("My IP is %s" %myIP)

#Check DNS we need to match against
try:
    currentDNS = socket.gethostbyname("pyrmont.alexperusco.com")
except socket.error as e:
    print "Failed to lookup DNS"
    print e
    sys.exit(1)

print("DNS is %s" %currentDNS)

#Check if IP and DNS match and update if necessary
if myIP != currentDNS:
    print "IPs DONT match"
    #Check we have a valid IP
    if re.match("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", myIP) is not None:

        #Initialise cPanel api client
        cpapi = client.Client("wootawes", "vmcp37.digitalpacific.com.au", password="xxxx", ssl=True, cpanel=True)

        #Execute dns update
        try:
            apiResult = cpapi.api2("ZoneEdit", "edit_zone_record", line=9, domain="alexperusco.com", name="pyrmont", type="A", ttl=60, address=myIP)
        except requests.exceptions.RequestException as e:
            print "cPanel API call failed"
            print e
            sys.exit(1)
        #print apiResult
        print "API call result is %s" %apiResult.get('cpanelresult', {}).get('data')
    
    else:
        print "Could not update DNS, IP was an invalid address"
        sys.exit(1)
else:
    print "IPs match"

sys.exit(0)

