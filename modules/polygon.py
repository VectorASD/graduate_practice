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
