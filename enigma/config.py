import copy
import random

import yaml


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

    def to_dict(self):
        return {
            'plug_board': {
                'exchange_map': self._plug_board_exchange_map,
            },
            'scrambler_1': {
                'exchange_map': self._scrambler_1_exchange_map,
                'counter_num': self._scrambler_1_counter_num,
            },
            'scrambler_2': {
                'exchange_map': self._scrambler_2_exchange_map,
                'counter_num': self._scrambler_2_counter_num,
            },
            'scrambler_3': {
                'exchange_map': self._scrambler_3_exchange_map,
                'counter_num': self._scrambler_3_counter_num,
            },
        }

    def dump(self, path):
        with open(path, 'w') as f:
            yaml.dump(self.to_dict(), f, encoding='utf-8')

    def __str__(self):
        return str(self.to_dict())

    @classmethod
    def new_from_dict(cls, dic):
        return cls(
            dic['plug_board']['exchange_map'],
            dic['scrambler_1']['exchange_map'], dic['scrambler_1']['counter_num'],
            dic['scrambler_2']['exchange_map'], dic['scrambler_2']['counter_num'],
            dic['scrambler_3']['exchange_map'], dic['scrambler_3']['counter_num']
        )

    @classmethod
    def new_from_yaml(cls, path):
        with open(path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            return cls.new_from_dict(data)

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
