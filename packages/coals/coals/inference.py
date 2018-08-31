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

from ecs_core.ecs_core import Entity

# Inferring concepts
from .coals_components import NGramDelta, Concept, Description, SecureLevel, IdealLevel, LongDescription, Notes, NGramDecay 
# Inferring constraints
from .coals_components import NGramConstraint


def Debug(*args):
    if debug:
        print(*args)


def infer_concepts_and_ngram_deltas(world):   # FIXME: WORLD.RESOURCES + WORLD.CONCEPTS could be passed in instead of world
                                              # NOTE: WORLD.CONCEPTS  **CHANGES** (enlargens) as a result of this call
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


def infer_conceptual_dependencies(world): # FIXME: WORLD.RESOURCES could be passed in instead of world
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


def get_resources_dependencies(world, resource):  # FIXME: WORLD.CONCEPTS could be passed in instead of world
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


def filter_resources_done(resources, user): # K
    resources_not_done = []
    for resource in resources:
        if not (resource.get_component("Resource").logical_id in user["resources_done"]):
            resources_not_done.append(resource)

    return resources_not_done


def requirements_for_resource(world, resource): # Concepts too...  # KCONCEPTS 
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
