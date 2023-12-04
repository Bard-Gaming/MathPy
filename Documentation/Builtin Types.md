# Builtin Types


## Numbers
#### Common Attributes:

#### Common Methods:

___
### Integers
Integers are represented by any number that isn't represented by a "." symbol.


___
### Strings
In MathPy, strings are computed as positive integers in a base that includes most
commonly used characters. This means that all mathematical operations that can be
applied to integers also work on strings.

___
#### Attributes:

##### ``.value``:
The ``.value`` attribute is defined as being the integer value of the string.
Considering the fact that strings in MathPy are represented by integers of a high
enough base, this attribute allows you to access that value.

- **Value:** ``int``

Example:
```js
var text = "Well hello there!";

log(text);  # prints 'Well hello there!'
log(text.value);  # prints 14479709841755490706022674961864534 (as of MathPy 1.0; subject to change)
```

##### ``.base_number``: 
The ``.base_number`` attribute is defined as being the base of the string's
aforementioned integer value. It is the same across a single version, but may vary
if more characters are added in future versions.

- **Value:** ``int``

Example:
```js
var text = "test";

log(text.base_number);  # prints 107 (as of MathPy 1.0; subject to change)
```

#### Methods:

``.to_int()``: Returns the integer value that makes the string. Functions the same as
the ``.value`` attribute.

``.reversed()``: Returns a new string that has its characters reversed from the original.
For instance, the string "hello" would turn into "olleh".

___
### Floating-point Numbers (Floats)

___
## Iterables

#### Common Attributes:
##### ``.length``:
The ``.length`` attribute returns an integer value that
represents the quantity of elements an iterable has.

- **Value:** ``int``

Example:
```js
var string = 'hello';
var list = [3, [1, 10], 2];

log(string.length);  # prints 5
log(list.length);  # prints 3
```

#### Common Methods:
##### ``.copy()``:
The ``.copy()`` method creates a perfect copy of the iterable.
This can be useful when you want to manipulate an iterable but
keep its original values intact.

- **Parameters:** `` ``
- **Return value:** ``iterable``

Example:
```js
var list_1 = [1, 2];
var list_2 = list_1.copy();
var list_3 = list_2;

log(list_1, list_2, list_3);  # prints [1, 2] [1, 2] [1, 2];
list_1.append(3);
log(list_1, list_2, list_3);  # prints [1, 2, 3] [1, 2] [1, 2]
list_2.append(4);  # since list_2 IS list_3, it changes both variables
log(list_1, list_2, list_3);  # prints [1, 2, 3] [1, 2, 4] [1, 2, 4]
```
___
### Lists
Lists are mutable index-based objects that can contain an assortment
of values, including other lists.

#### Attributes:

#### Methods:
##### ``.append()``:
The ``.append()`` method appends (i.e. inserts at the
last index) a value to the current list.

- **Parameters:** ``any``
- **Return value:** ``Null``

Example:
```js
var list = [1, 2];

log(list);  # prints [1, 2]
list.append(["hello", 3]);
log(list);  # prints [1, 2, ["hello", 3]]
```

##### ``.extend()``:
The ``.extend()`` method inserts every value from the given
argument into the list. No change is made to the argument's
value or order.

- **Parameters:** ``iterable``
- **Return value:** ``Null``

Example:
```js
var list_1 = [1, "test"];
var list_2 = [[2], 1];

log(list_1);  # prints [1, "test"]
log(list_2);  # prints [[2], 1]
list_1.extend(list_2);
log(list_1);  # prints [1, "test", [2], 1]
```

#### ``.reversed()``:
The ``.reversed()`` method returns a reversed version
of the list. The reversed version keeps the values in
the list unchanged, but inverts its order.

- **Parameters:** `` ``
- **Return value:** ``list`` (reversed)

Example:
```js
var list = [1, 2, ["bob", 2]];

log(list);  # prints [1, 2, ["bob", 2]]
log(list.reversed());  # prints [["bob", 2], 2, 1]
```

___

### Strings


## Miscellaneous
___

### Booleans

___
### Null

___
### Functions

___

