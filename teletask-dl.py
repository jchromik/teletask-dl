#!/usr/bin/env python

import os
import re
import sys
import textwrap
import urllib

def download(src, location):
    if location == '':
        location = '.'
    dest = location + '/' + src.split('/')[-1]
    localfile  = open(dest, 'wb')
    remotefile = urllib.urlopen(src)

    print "Downloading"
    print "Source:      " + src
    print "Destination: " + dest + "\n"

    localfile.write(remotefile.read())
    remotefile.close()
    localfile.close()

def print_usage():
    print(textwrap.dedent("""\
    Usage: %s [URL] [MODE] [LOCATION]

    [URL]
        The URL of the overview page. (required)

    [MODE]
        -C    Create list of download links.
              Does not download anything.
              List is writen to stdout but you can pipe it anywhere.

        -D    Download every podcast.
              This may take some time and produce trafic.

        default: -C

    [LOCATION]
        The location to
         * the file where the list of links shall be stored (if MODE = -C)
         * the folder where to store the podcasts (if MODE = -D).

        If no LOCATION is given the link list will be written to stdout
        and podcasts will be stored in the current working directory.
    """ % sys.argv[0]))

def get_child_urls(src):
    parent_content = urllib.urlopen(src).read()
    child_urls = []
    for line in parent_content.split('\n'):
        mo = re.search('/archive/video/ipod/[0-9]+/', line)
        if mo:
            child_urls.append("http://www.tele-task.de" + mo.group())
    return child_urls

def crawl_and_create_list(child_urls, location):
    if location != '':
        listfile = open(location, 'wb')
    for url in child_urls:
        child_content = urllib.urlopen(url).read()
        mo = re.search(
            'http://stream.hpi.uni-potsdam.de:8080/download/podcast/.*.mp4',
            child_content)
        if mo:
            if location == '':
                print mo.group()
            else:
                listfile.write(mo.group() + '\n')
    if location != '':
        listfile.close()

def crawl_and_download(child_urls, location):
    if location not in ['', '.']:
        if not os.path.exists(location):
            os.makedirs(location)

    for url in child_urls:
        child_content = urllib.urlopen(url).read()
        mo = re.search(
            'http://stream.hpi.uni-potsdam.de:8080/download/podcast/.*.mp4',
            child_content)
        if mo:
            download(mo.group(), location)

def main():
    # ensure that at least URL is given
    if len(sys.argv) < 2:
        print_usage()
        exit()

    # default values
    mode = 'C'
    location = ''

    # URL
    url = sys.argv[1]

    # MODE (or LOCATION) if no MODE is given
    if len(sys.argv) > 2:
        if sys.argv[2] == "-C":
            mode = 'C'
        elif sys.argv[2] == "-D":
            mode = 'D'
        else:
            mode = 'C'
            location = sys.argv[2]

    # LOCATION (if not specified before)
    if (len(sys.argv) > 3 and location == ''):
        location = sys.argv[3]

    child_urls = get_child_urls(url)

    if mode == "C":
        crawl_and_create_list(child_urls, location)
    elif mode == "D":
        crawl_and_download(child_urls, location)

main()
