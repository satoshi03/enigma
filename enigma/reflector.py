from .base import Encoder


class Reflector(Encoder):
    def __init__(self):
        self._exchange_list = [i for i in range(25, -1, -1)]

    def encode_char(self, char, order):
        index = self._to_index(char)
        encoded_index = self._exchange_list[index]
        return self._to_char(encoded_index)
