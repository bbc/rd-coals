#!/usr/bin/python3
#
# Copyright 2018 British Broadcasting Corporation
#
# Author: Michael Sparks <michael.sparks@bbc.co.uk>
#
# All Rights Reserved
#

debug = 0
import json
import pprint
import os

from ecs_core.ecs_core import Component, System, World, Entity, Quit, mkComponent
from .coals_components import *
from .util import slurp

# Deserialistion of MIME-like representation of entities

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
                print("Problem with file:", filename, "...skipping")
                print("           Detail:", e)
                continue
        json_world.append(json_entity)
    return json_world


# Deserialisation of MIME JSON representation of system. (Should be handled by ECS core)


def json_concept_to_entity_concept(concept):
    C = Entity()
    for key in concept:
        if key == "id":
            for item in concept[key]:
                C.add( Concept(logical_id=item) )
        if key == "description":
            for item in concept[key]:
                C.add( Description(description=item))
        if key == "depends":
            for item in concept[key]:
                C.add( Depends(depends=item))
        if key == "suggests":
            for item in concept[key]:
                C.add( Suggests(suggests=item))
        if key == "secure":
            for item in concept[key]:
                C.add( SecureLevel(secure=int(item)))
        if key == "ideal":
            for item in concept[key]:
                C.add( IdealLevel(ideal=int(item)))
        if key == "preamble":
            item = "\n".join(concept[key])
            C.add( LongDescription(longdescription=item))
        if key == "postamble":
            item = "\n".join(concept[key])
            C.add( Notes(notes=item))
        if key == "ngram_decay":
            for item in concept[key]:
                parts = item.split(" ")
                if len(parts) == 3:
                    decay_type, amount, when = parts
                    C.add( NGramDecay(decay_type=decay_type, amount=float(amount), when=when))
    return C


def json_resource_to_entity_resource(resource):
    R = Entity()
    for key in resource:
        if key == "id":
            for item in resource[key]:
                R.add( Resource(logical_id=item) )
        if key == "title":
            for item in resource[key]:
                R.add( Title(title=item) )
        if key == "name":
            for item in resource[key]:
                R.add( Name(name=item) )
        if key == "url":
            for item in resource[key]:
                R.add( Url(url=item) )
        if key == "concept":
            for item in resource[key]:
                R.add( CoversConcept(concept=item) )
        if key == "depends_resource":
            for item in resource[key]:
                R.add( DependsResource(depends_resource=item) )
        if key == "updated":
            for item in resource[key]:
                R.add( DateUpdated(date_updated=item) )
        if key == "template":
            for item in resource[key]:
                R.add( Template(template=item) )
        if key == "source_form":
            for item in resource[key]:
                R.add( SourceForm(source_form=item) )
        if key == "preamble":
            item = "\n".join(resource[key])
            R.add( ResourceSpecification(resource_specification=item))
        if key == "postamble":
            item = "\n".join(resource[key])
            R.add( ResourceContent(resource_content=item))
        if key == "ngram_constraint":
            for item in resource[key]:
                parts = item.split(" ")
                if len(parts) == 3:
                    op, ngram, level = parts
                    R.add( NGramConstraint(op=op, ngram=ngram, level=int(level)))
        if key == "ngram_delta":
            for item in resource[key]:
                parts = item.split(" ")
                if len(parts) == 3:
                    op, ngram, delta = parts
                    R.add( NGramDelta(op=op, ngram=ngram, delta=int(delta)))
    return R


def rebuild_world_state(world):
    concepts_json_world = load_mime_like_entity_collection("concepts")
    resources_json_world = load_mime_like_entity_collection("resources")

    for concept in concepts_json_world:
        C = json_concept_to_entity_concept(concept)
        world.add_entity(C)

    for resource in resources_json_world:
        R = json_resource_to_entity_resource(resource)
        world.add_entity(R)

    return world



def initialiseWorld():
    world = World()
    world.add_component_types(*concept_components)
    world.add_component_types(*resource_components)
    return world


def last_mod_directory(directory):
    last_mod = os.stat(directory).st_mtime  # Start off with when directory changed
    for filename in os.listdir(directory):
        mod_time = os.stat(os.path.join(directory, filename)).st_mtime
        if mod_time > last_mod:
            last_mod = mod_time
    return last_mod


def initialise_system():
    world = initialiseWorld()
    concepts_last_mod = last_mod_directory("concepts")
    resources_last_mod = last_mod_directory("resources")

    try:
        cache_last_mod = os.stat("stat_file.json").st_mtime
        if cache_last_mod < concepts_last_mod:
            raise ValueError("Concept cache invalid")
        if cache_last_mod < resources_last_mod:
            raise ValueError("Resource Cache invalid")
        world.restore_state()
    except:
        world = rebuild_world_state(world)

    return world












