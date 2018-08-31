#!/usr/bin/python3
#
# Copyright 2018 British Broadcasting Corporation
#
# Author: Michael Sparks <michael.sparks@bbc.co.uk>
#
# All Rights Reserved
#
import os

debug = 0 # Controls whether parsing error causes a crash or a warning

def slurp(filename):
    f = open(filename)
    raw = f.read()
    f.close()
    return raw






