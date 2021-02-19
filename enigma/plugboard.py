from .base import Encoder
from .common import Order


class PlugBoard(Encoder):
    def __init__(self, exchange_map):
        self._exchange_map = exchange_map

    def _get_reverse_exchange_map(self):
        return {v: k for k, v in self._exchange_map.items()}

    def encode_char(self, char, order):
        exchange_map = self._exchange_map
        if order == Order.Backward:
            exchange_map = self._get_reverse_exchange_map()

        if char in exchange_map:
            return exchange_map.get(char)
        return char
