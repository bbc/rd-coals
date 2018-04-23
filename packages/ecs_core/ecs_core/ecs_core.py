#!/usr/bin/python3
#
# Copyright 2018 British Broadcasting Corporation
#
# Author: Michael Sparks <michael.sparks@bbc.co.uk>
#
# All Rights Reserved
#

import json
import time
import uuid

debug = 0
def Debug(*args):
    if debug:
        print(*args)

class Quit(Exception):
    pass


class MoreComponents(Exception):
    pass


class InsufficientComponents(Exception):
    pass


class TooManyEntities(Exception):
    pass


class TooFewEntities(Exception):
    pass


# ECS INFRASTRUCTURE -----------------------------------------------------------------------
class Entity(object):
    def __init__(self, uid=None, *entities):
        self.components = {}
        if uid:
            self.id = uid               # Support deserialisation
        else:
            self.id = str(uuid.uuid4()) # Support serialisation
        self.world = None
        for entity in entities:
            self.add(entity)

    def set_world(self, world):
        self.world = world

    def has_component(self, component_name):
        return component_name in self.components

    def get_components(self, component_name):
        return self.components[component_name]

    def get_component(self, component_name):
        result = self.components[component_name]

        if len(result) > 1:
            raise MoreComponents(" ".join("We have", str(len(result)), "components of type",str(component_name),"in", str(self)) )
        if len(result) < 0:
            raise InsufficientComponents(" ".join("We have NO components of type",str(component_name),"in", str(self)) )
        return result [0]

    def remove_specific_component(self, component):
        "Remove a specific component from the entity"
        component_name = component.__class__.__name__
        to_filter = self.components[component_name]
        filtered = [ c for c in to_filter if c != component ]
        self.components[component_name] = filtered

        self.world.entity_update(self)

    def remove_components(self, component_name):
        try:
            del self.components[component_name]
            self.world.entity_update(self)
        except KeyError:
            pass

    def remove_component(self, component_name):
        try:
            self.components[component_name].pop()
            self.world.entity_update(self)
        except IndexError:
            del self.components[component_name]
            self.world.entity_update(self)
        except KeyError:
            pass

    def add(self, component):
        try:
            self.components[component.__class__.__name__].append( component )
        except KeyError:
            self.components[component.__class__.__name__] = [ component ]

        component.set_owner(self.id)
        return self

    def __repr__(self):
        tag = self.__class__.__name__
        parts = []
        names = list(self.components)
        names.sort()
        if "Name" in names:
            del names[names.index("Name")]
            names.insert(0,"Name")
        for name in names:
            for y in self.components[name]:
                parts.append(repr(y))

        return "Entity(" +  ", ".join(parts) + ")"

    def __str__(self):
        return  str(self.__json__()) 

    def __json__(self):
        jcomponents = {}
        for name in self.components:
            serialised = [ c.__json__()[name] for c in self.components[name]] 
            # assert serialised[0][name]
            jcomponents[name] = serialised

        return {self.id : jcomponents }


class World(object):  # This is really a World
    def __init__(self, uid=None):
        self.component_lookup = {}
        self.entities = []
        self.subsets = {}
        self.systems = []
        if uid:
            self.uid = uid
        else:
            self.uid = str(uuid.uuid4()) # Support serialisation

    def get_entity(self, component_name):
        result = self.get(component_name)
        if len(result) > 1:
            raise TooManyEntities("TooManyEntities: Should only be one %s Entity, actually %d" % (component_name, len(result)) )
        if len(result) < 1:
            raise TooFewEntities("TooFewEntities: Should only be one %s Entity, actually zero" % (component_name,) )
        return result[0]

    def get(self, *component_names):
        # get(SomeComponentName) -> Return all entites with this component
        # get(Component1, ..., ComponentN) -> Return all entites with these components
        if component_names in self.subsets:
            return self.subsets[component_names]

        search_group = self.entities
        for component_name in component_names:
            result = []
            for e in search_group:
                if e.has_component(component_name):
                    result.append(e)

            search_group = result     # Narrow search group for next iteration

        self.subsets[component_names] = result

        return result

    def entity_update(self, entity):
        filters = self.subsets.keys()
        for subset in self.subsets.keys():
            if entity in self.subsets[subset]:
                matches = True
                for name in subset:
                    matches = matches and entity.has_component(name)
                if not matches:
                    Debug("REMOVE ENTITY FROM SUBSET")
                    self.subsets[subset] = [ e for e in self.subsets[subset] if e != entity]

    def add_entity(self, entity):
        entity.set_world(self)
        filters = self.subsets.keys()
        for subset in self.subsets.keys():
            matches = True
            for name in subset:
                matches = matches and entity.has_component(name)
            if matches:
                self.subsets[subset].append(entity)

        self.entities.append(entity)

    def delete(self, entity):
        self.entities = [ x for x in self.entities if x != entity]
        for subset in self.subsets:
            if entity in self.subsets[subset]:
                self.subsets[subset] = [ x for x in self.subsets[subset] if x != entity]

    def add_systems(self, *system_classes):
        for system in system_classes:
            try:
                system = system(self)
            except TypeError:
                system = system.set_world(self)
            self.systems.append(system)

    def store_state(self, statefile="stat_file.json"):
        f = open(statefile, "w", encoding="utf8")
        f.write(json.dumps(self.__json__(), indent=4))
        f.close()

    def restore_state(self,statefile="stat_file.json"):
        f = open(statefile, "rb")
        j = json.loads(f.read().decode('utf-8'))
        f.close()
        Debug("PREVIOUS STATE", j)
        Debug()
        entity_uid = list(j.keys())[0]
        Debug("UID", entity_uid)
        for entity_json in j[entity_uid]:
            Debug("RESTORING ENTITY", entity_json)
            uid=list(entity_json.keys())[0]
            entity = Entity(uid=uid)
            Debug(entity)
            for component_type in entity_json[uid]:
                Debug("RESTORE COMPONENT TYPE", component_type)
                for component in entity_json[uid][component_type]:
                    Debug("            COMPONENT:", component)
                    callback = self.component_lookup[component_type]
                    Debug("CALLBACK", callback)
                    args = component
                    Debug("ARGS", args)
                    actual_component = callback(**args)
                    Debug("actual_component", actual_component)
                    entity.add(actual_component)
            self.add_entity(entity)

    def add_component_types(self, *component_classes):
        for klass in component_classes:
            self.component_lookup[klass.__name__] = klass

    def run(self):
        tstart = time.time()
        while True:
            if time.time()-tstart > 3:
                raise Quit()
            for system in self.systems:
                if isinstance(system, System):
                    system.tick()
                    continue
                system(self)

    def __json__(self):
        jentities = [e.__json__() for e in self.entities]
        return { self.uid : jentities }


class Component(object):
    fields = []
    def __init__(self):
        self.owner = None
    def set_owner(self, owner):
        self.owner = owner
    def __json__(self, add_owner=False):
        name = self.__class__.__name__
        args = {}
        for field in self.fields:
            args[field] = getattr(self, field)
        if add_owner:
            args["owner"] = self.owner
        return {name : args }

    def __repr__(self):
        str_state = []
        for field in self.fields:
            state = getattr(self, field)
            str_state.append( "%s=%s" % (field, repr(state)) ) 
        return "%s(%s)" % (self.__class__.__name__, ", ".join(str_state))

def mkComponent(Name, *argv):
    class theComponent(Component):
        fields = argv
        def __init__(self, **argd):
            for arg in argv:
                setattr(self, arg, argd[arg])

    theComponent.__name__ = Name
    return theComponent


class System(object):
    """ Common base class for systems - two reasons 1) to mark systems
        out as such.  Secondly, to provide a hook for setting the
        world for a system"""
    def __init__(self, world=None):
        self.world = world

    def set_world(self, world):
        self.world = world
        return self
