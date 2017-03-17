from Key import Key


class NumKey(Key):

    def __init__(self, number):
        super(NumKey, self).__init__()
        self.__number = number

    def get_value(self):
        return self.__number
