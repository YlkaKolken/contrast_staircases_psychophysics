
## Import libraries needed to run
from psychopy import visual, event, core
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gmean
import os
from ctypes import *
import time

using_eyetracker = False
    
## Set up eyetracking
if using_eyetracker:
    current_dir = os.getcwd()
    os.chdir("D:\\VPx64-Client")
    vpxDll = "VPX_InterApp_64.dll"
    #vpxDll = "C:\\Users/CHARUSAT/Desktop/eyetracking/VPX_InterApp.dll"

    if ( not os.access(vpxDll,os.F_OK) ):
            print("WARNING: Invalid vpxDll path; you need to edit the .py file")
    cdll.LoadLibrary( vpxDll )
    vpx = CDLL( vpxDll )
    
    os.chdir(current_dir)
    
    #vpxDll = "D:\\VPx64-Client\\VPX_InterApp_64.dll"

    #if ( not os.access(vpxDll,os.F_OK) ):
            #print("WARNING: Invalid vpxDll path; you need to edit the .py file")
    #cdll.LoadLibrary( vpxDll )
    #vpx = CDLL( vpxDll )

    #  ViewPoint CONSTANTS (see vpx.h for a full listing of constants)
    VPX_STATUS_ViewPointIsRunning = 1
    EYE_A = 0
    EYE_B = 1
    VPX_DAT_FRESH = 2
    ROI_NO_EVENT = -9999
    
    class RealPoint(Structure):
        pass

    RealPoint._fields_ = [
        ("x",c_float),
        ("y",c_float),   ]

    gp = RealPoint(1.1,1.1)
        
    fix_accuracy_y = 0.1*2/3
    fix_accuracy_x = 0.05*2/3 # radius of point 1.5 if set to fix_y = 0.1 and fix_x = 0.05 if 1 degree then fix_y = 0.1*2/3 and fix_x = 0.05*2/3
    
win = visual.Window(allowGUI=True, monitor='test2', units='deg', fullscr = True) 
win.mouseVisible = False

fix_message = visual.TextStim(win,units='deg',pos=[0,-5],
                                    alignHoriz='center',
                                    text='Please start fixating on the fixation circle now and then press any button to start once you are ready.')

fix_neutral = visual.GratingStim(win, color = 'black',
                                     tex = None, mask = 'circle', units = 'deg', 
                                   size = float(0.3), pos = (0, 0))
                                     
    # Paramters of FIXATION DOT continuously presented with CORRECT condition
fix_correct = visual.GratingStim(win, color = 'green',
                                     tex = None, mask = 'circle', units = 'deg', 
                                   size = float(0.3), pos = (0, 0))

     # Paramters of FIXATION DOT continuously presented with WRONG condition
fix_wrong = visual.GratingStim(win, color = 'red',
                                   tex = None, mask = 'circle', units = 'deg', 
                                   size = float(0.3), pos = (0, 0))

# Show welcome message and wait for user to receive instructions
fix_neutral.draw()
fix_message.draw()
fix_yellow = visual.GratingStim(win, color = 'yellow',
                                     tex = None, mask = 'circle', units = 'deg', 
                                   size = (0.1), pos = (0.5, 0.5))
    
fix_yellow.draw()
win.flip()
event.waitKeys()


if using_eyetracker:
    x_coord = np.array([])
    y_coord = np.array([])

# For 1 seconds at beginning of experiment get fixation average
section_start = time.time()
while time.time() - section_start < 1.0:
    if using_eyetracker:
        vpx.VPX_GetGazePoint(byref(gp)) # x = 0 -> left side x = 1 -> right side; y = 0 -> top of screen y = 1 -> bottom of screen
        x_coord = np.append(x_coord, gp.x-0.5)
        y_coord = np.append(y_coord, gp.y-0.5)
    fix_neutral.draw()
    win.flip()

if using_eyetracker:
    x_coord_mean = np.mean(x_coord)
    y_coord_mean = np.mean(y_coord)
    
key_pressed = ''
while key_pressed == '':  
    all_keys_pressed = event.getKeys()
    if len(all_keys_pressed) != 0:
        if 'q' in all_keys_pressed:
            win.close()
        key_pressed = all_keys_pressed[-1]  # only log the most recent key pressed

    vpx.VPX_GetGazePoint(byref(gp)) # x = 0 -> left side x = 1 -> right side; y = 0 -> top of screen y = 1 -> bottom of screen
    if gp.x-0.5 < (x_coord_mean + fix_accuracy_x) and gp.x-0.5 > (x_coord_mean - fix_accuracy_x):
        if gp.y-0.5 < (y_coord_mean + fix_accuracy_y) and gp.y-0.5 > (y_coord_mean - fix_accuracy_y):
            fix_correct.draw()
            #x_coord = np.roll(x_coord, 1)
            #x_coord[0] = gp.x-0.5
            #y_coord = np.roll(y_coord, 1)
            #y_coord[0] = gp.y-0.5
            #x_coord_mean = np.mean(x_coord)
            #y_coord_mean = np.mean(y_coord)
        
        else:
            fix_wrong.draw()
    else:
        fix_wrong.draw()
    
    fix_black = visual.GratingStim(win, color = 'black',
                                     tex = None, mask = 'circle', units = 'deg', 
                                   size = (0.1), pos = (gp.x-0.5, gp.y-0.5))
    
    fix_black.draw()
    
    
   
    win.flip()