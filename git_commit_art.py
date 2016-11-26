import png
import sys
import os
import json
from datetime import datetime, timedelta
import urllib.request


def processflatpixels(flatpixels, pixelqty):
    """ Take in flat list of pixels and convert it to a list of r,g,b tuples """
    groupedpixels = []
    pixelsprocessed = 0
    subpixelsprocessed = 0
    while pixelsprocessed < pixelqty:
        r = flatpixels[subpixelsprocessed]
        subpixelsprocessed += 1
        g = flatpixels[subpixelsprocessed]
        subpixelsprocessed += 1
        b = flatpixels[subpixelsprocessed]
        subpixelsprocessed += 1
        groupedpixels.append((r, g, b))
        pixelsprocessed += 1
    return groupedpixels


def grouppixelsbyrow(pixels):
    """ Convert a list of RGB tuples to a tuple of rows """
    pixelrows = []
    for row in range(artheight):
        pixelrow = tuple(pixels[row*artwidth:row*artwidth+artwidth])
        pixelrows.append(pixelrow)
    return pixelrows


def rowstocolumns(rows):
    """ Convert a group of pixel rows to a group of columns """
    pixcolumns = []
    for columnnumber in range(artwidth):
        pixcolumns.append([])
        for row in rows:
            pixcolumns[columnnumber].append(row[columnnumber])
    return pixcolumns


def printunicode(pixelrows):
    """
    Print out a rough unicode representation of the pixels.
    Designed for display on a dark background.
    """
    for row in pixelrows:
        for pix in row:
            if pix == (214, 230, 133):
                char = '\u2593'
            elif pix == (30, 104, 35):
                char = '\u2005\u2005\u2005'
            elif pix == (238, 238, 238):
                char = '\u2588'
            elif pix == (68, 163, 64):
                char = '\u2591'
            elif pix == (140, 198, 101):
                char = '\u2592'
            else:
                char = ''
            sys.stdout.write(char)
        sys.stdout.write('\n')


def colortocommitcount(pix):
    """
    Convert the git commit colors to numbers used to represent
    the number of daily commits which will create that color.
    """
    if pix == (214, 230, 133):
        commitcount = 1
    elif pix == (30, 104, 35):
        commitcount = 17
    elif pix == (238, 238, 238):
        commitcount = 0
    elif pix == (68, 163, 64):
        commitcount = 12
    elif pix == (140, 198, 101):
        commitcount = 6
    else:
        raise ValueError
    return commitcount

with open('config.json') as f:
    config = json.load(f)
    artimage = png.Reader('art.png')

artwidth, artheight, flatartpixels = artimage.read_flat()[0:3]
artpixelrows = grouppixelsbyrow(processflatpixels(flatartpixels, artwidth * artheight))
pixelcolumns = rowstocolumns(artpixelrows)

# Initialize the project directory and file
try:
    os.mkdir(config['gitprojectdir'])
except FileExistsError:
    pass
os.chdir(config['gitprojectdir'])
open('projectfile', 'a').close()
os.system('git init')
os.system('git config user.email ' + config['gitemail'])
os.system('git add projectfile')

# Determine the commit start date (53 weeks before next closest sunday).
# Github displays 53 up to weeks worth of commits on the contributions graph.
today = datetime.now()
# If today is not Sunday
if today.isoweekday() != 0:
    sunday = datetime.now() + timedelta((0 - datetime.now().isoweekday()) % 7)
else:
    sunday = datetime.now()
startdate = sunday - timedelta(371)

# Go through each day in a column (week) and generate commits to produced the appropriate pixel colors.
for pixelcolumn in pixelcolumns:
    response = urllib.request.urlopen('http://whatthecommit.com/index.txt')
    commitmessage = response.read().decode('utf-8').rstrip()
    for pixel in pixelcolumn:
        commitnum = colortocommitcount(pixel)
        for commit in range(commitnum):
            with open('projectfile', 'a') as f:
                f.write('*')
            command = \
                'git commit -am "' + commitmessage + '" --date ' +\
                str(startdate.year) + '-' + str(startdate.month) + '-' + str(startdate.day) + 'T00:00:' + str(commit)
            print(command)
            os.system(command)
        startdate += timedelta(1)
printunicode(artpixelrows)
