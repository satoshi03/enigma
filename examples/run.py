import sys

from enigma import Enigma, EnigmaConfig


def main():
    args = sys.argv
    if len(args) <= 1:
        print("ERROR. Please input encode/decode string.")
        print("e.g. {} 'HELLO WORLD'".format(__file__))
        return

    config = EnigmaConfig.random()
    enigma = Enigma(config)

    enc = enigma.encode(args[1])

    enigma = Enigma(config)
    dec = enigma.decode(enc)

    print(enc)
    print(dec)


if __name__ == "__main__":
    main()
