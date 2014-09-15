#! /usr/bin/env python
"""Checks HTML files for a4j routines

a4j routines are supposed to be in the way: 
1. watchA4jRequests
2. trigger ajax statement
3. waitForA4jRequest

When this is not the case, ajax requests detection may fail.
This script helps spotting uneven references in tests.

Usage: ./src/main/resources/check_ajax_statements.py ~/Downloads/results-rss.html 
Is waiting but not watch called first line 167
Is already waiting line 167
"""

import sys, getopt
from subprocess import check_output, Popen, PIPE

def main():
    inputfile = ''
    if len(sys.argv) > 1:
        inputfile = sys.argv[1]
    else:
        print 'no input file'
        sys.exit(2)

    # first perform a grep on file
    cmd = "/bin/grep -nr A4jRequest \"%s\"" %(inputfile,)
    grep = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)

    isOnWatch = False
    shouldBeWaiting = False
    prevn = 0
    for line in grep.stdout:
        if ":info:" in line:
            # skip detailed logs
            continue
        n = parseLineNumber(line)
        if "wait" in line:
            if not isOnWatch:
                print "Is waiting but not watch called first line " + n
            if not shouldBeWaiting:
                print "Is already waiting line " + n
            isOnWatch = False
            shouldBeWaiting = False
        if "watch" in line:
            if isOnWatch:
                print "Is watching line %s but is already watching line %s" %(n, prevn)
            if shouldBeWaiting:
                print "Is watching line %s but should be waiting according to line %s" %(n, prevn)
            isOnWatch = True
            shouldBeWaiting = True
        prevn = n

def parseLineNumber(line):
    return line.split(':')[0]


if __name__ == '__main__':
    main()

