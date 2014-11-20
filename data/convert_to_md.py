"""
Script to convert a given json file to markdown with yaml header
"""
from sys import argv

def categories(nbr):
    """
    Function that takes a number and spits out a category string
    """
    if nbr == 1:
        return 'firstyear'
    if nbr == 2:
        return 'secondyear'
    if nbr == 3:
        return 'thirdyear'

# Read in data in to python dictionary
jsonfile = open(argv[1], 'r')
dictionary = eval(jsonfile.read())
jsonfile.close()

# Convert data to correct string
fle = """---
layout      : post
categories  : module %s
title       : %s
prequesites : %s
url         : http://www.cardiff.ac.uk/maths/degreeprogrammes/modules/%s.html
---

Description goes here.

""" % (categories(dictionary["year"]), dictionary["name"], dictionary["requirements"], argv[1][:-5].lower())

# Write md file
mdfile = open(argv[1][:-5] + '.md', 'w')
mdfile.write(fle)
mdfile.close()
