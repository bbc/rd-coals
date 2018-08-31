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

# Deserialisation 
# Hmm. Really?
# Shouldn't that be handled by the ECS system somehow?
from .deserialise import initialise_system

def Debug(*args):
    if debug:
        print(*args)


# -- Simple Command line UI tools ----------------------------------------------
def banner(what, detail):
    print(what,":")
    print("--------------------------------------------------------------")
    if type(detail) in [ dict, list ]:
        print(json.dumps(detail, indent=4))
    else:
        print(detail)
    print("--------------------------------------------------------------")
    print()


def choose_numerical_option(tag, minoption, maxoption, default=None):
    while True:
        option = input(tag)
        if default:
            if option == "":
                return default
        try:
            opt_num = int(option)
        except ValueError:
            print("Must be a value between %d and %d (inclusive)" % (minoption, maxoption))
        if minoption <= opt_num <= maxoption:
            return opt_num
            print("Must be a value between %d and %d (inclusive)" % (minoption, maxoption))


def build_menu_options(candidates):
    options = {}
    count = 1
    menu_items = []
    for candidate in candidates:
        menu_items.append("%d. %s" % (count, candidate.get_component("Name").name) )
        options[str(count)] = candidate
        count = count + 1
    return options, menu_items


def display_menu(menu_items):
    print("Menu.")
    print()
    for menu_item in menu_items:
        print(menu_item)

    print()


def ask_user_to_choose_resource(candidates):
    options, menu_items = build_menu_options(candidates)
    display_menu(menu_items)
    choice = choose_numerical_option("Pick a resource> ", 1, len(menu_items), default=1)
    resource = options[str( choice )]
    return resource


def find_tutorials_for_user(tutorials, user):
    candidates = []
    for tutorial in tutorials:
        if tutorial["id"] in user["tutorials_done"]:
            Debug("Skipping since done:", repr(tutorial))
            continue

        Debug("Possible candidate tutorial:", tutorial["id"])
        is_candidate = True
        for requirement in tutorial["ngrams_required"]:
            ngram_id = requirement["ngram_id"]
            if ngram_id in user["ngrams"]:
                if requirement["ngram_min_level"] > user["ngrams"][ngram_id]:
                    is_candidate = False
            else:
                if requirement["ngram_min_level"] != 0:
                    is_candidate = False

        if is_candidate:
            Debug("Is still a candidate")
            candidates.append(tutorial)
    Debug("================================================================================")
    return candidates


def filter_secure_resources(world, candidates, user): # K
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


def filter_resources_done(resources, user): # K
    resources_not_done = []
    for resource in resources:
        if not (resource.get_component("Resource").logical_id in user["resources_done"]):
            resources_not_done.append(resource)

    return resources_not_done


def get_resources_dependencies(world, resource):
    resource_depends = set()
    resource_concepts = [ r.concept  for r in resource.get_components("CoversConcept") ]

    Debug(resource)
    try:
        constraints = resource.get_components("NGramConstraint")
    except KeyError:
        return resource_depends

    for constraint in constraints:
        concept = constraint.ngram
        resource_depends.add(concept)

    for concept in resource_concepts:
        for core_concept in world.get("Concept"):
            if core_concept.get_component("Concept").logical_id == concept:
                try:
                    depends_on = core_concept.get_components("Depends") 
                except KeyError:
                    continue
                depends = [ x.depends for x in depends_on ]
                resource_depends.update(set(depends))

    return resource_depends


def requirements_for_resource(world, resource): # Concepts too...  # K
    resource_depends = get_resources_dependencies(world, resource)
    requirements = {}
    r_ngrams = {}

    try:
        constraints = resource.get_components("NGramConstraint")
    except KeyError:
        return requirements

    for x in constraints:
        r_ngrams[x.ngram] = x
    Debug(r_ngrams)
    for concept in resource_depends:
        min_level = 0
        if concept in r_ngrams:
            ng = r_ngrams[concept]
            if ng.op == "ge":
                min_level = int(ng.level)
                Debug("min_level", min_level)

        requirements[concept] = min_level
    return requirements


def user_matches_resource_requirements(world, user, resource): # K
    requirements = requirements_for_resource(world, resource)
    for concept_id in requirements:
        if user["ngrams"].get(concept_id, 0) < requirements[concept_id]:
            return False
    return True


def find_resources_for_user(world, resources, user): # K

    resources = filter_resources_done(resources, user)
    candidate_resources = []
    for resource in resources:
        if user_matches_resource_requirements(world, user, resource):
            candidate_resources.append(resource)

    return candidate_resources 


def update_user_for_resource(user, resource): # TBD
    Debug("Updating user state")

    resource_id = resource.get_component("Resource").logical_id
    # for concept in resource["ngram_boost"]:
    for ngram_delta in resource.get_components("NGramDelta"):
        user["ngrams"][ngram_delta.ngram] = user["ngrams"].get(ngram_delta.ngram, 0) + ngram_delta.delta
        if resource_id not in user["resources_done"]:
            user["resources_done"].append(resource_id)


def present_resource(world, resource): # K
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


def concept_ids(world):
    ids = []
    for concept in world.get("Concept"):
        logical_id = concept.get_component("Concept").logical_id
        ids.append(logical_id)
    return list(set(ids))


def resource_ids(world):
    ids = []
    for resource in world.get("Resource"):
        logical_id = resource.get_component("Resource").logical_id
        ids.append(logical_id)
    return list(set(ids))


def infer_concepts_and_ngram_deltas(world):
    "infer ngram deltas for resources that don't define them"
    resources = world.get("Resource")
    concepts = world.get("Concept")
    concept_ids = [ x.get_component("Concept").logical_id for x in concepts]
    Debug("concept_ids", concept_ids)
    for resource in resources:
        covers_concepts = [x.concept for x in resource.get_components("CoversConcept")]
        delta_map = {}
        try:
            deltas = resource.get_components("NGramDelta")
            for delta in deltas:
                ngram_id = delta.ngram
                Debug("ngram_id", ngram_id)
                delta_map[ngram_id] = delta
        except KeyError:
            pass

        Debug(covers_concepts)
        Debug(delta_map)
        for covered_concept in covers_concepts:
            if covered_concept not in delta_map:
                Debug(" *** INFER DELTA *** for ", covered_concept)
                resource.add( NGramDelta(op="add", ngram=covered_concept, delta=1) )
            if covered_concept not in concept_ids:
                Debug(" *** INFER CONCEPT *** ", covered_concept)
                C = Entity()
                C.add( Concept(logical_id=covered_concept) )
                C.add( Description(description=("Inferred concept: %s" % covered_concept ) ))
                C.add( SecureLevel(secure=1)) # No way of inferring importantance at this stage - assume minimal level
                C.add( IdealLevel(ideal=1))   # We know we have at least one resource, so ideal might be to look at it
                C.add( LongDescription(longdescription=("Inferred concept: %s" % covered_concept ) ))
                C.add( Notes(notes=("Inferred concept: %s" % covered_concept ) ))
                # Add a default decay in. If this isn't right, remember this would be overridden.
                C.add( NGramDecay(decay_type="mul", amount=0.95, when="step"))
                world.add_entity(C)
                concept_ids.append(covered_concept)


def infer_conceptual_dependencies(world):
    "This method infers all the dependencies between the concepts"

    # Structures to build
    resources_byid = {}
    resources_2id = {}
    resource_concepts = {}  # Key is a resource, list contains concepts it explains
    resource_preconcepts = {}  # Key is a resource, list contains concepts it depends on
    resource_preresources = {} # Key is a resource, list contains resources it depends on

    resources = world.get("Resource")

    for resource in resources:  #USED
        resource_id = resource.get_component("Resource").logical_id
        resources_byid[resource_id] = resource
        resources_2id[resource] = resource_id

    for resource in resources:  #USED
        try:
            depends_resources = resource.get_components("DependsResource")
        except KeyError:
            depends_resources = []

        Debug(depends_resources)
        resource_id = resources_2id[resource]

        resource_preresources[resource_id] = []  #USED
        for depends_on in depends_resources:
            depends_on_id = depends_on.depends_resource
            if not depends_on_id: # depends on id might be empty
                Debug("EMPTY DEPENDS FOR RESOURCE", resource_id)
                continue

            resource_preresources[resource_id].append(depends_on_id)

        try:  # USED
            concepts = resource.get_components("CoversConcept")
        except KeyError:
            concepts = []

        resource_concepts[resource_id] = []  # USED
        for concept in concepts:
            resource_concepts[resource_id].append(concept.concept)

        try: # USED
            ngram_constraints = resource.get_components("NGramConstraint")
        except KeyError:
            ngram_constraints = []

        resource_preconcepts[resource_id] = []
        for constraint in ngram_constraints:
            resource_preconcepts[resource_id].append(constraint.ngram)

    Debug("=============================")
    Debug("resource explains concepts")
    Debug(pprint.pformat(resource_concepts))
    Debug("=============================")
    Debug("resource depends on these concepts")
    Debug(json.dumps(resource_preconcepts,indent=4))
    Debug("=============================")
    Debug("resource depends on these resources")
    Debug(pprint.pformat(resource_preresources,indent=4))
    Debug("=============================")

    for resource in resource_preconcepts:
        collated_concepts = []
        for pre_resource in resource_preresources[resource]:
            concepts = resource_concepts[pre_resource]
            collated_concepts =  collated_concepts + concepts

        for concept in collated_concepts:
            if concept not in resource_preconcepts[resource]:
                constraint = NGramConstraint(op="ge", ngram=concept ,level=1)
                resources_byid[resource].add(constraint)
                Debug("Dependency")
                Debug(resource, "depends on", concept)
