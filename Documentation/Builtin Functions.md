# Builtin Functions

## Logging values

### log()
The ``log()`` function prints the argument values into the console.
Multiple arguments are separated by a space. The function
doesn't mutate values in any way, and doesn't return anything.

**Parameters:** ``*any``


**Return value:** ``None``

**Example:**
```js
var a = [2, 3, "hello",];

log(a);  # prints "[2, 3, hello]" to the console
log("hello", 3);  # prints "hello 3" to the console
```


## Functions involving Randomness

### random()
The ``random()`` function is used to get a random value
between 0 (inclusive) and 1 (exclusive).

**Parameters:** [No parameters]

**Return value:** ``float`` in the interval of [0; 1[

Example:
```js
var rand = random();

log(rand);  # prints random value between 0 and 1
log(3 + 5 * random());  # prints random value between 3 and 5
```

## Converter Functions

### int()
The ``int()`` function takes in a single argument and turns
the value into an integer. If a type that doesn't have
an integer representation is used as argument, an error
is raised.

**Parameters:** ``any``

**Return value:** ``int``