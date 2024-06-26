# MathPy

For information about the language itself,
check out the [documentation](#https://github.com/Bard-Gaming/MathPy/tree/main/Documentation).

## About
MathPy is a Python library that acts as a completely new
programming language.

The goal of this project is to experiment with strings as 
numbers in a high enough base to allow for a multitude of
characters, and to see if this could be a viable alternative
to the classical way of implementing character strings.

For instance, in hexadecimal, the string "baba" would
have a numerical value of 47802.

## Install MathPy
```commandline
pip install mathpy-string
```

## Run files in MathPy
### The Python way
If you wish to run your MathPy files through a Python program,
you can do so by importing the ``run_file()`` function from
the mathpy library, as follows:

```python
from mathpy import run_file

with open("[filepath]", 'rt', encoding='utf-8') as file:
    run_file(file)
```

### The command line way
If you wish to run your MathPy files through the command line,
you can do it as follows:

```commandline
python -m mathpy-string run [filepath]
```

or, if you wish to access the shell:

```commandline
python -m mathpy-string shell
```

or simply:

```commandline
python -m mathpy-string
```
