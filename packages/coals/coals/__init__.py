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

def Debug(*args):
    if debug:
        print(*args)


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

# Components used in Concepts
Concept = mkComponent("Concept", "logical_id") # LogicalID 
Description = mkComponent("Description", "description")
Depends = mkComponent("Depends", "depends")
Suggests = mkComponent("Suggests", "suggests")
NGramDecay = mkComponent("NGramDecay", "decay_type", "amount", "when")
SecureLevel = mkComponent("SecureLevel", "secure")
IdealLevel= mkComponent("IdealLevel", "ideal")
LongDescription = mkComponent("LongDescription", "longdescription")
Notes = mkComponent("Notes", "notes")

concept_components = [Concept, Description, Depends, Suggests, NGramDecay, SecureLevel, IdealLevel, LongDescription, Notes]

# Components used in Resources
Resource = mkComponent("Resource", "logical_id")
Title = mkComponent("Title", "title")
Name = mkComponent("Name", "name")
Url = mkComponent("Url", "url")
CoversConcept = mkComponent("CoversConcept", "concept")
NGramDelta = mkComponent("NGramDelta", "op", "ngram", "delta")
NGramConstraint = mkComponent("NGramConstraint", "op","ngram", "level")
DependsResource = mkComponent("DependsResource", "depends_resource")
DateUpdated = mkComponent("DateUpdated", "date_updated")
Template = mkComponent("Template", "template")
SourceForm = mkComponent("SourceForm", "source_form")
ResourceSpecification = mkComponent("ResourceSpecification", "resource_specification")
ResourceContent= mkComponent("ResourceContent", "resource_content")

resource_components = [Resource, Title, Name, Url, CoversConcept, NGramDelta, 
                       NGramConstraint, DependsResource, DateUpdated, Template, 
                       SourceForm, ResourceSpecification, ResourceContent]


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


def last_mod_directory(directory):
    last_mod = os.stat(directory).st_mtime  # Start off with when directory changed
    for filename in os.listdir(directory):
        mod_time = os.stat(os.path.join(directory, filename)).st_mtime
        if mod_time > last_mod:
            last_mod = mod_time
    return last_mod


def initialiseWorld():
    world = World()
    world.add_component_types(*concept_components)
    world.add_component_types(*resource_components)
    return world


def initialise_system():
    global world
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


def filter_secure_resources(candidates, user): # K
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


def get_resources_dependencies(resource): # K
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


def requirements_for_resource(resource): # Concepts too...  # K
    resource_depends = get_resources_dependencies(resource)
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


def user_matches_resource_requirements(user, resource): # K
    requirements = requirements_for_resource(resource)
    for concept_id in requirements:
        if user["ngrams"].get(concept_id, 0) < requirements[concept_id]:
            return False
    return True


def find_resources_for_user(resources, user): # K

    resources = filter_resources_done(resources, user)
    candidate_resources = []
    for resource in resources:
        if user_matches_resource_requirements(user, resource):
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


def present_resource(resource): # K
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


def infer_concepts_and_ngram_deltas():
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


def infer_conceptual_dependencies():
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

world = None
