#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gooey import Gooey, GooeyParser
from openpyxl import load_workbook

from classes.experiment import Experiment
from classes.block import Block
from classes.matrix import Matrix

__author__ = 'ociepkam'


def load_info(filename):
    experiment_file = load_workbook(filename)
    sheet = experiment_file.get_active_sheet()

    experiment = []
    for row_idx in range(len(sheet.columns[0]) - 1):
        trial = {}
        for column_idx, column in enumerate(sheet.columns):
            if column_idx == 19:
                break
            if isinstance(column[row_idx + 1].value, (str, unicode)):
                trial.update({str(column[0].value): str(column[row_idx + 1].value)})
            elif not isinstance(column[row_idx + 1].value, type(None)):
                trial.update({str(column[0].value): int(column[row_idx + 1].value)})

        experiment.append(trial)

    number_of_blocks = max([int(x.value) for x in sheet.columns[0][1:]])
    return number_of_blocks, experiment


def concrete_experiment(participant_id, participant_sex, participant_age, file_name, random=1, eeg=0, fnirs=0):
    experiment_file_name = file_name + ".xlsx"
    number_of_blocks, data = load_info(experiment_file_name)
    experiment = Experiment(id=participant_id, sex=participant_sex, age=participant_age, eeg=eeg, fnirs=fnirs)

    for idx in range(number_of_blocks):
        block = Block([])
        experiment.list_of_blocks.append(block)

    for idx in range(len(data)):
        trial_info = data[idx]
        block_number = trial_info['block_number']
        if trial_info['trial_type'] == 'instruction':
            if trial_info['tip'][-3:] == 'txt':
                instruction_type = 'text'
            elif trial_info['tip'][-3:] == 'bmp' or trial_info['tip'][-3:] == 'jpg':
                instruction_type = 'image'
            else:
                raise AssertionError("wrong instruction file type")
            experiment.list_of_blocks[block_number-1].instruction = trial_info['tip']
            experiment.list_of_blocks[block_number-1].instruction_time = trial_info['tip_time']
            experiment.list_of_blocks[block_number-1].instruction_type = instruction_type
        else:
            matrix = Matrix(elements=trial_info['elements'], ftime=trial_info['ftime'], mtime=trial_info['mtime'],
                           stime=trial_info['stime'], maxtime=trial_info['maxtime'], var=trial_info['var'],
                           shint=trial_info['shint'], ehint=trial_info['ehint'], feedb=trial_info['feedb'],
                           wait=trial_info['wait'], exp=trial_info['trial_type'], change=trial_info['change'],
                           unique=trial_info['unique'], figure=trial_info['figure'], colors=trial_info['colors'],
                           all=trial_info['all'])

            matrix.convert_matrix()
            experiment.list_of_blocks[block_number - 1].list_of_matrix.append(matrix)

    if random:
        experiment.randomize()
    experiment.save()


@Gooey(language='english',  # Translations configurable via json
       default_size=(450, 500),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def main():
    parser = GooeyParser(description='Create_concrete_experiment')
    parser.add_argument('Experiment_file_name', widget='FileChooser', help='Choose experiment file with general info')
    parser.add_argument('Participant_ID', type=str)
    parser.add_argument('Participant_Age', default=0, type=int)
    parser.add_argument('Participant_Sex', default='M', choices=['M', 'F'])
    parser.add_argument('Random', default='True', choices=['True', 'False'], help="Present trials in random order")
    parser.add_argument('EEG_connected', default='0', choices=['1', '0'], help='Choice')
    parser.add_argument('fNIRS_connected', default='0', choices=['1', '0'], help='Choice')

    args = parser.parse_args()

    file_name = args.Experiment_file_name.split("/")[-1][:-5]

    concrete_experiment(args.Participant_ID, args.Participant_Sex, args.Participant_Age,
                        file_name, args.EEG_connected, args.fNIRS_connected)


if __name__ == '__main__':
    main()
