'''
This file stores the configuration information for the simulator.
'''
# This file is part of SimMeR, an educational mechatronics robotics simulator.
# Initial development funded by the University of Toronto MIE Department.
# Copyright (C) 2023  Ian G. Bennett
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pygame.math as pm
from devices.motors import MotorSimple
from devices.ultrasonic import Ultrasonic
from devices.gyroscope import Gyroscope
from devices.compass import Compass
from devices.infrared import Infrared
from devices.drive import Drive

# Control Flags and Setup
rand_error = False          # Use either true random error generator (True) or repeatable error generation (False)
rand_bias = False           # Use a randomized, normally distributed set of bias values for drives (placeholder, not implemented)
bias_strength = [0.05, 1]   # How intense the random drive bias is, if enabled (placeholder, not implemented)

# Network configuration for sockets
host = '127.0.0.1'
port_rx = 61200
port_tx = 61201
timeout = 300
str_encoding = 'utf-8'

# Block information
block_position = [66, 5]        # Block starting location
block_rotation = 0              # Block rotation (deg)
block_size = 3                  # Block side length in inches

# Robot information
robot_start_position = [6, 42]  # Robot starting location (in)
robot_start_rotation = 180      # Robot starting rotation (deg)
robot_width = 5.5                 # Robot width in inches
robot_height = 5.5                # Robot height in inches
robot_outline = [               # Robot outline, relative to center position
                pm.Vector2(-robot_width/2, -robot_width/2),
                pm.Vector2(-robot_width/2,  robot_width/2),
                pm.Vector2( robot_width/2,  robot_width/2),
                pm.Vector2( robot_width/2, -robot_width/2)
                ]

# Maze definition information
wall_segment_length = 12    # Length of maze wall segments (inches)
floor_segment_length = 3    # Size of floor pattern squares (inches)
walls = [[3,3,1,1,0,2,0,2],
         [3,3,0,1,1,1,1,1],
         [1,0,2,0,0,1,0,1],
         [1,1,1,1,1,1,0,2]] # Matrix to define the maze walls
floor_seed = 5489           # Randomization seed for generating correctfloor pattern

# Graphics information
frame_rate = 60             # Target frame rate (Hz)
ppi = 10                    # Number of on-screen pixels per inch on display
border_pixels = floor_segment_length * ppi  # Size of the border surrounding the maze area

background_color = (43, 122, 120)

wall_thickness = 0.25       # Thickness to draw wall segments, in inches
wall_color = (255, 0, 0)    # Tuple with wall color in (R,G,B) format

robot_thickness = 0.25      # Thickness to draw robot perimeter, in inches
robot_color = (0, 0, 255)   # Tuple with robot perimeter color in (R,G,B) format

block_thickness = 0.25      # Thickness to draw robot perimeter, in inches
block_color = (127, 127, 0) # Tuple with robot perimeter color in (R,G,B) format



### DEVICE CONFIGURATION ###
# Motors
m0_info = {
    'id': 'm0',
    'position': [3, 0],
    'rotation': 0,
    'visible': True
}

m1_info = {
    'id': 'm0',
    'position': [-3, 0],
    'rotation': 0,
    'visible': True
}

motors = {
    'm0': MotorSimple(m0_info),
    'm1': MotorSimple(m1_info)
}

# Drives
w0_info = {
    'id': 'w0',
    'position': [0, 0],
    'rotation': 0,
    'visible': False,
    'velocity': [0, 6],
    'ang_velocity': 0,
    'motors': [motors['m0'], motors['m1']],
    'motor_direction': [1, 1],
    'bias': {'x': 0, 'y': 0, 'rotation': 0.2},
    'error': {'x': 0.05, 'y': 0.05, 'rotation': 1}
}

r0_info = {
    'id': 'r0',
    'position': [0, 0],
    'rotation': 0,
    'visible': False,
    'velocity': [0, 0],
    'ang_velocity': 120,
    'motors': [motors['m0'], motors['m1']],
    'motor_direction': [1, -1],
    'bias': {'x': 0, 'y': 0, 'rotation': 0.01},
    'error': {'x': 0.003, 'y': 0.003, 'rotation': 0.05}
}

drives = {
    'w0': Drive(w0_info),
    'r0': Drive(r0_info)
}

# Sensors
u0_info = {
    'id': 'u0',
    'position': [1.25, 2.25],
    'height': 2,
    'rotation': 0,
    'error': 0.02,
    'outline': [
        pm.Vector2(-0.5, -0.5),
        pm.Vector2(-0.5, 0.5),
        pm.Vector2(0.5, 0.5),
        pm.Vector2(0.5, -0.5)
    ],
    'visible': True,
    'visible_measurement': True
}

u1_info = {
    'id': 'u1',
    'position': [-1.25, 2.25],
    'height': 4,
    'rotation': 0,
    'error': 0.02,
    'outline': [
        pm.Vector2(-0.5, -0.5),
        pm.Vector2(-0.5, 0.5),
        pm.Vector2(0.5, 0.5),
        pm.Vector2(0.5, -0.5)
    ],
    'visible': True,
    'visible_measurement': True
}

u2_info = {
    'id': 'u2',
    'position': [-2.25, 2.25],
    'height': 4,
    'rotation': 90,
    'error': 0.02,
    'outline': [
        pm.Vector2(-0.5, -0.5),
        pm.Vector2(-0.5, 0.5),
        pm.Vector2(0.5, 0.5),
        pm.Vector2(0.5, -0.5)
    ],
    'visible': True,
    'visible_measurement': True
}

u3_info = {
    'id': 'u3',
    'position': [-2.25, -2.25],
    'height': 4,
    'rotation': 90,
    'error': 0.02,
    'outline': [
        pm.Vector2(-0.5, -0.5),
        pm.Vector2(-0.5, 0.5),
        pm.Vector2(0.5, 0.5),
        pm.Vector2(0.5, -0.5)
    ],
    'visible': True,
    'visible_measurement': True
}

u4_info = {
    'id': 'u4',
    'position': [2.25, -2.25],
    'height': 4,
    'rotation': -90,
    'error': 0.02,
    'outline': [
        pm.Vector2(-0.5, -0.5),
        pm.Vector2(-0.5, 0.5),
        pm.Vector2(0.5, 0.5),
        pm.Vector2(0.5, -0.5)
    ],
    'visible': True,
    'visible_measurement': True
}

u5_info = {
    'id': 'u5',
    'position': [2.25, 2.25],
    'height': 4,
    'rotation': -90,
    'error': 0.02,
    'outline': [
        pm.Vector2(-0.5, -0.5),
        pm.Vector2(-0.5, 0.5),
        pm.Vector2(0.5, 0.5),
        pm.Vector2(0.5, -0.5)
    ],
    'visible': True,
    'visible_measurement': True
}

sensors = {
    'u0': Ultrasonic(u0_info),
    'u1': Ultrasonic(u1_info),
    'u2': Ultrasonic(u2_info),
    'u3': Ultrasonic(u3_info),
    'u4': Ultrasonic(u4_info),
    'u5': Ultrasonic(u5_info)
}



### TESTING AND DEBUG SETTINGS ###
simulate_list = ['u0', 'u1', 'u2', 'u3', 'u4', 'u5']
