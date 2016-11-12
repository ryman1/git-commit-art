import png
import sys


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
    pixelcolumns = []
    for columnnumber in range(artwidth):
        pixelcolumns.append([])
        for row in rows:
            pixelcolumns[columnnumber].append(row[columnnumber])
    return pixelcolumns


def printunicode(pixelrows):
    for row in pixelrows:
        for pixel in row:
            if pixel == (214, 230, 133):
                char = '\u2593'
            if pixel == (30, 104, 35):
                char = '\u2005\u2005\u2005'
            if pixel == (238, 238, 238):
                char = '\u2588'
            if pixel == (68, 163, 64):
                char = '\u2591'
            if pixel == (140, 198, 101):
                char = '\u2592'
            sys.stdout.write(char)
        sys.stdout.write('\n')

artimage = png.Reader('art.png')
artwidth, artheight, flatartpixels = artimage.read_flat()[0:3]
artpixelrows = grouppixelsbyrow(processflatpixels(flatartpixels, artwidth * artheight))
pixelcolumns = rowstocolumns(artpixelrows)

printunicode(artpixelrows)
