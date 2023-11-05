import PySimpleGUI as sg
import gabor_patch_testing
import fixation_circle_testing
import staircase_core
import orientation_list_creation
import os

def read_file():
    r_layout = [[sg.T("")], [sg.Text("Choose a parameter file: "), sg.FileBrowse(key="-IN-", file_types=(("Staircase Parameter Files", "*.spf"),))], [sg.Button("Submit")]]
    r_window = sg.Window("Parameter File", r_layout, size=(600, 150))
    while True:
        r_event, r_values = r_window.read()
        if r_event == sg.WIN_CLOSED or r_event=="Exit":
            return 0
            break
        elif r_event == "Submit":
            file = (r_values["-IN-"])
            r_window.close()
            break
    return(file)

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Button('Run Staircase', size=(40, 4), pad=(350, 35))],
            [sg.Button('Create Parameter File', size=(40, 4), pad=(350, 35))],
            [sg.Button('Edit Parameter File', size=(40, 4), pad=(350, 35))],
            [sg.Button('Test Stimuli', size=(40, 4), pad=(350, 35))]]

# Create the Window
window = sg.Window('Staircase Software', layout,size=(1000, 600))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    elif event == 'Run Staircase':
        filename = read_file()
        file = open(filename, 'r')
        user_data = []
        # Strips the newline character
        for line in file.readlines():
            user_data.append(line.strip().split(';')[1])
        file.close()
        filename = filename.split('/')[-1]
        
        p_layout = [[sg.T("")], [sg.Text("Choose a folder to save data file in: "), sg.FolderBrowse(key="-IN-")], [sg.Button("Submit")]]
        p_window = sg.Window("Data File", p_layout, size=(600, 150))
        while True:
            p_event, p_values = p_window.read()
            if p_event == sg.WIN_CLOSED or p_event=="Exit":
                break
            elif p_event == "Submit":
                folder_path = (p_values["-IN-"])
                p_window.close()

        ori_list = orientation_list_creation.create_orientation_list(22.5, 1.2, 28)
        con_list = orientation_list_creation.create_contrast_list(1, 1.25, 20)
        
        ori_layout = [[sg.Radio(ori, "RADIO1", default=True)] for ori in ori_list]
        ori_layout.append([sg.Button('Submit')])
        ori_layout.insert(0, [sg.Text('Choose the starting orientation for the participant')])
        ori_window = sg.Window('Select Orientation Value', ori_layout)
        
        while True:
            ori_event, ori_values = ori_window.read()
            if ori_event == sg.WIN_CLOSED or ori_event=="Exit":
                break
            elif ori_event == 'Submit':
                ori_c = 0
                for idx in range(len(ori_values)):
                    if ori_values[idx] == True:
                        ori_c = idx
                ori_window.close()
    
        con_layout = [[sg.Radio(con, "RADIO1", default=True)] for con in con_list]
        con_layout.append([sg.Button('Submit')])
        con_layout.insert(0, [sg.Text('Choose the starting contrast for the participant')])
        con_window = sg.Window('Select Contrast Value', con_layout)
        
        while True:
            con_event, con_values = con_window.read()
            if con_event == sg.WIN_CLOSED or con_event=="Exit":
                break
            elif con_event == 'Submit':
                con_c = 0
                for idx in range(len(con_values)):
                    if con_values[idx] == True:
                        con_c = idx
                con_window.close()
                
        size1 = 80
        size2 = 1
        rs_layout = [[sg.Text('Observer Name', size=(size1, size2)), sg.Input()],
                    [sg.Text('Participant ID - used to create filename', size=(size1, size2)), sg.Input()],
                    [sg.Text('Participant Session - used to create filename', size=(size1, size2)), sg.Input()],
                    [sg.Text('Number of runs', size=(size1, size2)), sg.Input()],
                    [sg.Text('Fix accuracy - any float e.g. 0.2', size=(size1, size2)), sg.Input()],
                    [sg.Button('Run Staircase', pad=(500, 20))]
                    ]
        rs_window = sg.Window('Run Staircase', rs_layout)
        while True:
            rs_event, rs_values = rs_window.read()
            if rs_event == sg.WIN_CLOSED or rs_event=="Exit":
                break
            elif rs_event == 'Run Staircase':
                rs_window.close()

                staircase_core.run_staircase(user_data, filename, rs_values, ori_c, con_c, folder_path + '/')
    elif event == 'Create Parameter File':
        size1 = 80
        size2 = 1
        p_layout = [[sg.Text('How many correct trials in a row to decrease the change in orientation (any integer e.g. 4)', size=(size1, size2)), sg.Input()],
                    [sg.Text('How many wrong trials in a row to increase the change in orientation (any integer, e.g. 1)', size=(size1, size2)), sg.Input()],
                    [sg.Text('After how many trials should staircase end (any integer e.g. 200)', size=(size1, size2)), sg.Input()],
                    [sg.Text('After how many reversal points should the staircase end (any integer e.g. 15)', size=(size1, size2)), sg.Input()],
                    [sg.Text('Which I-lab will this staircase run in (2 or 3)', size=(size1, size2)), sg.Input()],
                    [sg.Text('Will you be using the eyetracker (y or n)', size=(size1, size2)), sg.Input()],
                    [sg.Button('Next', pad=(500, 20))]
                    ]
        p_window = sg.Window('General Parameters', p_layout)
        while True:
            p_event, p_values = p_window.read()
            if p_event == sg.WIN_CLOSED or p_event=="Exit":
                break
            elif p_event == 'Next':
                general_p = p_values
                p_window.close()
                p_layout = [[sg.Text('What is the reference orientation (any float e.g. 45.0)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the total number of orientation differences required (any integer, e.g. 28)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the maximum orientation difference in 1 direction (any float e.g. 22.5)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the ratio between two consecutive orientation differences (any float e.g. 1.2)', size=(size1, size2)), sg.Input()],
                            [sg.Button('Next', pad=(500, 20))]
                            ]
                p_window = sg.Window('Orientation List', p_layout)
                while True:
                    p_event, p_values = p_window.read()
                    if p_event == sg.WIN_CLOSED or p_event=="Exit":
                        break
                    elif p_event == 'Next':
                        ol_p = p_values
                        p_window.close()
                        p_layout = [[sg.Text('What is the contrast of the orientation grating (between 0.0 and 1.0 e.g. 0.5)', size=(size1, size2)), sg.Input()],
                                    [sg.Text('What is the spatial frequency of the orientation grating (any float, e.g. 2.37)', size=(size1, size2)), sg.Input()],
                                    [sg.Text('What is the size of the orientation grating (in degrees, any float e.g. 3.0)', size=(size1, size2)), sg.Input()],
                                    [sg.Text('What is the x-position of the orientation grating (in degrees, any float e.g. 4.5)', size=(size1, size2)), sg.Input()],
                                    [sg.Text('What is the y-position of the orientation grating (in degrees, any float e.g. 4.5)', size=(size1, size2)), sg.Input()],
                                    [sg.Button('Next', pad=(500, 20))]
                                    ]
                        p_window = sg.Window('Stimulus Grating', p_layout)
                        while True:
                            p_event, p_values = p_window.read()
                            if p_event == sg.WIN_CLOSED or p_event=="Exit":
                                break
                            elif p_event == 'Next':
                                sg_p = p_values
                                p_window.close()
                                p_layout = [[sg.Text('What is the size of the fixation circle (in degrees, any float e.g. 0.2)', size=(size1, size2)), sg.Input()],
                                            [sg.Text('What is the x-position of the fixation circle (in degrees, any float e.g. 0.0)', size=(size1, size2)), sg.Input()],
                                            [sg.Text('What is the y-position of the fixation circle (in degrees, any float e.g. 0.0)', size=(size1, size2)), sg.Input()],
                                            [sg.Text('What is the colour of the NEUTRAL fixation circle be (in hexadecimal code e.g. white - #ffffff)', size=(size1, size2)), sg.Input()],
                                            [sg.Text('What is the feedback colour for a CORRECT response (in hexadecimal code e.g. green - #013220)', size=(size1, size2)), sg.Input()],
                                            [sg.Text('What is the feedback colour for a WRONG response (in hexadecimal code e.g. red - #ff0000)', size=(size1, size2)), sg.Input()],
                                            [sg.Text('What is the feedback colour when response is given TOO LATE (in hexadecimal code e.g. orange - #ffa500)', size=(size1, size2)), sg.Input()],
                                            [sg.Text('What is the feedback colour when fixation is lost (in hexadecimal code e.g. #00FFFF)', size=(size1, size2)), sg.Input()],
                                            [sg.Button('Submit', pad=(500, 20))]
                                            ]
                                p_window = sg.Window('Fixation Circle', p_layout)
                                while True:
                                    p_event, p_values = p_window.read()
                                    if p_event == sg.WIN_CLOSED or p_event=="Exit":
                                        break
                                    elif p_event == 'Submit':
                                        fc_p = p_values
                                        p_window.close()
                                        p_layout = [[sg.T("")], [sg.Text("Choose a folder to save file in: "), sg.FolderBrowse(key="-IN-")], [sg.Button("Submit")]]
                                        p_window = sg.Window("Parameter File", p_layout, size=(600, 150))
                                        while True:
                                            p_event, p_values = p_window.read()
                                            if p_event == sg.WIN_CLOSED or p_event=="Exit":
                                                break
                                            elif p_event == "Submit":
                                                folder_path = (p_values["-IN-"])
                                                p_window.close()
                                                p_layout = [[sg.T("")], [sg.Text("Give the parameter file a name: "), sg.Input()], [sg.Button("Submit")]]
                                                p_window = sg.Window("Parameter File", p_layout, size=(600, 150))
                                                while True:
                                                    p_event, p_values = p_window.read()
                                                    if p_event == sg.WIN_CLOSED or p_event=="Exit":
                                                        break
                                                    elif p_event == "Submit":
                                                        filename = p_values[0]
                                                        p_window.close()
                                                        
                                                        labels_required = [
                                                                            ['num_correct_trials','num_wrong_trials', 'num_max_trials', 'num_max_reversals', 'eyelab', 'eyetracker'],  # general staircase parameters
                                                                            ['ref_ori', 'ori_list_length', 'ori_list_max', 'ori_list_div'], # orientations
                                                                            ['ori_contrast', 'ori_sf', 'ori_size', 'ori_x_pos', 'ori_y_pos'],  # grating stimulus
                                                                            ['fix_size', 'fix_x_pos', 'fix_y_pos', 'fix_neutral_col', 'fix_cor_col',
                                                                             'fix_wro_col', 'fix_late_col', 'fix_fixloss_col']  # Fixation circle
                                                                            ]
                                                        user_data = [general_p, ol_p, sg_p, fc_p]
                                                                            
                                                        file = open(folder_path + '/' + filename + '.spf', 'w')
                                                        i = 0
                                                        for i in range(len(labels_required)):
                                                            j = 0
                                                            for j in range(len(labels_required[i])):
                                                                file.write(labels_required[i][j])
                                                                file.write(';')
                                                                file.write(user_data[i][j])
                                                                file.write('\n')
                                                                j += 1
                                                            i += 1
                                                        file.close()
    elif event == 'Edit Parameter File':
        filename = read_file()
        file = open(filename, 'r')
        user_data = []
        # Strips the newline character
        for line in file.readlines():
            user_data.append(line.strip().split(';')[1])
        file.close()
        size1 = 80
        size2 = 1
        p_layout = [[sg.Text('How many correct trials in a row to decrease the change in orientation (any integer e.g. 4)', size=(size1, size2)), sg.Input(user_data[0])],
                    [sg.Text('How many wrong trials in a row to increase the change in orientation (any integer, e.g. 1)', size=(size1, size2)), sg.Input(user_data[1])],
                    [sg.Text('After how many trials should staircase end (any integer e.g. 200)', size=(size1, size2)), sg.Input(user_data[2])],
                    [sg.Text('After how many reversal points should the staircase end (any integer e.g. 15)', size=(size1, size2)), sg.Input(user_data[3])],
                    [sg.Text('Which I-lab will this staircase run in (2 or 3)', size=(size1, size2)), sg.Input(user_data[4])],
                    [sg.Text('Will you be using the eyetracker (y or n)', size=(size1, size2)), sg.Input(user_data[5])],
                    [sg.Button('Next', pad=(500, 20))]
                    ]
        p_window = sg.Window('General Parameters', p_layout)
        while True:
            p_event, p_values = p_window.read()
            if p_event == sg.WIN_CLOSED or p_event=="Exit":
                break
            elif p_event == 'Next':
                general_p = p_values
                p_window.close()
                p_layout = [[sg.Text('What is the reference orientation (any float e.g. 45.0)', size=(size1, size2)), sg.Input(user_data[6])],
                            [sg.Text('What is the total number of orientation differences required (any integer, e.g. 28)', size=(size1, size2)), sg.Input(user_data[7])],
                            [sg.Text('What is the maximum orientation difference in 1 direction (any float e.g. 22.5)', size=(size1, size2)), sg.Input(user_data[8])],
                            [sg.Text('What is the ratio between two consecutive orientation differences (any float e.g. 1.2)', size=(size1, size2)), sg.Input(user_data[9])],
                            [sg.Button('Next', pad=(500, 20))]
                            ]
                p_window = sg.Window('Orientation List', p_layout)
                while True:
                    p_event, p_values = p_window.read()
                    if p_event == sg.WIN_CLOSED or p_event=="Exit":
                        break
                    elif p_event == 'Next':
                        ol_p = p_values
                        p_window.close()
                        p_layout = [[sg.Text('What is the contrast of the orientation grating (between 0.0 and 1.0) e.g. 0.5', size=(size1, size2)), sg.Input(user_data[10])],
                                    [sg.Text('What is the spatial frequency of the orientation grating (any float, e.g. 2.37)', size=(size1, size2)), sg.Input(user_data[11])],
                                    [sg.Text('What is the size of the orientation grating (in cm, any float e.g. 3.0)', size=(size1, size2)), sg.Input(user_data[12])],
                                    [sg.Text('What is the x-position of the orientation grating (in cm, any float e.g. 4.5)', size=(size1, size2)), sg.Input(user_data[13])],
                                    [sg.Text('What is the y-position of the orientation grating (in cm, any float e.g. 4.5)', size=(size1, size2)), sg.Input(user_data[14])],
                                    [sg.Button('Next', pad=(500, 20))]
                                    ]
                        p_window = sg.Window('Stimulus Grating', p_layout)
                        while True:
                            p_event, p_values = p_window.read()
                            if p_event == sg.WIN_CLOSED or p_event=="Exit":
                                break
                            elif p_event == 'Next':
                                sg_p = p_values
                                p_window.close()
                                p_layout = [[sg.Text('What is the size of the fixation circle (in cm, any float e.g. 0.2)', size=(size1, size2)), sg.Input(user_data[15])],
                                            [sg.Text('What is the x-position of the fixation circle (in cm, any float e.g. 0.0)', size=(size1, size2)), sg.Input(user_data[16])],
                                            [sg.Text('What is the y-position of the fixation circle (in cmn any float e.g. 0.0)', size=(size1, size2)), sg.Input(user_data[17])],
                                            [sg.Text('What is the colour of the NEUTRAL fixation circle be (in hexadecimal code e.g. #000000)', size=(size1, size2)), sg.Input(user_data[18])],
                                            [sg.Text('What is the feedback colour for a CORRECT response (in hexadecimal code e.g. #000000)', size=(size1, size2)), sg.Input(user_data[19])],
                                            [sg.Text('What is the feedback colour for a WRONG response (in hexadecimal code e.g. #000000)', size=(size1, size2)), sg.Input(user_data[20])],
                                            [sg.Text('What is the feedback colour when response is given TOO LATE (in hexadecimal code e.g. #000000)', size=(size1, size2)), sg.Input(user_data[21])],
                                            [sg.Text('What is the feedback colour when fixation is lost (in hexadecimal code e.g. #000000)', size=(size1, size2)), sg.Input(user_data[22])],
                                            [sg.Button('Submit', pad=(500, 20))]
                                            ]
                                p_window = sg.Window('Fixation Circle', p_layout)
                                while True:
                                    p_event, p_values = p_window.read()
                                    if p_event == sg.WIN_CLOSED or p_event=="Exit":
                                        break
                                    elif p_event == 'Submit':
                                        fc_p = p_values
                                        p_window.close()
                                        labels_required = [
                                                            ['num_correct_trials','num_wrong_trials', 'num_max_trials', 'num_max_reversals','eyelab', 'eyetracker'],  # general staircase parameters
                                                            ['ref_ori', 'ori_list_length', 'ori_list_max', 'ori_list_div'], # orientations
                                                            ['ori_contrast', 'ori_sf', 'ori_size', 'ori_x_pos', 'ori_y_pos'],  # grating stimulus
                                                            ['fix_size', 'fix_x_pos', 'fix_y_pos', 'fix_neutral_col', 'fix_cor_col',
                                                             'fix_wro_col', 'fix_late_col', 'fix_fixloss_col']  # Fixation circle
                                                            ]
                                        user_data = [general_p, ol_p, sg_p, fc_p]
                                                            
                                        file = open(filename, 'w')
                                        i = 0
                                        for i in range(len(labels_required)):
                                            j = 0
                                            for j in range(len(labels_required[i])):
                                                file.write(labels_required[i][j])
                                                file.write(';')
                                                file.write(user_data[i][j])
                                                file.write('\n')
                                                j += 1
                                            i += 1
                                        file.close()
    elif event == 'Test Stimuli':
        size1 = 80
        size2 = 1
        t_layout = [[sg.Button('Gabor Patch', size=(40, 4), pad=(100, 35))],
                    [sg.Button('Fixation Circle', size=(40, 4), pad=(100, 35))],
                    ]
        t_window = sg.Window('Test Stimuli', t_layout,size=(500, 300))
        while True:
            t_event, t_values = t_window.read()
            if t_event == sg.WIN_CLOSED or t_event=="Exit":
                break
            elif t_event == "Gabor Patch":
                g_layout = [[sg.Text('What is the contrast of the orientation grating (between 0.0 and 1.0)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the spatial frequency of the orientation grating (any float, e.g. 2.37)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the size of the orientation grating (in degrees, any float e.g. 4.0)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the x-position of the orientation grating (in degrees, any float e.g. 4.5)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the y-position of the orientation grating (in degrees, any float e.g. 4.5)', size=(size1, size2)), sg.Input()],
                            [sg.Button('View', pad=(500, 20))]
                            ]
                g_window = sg.Window('Stimulus Grating', g_layout)
                while True:
                    g_event, g_values = g_window.read()
                    if g_event == sg.WIN_CLOSED or g_event=="Exit":
                        break
                    elif g_event == 'View':
                        gp_data = g_values
                        gabor_patch_testing.show(gp_data)
            elif t_event == 'Fixation Circle':
                g_layout = [[sg.Text('What is the size of the fixation circle (in degrees, any float e.g. 0.3)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the x-position of the fixation circle (in degrees, any float e.g. 0.0)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the y-position of the fixation circle (in degrees, any float e.g. 0.0)', size=(size1, size2)), sg.Input()],
                            [sg.Text('What is the colour of the NEUTRAL fixation circle be (in hexadecimal code e.g. #000000)', size=(size1, size2)), sg.Input()],
                            [sg.Button('View', pad=(500, 20))]
                            ]
                g_window = sg.Window('Stimulus Grating', g_layout)
                while True:
                    g_event, g_values = g_window.read()
                    if g_event == sg.WIN_CLOSED or g_event=="Exit":
                        break
                    elif g_event == 'View':
                        gp_data = g_values
                        fixation_circle_testing.show(gp_data)
            else:
                break 
    else:
        break
        
window.close()