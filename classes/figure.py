import random
from data import figure_list


class Figure:
    def __init__(self, parameters):
        self.parameters = parameters

    def change(self, figure, color, all=1):
        elem_to_change = [0, 1]

        if not figure:
            elem_to_change.remove(0)
        elif not color:
            elem_to_change.remove(1)

        if all:
            if elem_to_change == 0:
                new_parameters = random.choice(
                    [x for x in figure_list if x[0] != self.parameters[0] and x[1] == self.parameters[1]])
                self.parameters = new_parameters
            elif elem_to_change == 1:
                new_parameters = random.choice(
                    [x for x in figure_list if x[0] == self.parameters[0] and x[1] != self.parameters[1]])
                self.parameters = new_parameters
        else:
            if elem_to_change == 0:
                new_parameters = random.choice(
                    [x for x in figure_list if x[0] != self.parameters[0] and x[1] == self.parameters[1]
                     and 0 <= x[0] < 5])
                self.parameters = new_parameters
            elif elem_to_change == 1:
                new_parameters = random.choice(
                    [x for x in figure_list if x[0] == self.parameters[0] and x[1] != self.parameters[1]
                     and 0 <= x[1] < 5])
                self.parameters = new_parameters

    def info(self):
        return list(self.parameters)

    def __str__(self):
        return str(self.parameters)
