class MineField:

    def __init__(self, field_size):
        self.field_size = field_size
        self.__field = None

    @property
    def field(self):
        if self.__field:
            return self.__field

        self.__field = self.__generate_field()

        return self.__field

    def __generate_field(self):
        [[0 for i in range(self.field_size)] for i in range(self.field_size)]

class MineSweeper:

    def __init__(self, field):
        self.my_attr = 1
        self.field   = field

field = MineField(3)

game = MineSweeper(field)

print game.field.field
