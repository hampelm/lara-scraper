# You got cookie.
# So share it maybe?

# This script scrapes Michigan business license records page by HMTL page
# and saves them locally for later processing. 

# env: business
from bs4 import BeautifulSoup

import os
import re
import requests
import string
import time
import urllib2


base = 'http://www.dleg.state.mi.us/bcs_corp/dt_corp.asp?id_nbr='

# ------------------------------------------------------------------------------
# First, get all the businesses _without_ a letter prefix or suffix.
#
# Print out which files we've already completed.
# We'll start scraping at the next file in line.
# This is useful because the DLEG server goes down nightly, so the scraper
# will crash and you'll have to restart it the next day.
try:
    start = 0
    done = os.listdir('html')
    done = sorted(done)
    if len(done) != 0:
        last = done[-1].strip('.html')
        start = int(last) + 1
    print done[-10:]
    print start
except:
    print "There's a letter in the mix; skipping on"

# Set a unique User-Agent so that the State can easily block us if they want.
headers = dict()
headers['User-Agent'] = 'blockable-public-data-scraper'
headers['Accept-Encoding'] = 'gzip'

# Scrape the businesses
businesses = []
for num in range(start,1000000):
    time.sleep(1)
    num = str(num)
    num = num.zfill(6) #
    print "Starting " + num

    r = requests.get(base + num, headers=headers)

    print r
    if r.status_code == 500:
        print "none found for " + num
    else:
        print "downloading " + num
        f = open('html/' + num + '.html', 'w')
        f.write(r.text)
        f.close()


# ------------------------------------------------------------------------------
# Now, deal with trailing letter businesses, eg 10000A
start = 1

# Check what we've processed so far
done = os.listdir('html')
done = sorted(done)

# If we aren't starting from the beginning, figure out which
# business to continue with.
# This time, we need to strip the trailing letter
if len(done) != 0:
    # Strip the .html from the filename
    last = done[-1].strip('.html')
    print last

    # Strip any trailing letter
    last = last[0:-1]
    print last
    # Repeat the last one just in case
    try:
        start = int(last)
    except:
        "Starting from the start"

print done[-10:] # The last 10 completed
print start # The next to scrape

# Check all the businesses with suffixes:
for num in range(start,99999):
    this_round = num

    # Check each possible suffixes in order
    for letter in [string.ascii_uppercase]:
        time.sleep(1) # Wait a second for courtesy
        num = str(this_round) + letter
        num = num.zfill(6)
        print "Starting " + num
        r = requests.get(base + num, headers=headers)
        print r
        if r.status_code == 500:
            print "none found for " + num
        else:
            print "downloading " + num
            f = open('html/' + num + '.html', 'w')
            f.write(r.text)
            f.close()

# ------------------------------------------------------------------------------
# TODO: Check all the businesses with suffixes _AND_ prefixes.
# Now, deal with trailing letter businesses, eg B9000T
