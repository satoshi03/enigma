from enigma import Enigma, EnigmaConfig


def main():
    config = EnigmaConfig.new_from_yaml('examples/config.yaml')
    enigma = Enigma(config)

    enc = enigma.encode('HELLO WORLD')

    enigma = Enigma(config)
    dec = enigma.decode(enc)

    print(enc)
    print(dec)


if __name__ == "__main__":
    main()
