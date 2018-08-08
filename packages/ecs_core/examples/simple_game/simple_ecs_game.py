#!/usr/bin/python3

# Copyright 2018 British Broadcasting Corporation
#
# Author: Michael Sparks <michael.sparks@bbc.co.uk>
#
# All Rights Reserved

import pygame

from ecs_core.ecs_core import Component, System, World, Entity, Quit
from ecs_core.ecs_core import mkComponent

def _mkComponent(Name, *argv):
    class theComponent(Component):
        fields = argv
        def __init__(self, **argd):
            for arg in argv:
                setattr(self, arg, argd[arg])
    theComponent.__name__ = Name
    print(theComponent)
    return theComponent

# COMPONENTS IN THIS APPLICATION ===========================================================
#
# Some of these are probably reusable
#
# But for the moment, assume that they're not
#

# PYGAME COMPONENTS -------------------------------------r

class Display(Component):   # Component
    fields = ["width", "height"]
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = None
        self.initialise()
    def initialise(self):
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.background = pygame.Surface([self.width, self.height])

    @staticmethod
    def initialise_dependencies():
        pygame.init()


class Image(Component):   # Component
    fields = ["path"]
    def __init__(self, path):
        self.path = path
        self.image = None
        self.initialise()
    def initialise(self):
        image = self.image = pygame.image.load(self.path)
        image.set_colorkey( image.get_at((0,0)) )

# PHYSICAL MODELLING COMPONENTS -------------------------------------

Position = mkComponent("Position", "pos")
Velocity = mkComponent("Velocity", "velocity")
Thrust = mkComponent("Thrust", "thrust")


# SYSTEMS -------------------------------------------------------------------------

def draw_image(screen, pos, the_image):
    height = screen.get_height()

    image_x,image_y = pos

    size = the_image.get_size()
    image_w, image_h = size 
    screen.blit(the_image, [image_x-(image_w/2),(height-image_y)-(image_h/2)] )

class Ticker(System):
    default_tick = 0.5
    def __init__(self, world=None, update_time=None):
        self.update_time = update_time
        self.world = world
        self.last_tick = 0

    def tick(self):
        update_time = self.update_time
        if update_time == None:
            print("NO UPDATE TIME SET DEFAULTING")
            update_time = self.default_tick
        t_now = time.time()
        sleep_time = update_time - (t_now - self.last_tick)
        if sleep_time > 0: # If <0 we're late
            time.sleep(sleep_time)
        else:
            pass
            # Processing time exceeded expected sleep time
        self.last_tick = t_now


class EventHandler(System):
    def __init__(self, world):
        self.world = world
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               raise Quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
               print("SAVE STATE")
               pprint.pprint(self.world.__json__(), width=128)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
               b = newBanana()
               print("NEW BANANA")
               self.world.add_entity(b)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                print("DELETE BANANA...")
                renderable = self.world.get("Image")
                if len(renderable)>0:
                    last = renderable[-1]
                    self.world.delete(last)
                else:
                    print("NONE TO DELETE!")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                print("DELETE THRUST...")
                renderable = self.world.get("Image")
                if len(renderable)>0:
                    last = renderable[-1]
                    print("FROM", last.__json__())
                    try:
                        thrusts = last.get_components("Thrust")
                        try:
                            thrust = thrusts[-1]
                            last.remove_specific_component(thrust)
                            print("(after)", last.__json__())
                        except IndexError:
                            print("HAVE REMOVED ALL THRUST from", last.__json__())

                    except KeyError:
                        pass
                else:
                    print("NONE TO DELETE!")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                print("DELETE ALL THRUSTS...")
                renderable = self.world.get("Image")
                if len(renderable)>0:
                    last = renderable[-1]
                    print("FROM", last.__json__())
                    last.remove_components("Thrust")
                    print("(after)", last.__json__())

                else:
                    print("NONE TO DELETE!")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                print("DELETE A THRUST BY NAME..")
                renderable = self.world.get("Image")
                if len(renderable)>0:
                    last = renderable[-1]
                    print("FROM", last.__json__())
                    last.remove_component("Thrust")
                    print("(after)", last.__json__())

                else:
                    print("NONE TO DELETE!")

            if event.type == pygame.KEYDOWN and event.key  == pygame.K_ESCAPE:
               raise Quit()


class ControlThrust(System):
    def tick(self):
        thrusting = self.world.get("Thrust", "Velocity")
        for item in thrusting:
            velocity = item.get_component("Velocity")
            thrust = item.get_components("Thrust")

            dx, dy = velocity.velocity

            for t in thrust:
                tx, ty = t.thrust

                if dx >30:
                    tx = -1*tx
                if dx < -30:
                    tx = -1*tx
                if dy > 30:
                    ty = -1*ty
                if dy < -30:
                    ty = -1*ty

                t.thrust = (tx,ty)


class ApplyThrust(System):
    def tick(self):
        thrusting = self.world.get("Thrust", "Velocity")
        for item in thrusting:
            velocity = item.get_component("Velocity")
            thrust = item.get_components("Thrust")
            dx, dy = velocity.velocity

            for t in thrust:
                tx, ty = t.thrust
                dx = dx + tx
                dy = dx + ty

            velocity.velocity = (dx, dy)


class Movement(System):
    def tick(self):
        moving = self.world.get("Velocity", "Position")
        for item in moving:
            position = item.get_component("Position")
            velocity = item.get_component("Velocity")
            x,y = position.pos
            dx, dy = velocity.velocity
            x = x + dx
            y = y + dy
            position.pos = (x,y)


class WrapMovement(System):
    def tick(self):
        moving = self.world.get("Position")
        for item in moving:
            position = item.get_component("Position")
            x,y = position.pos
            while x> 1280:
               x = x - 1280
            while x< 0:
               x = x + 1280

            while y> 720:
               y = y - 720
            while y< 0:
               y = y + 720
            position.pos = (x,y)


class BlankScreen(System):
    def tick(self):
        pygame.display.update()
        display = self.world.get_entity("Display").get_component("Display")
        screen, background = display.screen, display.background
        screen.blit(background, [0,0])


class Render(System):
    def tick(self):  # System
        display = self.world.get_entity("Display").get_component("Display")
        screen = display.screen
        renderable = self.world.get("Image", "Position")
        for item in renderable:
            pos = item.get_component("Position").pos
            image = item.get_component("Image").image
            draw_image(screen, pos, image)


class DisplaySwapper(System):
    def tick(self):
        pygame.display.update()


class Snapshotter(System):
    def __init__(self, world):
        self.last = 0
        self.interval = 1
        self.frame_number = 0
        self.world = world

    def tick(self):

        display = self.world.get_entity("Display").get_component("Display")
        screen = display.screen

        if time.time() - self.last < self.interval:
            return

        self.last = time.time()
        c = screen.copy()
        self.frame_number += 1
        fname = "snaps/" + ("%06d" % self.frame_number ) + ".png"
        print(fname)
        pygame.image.save(c, fname)



if __name__ == "__main__":
    import random
    import time

    def newBanana():
        tx, ty = random.randint(-10,10),random.randint(-20,20)
        tx2, ty2 = random.randint(-20,20),random.randint(-10,10)
        Banana = Entity().add( Image("banana-katana.png") )      \
                         .add( Position( pos=(random.randint(2,80)*10 ,random.randint(2,40)*10) ) )  \
                         .add( Velocity( velocity=(random.randint(-10,10),random.randint(-10,10)) ) )     \
                         .add( Thrust( thrust=(tx,ty) ) )  \
                         .add( Thrust( thrust=(ty2,tx2) ) )

        return Banana


    Display.initialise_dependencies()

    world = World()
    world.add_component_types(Display, Image, Position, Velocity, Thrust) # Can't restore without these

    try:
        world.restore_state()
    except IOError:  # No stored state
        world.add_entity(newBanana()) # Just one for now
        Screen = Entity().add( Display(1280, 720))
        world.add_entity(Screen)
    

    world.add_systems(Ticker(update_time=1/30.0), EventHandler)
    world.add_systems(ControlThrust, ApplyThrust, Movement, WrapMovement)
    world.add_systems(BlankScreen, Render, DisplaySwapper)
    world.add_systems(Snapshotter)

    try:
        world.run()
    except Quit:
        print("Bye then")
        print("FINAL STATE", world.__json__())
        world.store_state()
