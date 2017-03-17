from Key import Key


class NumKey(Key):

    def __init__(self, number):
        super(NumKey, self).__init__()
        self.__number = number

    def get_value(self):
        return self.__number

    def __str__(self):
        return "Key with value: {value}".format(value=self.__number)

    def __repr__(self):
        return self.__str__()