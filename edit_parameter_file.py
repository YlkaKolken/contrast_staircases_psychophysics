from psychopy import gui
import os
import sys


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


folder_path = get_script_path()

os.chdir(folder_path)

if not os.path.isdir('parameter_files'):
    os.mkdir('parameter_files')

myDlg = gui.Dlg(title="Parameter file name")
# myDlg.addText('Subject info')
myDlg.addField('What is the name of the parameter file you want to edit')

filename = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    pass
else:
    print('User cancelled - script will fail')

file = open('parameter_files/' + filename[0] + '.spf', 'r')

data = []

for line in file:
    data.append(line.split(';')[1].replace('\n', ''))
    
myDlg = gui.Dlg(title="General Parameters")
myDlg.addField('How many correct trials in a row to decrease the change in orientation (any integer e.g. 4)', data[0])
myDlg.addField('How many wrong trials in a row to increase the change in orientation (any integer, e.g. 1)', data[1])
myDlg.addField('After how many trials should staircase end (any integer e.g. 200)', data[2])
myDlg.addField('After how many reversal points should the staircase end (any integer e.g. 15)', data[3])
general_p = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    pass
else:
    print('User cancelled - script will fail')


myDlg = gui.Dlg(title="Orientation List Creation")
# myDlg.addText('Subject info')
myDlg.addField('What is the reference orientation (any float e.g. 45.0)', data[4])
myDlg.addField('What is the total number of orientation differences required (any integer, e.g. 28)', data[5])
myDlg.addField('What is the maximum orientation difference in 1 direction (any float e.g. 22.5)', data[6])
myDlg.addField('What is the ratio between two consecutive orientation differences (any float e.g. 1.2)', data[7])
ol_p = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    pass
else:
    print('User cancelled - script will fail')


myDlg = gui.Dlg(title="Stimulus Grating Parameters")
# myDlg.addText('Subject info')
myDlg.addField('What is the contrast of the orientation grating (between 0.0 and 1.0)', data[8])
myDlg.addField('What is the spatial frequency of the orientation grating (any float, e.g. 2.4)', data[9])
myDlg.addField('What is the size of the orientation grating (in degrees, any float e.g. 4.0)', data[10])
myDlg.addField('What is the x-position of the orientation grating (in degrees, any float e.g. 4.5)', data[11])
myDlg.addField('What is the y-position of the orientation grating (in degrees, any float e.g. 4.5)', data[12])
sg_p = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    pass
else:
    print('User cancelled - script will fail')


myDlg = gui.Dlg(title="Fixation Circle Parameters")
# myDlg.addText('Subject info')
myDlg.addField('What is the size of the fixation circle (in degrees, any float e.g. 0.3)', data[13])
myDlg.addField('What is the x-position of the fixation circle (in degrees, any float e.g. 0.0)', data[14])
myDlg.addField('What is the y-position of the fixation circle (in degrees, any float e.g. 0.0)', data[15])
myDlg.addField('What is the colour of the NEUTRAL fixation circle be (in hexadecimal code e.g. white - #ffffff)', data[16])
myDlg.addField('What is the feedback colour for a CORRECT response (in hexadecimal code e.g. green - #00ff00)', data[17])
myDlg.addField('What is the feedback colour for a WRONG response (in hexadecimal code e.g. red - #ff0000)',data[18])
myDlg.addField('What is the feedback colour when response is given TOO LATE (in hexadecimal code e.g. orange - #ffa500)', data[19])
myDlg.addField('What is the feedback colour when fixation is lost (in hexadecimal code e.g. purple - #800080)', data[20])

fc_p = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    pass
else:
    print('User cancelled - script will fail')

labels_required = [
    ['num_correct_trials', 'num_wrong_trials', 'num_max_trials', 'num_max_reversals'],  # general staircase parameters
    ['ref_ori', 'ori_list_length', 'ori_list_max', 'ori_list_div'], # orientations
    ['ori_contrast', 'ori_sf', 'ori_size', 'ori_x_pos', 'ori_y_pos'],  # grating stimulus
    ['fix_size', 'fix_x_pos', 'fix_y_pos', 'fix_neutral_col', 'fix_cor_col', 'fix_wro_col', 'fix_late_col', 'fix_fixloss_col']  # Fixation circle
    ]
    
user_data = [general_p, ol_p, sg_p, fc_p]

folder_path = get_script_path()

os.chdir(folder_path)

if not os.path.isdir('parameter_files'):
    os.mkdir('parameter_files')


file = open('parameter_files/' + filename[0] + '.spf', 'w')
i = 0
for i in range(len(labels_required)):
    j = 0
    for j in range(len(labels_required[i])):
        file.write(labels_required[i][j])
        file.write(';')
        file.write(str(user_data[i][j]))
        file.write('\n')
        j += 1
    i += 1
file.close()