from .common import Order
from .base import Encoder


class RotateRule():
    def __init__(self, n=4):
        self._n = n

    def is_rotate(self, encode_num):
        return True


class Scrambler1RotateRule(RotateRule):
    def is_rotate(self, encode_num):
        return True


class Scrambler2RotateRule(RotateRule):
    def is_rotate(self, encode_num):
        return encode_num % self._n == 0


class Scrambler3RotateRule(RotateRule):
    def is_rotate(self, encode_num):
        return encode_num % pow(self._n, 2) == 0


class Scrambler(Encoder):
    def __init__(self, rotate_rule, counter, exchange_map):
        self._rotate_rule = rotate_rule
        self._counter = counter
        self._exchange_map = exchange_map
        self._rotate_num = 0
        self._encode_num = 0
        self.rotate(self._counter)

    def _get_reverse_exchange_map(self):
        return {v: k for k, v in self._exchange_map.items()}

    def encode_char(self, char, order):
        exchange_map = self._exchange_map
        if order == Order.BACKWARD:
            exchange_map = self._get_reverse_exchange_map()
        r = exchange_map.get(char)
        if order == Order.BACKWARD:
            self._encode_num += 1
            if self.is_rotate():
                self.rotate(1)
        return r

    def is_rotate(self):
        return self._rotate_rule.is_rotate(self._encode_num)

    def rotate(self, num):
        for i in range(0, num):
            self._exchange_map = {
                k: self._exchange_map[chr(ord(k)-1) if ord(k) > ord('A') else 'Z']
                for k, v in self._exchange_map.items()}
            self._rotate_num += 1
