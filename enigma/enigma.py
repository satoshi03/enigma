import copy
import random

class Encoder():
    def encode(self, value, order):
        s = ''
        for c in value:
            if c == ' ':
                s += ' '
            else:
                s += self._encode_char(c, order)
        return s

    def _encode_char(self, char):
        return char

    def _to_index(self, char):
        return ord(char) - ord('A')

    def _to_char(self, index):
        return chr(index + ord('A'))


class EnigmaConfig():
    def __init__(self, plug_board_exchange_map,
                 scrambler_1_exchange_map, scrambler_1_counter_num,
                 scrambler_2_exchange_map, scrambler_2_counter_num,
                 scrambler_3_exchange_map, scrambler_3_counter_num):
        self._plug_board_exchange_map = plug_board_exchange_map
        self._scrambler_1_exchange_map = scrambler_1_exchange_map
        self._scrambler_2_exchange_map = scrambler_2_exchange_map
        self._scrambler_3_exchange_map = scrambler_3_exchange_map
        self._scrambler_1_counter_num = scrambler_1_counter_num
        self._scrambler_2_counter_num = scrambler_2_counter_num
        self._scrambler_3_counter_num = scrambler_3_counter_num

    @classmethod
    def random(cls):
        alphabet_list = [chr(i + ord('A'))for i in range(0, 26)]
        random_alphabet_list = copy.copy(alphabet_list)
        random.shuffle(random_alphabet_list)
        plug_board_exchange_map = {key: alphabet_list[random_alphabet_list.index(key)]
                                   for key in random_alphabet_list[:3]}
        plug_board_exchange_map.update({v: k for k, v in plug_board_exchange_map.items()})

        random.shuffle(random_alphabet_list)
        scrambler_1_exchange_map = {key: random_alphabet_list[alphabet_list.index(key)]
                                    for key in alphabet_list}
        scrambler_1_counter_num = random.randint(0, 25)

        random.shuffle(random_alphabet_list)
        scrambler_2_exchange_map = {key: random_alphabet_list[alphabet_list.index(key)]
                                    for key in alphabet_list}
        scrambler_2_counter_num = random.randint(0, 25)

        random.shuffle(random_alphabet_list)
        scrambler_3_exchange_map = {key: random_alphabet_list[alphabet_list.index(key)]
                                    for key in alphabet_list}
        scrambler_3_counter_num = random.randint(0, 25)

        return cls(plug_board_exchange_map,
                   scrambler_1_exchange_map, scrambler_1_counter_num,
                   scrambler_2_exchange_map, scrambler_2_counter_num,
                   scrambler_3_exchange_map, scrambler_3_counter_num)


class Order:
    Forward = 1
    Backward = -1


class Enigma(Encoder):

    def __init__(self, config):
        self._plug_board = PlugBoard(config._plug_board_exchange_map)
        self._scrambler_1 = Scrambler(Scrambler1RotateRule(),
                                      config._scrambler_1_counter_num,
                                      config._scrambler_1_exchange_map)
        self._scrambler_2 = Scrambler(Scrambler2RotateRule(4),
                                      config._scrambler_2_counter_num,
                                      config._scrambler_2_exchange_map)
        self._scrambler_3 = Scrambler(Scrambler3RotateRule(4),
                                      config._scrambler_3_counter_num,
                                      config._scrambler_3_exchange_map)
        self._reflector = Reflector()

    def encode(self, value):
        value = self._plug_board.encode(value, Order.Forward)
        value = self._scrambler_1.encode(value, Order.Forward)
        value = self._scrambler_2.encode(value, Order.Forward)
        value = self._scrambler_3.encode(value, Order.Forward)
        value = self._reflector.encode(value, Order.Forward)
        value = self._scrambler_3.encode(value, Order.Backward)
        value = self._scrambler_2.encode(value, Order.Backward)
        value = self._scrambler_1.encode(value, Order.Backward)
        value = self._plug_board.encode(value, Order.Backward)

        if self._scrambler_1.is_rotate():
            self._scrambler_1.rotate(1)
        if self._scrambler_2.is_rotate():
            self._scrambler_2.rotate(1)
        if self._scrambler_3.is_rotate():
            self._scrambler_3.rotate(1)

        return value

    def decode(self, value):
        return self.encode(value)


class PlugBoard(Encoder):
    def __init__(self, exchange_map):
        self._exchange_map = exchange_map

    def _get_reverse_exchange_map(self):
        return {v: k for k, v in self._exchange_map.items()}

    def _encode_char(self, char, order):
        exchange_map = self._exchange_map
        if order == Order.Backward:
            exchange_map = self._get_reverse_exchange_map()

        if char in exchange_map:
            return exchange_map.get(char)
        return char


class RotateRule():
    def __init__(self, n=0):
        self._n = n

    def is_rotate(self, rotate_num):
        return True


class Scrambler1RotateRule(RotateRule):
    def is_rotate(self, rotate_num):
        return True


class Scrambler2RotateRule(RotateRule):
    def is_rotate(self, rotate_num):
        return rotate_num % self._n == 0


class Scrambler3RotateRule(RotateRule):
    def is_rotate(self, rotate_num):
        return rotate_num % pow(self._n, 2) == 0


class Scrambler(Encoder):
    def __init__(self, rotate_rule, counter, exchange_map):
        self._rotate_rule = rotate_rule
        self._counter = counter
        self._exchange_map = exchange_map
        self.rotate(self._counter)
        self._rotate_num = 0
        return

    def _get_reverse_exchange_map(self):
        return {v: k for k, v in self._exchange_map.items()}

    def _encode_char(self, char, order):
        exchange_map = self._exchange_map
        if order == Order.Backward:
            exchange_map = self._get_reverse_exchange_map()
        r = exchange_map.get(char)
        self._rotate_num += 1
        return r

    def is_rotate(self):
        return self._rotate_rule.is_rotate(self._rotate_num)

    def rotate(self, num):
        for i in range(0, num):
            self._exchange_map = {
                k: self._exchange_map[chr(ord(k)-1) if ord(k) > ord('A') else 'Z']
                for k, v in self._exchange_map.items()}


class Reflector(Encoder):
    def __init__(self):
        self._exchange_list = [i for i in range(25, -1, -1)]

    def _encode_char(self, char, order):
        index = self._to_index(char)
        encoded_index = self._exchange_list[index]
        return self._to_char(encoded_index)
