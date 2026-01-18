from enum import Enum

# class syntax
class Type(Enum):

    fire = 1
    plant = 2
    water = 4

    def __init__(self, value):
        super().__init__()
        

# functional syntax
Type = Enum('type', [('fire', 1), ('plant', 2), ('water', 4)])