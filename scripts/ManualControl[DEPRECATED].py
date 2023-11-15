'''
This file is part of SimMeR, an educational mechatronics robotics simulator.
Initial development funded by the University of Toronto MIE Department.
Copyright (C) 2023  Ian G. Bennett

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# Basic echo client, for testing purposes
# Code modified from examples on https://realpython.com/python-sockets/
# and https://www.geeksforgeeks.org/python-display-text-to-pygame-window/

import socket
import struct
import time
import math
from threading import Thread
import _thread
from datetime import datetime
import tkinter as tk

def transmit(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT_TX))
            s.send(data.encode('utf-8'))
        except (ConnectionRefusedError, ConnectionResetError):
            print('Tx Connection was refused or reset.')
            _thread.interrupt_main()
        except TimeoutError:
            print('Tx socket timed out.')
            _thread.interrupt_main()
        except EOFError:
            print('\nKeyboardInterrupt triggered. Closing...')
            _thread.interrupt_main()

def receive():
    global responses
    global time_rx
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            try:
                s2.connect((HOST, PORT_RX))
                response_raw = s2.recv(1024)
                if response_raw:
                    responses = bytes_to_list(response_raw)
                    time_rx = datetime.now().strftime("%H:%M:%S")
            except (ConnectionRefusedError, ConnectionResetError):
                print('Rx connection was refused or reset.')
                _thread.interrupt_main()
            except TimeoutError:
                print('Response not received from robot.')
                _thread.interrupt_main()

def transmit_bt(data):
    with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
        try:
            s.connect((MAC_ADDRESS, COMM_PORT))
            s.send(data.encode('utf-8'))
        except (ConnectionRefusedError, ConnectionResetError):
            print('Tx Connection was refused or reset.')
            _thread.interrupt_main()
        except TimeoutError:
            print('Tx socket timed out.')
            _thread.interrupt_main()
        except EOFError:
            print('\nKeyboardInterrupt triggered. Closing...')
            _thread.interrupt_main()

def receive_bt():
    global responses
    global time_rx
    while True:
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s2:
            try:
                s2.connect((MAC_ADDRESS, COMM_PORT))
                response_raw = s2.recv(1024)
                if response_raw:
                    responses = bytes_to_list(response_raw)
                    time_rx = datetime.now().strftime("%H:%M:%S")
            except (ConnectionRefusedError, ConnectionResetError):
                print('Rx connection was refused or reset.')
                _thread.interrupt_main()
            except TimeoutError:
                print('Response not received from robot.')
                _thread.interrupt_main()

def bytes_to_list(msg):
    num_responses = int(len(msg)/8)
    data = struct.unpack("%sd" % str(num_responses), msg)
    return data


### Network Setup ###
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT_TX = 61200     # The port used by the *CLIENT* to receive
PORT_RX = 61201     # The port used by the *CLIENT* to send data

MAC_ADDRESS = '98:d3:51:f9:48:05'
COMM_PORT = 9

# Received responses
responses = [False]
time_rx = 'Never'

# Create tx and rx threads
Thread(target = receive, daemon = True).start()

# Run manual control
window = tk.Tk()

# label widgets for car
rover_icon = tk.Label(window, text=' /   \\\n0     0\n\n|     |\n0_____0')  #car graphic

# label widgets for sensor output
f_dist = tk.Label(window, text='Initializing')  #reading from forward sensor
s_dist = tk.Label(window, text='Initializing')  #reading from starboard sensor
p_dist = tk.Label(window, text='Initializing')  #reading from port sensor
a_dist = tk.Label(window, text='Initializing')  #reading from aft sensor

# Sensor setup
def ScanSensors():
    '''scans all four ultrasonmic sensors and updates GUI'''
    sensors = ['u0', 'u1', 'u2', 'u3']
    readings = []
    
    #scan sensors
    for sensor in sensors:
        transmit_bt(sensor)
        time.sleep(0.1)
        readings.append(round(responses[0], 3))
      
    #update GUI
    f_dist.config(text = str(readings[0]-1))
    s_dist.config(text = str(readings[1]-1))
    a_dist.config(text = str(readings[2]-1))
    p_dist.config(text = str(readings[3]-1))
    

#motion commands
def MoveRobot(command):
    '''applies command and checks sensors
    
    command : [str] command to be applied to SimMer
    '''
    transmit_bt(command)
    time.sleep(0.5)
    ScanSensors()

# buttons for motion
f_move_1 = tk.Button(window, text = "1in\n^\n|", command = lambda: MoveRobot('f'))  #move forward one inch
f_move_6 = tk.Button(window, text = "5in\n^\n|", command = lambda: MoveRobot('F'))  #move forward 6 inches

a_move_1 = tk.Button(window, text = "1in\n|\nv", command = lambda: MoveRobot('w0--1'))    
a_move_6 = tk.Button(window, text = "5in\n|\nv", command = lambda: MoveRobot('w0--5'))

cw_turn_2 = tk.Button(window, text = "2deg\n__\n  |\n  v",anchor="w", justify="left", command = lambda: MoveRobot('r0-2')) #rotate 2deg clockwise    
cw_turn_90 = tk.Button(window, text = "90deg\n__\n  |\n  v",anchor="w", justify="left", command = lambda: MoveRobot('r0-90'))#rotate 90deg clockwise

ccw_turn_2 = tk.Button(window, text = "2deg\n __\n|\nv",anchor="w", justify="left", command = lambda: MoveRobot('r0--2')) #rotate 2deg counterclockwise    
ccw_turn_90 = tk.Button(window, text = "90deg\n __\n|\nv",anchor="w", justify="left", command = lambda: MoveRobot('r0--90'))

#arranging elements on window (starts at top left corner)
#row0
ccw_turn_90.grid(row = 0, column = 0, pady = 2)
f_move_6.grid(row = 0, column = 3, pady = 2)
cw_turn_90.grid(row = 0, column = 6, pady = 2)
#row1
ccw_turn_2.grid(row = 1, column = 1, pady = 2)
f_move_1.grid(row = 1, column = 3, pady = 2)
cw_turn_2.grid(row = 1, column = 5, pady = 2)
#row 2
f_dist.grid(row = 2, column = 3, pady = 2)
#row3
p_dist.grid(row = 3, column = 2, pady = 2)
rover_icon.grid(row = 3, column = 3, pady = 2)
s_dist.grid(row = 3, column = 4, pady = 2)
#row 4
a_dist.grid(row = 4, column = 3, pady = 2)
#row 5
a_move_1.grid(row = 5, column = 3, pady = 2)
#row 6
a_move_6.grid(row = 6, column = 3, pady = 2)

ScanSensors()
   
window.mainloop()

