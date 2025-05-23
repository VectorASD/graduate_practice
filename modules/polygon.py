"""
var = 123
print(var) # начинаем с малого
print() # без аргументов
print((1, 2, 3, 127, 128, -1, -128, -129)) # tuple const

print(123 + 128, 123 - 128, 123 * 128, 128 / 2, 123 // 2, 1234 % 123, 123 ** 3)
# print(123 @ 128) с int'ами всё равно работать не будет, но с точки зрения генератора кода - всё ок
print(1234 & 127, 1234 ^ 128, 1234 | 128, 1234 << 3, 1234 >> 3)

a = 1234
print(+a, -a, ~a, not a, not 0)
print(1 < 2, 1 == 2, 1 > 2, 1 <= 2, 1 != 2, 1 >= 2)

print(type(1234) is int, type(1234) is tuple)
print(2 in (1, 2, 3), 127 in (1, 2, 3))

print("Пора добавить оставшиеся типы констант:\nстрока", b"bytes", None, True, False, 1.5)

ListZero = []
ListOne = [1]
List = [1, 2, 3]
List[0] = List[-1] * 5
print(ListZero, ListOne, List)
a, b, c = List # 15, 2, 3
Tuple = a, b, b, c, b, a, c
print(Tuple)

print(Tuple[2:-1])
List[1:2] = (4, 5, 6)
print(List) # 15, 4, 5, 6, 3
List[-2:-5:-1] = (7, 8, 9)
print(List) # 15, 9, 8, 7, 3

from java.lang.Math import Math
from double import DOUBLE
print(Math, DOUBLE)

sin = Math._mw_sin(DOUBLE)
cos = Math._mw_cos(DOUBLE)
pi = Math._f_PI
print(sin, cos, pi)
print(sin(pi * 1.5), cos(pi * 1.5))

for i in range(10):
  # print(i)
  if i in range(3, 5): print("•")
  else: print(i)
print("yeah!")

print([2 ** i for i in (3, 1, 2, 4)])

with BytesIO(): pass # без as
with BytesIO() as file:
  file.writeLong(123)
print(file.getvalue().hex())

for error in (KeyError, IndexError, TypeError, AttributeError):
  try:
    raise error("msg")
  except KeyError: print("KeyError")
  except IndexError as e: print("IndexError:", e)
  except TypeError: print("TypeError")
  except Exception as e: print("Exception:", e)

for i in range(3):
  try:
    if i == 0: raise KeyError
    try:
      if i == 1: raise KeyError
    except KeyError: print("outer")
    if i == 2: raise KeyError
  except KeyError: print("inner")
"""

dict1 = {}
dict2 = {1: "a"}
dict3 = {1: "a", 2: "b"}
print(dict1, dict2, dict3, {k : k ** 5 % 7 for k in range(1, 7)})

tuple1 = ()
tuple2 = (5,)
tuple3 = (1, 2, 4)
print(tuple1, tuple2, tuple3, tuple(i ** 5 % 7 for i in range(1, 7)))

set1 = set()
set2 = {5}
set3 = {1, 2, 4}
print(set1, set2, set3) # мой компилятор пока не поддерживает set_maker поверх dict_maker'а... {i ** 5 % 7 for i in range(1, 7)})

for item in (-1, 0, 1, None, True, False, b"", b"123"):
  print("    %r:" % item, item and "yes" or "no")

for a, b in ((1, 2), (3, 4)): print(a, b)

def simple():
  print("yeah!")
  return 123

def with_args(a, b, c):
  print("args:", a, b, c)

print(simple)
print("returned:", simple())
try: with_args(8, 5)
except TypeError as e: print(e)
try: with_args(8, 5, 3, 2)
except TypeError as e: print(e)
with_args(8, 5, 3)
