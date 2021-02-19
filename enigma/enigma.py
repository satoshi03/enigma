import re

from .base import Encoder
from .scrambler import Scrambler, Scrambler1RotateRule, Scrambler2RotateRule, Scrambler3RotateRule
from .plugboard import PlugBoard
from .reflector import Reflector
from .common import Order


class Enigma(Encoder):

    def __init__(self, config):
        self._plug_board = PlugBoard(config._plug_board_exchange_map)
        self._scrambler_1 = Scrambler(Scrambler1RotateRule(),
                                      config._scrambler_1_counter_num,
                                      config._scrambler_1_exchange_map)
        self._scrambler_2 = Scrambler(Scrambler2RotateRule(),
                                      config._scrambler_2_counter_num,
                                      config._scrambler_2_exchange_map)
        self._scrambler_3 = Scrambler(Scrambler3RotateRule(),
                                      config._scrambler_3_counter_num,
                                      config._scrambler_3_exchange_map)
        self._reflector = Reflector()

    def encode(self, value):
        s = ''
        for c in value:
            if re.search("[A-Z]", c):
                s += self.encode_char(c)
            else:
                s += c
        return s

    def encode_char(self, c):
        c = self._plug_board.encode_char(c, Order.Forward)
        c = self._scrambler_1.encode_char(c, Order.Forward)
        c = self._scrambler_2.encode_char(c, Order.Forward)
        c = self._scrambler_3.encode_char(c, Order.Forward)
        c = self._reflector.encode_char(c, Order.Forward)
        c = self._scrambler_3.encode_char(c, Order.Backward)
        c = self._scrambler_2.encode_char(c, Order.Backward)
        c = self._scrambler_1.encode_char(c, Order.Backward)
        c = self._plug_board.encode_char(c, Order.Backward)
        return c

    def decode(self, value):
        return self.encode(value)
