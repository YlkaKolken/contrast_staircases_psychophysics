# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 14:15:55 2020

@author: Ibrahim Hashim

@github: https://github.com/Ibrahim-Hashim-Coding


In geometric mean - one sided and add double of this
Add fixation drift mean -> new mean calculated at beginning of trial
"""

## Import libraries needed to run
from psychopy import visual, event, core
import staircase_functions as stf
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gmean
import os
from ctypes import *
import time

# Add fixation task
fix_task_duration = 1.0  # Duration of fixation task in seconds
fix_task_tolerance = 0.05  # Tolerance for fixation task (in degrees)
fix_task_color = [1, -1, -1]  # Color of fixation task dot (red)

def run_staircase(parameters, parameter_file, last_info, start_ori_list_counter, start_con_list_counter, folder_path):
    ## Documentation
    # fix_task_timer = core.Clock()
    # fix_task_complete = False

    # while not fix_task_complete:
    #     fix_task_timer.reset()
    #     fixation_loss = False

    #     # Perform fixation task for fix_task_duration seconds
    #     while fix_task_timer.getTime() < fix_task_duration:
    #         fix_neutral.draw()
    #         win.flip()

    #     if fixation_loss:
    #         all_keys_pressed = event.getKeys()
    #         if len(all_keys_pressed) != 0 and 'q' in all_keys_pressed:
    #             win.close()
    #     else:
    #         fix_task_complete = True

    participant_id = last_info[1]
    observer = last_info[0]
    session = last_info[2]
    number_runs = int(last_info[3])
    
    eyetracker = parameter_file[5]
    if eyetracker == 'y':
        using_eyetracker = True
    else:
        using_eyetracker = False
    
    # using_eyetracker = True
    
    ## Set up eyetracking
    if using_eyetracker:
        current_dir = os.getcwd()
        #os.chdir(")
        vpxDll = "D:\\VPx64-Client/VPX_InterApp_64.dll"
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
            ("y",c_float),
        ]

        gp = RealPoint(1.1,1.1)
        
        fix_accuracy = float(last_info[4])
    
    
    ## Create orientation list and setting reference orientation_list
    reference_ori = float(parameters[6])
    ori_list_length = int(parameters[7])
    ori_list_max = float(parameters[8])
    ori_list_div = float(parameters[9])
    ori_list_created = stf.create_orientation_list(ori_list_max, ori_list_div,
                                                   ori_list_length)
    
    con_list_max = 0.3169
    con_list_div = 1.26
    con_list_length = 15
    con_list_created = stf.create_contrast_list(con_list_max, con_list_div,
                                                   con_list_length)
    

    ## Create window and obtain data
    # This defines the parameters for the WINDOW where stimuli are shown
    win = visual.Window(allowGUI=True, monitor='testMonitor', units='deg', fullscr = True) 
    win.mouseVisible = False

    # Gets frame rate of pc and rounds (usually to 60 or 30)
    win_fps = round(win.getActualFrameRate(), 0) 
    
    
    ## Set up text for intro screen
    start_message = visual.TextStim(win,units='deg',pos=[0,1],
                                    alignHoriz='center',alignVert='bottom',
                                    text='The observer will now explain the experiment to you. Once they have done this you may start the experiment by pressing any button.')
    fix_message = visual.TextStim(win,units='deg',pos=[0,-5],
                                    alignHoriz='center',
                                    text='Please start fixating on the fixation circle now and then press any button to start once you are ready.')

    ## Create fixation stimuli
    # Paramters of FIXATION DOT continuously presented with NEUTRAL condition
    fix_neutral = visual.GratingStim(win, color = parameters[18],
                                     tex = None, mask = 'circle', units = 'deg', 
                                     size = float(parameters[15]), pos = (float(parameters[16]), float(parameters[17])))

    # Paramters of FIXATION DOT continuously presented with CORRECT condition
    fix_correct = visual.GratingStim(win, color = parameters[19],
                                     tex = None, mask = 'circle', units = 'deg', 
                                     size = float(parameters[15]), pos = (float(parameters[16]), float(parameters[17])))

     # Paramters of FIXATION DOT continuously presented with WRONG condition
    fix_wrong = visual.GratingStim(win, color = parameters[20],
                                   tex = None, mask = 'circle', units = 'deg', 
                                   size = float(parameters[15]), pos = (float(parameters[16]), float(parameters[17])))
 
    # Paramters of FIXATION DOT continuously presented with EARLY or LATE condition
    fix_time = visual.GratingStim(win, color = parameters[21],  
                                  tex = None, mask = 'circle', units = 'deg', 
                                  size = float(parameters[15]), pos = (float(parameters[16]), float(parameters[17])))
                                  
    # Paramters of FIXATION DOT continuously presented with LATE condition
    fix_loss = visual.GratingStim(win, color = parameters[22],  
                                  tex = None, mask = 'circle', units = 'deg', 
                                     size = float(parameters[15]), pos = (float(parameters[16]), float(parameters[17])))

    # Show welcome message and wait for user to receive instructions
    start_message.draw()
    win.flip()
    event.waitKeys()
    
    for run in range(number_runs):
        ori_list_counter = start_ori_list_counter
        last_ori_list_counter = ori_list_counter

        con_list_counter = start_con_list_counter
        last_con_list_counter = con_list_counter
        
        ## Set both staircase counters to 0
        staircase_counter_up = staircase_counter_down = 0   

        ## Create movement variables
        movement_direction = 'no_change'
        last_direction = 'not_set_yet'
        
        ## Record time and date
        now = datetime.now() # current date and time
        date_time = now.strftime("%d_%m_%Y %H:%M")
        data_file_name = folder_path + 'pid_' + participant_id + '_sess_' + session + '_run_' + str(run + 1)
        
        ## Recording for graph and later calculations
        graph_orientations = []
        reversal_point_orientations = []
        reversal_point_trials = []
    
        ## Set staircase values
        number_reversals = int(parameters[3])  # if this reaches 0, staircase ends
        number_trials =  int(parameters[2]) # if this reaches 0, staircase ends
        n_up = int(parameters[1])
        n_down = int(parameters[0])
        trial_counter = 0
        
        ## Create and open data file to record user output ADD TIMING OF EVERY TRIAL ETC
        data_file = open(data_file_name + '_data.txt'.format(run), 'w') 
        data_file.write('ParameterFile: {}\n'.format(parameter_file))
        data_file.write('FPS: {}\n'.format(win_fps))
        data_file.write('DateTime: {}\n'.format(date_time))
        data_file.write('ParticipantID: {}\n'.format(participant_id))
        data_file.write('Observer: {}\n'.format(observer))
        data_file.write('Orientation: {}\n'.format(ori_list_created[ori_list_counter]))
        data_file.write('Session: {}\n'.format(session))
        data_file.write('Run {} out of {}\n'.format(run+1, number_runs))
        data_file.write('Trial\tOrientationCounter\tOrientationValue\tDirection\tResponse\t\tReversalPointsLeft\tTrialNumbersLeft\n')
        data_file.close()
        
        time_file = open(data_file_name + '_timings.txt'.format(run), 'w')
        time_file.write('GetFixation\t\tPresentStimulus\t\tUserInput\t\tFeedback\t\tWaiting\t\tTotalTrial\n')
        
        ## Start of run
        run_message = visual.TextStim(win,units='deg',pos=[0,-5],
                                    alignHoriz='center',
                                    text='This is run number {} out of {}. Press any button to start.'.format(run+1, number_runs))
        run_message.draw()
        fix_neutral.draw()
        win.flip()
        event.waitKeys()

        if using_eyetracker:
            fix_message.draw()
            fix_neutral.draw()
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
                    x_coord = np.append(x_coord, gp.x)
                    y_coord = np.append(y_coord, gp.y)
                fix_neutral.draw()
                win.flip()
        
        if using_eyetracker:
            x_coord_mean = np.mean(x_coord)
            y_coord_mean = np.mean(y_coord)
        
        ## Start trials
        while number_reversals != 0 and number_trials != 0:  # ends when either is achieved
                        
            if using_eyetracker:
                fixation_loss = True  # set as true here, but becomes false onces fixated
            else:
                fixation_loss = False  # just set as false for timing things
            
            trial_start = time.time()  # check if trial is less than 2000 ms, if yes, show blank at end for that duration
            
            # Check for fixation for 1 second
            section_start = time.time()
            while time.time() - section_start < 1.0:
                if using_eyetracker:
                    vpx.VPX_GetGazePoint(byref(gp)) # x = 0 -> left side x = 1 -> right side; y = 0 -> top of screen y = 1 -> bottom of screen
                    if gp.x < (x_coord_mean + fix_accuracy) and gp.x > (x_coord_mean - fix_accuracy):
                        if gp.y < (y_coord_mean + fix_accuracy) and gp.y > (y_coord_mean - fix_accuracy):
                            fixation_loss = False
                            break
                fix_neutral.draw()
                win.flip()
            
            if fixation_loss:
                all_keys_pressed = event.getKeys()
                if len(all_keys_pressed) != 0:
                    if 'q' in all_keys_pressed:
                        win.close()
            else:
                # Fix-check steady time for 250 ms
                tic = time.time()
                section_start = time.time()
                if using_eyetracker:
                    x_coord_add = np.array([])
                    y_coord_add = np.array([])
                    
                while time.time() - section_start < 0.25:
                    if using_eyetracker:
                        vpx.VPX_GetGazePoint(byref(gp)) # x = 0 -> left side x = 1 -> right side; y = 0 -> top of screen y = 1 -> bottom of screen
                        x_coord_add = np.append(x_coord_add, gp.x)
                        y_coord_add = np.append(y_coord_add, gp.y)
                    fix_neutral.draw()
                    win.flip()
                
                if using_eyetracker:
                    x_coord = np.roll(x_coord, len(x_coord_add))
                    y_coord = np.roll(y_coord, len(y_coord_add))
                    x_coord[:len(x_coord_add)] = x_coord_add
                    y_coord[:len(y_coord_add)] = y_coord_add
                    x_coord_mean = np.mean(x_coord)
                    y_coord_mean = np.mean(y_coord)
                            
                toc = time.time()
                time_file.write('{}\t\t\t'.format(np.round(toc-tic, 5)))
                
                # calculate grating orientation and create stimulus grating
                grating_ori, grating_dir = stf.calculate_grating_orientation(reference_ori, 
                                                                             ori_list_created[ori_list_counter])
                
                grating_ori_dia, grating_dir_dia = stf.calculate_grating_orientation(reference_ori, 
                                                                             ori_list_created[ori_list_counter])
                                
                # grating = visual.GratingStim(win, contrast = float(parameters[10]), units = 'deg', mask = 'circle', sf = float(parameters[11]), 
                #                              size = float(parameters[12]), ori = grating_ori, pos=(float(parameters[13]), float(parameters[14])))
                # grating_dia = visual.GratingStim(win, contrast = float(parameters[10]), units = 'deg', mask = 'circle', sf = float(parameters[11]), 
                #                              size = float(parameters[12]), ori = grating_ori_dia, pos=(-float(parameters[13]), -float(parameters[14])))
                grating = visual.GratingStim(win, contrast = float(con_list_created[con_list_counter]), units = 'deg', mask = 'circle', sf = float(parameters[11]), 
                                             size = float(parameters[12]), ori = grating_ori, pos=(float(parameters[13]), float(parameters[14])))
                grating_dia = visual.GratingStim(win, contrast = float(con_list_created[con_list_counter]), units = 'deg', mask = 'circle', sf = float(parameters[11]), 
                                             size = float(parameters[12]), ori = grating_ori_dia, pos=(-float(parameters[13]), -float(parameters[14])))
                
                event.getKeys()  # clear all key presses
                key_pressed = ''  # used to record last key pressed by user in underneath loop
                # present the stimulus 500 ms
                # for first 150 ms, check if person pressed button -> this would be too early, therefore repeat trial
                section_start = time.time()
                while time.time() - section_start < 0.15: 
                    if using_eyetracker:
                        vpx.VPX_GetGazePoint(byref(gp)) # x = 0 -> left side x = 1 -> right side; y = 0 -> top of screen y = 1 -> bottom of screen
                        if gp.x > (x_coord_mean + fix_accuracy) or gp.x < (x_coord_mean - fix_accuracy):
                            fixation_loss = True
                            break
                        elif gp.y > (y_coord_mean + fix_accuracy) or gp.y < (y_coord_mean - fix_accuracy):
                            fixation_loss = True
                            break
                        else:
                            pass
                    fix_neutral.draw()
                    grating.draw()
                    grating_dia.draw()
                    win.flip()
                
                if fixation_loss:
                    time_file.write('FixLoss\n')
                    all_keys_pressed = event.getKeys()
                    if len(all_keys_pressed) != 0:
                        if 'q' in all_keys_pressed:
                            win.close()
                else:
                    event.getKeys()  # clear all key presses
                    key_pressed = ''  # used to record last key pressed by user in underneath loop
                    while time.time() - section_start < 0.5: 
                        if using_eyetracker:
                            vpx.VPX_GetGazePoint(byref(gp)) # x = 0 -> left side x = 1 -> right side; y = 0 -> top of screen y = 1 -> bottom of screen
                            if gp.x > (x_coord_mean + fix_accuracy) or gp.x < (x_coord_mean - fix_accuracy):
                                fixation_loss = True
                                break
                            elif gp.y > (y_coord_mean + fix_accuracy) or gp.y < (y_coord_mean - fix_accuracy):
                                fixation_loss = True
                                break
                            else:
                                pass
                                
                        all_keys_pressed = event.getKeys()
                        if len(all_keys_pressed) != 0:
                            if 'q' in all_keys_pressed:
                                win.close()
                            if key_pressed == '':
                                key_pressed = all_keys_pressed[-1]  # only log the most recent key pressed
                            
                        fix_neutral.draw()
                        grating.draw()
                        grating_dia.draw()
                        win.flip()
                    
                    if fixation_loss:
                        time_file.write('FixLoss\n')
                        all_keys_pressed = event.getKeys()
                        if len(all_keys_pressed) != 0:
                            if 'q' in all_keys_pressed:
                                win.close()
                    else:
                        toc2 = time.time()
                        time_file.write('{}\t\t\t'.format(np.round(toc2-toc, 5)))
                        toc = toc2
                        # obtain user feedback - for 1500 ms (also includes 500 ms from stimulus presentation time)
                        # event.getKeys()  # clear all key presses
                        section_start = time.time()
                        while time.time() - section_start < 1.0 and key_pressed == '':  
                            fix_neutral.draw()
                            win.flip()
                            all_keys_pressed = event.getKeys()
                            if len(all_keys_pressed) != 0:
                                if 'q' in all_keys_pressed:
                                    win.close()
                                key_pressed = all_keys_pressed[-1]  # only log the most recent key pressed
                            
                        toc2 = time.time()
                        time_file.write('{}\t\t\t'.format(np.round(toc2-toc, 5)))
                        toc = toc2
                        
                        # determine response type and show user feedback

                        if using_eyetracker:
                            response = stf.calculate_response(key_pressed, grating_dir, fixation_loss)  
                        else:
                            response = stf.calculate_response(key_pressed, grating_dir)  

                        section_start = time.time()
                        while time.time() - section_start < 0.25:
                            if response == 1:
                                fix_correct.draw()
                            elif response == -1:
                                fix_wrong.draw()
                            elif response == 0:
                                fix_time.draw()
                            elif response == 99:
                                fix_loss.draw()
                            else:
                                print('Error in feedback to user')
                                core.quit()
                            win.flip()
                        
                        toc2 = time.time()
                        time_file.write('{}\t\t\t'.format(np.round(toc2-toc, 5)))

                        toc = toc2
                        
                        toc2 = time.time()
                        time_file.write('{}\t\t'.format(np.round(toc2-toc, 5)))
                        toc = toc2
                        time_file.write('{}\n'.format(np.round(time.time() - trial_start, 5)))
                                
                        if response != 0 and response != 99:  # only "successful" trials count as trials
                                 
                            # calculate staircase values
                            # staircase_counter_up, staircase_counter_down, movement_direction = stf.update_staircase_count(staircase_counter_up,
                            #                                                                                                staircase_counter_down,
                            #                                                                                                n_up, n_down, response, ori_list_created[ori_list_counter],
                            #                                                                                                ori_list_created[0])
                            
                            staircase_counter_up, staircase_counter_down, movement_direction = stf.update_staircase_count_contrast(staircase_counter_up,
                                                                                                                           staircase_counter_down,
                                                                                                                           n_up, n_down, response, con_list_created[con_list_counter],
                                                                                                                           con_list_created[0])
                             
                            # ori_list_counter, last_ori_list_counter = stf.calculate_orientation_list_counter(ori_list_counter, 
                            #                                                            movement_direction,
                            #                                                            len(ori_list_created))
                            
                            con_list_counter, last_con_list_counter = stf.calculate_contrast_list_counter(con_list_counter, 
                                                                                       movement_direction,
                                                                                       len(con_list_created) - 1)
                             
                            last_number_reversals = number_reversals
                            number_reversals, movement_direction, last_direction = stf.calculate_number_reversals(number_reversals,
                                                                                                                   movement_direction,
                                                                                                                   last_direction)
                            number_trials -= 1
                            # graph_orientations.append(ori_list_created[last_ori_list_counter])
                            # if last_number_reversals != number_reversals:
                            #     reversal_point_orientations.append(ori_list_created[last_ori_list_counter])
                            #     reversal_point_trials.append(trial_counter)

                            graph_orientations.append(con_list_created[last_con_list_counter])
                            if last_number_reversals != number_reversals:
                                reversal_point_orientations.append(con_list_created[last_con_list_counter])
                                reversal_point_trials.append(trial_counter)
                            trial_counter += 1
                     
                    data_file = open(data_file_name + '_data.txt'.format(run), 'a') 
                    data_file.write('{}\t{}\t\t\t{}\t\t\t{}\t\t{}\t\t\t{}\t\t\t{}\n'.format(trial_counter-1, 
                                                                #   last_ori_list_counter,
                                                                #   ori_list_created[last_ori_list_counter], 
                                                                  last_con_list_counter,
                                                                  con_list_created[last_con_list_counter],
                                                                  grating_dir, response, 
                                                                  number_reversals,
                                                                  number_trials))
                    data_file.close()
            # If trial has been less than 2.5 seconds, then keep showing fixation dot until 2 seconds has been achieved            
            while time.time() - trial_start < 2.5:
                fix_neutral.draw()
                win.flip()
                
        plt.figure()
        plt.plot(graph_orientations, marker='x')
        for idx, rtrial in enumerate(reversal_point_trials):
            plt.plot(rtrial, reversal_point_orientations[idx], marker='o', markerfacecolor='red')
        plt.savefig(data_file_name + '.png'.format(run))
    
        data_file = open(data_file_name + '_data.txt'.format(run), 'a') 
        data_file.write('\n\nGeometric Mean One Sided:\t\t{}\n'.format(gmean(reversal_point_orientations)))
        data_file.write('\n\nGeometric Mean Two Sided:\t\t{}'.format(2*gmean(reversal_point_orientations)))

        data_file.close()
    win.close()
    
    if __name__ == '__main__':
        run_staircase()