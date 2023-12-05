# Builtin Types


## Numbers
#### Common Attributes:

##### ``.numerator``:
The ``.numerator`` attribute is defined as being the numerator
of a ratio equal to the given number, such that the numerator
and the denominator of the ratio are the smallest
combination of integers possible.

- **Value:** ``int``

Example:
```js
var test_number = 0.25;

log(test_number);  # prints 0.25 (float)
log(test_number.numerator);  # prints 1 (int), since 1/4 = 0.25
```

##### ``.denominator``:
The ``.denominator`` attribute is defined as being the
denominator of a ration equal to the given number, such that
the numerator and the denominator of the ratio are the small
combination of integers possible. Note: due to the nature of
integers and strings, their denominators are always equal to 1.

- **Value:** ``int``

Example:
```js
var test_number = 0.25;

log(test_number);  # prints 0.25 (float)
log(test_number.denominator);  # prints 4 (int), since 1/4 = 0.25
```

#### Common Methods:

##### ``.as_integer_ratio()``:
The ``.as_integer_ratio()`` method returns a list containing
the numerator (index 0) and denominator (index 1) as integers.
The numerator and denominator values are the same as the
number's [numerator](#numerator) and [denominator](#denominator)
values.

- **Parameters:** `` ``
- **Return value:** ``list[int, int]``

Example:
```js
var test_number = 0.25;

log(test_number);  # prints 0.25 (float)
log(test_number.as_integer_ratio());  # prints [1, 4] (list)
```

___
### Integers
Integers are whole numbers that aren't represented by a point
("."). They have the lowest priority when it comes to operations
between numbers, meaning that any operation involving an integer
and any other number type.

#### Attributes:

#### Methods:

___
### Strings
In MathPy, strings are computed as positive integers in a base that includes most
commonly used characters. This means that all mathematical operations that can be
applied to integers also work on strings.


#### Attributes:

##### ``.value``:
The ``.value`` attribute is defined as being the integer value of the string.
Considering the fact that strings in MathPy are represented by integers of a high
enough base, this attribute allows you to access that value.

- **Value:** ``int``

Example:
```js
var text = "hi";

log(text);  # prints 'hi'
log(text.value);  # prints 865 (as of MathPy 1.0; subject to change)
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

##### ``.to_int()``:
The ``.to_int()`` method returns the same value as the
[``.value``](#value) attribute and exists purely for ease of use.

- **Parameters:** `` ``
- **Return value:** ``int``

Example:
```js
var text = "hi";

log(text);  # prints 'hi'
log(text.value);  # prints 865 (as of MathPy 1.0; subject to change)
```

##### ``.reversed()``:
The ``.reversed()`` method takes no arguments and returns a new
string, equivalent to the original string but with its characters
inverted.

- **Parameters:** `` ``
- **Return value:** ``str``

Example:
```js
var text = "hello";

log(text);  # prints 'hello'
log(text.reversed());  # prints 'olleh'
```

___
### Floating-point Numbers (Floats)
Floating-point numbers (floats for short) can be used to
represent any real number. They are represented by an
integer part, separated by a point (or dot, "."), followed by
a fractional part (can be 0).

#### Attributes:

##### ``.integer_part``:
The integer part of a float is the integer you get when you leave
out anything after the decimal point. It is equal to taking the
floor of a positive float, and the ceiling of a negative float.

- **Value:** ``int``

Example:
```js
var test_number = -52.68;

log(test_number);  # prints -52.68 (float)
log(test_number.integer_part);  # prints -52 (int)
```

##### ``.fractional_part``:
The fractional part of a float is a floating point number
in the range of ]-1; 1[ that you get by subtracting the given
float by its integer part.

- **Value:** ``float``

Example:
```js
var test_number = -52.68;

log(test_number);  # prints -52.68 (float)
log(test_number.fractional_part);  # prints -0.68 (float)
```

#### Methods:

##### ``.round()``:
The ``.round()`` method rounds a number to its nearest integer.
The amount of rounding can be set with its argument.

- **Parameters:** ``int | str`` (needs to be greater than or equal to 0)
- **Return value:** ``int | float`` (int if argument is 0)

Example:
```js
var test_number = 52.687;

log(test_number);  # prints 52.687
log(test_number.round(0));  # prints 53 (int)
log(test_number.round(1));  # prints 52.7 (float)
```
 
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
Due to the very nature of strings, they are classified as being iterables as much
as they can be represented by numbers. As such, they inherit the common attributes
and methods from both all number derived types and iterable derived types.

For more info, check out the **[Strings](#strings)** section in [Numbers](#numbers).

___
## Miscellaneous
___

### Booleans

___
### Null

___
### Functions

___

