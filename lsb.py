#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import png, sys, os
import getopt

COLOR_GREEN = '\033[0;32m'
COLOR_YELLOW = '\033[0;33m'
COLOR_NONE = '\033[1;m'

def hide_data(file_path, png_path, output_path):
    if not png_path or not os.path.isfile(png_path):
        raise Exception('Invalid PNG file')    

    if not file_path or not os.path.isfile(file_path):
        raise Exception('Invalid data file')

    if not output_path:
        raise Exception('Invalid output path')

    print COLOR_YELLOW + ' ⚫ Injecting hidden image' + COLOR_NONE    

    png_reader = png.Reader(png_path)
    png_width, png_height, png_pixels, png_meta = png_reader.read_flat()

    file_reader = png.Reader(file_path)
    file_width, file_height, file_pixels, file_meta = file_reader.read_flat()

    for i in xrange(file_width * file_height):
        if file_pixels[i] == 0:
            if png_pixels[i*3] % 2 != 0:
                if png_pixels[i*3] == 255:
                    png_pixels[i*3] = 254
                else:
                    png_pixels[i*3] = png_pixels[i*3] + 1
        else:
            if png_pixels[i*3] % 2 == 0:
                png_pixels[i*3] = png_pixels[i*3] + 1

    output_file = open(output_path, 'wb')
    output_writer = png.Writer(png_width, png_height)
    output_writer.write_array(output_file, png_pixels)
    output_file.close()   

    print COLOR_GREEN + ' ✔ Hidden image was injected successfully' + COLOR_NONE


def recover_data(png_path, output_path):
    if not png_path or not os.path.isfile(png_path):
        raise Exception('Invalid PNG file')    

    if not output_path:
        raise Exception('Invalid output path')

    print COLOR_YELLOW + ' ⚫ Extracting hidden image' + COLOR_NONE

    png_reader = png.Reader(png_path)
    width, height, pixels, meta = png_reader.asRGB8()        

    recoverd_data = []
    for row in pixels:
      for i in xrange(width):
          pixel = row[i*3]
          pixel = pixel % 2 != 0      
          recoverd_data.append(int(pixel))

    output_file = open(output_path, 'wb')
    output_writer = png.Writer(width, height, greyscale=True, bitdepth=1)
    output_writer.write_array(output_file, recoverd_data)
    output_file.close()          

    print COLOR_GREEN + ' ✔ Hidden image was extracted successfully' + COLOR_NONE


def print_usage():
    print "\nUsage:\n" + \
          "  ./lsb.py --hide --file [PATH] --png [PATH] --output [PATH]\n" + \
          "  ./lsb.py --recover --png [PATH] --output [PATH]\n" + \
          "\nArguments:\n" + \
          "  -h, --hide        To hide data in a png file\n" + \
          "  -r, --recover     To recover data from a png file\n" + \
          "  -p, --png=        Path to a .png file\n" + \
          "  -f, --file=       Path to a file to hide in the png file\n" + \
          "  -o, --output=     Path to an output file\n" + \
          "  --help            Display this message\n"

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hrp:f:o:',
        ['hide', 'recover', 'png=', 'file=', 'output=', 'help'])

except getopt.GetoptError, e:
    print e
    print_usage()
    sys.exit(1)

hiding_data = False
recovering_data = False
png_path = None
file_path = None
output_path = None

for opt, arg in opts:
    if opt in ("-h", "--hide"):
        hiding_data = True
    elif opt in ("-r", "--recover"):
        recovering_data = True
    elif opt in ("-p", "--png"):
        png_path = arg
    elif opt in ("-f", "--file"):
        file_path = arg
    elif opt in ("-o", "--output"):
        output_path = arg
    elif opt in ("--help"):
        print_usage()
        sys.exit(1)
    else:
        print("Invalid argument {}".format(opt))

if (not hiding_data and not recovering_data):
    print_usage()
    sys.exit(0)

try:    
    if (hiding_data):
        hide_data(file_path, png_path, output_path)
    if (recovering_data):
        recover_data(png_path, output_path)

except Exception as e:    
    print e
    print_usage()
    sys.exit(1)


