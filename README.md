# Enigma

A simple implemention of Enigma (a cipher device used in the early- to mid-20th century) in Python.

## How to run

```python
from enigma import Enigma, EnigmaConfig

# Generate config with random parameters
config = EnigmaConfig.random()

# Init enigma
enigma = Enigma(config)
# Encrypt code
enc = enigma.encode('HELLO WORLD')
print(enc)

# Init enigma
enigma = Enigma(config)
# Decrypt code (Actuall, same imple as encode)
dec = enigma.decode(enc)
print(dec)
```

Then, output result in command line.

```
PGMMT FTUMA
HELLO WORLD
```


## License

MIT License
