from Key import Key


class SymbolKey(Key):

    def __init__(self, symbol):
        super(SymbolKey, self).__init__()
        self.__symbol = symbol

    def get_value(self):
        return self.__symbol
