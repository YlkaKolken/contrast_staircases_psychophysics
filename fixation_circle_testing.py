from psychopy import visual, event, core


def show(parameters):
    # This defines the parameters for the WINDOW where stimuli are shown
    win = visual.Window([1600,900],allowGUI=True, monitor='testMonitor', 
                        units='deg', fullscr = True) 

    fix = visual.GratingStim(win, color = parameters[3],
                                 tex = None, mask = 'circle', units = 'deg', 
                                 size = parameters[0], pos = (parameters[1], parameters[2]))
    
    key_pressed = ''  # used to record last key pressed by user in underneath loop
    event.getKeys()  # clear all key presses
    frame_counter = 0
    while key_pressed == '':  
        fix.draw()
        win.flip()
        all_keys_pressed = event.getKeys()
        if len(all_keys_pressed) != 0:
            key_pressed = all_keys_pressed[-1]  # only log the most recent key pressed
    win.close()
    
if __name__ == '__main__':
    show()