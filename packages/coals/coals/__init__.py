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
from .coals_components import concept_components
from .coals_components import resource_components

# Inferring concepts
from .coals_components import NGramDelta, Concept, Description, SecureLevel, IdealLevel, LongDescription, Notes, NGramDecay 
# Inferring constraints
from .coals_components import NGramConstraint

from .deserialise import initialise_system

# Console UI related functionality
from .util import banner, choose_numerical_option, display_menu

from .inference import infer_concepts_and_ngram_deltas
from .inference import infer_conceptual_dependencies
from .inference import get_resources_dependencies
from .inference import find_resources_for_user


def Debug(*args):
    if debug:
        print(*args)


def build_menu_options(candidates):
    options = {}
    count = 1
    menu_items = []
    for candidate in candidates:
        menu_items.append("%d. %s" % (count, candidate.get_component("Name").name) )
        options[str(count)] = candidate
        count = count + 1
    return options, menu_items


def ask_user_to_choose_resource(candidates):
    options, menu_items = build_menu_options(candidates)
    display_menu(menu_items)
    choice = choose_numerical_option("Pick a resource> ", 1, len(menu_items), default=1)
    resource = options[str( choice )]
    return resource


def filter_secure_resources(world, candidates, user): # FIXME: WORLD.CONCEPTS could be passed in instead of world
    # Remove the tutorials the user is secure with
    shoulddo = []
    optional = []
    concepts = world.get("Concept")
    Debug("FILTER SECURE RESOURCES", len(candidates))
    Debug(candidates)
    for resource in candidates:
        constraint_status = []
        for concept in resource.get_components("CoversConcept"):
            for concept_def in concepts:
                if concept_def.get_component("Concept").logical_id == concept.concept:
                    Debug(concept_def.get_component("Concept").logical_id)
                    if user["ngrams"].get(concept.concept, 0) >= concept_def.get_component("SecureLevel").secure:
                        constraint_status.append( True )
                    else:
                        constraint_status.append( False )
        not_needed = True
        for cond in constraint_status:
            not_needed = (not_needed and cond)

        Debug(constraint_status)
        if not_needed:
            Debug("WE DON'T NEED THIS ONE", resource.get_component("Name").name)
            Debug("BECAUSE ", constraint_status )
            optional.append(resource)
        else:
            shoulddo.append(resource)

    return shoulddo, optional






def update_user_for_resource(user, resource):
    Debug("Updating user state")

    resource_id = resource.get_component("Resource").logical_id
    # for concept in resource["ngram_boost"]:
    for ngram_delta in resource.get_components("NGramDelta"):
        user["ngrams"][ngram_delta.ngram] = user["ngrams"].get(ngram_delta.ngram, 0) + ngram_delta.delta
        if resource_id not in user["resources_done"]:
            user["resources_done"].append(resource_id)


def present_resource(world, resource): # FIXME: WORLD.CONCEPTS could be passed in instead of world
    concepts = [ x.concept for x in resource.get_components("CoversConcept") ]
    Debug("CONCEPTS", concepts)

    concept_descriptions = []
    for concept in world.get("Concept"):
        if concept.get_component("Concept").logical_id in concepts:
            concept_descriptions.append(concept.get_component("Description").description)

    name = resource.get_component("Name").name
    location = resource.get_component("Url").url
    Debug()
    print("Resource:\t", name)
    print("Location:\t", location)
    print(repr(concept_descriptions))
    print("CoversConcepts:\t", ";".join(concept_descriptions))
    print()

    print()


def concept_ids(world): # FIXME: WORLD.CONCEPTS could be passed in instead of world
    ids = []
    for concept in world.get("Concept"):
        logical_id = concept.get_component("Concept").logical_id
        ids.append(logical_id)
    return list(set(ids))


def resource_ids(world):  # FIXME: WORLD.RESOURCES could be passed in instead of world
    ids = []
    for resource in world.get("Resource"):
        logical_id = resource.get_component("Resource").logical_id
        ids.append(logical_id)
    return list(set(ids))


