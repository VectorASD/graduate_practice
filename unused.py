###~~~### match-case-test

""" Два серьёзных нововведения:
1.) Теперь QPython 3L не посылает код после разделителя "###~~~###" + пробел, что позволяет запускать этот скрипт с его 3.6.6 грамматикой, и любой грамматикой после первого разделителя
2.) Добавил в грамматику lib2to3 (используется, как основной парсер моего компилятора) конструкцию match-case
"""

# тяжело было из нового PEG (python >=3.10) переписать в старый PEG (python <=3.9), поскольку пришлось серьёзно изучить сразу две мета-грамматики
# пока в case поддерживаются только числа со знаком и без (signed_number), строки (STRING) и wildcard '_' (конфликтует с NAME, по этому там NAME с проверкой на '_')
# ещё, добавлена поддержка or-паттерна, чтобы в одном case было несколько (NUMBER, либо '_')

print("~" * 77)
for i in range(12):
  match i - 1:
    case 1: print("1")
    case 4 | 5: print("4|5")
    case _: print("default:", i - 1)
    case -1 | -2:
      print("signed_number:", i - 1)
    case 9: print("great! (9)")
    case 20: pass # справоцирует sparse вместо packed
# все 4 источника SyntaxError отрабатывают на ура:
  # case _: pass # repeat wildcard
  # case 5: pass # repeat number: 5
  # case 7 | _: pass # repeat wildcard
  # case 3 | 4: pass # repeat number: 4
print("~" * 77)

###~~~### optimizer-check

"""
def glob_func():
  global abc
  def abc(): return 25

abc = None
glob_func()
print(abc())

from double import DOUBLE
from java.lang.Math import Math
log = Math._mw_log(DOUBLE)
LOG_2 = log(2)
print(LOG_2)
"""

def check():
  for i in a: pass # NameError по прежнему работает
  a = 10
  return a

print(range(1, 25, -18)) # range-int
print(range(0x7fffffff)) # range-int
print(range(0x80000000)) # range
check()
