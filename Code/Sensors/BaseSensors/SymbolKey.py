from Key import Key


class SymbolKey(Key):

    def __init__(self, symbol):
        super(SymbolKey, self).__init__()
        self.__symbol = symbol

    def get_value(self):
        return self.__symbol

    def __str__(self):
        return "Key with value: {value}".format(value=self.__symbol)

    def __repr__(self):
        return self.__str__()
