import urllib
import re
import sys

def download(src):
    dest = src.split('/')[-1]
    localfile  = open(dest, 'wb')
    remotefile = urllib.urlopen(src)

    print "Downloading"
    print "Source:      " + src
    print "Destination: " + dest + "\n"

    localfile.write(remotefile.read())
    remotefile.close()
    localfile.close()

def print_usage():
    print "Usage: python", sys.argv[0], "[MODE] [URL]"
    print "[MODE]"
    print "    -C    Create list of download links."
    print "          Does not download anything."
    print "          List is writen to stdout but you can pipe it anywhere."
    print ""
    print "    -D    Download every podcast."
    print "          This may take some time and produce trafic."
    print ""
    print "[URL]     The URL of the overview page."
    print ""

def get_child_urls(src):
    parent_content = urllib.urlopen(src).read()
    child_urls = []    
    for line in parent_content.split('\n'):
        mo = re.search('/archive/video/ipod/[0-9]+/', line)
        if mo:
            child_urls.append("http://www.tele-task.de" + mo.group())
    return child_urls

def crawl_and_create_list(child_urls):
    for url in child_urls:
        child_content = urllib.urlopen(url).read()
        mo = re.search(
            'http://stream.hpi.uni-potsdam.de:8080/download/podcast/.*.mp4',
            child_content)
        if mo:
            print mo.group()

def crawl_and_download(child_urls):
    for url in child_urls:
        child_content = urllib.urlopen(url).read()
        mo = re.search(
            'http://stream.hpi.uni-potsdam.de:8080/download/podcast/.*.mp4',
            child_content)
        if mo:
            download(mo.group())

def main():
    if len(sys.argv) != 3:
        print_usage()
        exit()

    if sys.argv[1] not in ["-C", "-D"]:
        print_usage()
        exit()
    
    child_urls = get_child_urls(sys.argv[2])
    
    if sys.argv[1] == "-C":
        crawl_and_create_list(child_urls)
    
    if sys.argv[1] == "-D":
        crawl_and_download(child_urls)

main()    
