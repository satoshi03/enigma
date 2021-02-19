class Encoder():
    def encode_char(self, char, order):
        return char

    def _to_index(self, char):
        return ord(char) - ord('A')

    def _to_char(self, index):
        return chr(index + ord('A'))
