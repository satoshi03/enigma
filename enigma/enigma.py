import re

from .base import Encoder
from .scrambler import Scrambler, Scrambler1RotateRule, Scrambler2RotateRule, Scrambler3RotateRule
from .plugboard import PlugBoard
from .reflector import Reflector
from .common import Order


class Enigma(Encoder):

    def __init__(self, config):
        self._plug_board = PlugBoard(config.plug_board_exchange_map)
        self._scrambler_1 = Scrambler(Scrambler1RotateRule(),
                                      config.scrambler_1_counter_num,
                                      config.scrambler_1_exchange_map)
        self._scrambler_2 = Scrambler(Scrambler2RotateRule(),
                                      config.scrambler_2_counter_num,
                                      config.scrambler_2_exchange_map)
        self._scrambler_3 = Scrambler(Scrambler3RotateRule(),
                                      config.scrambler_3_counter_num,
                                      config.scrambler_3_exchange_map)
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
        c = self._plug_board.encode_char(c, Order.FORWARD)
        c = self._scrambler_1.encode_char(c, Order.FORWARD)
        c = self._scrambler_2.encode_char(c, Order.FORWARD)
        c = self._scrambler_3.encode_char(c, Order.FORWARD)
        c = self._reflector.encode_char(c, Order.FORWARD)
        c = self._scrambler_3.encode_char(c, Order.BACKWARD)
        c = self._scrambler_2.encode_char(c, Order.BACKWARD)
        c = self._scrambler_1.encode_char(c, Order.BACKWARD)
        c = self._plug_board.encode_char(c, Order.BACKWARD)
        return c

    def decode(self, value):
        return self.encode(value)
