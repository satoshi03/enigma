from enigma import Enigma, EnigmaConfig


def main():
    config = EnigmaConfig.random()
    enigma = Enigma(config)

    enc = enigma.encode('HELLO WORLD')

    enigma = Enigma(config)
    dec = enigma.decode(enc)

    print(enc)
    print(dec)


if __name__ == "__main__":
    main()
