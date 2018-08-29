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


def split_raw_mimelike(raw_file_data):
    lines = raw_file_data.split("\n")
    sections = []
    section = []
    for line in lines:
        if line == "---":
            sections.append(section)
            section = []
        else:
            section.append(line)

    sections.append(section)
    header = sections.pop(0)
    return header, sections


def parse_mimelike_header_lines(header):
    result = {}
    for line in header:
        c = line.find(":")
        key = line[:c].lower()  # Force key to lower case
        value = line[c+1:].lstrip() # Removing leading whitespace from value
        if key not in result:
            result[key] = []
        result[key].append(value)
    return result


def mime_like_entity_to_json_entity(raw_file_data):
    header_lines, body_sections = split_raw_mimelike(raw_file_data)
    json_entity = parse_mimelike_header_lines(header_lines)
    json_entity["preamble"] = []
    json_entity["postamble"] = []
    if len(body_sections)>0:
        json_entity["preamble"] = body_sections[0]
    if len(body_sections) > 1:
        json_entity["postamble"] = body_sections[1]
    return json_entity


def load_mime_like_entity(filename):
    raw_file = slurp(filename)
    return mime_like_entity_to_json_entity(raw_file)


def load_mime_like_entity_collection(directory):
    json_world = []
    for filename in os.listdir(directory):
        if filename == ".keep":
            continue
        try:
            json_entity = load_mime_like_entity(os.path.join(directory, filename))
        except Exception as e:
            if debug:
                raise
            else:
                print("Problem with file", filename, "...skipping")
                print("           Detail", e)
                continue
        json_world.append(json_entity)
    return json_world
