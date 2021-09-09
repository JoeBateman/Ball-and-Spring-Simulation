# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 14:29:57 2021

@author: joebo
"""

from vpython import *
import numpy as np

import sympy as sym


running = False
on = True

a = vector(0,-9.81,0) # m/s^2, acceleration due to gravity
l = 1.5 # m, natural length of spring
m1 = 10  # kg, mass of the ball

def pause_play():
    # Function to change the state of global variable "running" from true to
    # false, or vice versa. This function is allows the user to pause or play
    # the animation in real time
    global running
    if running == True:
        running = False
    else: running = True

def off():
    # Function to change the state of global variable "on" from true to
    # false. By default, this variable is set to on, and when the stop button
    # is pressed by the user, the simulation ends.
    global on
    on = False

def adjustAngle1():
    # Function corresponding to the first angle slider presented to the user.
    # When the slider is moved, this function changes angle 1 of the initial
    # position of the ball
    global angle1
    angle1 = angle1Change.value/180*np.pi
    angle1ChangeReadout.text = str(angle1Change.value) + " degrees"

def adjustAngle2():
    # Function corresponding to the second angle slider presented to the user.
    # When the slider is moved, this function changes angle 2 of the initial
    # position of the ball
    global angle2
    angle2 = angle2Change.value/180*np.pi
    angle2ChangeReadout.text = str(angle2Change.value) + " degrees"



time = 0
step = 0.001

### Creating the angle sliders to be used to set the initial position of the
### ball.
angle1Change = slider(left=10, min=0, max=360, step=1, value=0, bind=adjustAngle1)
scene.append_to_caption(" Angle = ")
angle1ChangeReadout = wtext(text="0 degrees")
scene.append_to_caption("\n")

angle2Change = slider(left=10, min=0, max=180, step=1, value=135, bind=adjustAngle2)
scene.append_to_caption(" Angle = ")
angle2ChangeReadout = wtext(text="135 degrees")

angle1 = angle1Change.value/180*np.pi
angle2 = angle2Change.value/180*np.pi


### Defining the objects in the scene, the ball, spring, floor and ceiling.
ceiling = box(pos=vector(0,1.5,0), size = vector(1,0.1,1))
floor = box(pos=vector(0,0,0), size = vector(5,0.1,5))
ball1 = sphere(pos=ceiling.pos - vector(l*sym.cos(angle1)*sin(angle2),l*cos(angle2),  l*sym.sin(angle1)*sin(angle2)), radius=(0.1))
string = cylinder(pos= ceiling.pos, axis=ball1.pos-ceiling.pos, radius=0.01)

### Defining the properties of the ball and spring
v1 = vector(0,0,0)
p1 = m1*v1
b = 5
k = 10

scene.append_to_caption("\n\n")
button(text="Pause/Play", bind=pause_play)
button(text="Stop", bind=off)
#
while on == True and running == False:
    ball1.pos = ceiling.pos - vector(l*sym.cos(angle1)*sin(angle2),l*cos(angle2),  l*sym.sin(angle1)*sin(angle2))
    string.axis =ball1.pos-ceiling.pos


while on == True:
    while running == True and on == True:
        rate(int(1/step))
        r1 = ball1.pos-ceiling.pos
        f1 = m1*a - k*(r1-l*r1.norm()) + b*(-p1/m1)
        
        p1 = p1 + f1*step
        
        # Position checks on the ball position to prevent clipping. The loss
        # in momentum in each bounce is chosen to be 10% of its instantaneous
        # momentum.
        if ceiling.pos.y < ball1.pos.y - ball1.radius  and ball1.pos.y - ball1.radius< (ceiling.pos.y + ceiling.size.y/2):
            if np.abs(ball1.pos.x) < ceiling.size.x/2 and np.abs(ball1.pos.z) < ceiling.size.z/2:
                p1.y = 0.9*np.abs(p1.y)

        if (ceiling.pos.y -ceiling.size.y/2) < ball1.pos.y + ball1.radius and ball1.pos.y + ball1.radius < (ceiling.pos.y):
            if np.abs(ball1.pos.x) < ceiling.size.x/2 and np.abs(ball1.pos.z) < ceiling.size.z/2:
                p1.y = -0.9*np.abs(p1.y)
        
        if ball1.pos.y - ball1.radius < (floor.pos.y + floor.size.y/2):
            p1.y = 0.9*np.abs(p1.y)
        
        ball1.pos=ball1.pos + (p1/m1)*step
        string.axis = ball1.pos - ceiling.pos  
        
        
