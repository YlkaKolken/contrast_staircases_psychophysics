from psychopy import visual, event, core


def show(parameters):
    # This defines the parameters for the WINDOW where stimuli are shown
    win = visual.Window([1600,900],allowGUI=True, monitor='testMonitor', 
                        units='deg', fullscr = True) 
                                 
    grating = visual.GratingStim(win,contrast = parameters[0], units = 'deg', mask = 'circle', sf = parameters[1], 
                                size = parameters[2], ori = 45, pos=(parameters[3], parameters[4]))
    
    key_pressed = ''  # used to record last key pressed by user in underneath loop
    event.getKeys()  # clear all key presses
    frame_counter = 0
    while key_pressed == '':  
        grating.draw()
        win.flip()
        all_keys_pressed = event.getKeys()
        if len(all_keys_pressed) != 0:
            key_pressed = all_keys_pressed[-1]  # only log the most recent key pressed
    win.close()
    
if __name__ == '__main__':
    show()