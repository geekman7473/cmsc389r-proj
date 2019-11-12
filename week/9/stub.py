#!/usr/bin/env python2

import sys
import struct

# You can use this method to exit on failure conditions.
def bork(msg):
    sys.exit(msg)

# Some constants. You shouldn't need to change these.
MAGIC = 0x8BADF00D
VERSION = 1

SECTION_ASCII = 1
SECTION_UTF8 = 2
SECTION_WORDS = 3
SECTION_DWORDS = 4
SECTION_DOUBLES = 5
SECTION_COORD = 6
SECTION_REFERENCE = 7
SECTION_PNG = 8
SECTION_GIF87 = 9
SECTION_GIF89 = 10

section_to_name_map = {1:"ASCII", 2:"UTF-8", 3:"WORDS", 4:"DWORDS", 5:"DOUBLES", 6:"COORD", 7:"REFERENCE", 8:"PNG", 9:"GIF87", 10:"GIF89"}
image_format_offset_table = {8:[137, 80, 78, 71, 13, 10, 26, 10], 9:[47, 49, 46, 38, 37, 61], 10:[47, 49, 46, 38, 39, 61]}

if len(sys.argv) < 2:
    sys.exit("Usage: python stub.py input_file.fpff")

# Normally we'd parse a stream to save memory, but the FPFF files in this
# assignment are relatively small.
with open(sys.argv[1], 'rb') as fpff:
    data = fpff.read()

magic, version = struct.unpack("<LL", data[0:8])
timestamp, author = struct.unpack("<L8s", data[8:20])
(sections,) = struct.unpack("<L", data[20:24])


if magic != MAGIC:
    bork("Bad magic! Got %s, expected %s" % (hex(magic), hex(MAGIC)))

if version != VERSION:
    bork("Bad version! Got %d, expected %d" % (int(version), int(VERSION)))

print("------- HEADER -------")
print("MAGIC: %s" % hex(magic))
print("VERSION: %d" % int(version))
print("TIMESTAMP: %d" % int(timestamp))
print("AUTHOR: %s" % str(author))
print("SECTIONS: %d" % int(sections))

print("-------  BODY  -------")
offset = 24

for i in range(int(sections)):
    section_type, section_len = struct.unpack("<LL", data[offset:offset+8])
    section_len = int(section_len)

    if section_type == SECTION_ASCII or section_type == SECTION_UTF8:
        (output,) = struct.unpack(("<%ds" % section_len), data[offset + 8: (offset + 8 + section_len)])
        output = output.decode('utf-8' if section_type == SECTION_UTF8 else 'ascii')
        print(section_to_name_map[section_type] + " OUTPUT: %s" % (output))
        
    elif section_type == SECTION_WORDS or section_type == SECTION_DWORDS or section_type == SECTION_DOUBLES:
        size = int(section_len/(4 if section_type == SECTION_WORDS else 8))
        (output,) = struct.unpack(("<%s" % ('L' * size)), data[offset + 8: (offset + 8 + section_len)])
        print(section_to_name_map[section_type] + " OUTPUT: %s" % (output))

    elif section_type == SECTION_COORD:
        output = struct.unpack("<dd", data[offset + 8: (offset + 8 + section_len)])
       	print("COORDS OUTPUT: %s" % str(output))

    elif section_type == SECTION_REFERENCE:
        output = struct.unpack("<L", data[offset + 8: (offset + 8 + section_len)])
        print("REFRENCE OUTPUT: %d" % output[0])
            
    elif section_type == SECTION_PNG or section_type == SECTION_GIF87 or section_type == SECTION_GIF89:
        output = struct.unpack(("<%s" % ('B' * section_len)), data[offset + 8: (offset + 8 + section_len)])
        im_data = image_format_offset_table[section_type] + list(output)
        file = open("output" + (".png" if section_type == SECTION_PNG else ".gif"), "wb")
        file.write(bytearray(im_data))
        print(section_to_name_map[section_type] + " CREATED")

    offset += section_len + 8
