import copy
import random

class Encoder():
    def encode_char(self, char, order):
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
        s = ''
        for c in value:
            if c == ' ':
                s += ' '
            else:
                s += self.encode_char(c)
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


class RotateRule():
    def __init__(self, n=0):
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
        if order == Order.Backward:
            exchange_map = self._get_reverse_exchange_map()
        r = exchange_map.get(char)
        if order == Order.Backward:
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


class Reflector(Encoder):
    def __init__(self):
        self._exchange_list = [i for i in range(25, -1, -1)]

    def encode_char(self, char, order):
        index = self._to_index(char)
        encoded_index = self._exchange_list[index]
        return self._to_char(encoded_index)
