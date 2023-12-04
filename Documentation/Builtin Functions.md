# Builtin Functions

## Logging values

### log()
The ``log()`` function prints the argument values into the console.
Multiple arguments are separated by a space. The function
doesn't mutate values in any way, and doesn't return anything.

- **Parameters:** ``*any``
- **Return value:** ``None``

**Example:**
```js
var a = [2, 3, "hello",];

log(a);  # prints "[2, 3, hello]" to the console
log("hello", 3);  # prints "hello 3" to the console
```
___

## Functions involving Randomness

### random()
The ``random()`` function is used to get a random value
between 0 (inclusive) and 1 (exclusive).

- **Parameters:** `` ``
- **Return value:** ``float`` in the interval of [0; 1[

Example:
```js
var rand = random();

log(rand);  # prints random value between 0 and 1
log(3 + 5 * random());  # prints random value between 3 and 5
```
___

## Converter Functions

### str()
The ``str()`` function takes in a single argument and turns
its value into a string representation of the value.
If a type that doesn't have a string representation is used
as an argument, an error is raised.

- **Parameters:** ``any``
- **Return value:** ``str``

```js
var number = 123.29;

log(number * 2);  # prints 246.58 (float)
log(str(number));  # prints "123.29" (string)
log(str(number) * 2);  # prints "aJLNßLY" (string)
```
___

### int()
The ``int()`` function takes in a single argument and turns
its value into an integer.
If a type that doesn't have an integer representation is used
as an argument, an error is raised.

- **Parameters:** ``any``
- **Return value:** ``int``

Example:
```js
var number_text = "129";

log(number_text + 1);  # prints "12(" (string)
log(int(number_text));  # prints 129 (integer)
log(int(number_text) + 1);  # prints 130 (integer)
```
___

### bool()
The ``bool()`` function takes in a single argument and turns
its value into a boolean representation of the value.
If a type that doesn't have a boolean representation is used
as an argument, an error is raised.

- **Parameters:** ``any``
- **Return value:** ``bool``

Example:
```js
var value = 52;

log(value);  # prints 52
log(bool(value));  # prints true
```
___

## Generative Functions

### range()
The ``range()`` function takes up to 3 arguments that specify an interval and
returns a list of all natural numbers in the specified interval.
If a single argument is used, it will be considered as the "stop" parameter.
If 2 arguments are used, they will be considered as
the "start", and "stop" parameters respectively.
If 3 arguments are used, they will be considered as the "start", "stop",
and "step" parameters.

- **Parameters:**
  - ``int (stop)`` or
  - ``int (start)``, ``int (stop)`` or
  - ``int (start)``, ``int (stop)``, ``int (step)``
- **Return value:** ``list``

Example:
```js
var interval = range(5);

log(interval);  # prints [0, 1, 2, 3, 4] (list)
log(interval.reversed());  # prints [4, 3, 2, 1, 0] (list)
log(range(4, -1, -1));  # prints [4, 3, 2, 1, 0] (list)
```