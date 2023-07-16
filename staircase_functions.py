# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 14:15:55 2020

@author: Ibrahim Hashim

@github: https://github.com/Ibrahim-Hashim-Coding
"""

## Import libraries needed to run
import random


def calculate_grating_orientation(reference_orientation, 
                                  current_orientation):
    '''
    Calculates the orientation and direction that the grating has to have for 
    the current trial.

    Parameters
    ----------
    reference_orientation : float
        The reference orientation which the user has to compare the grating 
        orientations to.
    current_orientation : float
        The current orientation which is added to the reference orientation to
        find the grating orientation

    Returns
    -------
    grating_orientation, grating_direction : UNION[float, str]
        The grating_orientation is the combination of the reference orientation
        and the current_orientation x grating_direction. The grating_direction 
        is either 1 or -1. 

    '''
    grating_direction = random.choice([-1, 1])
    grating_orientation = reference_orientation + current_orientation*grating_direction
    
    return grating_orientation, grating_direction


def calculate_number_reversals(number_reversals, movement_direction,
                               last_direction):
    '''
    Calculates if a reversal point has been reached if the last_direction
    and movement_direction do not match. Also updates last_direction

    Parameters
    ----------
    number_reversals : int
        Total number of reversal points still left.
    movement_direction : str
        The current direction (no_change, up or down) in the staircase.
    last_direction : str
        The last direction (up or down) in the staircase.

    Returns
    -------
    Union[int, str, str]
        

    '''
    if movement_direction == 'no_change':
        pass
    elif last_direction == 'not_set_yet':
        last_direction = movement_direction
    elif movement_direction != last_direction:
        last_direction = movement_direction
        number_reversals -= 1
    return number_reversals, movement_direction, last_direction


def calculate_orientation_list_counter(orientation_list_counter, 
                                       movement_direction, 
                                       length_orientation_list):
    '''
    This function determines whether the orientation_list_counter has to be
    increased, decreased or kept the same.

    Parameters
    ----------
    orientation_list_counter : int
        Current index of orientation list defining the current orientation
    movement_direction : str
        The current direction (no_change, up or down) in the staircase.
    length_orientation_list : int
        The total number of orientations in the orientation list

    Returns
    -------
    orientation_list_counter : int
        Updated index of orientation list defining the updated orientation

    '''
    last_orientation_list_counter = orientation_list_counter
    if movement_direction == 'no_change':
        pass
    elif movement_direction == 'up':
        if orientation_list_counter != 0:
            orientation_list_counter -= 1
    elif movement_direction == 'down':
        if orientation_list_counter != length_orientation_list:
            orientation_list_counter += 1
    return orientation_list_counter, last_orientation_list_counter


def calculate_contrast_list_counter(contrast_list_counter, 
                                       movement_direction, 
                                       length_contrast_list):
    '''
    This function determines whether the contrast_list_counter has to be
    increased, decreased or kept the same.

    Parameters
    ----------
    contrast_list_counter : int
        Current index of contrast list defining the current contrast
    movement_direction : str
        The current direction (no_change, up or down) in the staircase.
    length_contrast_list : int
        The total number of contrasts in the contrast list

    Returns
    -------
    contrast_list_counter : int
        Updated index of contrast list defining the updated contrast

    '''
    last_contrast_list_counter = contrast_list_counter
    if movement_direction == 'no_change':
        pass
    elif movement_direction == 'up':
        if contrast_list_counter != 0:
            contrast_list_counter -= 1
    elif movement_direction == 'down':
        if contrast_list_counter != length_contrast_list:
            contrast_list_counter += 1
    return contrast_list_counter, last_contrast_list_counter


def calculate_response(key_pressed, grating_direction, fixation_loss = False):
    '''
    This function determines whether the key pressed by the user was a 
    correct or wrong response (or not given).

    Parameters
    ----------
    key_pressed : str
        Whether the key pressed was the left or right key
    grating_direction : int
        The direction of the grating, either 1 (right) or -1 (left)
    fixation_loss : bool
        If using eyetracker and participant looses fixation during trial
        
    Returns
    -------
    response: int
        Whether the response was correct (1), wrong(-1) or no valid response 
        was given (0).

    '''
    if fixation_loss:
        response = 99  # indicates fixation was lost
    elif key_pressed == 'left':
        if grating_direction == -1:
            response = 1  # indicates correct answer
        else:
            response = -1  # indicates wrong answer
    elif key_pressed == 'right':
        if grating_direction == 1:
            response = 1  # indicates correct answer
        else:
            response = -1  # indicates wrong answer
    else:
        response = 0  # indicates no response or wrong key pressed
    return response


def create_orientation_list(maximum_value, division_value, 
                            length_list):
    '''
    This function creates all the possible orientations required by the user. 
    The orientations will be used to modify the reference orientation of the 
    stimulus grating set by the user and are stored in a list.
    
    Parameters
    ----------
    maximum_value : float
        The biggest difference between the reference orientation and the shown
        orientation of the stimulus grating.
    division_value : float
        The divisor between two adjacent orientations.
    length_list : int
        The total amount of orientations required by the user.

    Returns
    -------
    List[float]
        A list containing all the orientations required by the user to modify
        the reference orientation of the stimulus grating. The orientations are
        sorted in a descending order.

    '''
    orientation_list = [round(float(maximum_value)/(float(division_value)**
                                                    float(x)), 3) 
                        if x != 0 else float(maximum_value) for x in 
                        range(0, length_list)]
    
    return orientation_list


def create_contrast_list(maximum_value, division_value, 
                            length_list):
    '''
    This function creates all the possible contrasts required by the user. 
    The contrasts will be used to modify the reference contrast of the 
    stimulus grating set by the user and are stored in a list.
    
    Parameters
    ----------
    maximum_value : float
        The biggest difference between the reference contrast and the shown
        contrast of the stimulus grating.
    division_value : float
        The divisor between two adjacent contrasts.
    length_list : int
        The total amount of contrasts required by the user.

    Returns
    -------
    List[float]
        A list containing all the contrasts required by the user to modify
        the reference contrast of the stimulus grating. The contrasts are
        sorted in a descending order.

    '''
    contrast_list = [round(float(maximum_value)/(float(division_value)**
                                                    float(x)), 3) 
                        if x != 0 else float(maximum_value) for x in 
                        range(0, length_list)]
    
    return contrast_list


def update_staircase_count(staircase_counter_up, 
                           staircase_counter_down, n_up, 
                           n_down, response, orientation_gradient, max_orientation_gradient):
                                                                
    '''
    This function updates the staircase counters and decides whether the 
    staircase should be moving up or down based on the number of correct and
    wrong answer a participant has given.

    Parameters
    ----------
    staircase_counter_up : int
        Sum of number of wrong responses.
    staircase_counter_down : int
        Sum of number of correct responses.
    n_up : int
        User specified number of wrong responses to go up orientation level.
    n_down : int
        User specified number of correct responses to go down orientation 
        level.
    response : int
        Whether the response was correct (1), wrong(-1) or no valid response 
        was given (0).
    orientation_gradient : float
        The current orientation gradient that the user is seeing.
    max_orientation_gradient : float
        The maximum orientation gradient in one direction that the user can see.

    Returns
    -------
    Union[int, int, str]
        Returns updated staircase counters and movement direction

    '''
    if float(orientation_gradient) != float(max_orientation_gradient):
        if response == 1:  # if correct response
            staircase_counter_down += 1
        elif response == -1:  # if wrong response
            staircase_counter_up += 1
    else:
        staircase_counter_down += 1  # at max orientation always go down
        
    if staircase_counter_down == n_down:  
        movement_direction = 'down'
        staircase_counter_up = staircase_counter_down = 0  
    elif staircase_counter_up == n_up:
        movement_direction = 'up'
        staircase_counter_up = staircase_counter_down = 0 
    else:
        movement_direction = 'no_change' 

    return staircase_counter_up, staircase_counter_down, movement_direction


def update_staircase_count_contrast(staircase_counter_up, 
                           staircase_counter_down, n_up, 
                           n_down, response, orientation_contrast, max_orientation_contrast):
                                                                
    '''
    This function updates the staircase counters and decides whether the 
    staircase should be moving up or down based on the number of correct and
    wrong answer a participant has given.

    Parameters
    ----------
    staircase_counter_up : int
        Sum of number of wrong responses.
    staircase_counter_down : int
        Sum of number of correct responses.
    n_up : int
        User specified number of wrong responses to go up orientation level.
    n_down : int
        User specified number of correct responses to go down orientation 
        level.
    response : int
        Whether the response was correct (1), wrong(-1) or no valid response 
        was given (0).
    orientation_contrast : float
        The current orientation contrast that the user is seeing.
    max_orientation_contrast : float
        The maximum orientation contrast in one direction that the user can see.

    Returns
    -------
    Union[int, int, str]
        Returns updated staircase counters and movement direction

    '''
    if float(orientation_contrast) != float(max_orientation_contrast):
        if response == 1:  # if correct response
            staircase_counter_down += 1
        elif response == -1:  # if wrong response
            staircase_counter_up += 1
    else:
        staircase_counter_down += 1  # at max orientation always go down
        
    if staircase_counter_down == n_down:  
        movement_direction = 'down'
        staircase_counter_up = staircase_counter_down = 0  
    elif staircase_counter_up == n_up:
        movement_direction = 'up'
        staircase_counter_up = staircase_counter_down = 0 
    else:
        movement_direction = 'no_change' 

    return staircase_counter_up, staircase_counter_down, movement_direction
