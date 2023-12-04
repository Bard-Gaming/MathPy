# Builtin Types


## Numbers
Common attributes shared amongst all number types:



### Integers
Integers are represented by any number that isn't represented by a "." symbol.

```js

```

### Strings
In MathPy, strings are computed as positive integers in a base that includes most
commonly used characters. This means that all mathematical operations that can be
applied to integers also work on strings.

#### Attributes:

``.value``: Returns the positive integer that represents the string.
Note that this is not the same thing as using the ``int()`` function, as
the latter tries to convert the characters of a string into a number, whereas
the ``.value`` attribute simply returns the value that makes the string.

``.base_number``: Returns an integer of the base used for the string. The value of the
base number is static across a single version, but can change with a newer version of
MathPy (last updated base number: ``107``).

``.length``: Returns an integer representing the length
(i.e. the quantity of characters) the string contains.

#### Methods:

``.to_int()``: Returns the integer value that makes the string. Functions the same as
the ``.value`` attribute.

``.reversed()``: Returns a new string that has its characters reversed from the original.
For instance, the string "hello" would turn into "olleh".

### Floating-point Numbers (Floats)


## Iterables

#### Common Attributes:
``.length``: Returns an integer representing
the quantity of elements contained in the iterable.

#### Common Methods:

### Lists
Lists are mutable index-based objects that can contain any value, including other lists.

#### Attributes:
``.length``: Returns a positive or null integer that represents 
the quantity of elements inside the list.

#### Methods:
``.append(arg)``:

``.extend(arg)``:

``.reversed()``:

### Strings


## Miscellaneous

### Booleans

### Null

### Functions

