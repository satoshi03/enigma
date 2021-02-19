# Enigma

A simple implemention of Enigma (a cipher device used in the early- to mid-20th century) in Python.

This program currently supports UPPERCASE ALPHABETS like `HELLO WORLD`.


## Getting Started

Clone repository and set PYTHONPATH to project dir.

```
$ git clone git@github.com:satoshi03/enigma.git
$ cd enigma
$ export PYTHONPATH=`pwd`
```

Install dependencies.

```
$ pip install -r requirements.txt
```

Run example script.

```
$ python examples/run.py 'HELLO WORLD'
```

Then, output result in command line.

```
PGMMT FTUMA
HELLO WORLD
```

This example script configures Enigma setting randomly everytime.
Therefore, encoded strings are different everytime.

## Run with config

If you want to use specifc Enigma setting, you can refer to following example script.

```
$ python examples/run_with_config.py 'HELLO WORLD'
```

This example script outputs same result as long as a config is same.

```
ZTPCE NBHVB
```

Decrypt string using the result.

```
$ python examples/run_with_config.py 'ZTPCE NBHVB'
```

Then, you can get decrypted string.

```
HELLO WORLD
```


## License

MIT License
