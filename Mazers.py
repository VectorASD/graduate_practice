if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  load_codes("Mazers.py")
  n = 0
  main(("mazers", "time-tests")[n], False, ("/sdcard/my_code3.asd", "/sdcard/my_debug3.asd"))
  exit()

###~~~### time-tests

def time_test():
  def report():
    clear()
    print("min: %.6f %.6f" % (td_min, td2_min))
    print("%.6f %.6f" % res)

  data = tuple((0, "5") for i in range(100000))
  td_sum = td2_sum = count = 0
  td_min = td2_min = float("inf")
  while True:
    check = (lambda value: None,)
    T = time()
    for TypeV, value in data:
      check[TypeV](value)
    td = time() - T

    check = (None,)
    T = time()
    for TypeV, value in data:
      func = check[TypeV]
      if func is not None: func(value)
    td2 = time() - T

    res = td, td2
    # Замечен факт: чем больше операций после замеряемых по времени участков,
    # тем выше трудоёмкость самих участков. Может это и не логично,
    # но, предположительно, нагрузка на Java-мусоросборщик влияет на ВЕСЬ код

    td_min  = min(td_min, td)
    td2_min = min(td2_min, td2)

    # print(td, td2) # 0.8 vs 0.04 (вызов пустой функции в 20 раз дороже, чем проверка на None)

    """
После ОЧЕНЬ серьёзной оптимизационной работы моего py-движка:
  редизайн виртуального процессора с упором на уменьшения числа dalvik-операций;
  регистры и scope-области выделяются теперь заранее;
  в обработчике аргументов, регистры только очищаются через Arrays.fill(regs, null);
  обработчик аргументов написан более осознанно и теперь менее требовательный;
  в 1000 раз теперь понятнее, как В БУДУЩЕМ реализовать yield и gen_expr-механику
    """
    # print(*res)    # 0.049 vs 0.0418 (x17 к скорости вызова пустой функции!!!)

    """
После оптимизации лишних переходов регистров:
  к сожалению, это ещё не идеальный вариант, т.к. для идеального,
  пришлось бы строить полноценный граф управления программы;
  теперь все константы выгружаются в регистры в самом начале каждой функции;
  все регистры и локальные переменные объеденены в регистры
    """
    # print(*res)    # 0.0405 vs 0.0267 (x1.5 к скорости обычного выполнения)

    """
После оптимизации самого исполнительного ядра:
  сильно поменялся дизайн исполнителя: уменьшено количество dalvik-операций по максимуму;
  range теперь имеет ускоренную версию range-int за счёт int вместо BigInteger
    """
    # print(*res)    # 0.0372 vs 0.0289 (странненько, они приблизились)

    """
Оптимизация концепции builtins, globals, consts и locals:
  построена обобщёная схема всех команд виртуального процессора;
  за счёт этой схемы, исправлены некоторые ошибки оптимизатора;
  вместо отдельного globals, теперь, вместо него, locals модуля;
  bultins и globals теперь объеденены;
  константы загружаются в регистры теперь на этапе объявления функции, а не прямо внутри тела функции
    """

    # report()    # 0.0326 vs 0.0277 (функции работают ещё чуть-быстрее)

    """
Просто пометил в AndroidManifest приложение, как "игра":
  автоматически включается Hyperboost realme для ускорения
    """

    # report()    # 0.02821 vs 0.02129 (почти обогнал функции оригинального питона)

    # print(100000 / td, 100000 / td2)

# замеры на QPython3 (это же устройство):
#    0.02744 vs 0.0112
# я довольно-таки близок к тому, чтобы обогнать его!
# при том QPython3 на .so-библиотеке, т.е. это тот же CPython, а у меня - чистая Java

def time_test2():
  while True:
    T = time()
    for i in range(1000000): pass
    print(1000000 / (time() - T))

Thread(time_test).start()

###~~~### mazers

import common # adler32, sha1, dex, context





def DalvikAssembler(codes_b, Pool):
  # Самый настоящий ассемблер DVM-байткода

  # Самая "тяжёлая" функция! К ней особое внимание по оптимизации
  # Начиная с 1.10 версии Python, вводится match-case.
  # Позже (уже), добавлю это в грамматический файл, а также, реализую в своём компиляторе, с механикой от Java, чтобы заменить все dispatch-объекты на них

  def main(code_data):
    w_byte = codes_b.w_byte
    write  = codes_b.write
    write2 = codes_b.write2
    write4 = codes_b.write4
    write8 = codes_b.write8
    tell   = codes_b.tell
    seek   = codes_b.seek

    str_d    = Pool.str_d
    type_d   = Pool.type_d
    proto_d  = Pool.proto_d
    field_d  = Pool.field_d
    method_d = Pool.method_d

    # codes_b и Pool дальше явно не используются

    PackedSwitch = {}
    SparseSwitch = {}

    seek(4, 1) # пока неизвестен размер кода
    begin = tell()

    if type(code_data) is dict:
      code_data = code_data.values()

    for data in code_data:
      line = tell() - begin
      assert line & 1 == 0
      line >>= 1

      code = data[0]

      # Добавил поддержку токена '..' со всеми исправлениями конфликтов с вещественными числами
      # т.е., ещё и токенайзер пришлось изучать, хотя, казалось, он должен быть гораздо сложнее (вся основная работа в одной регулярке)
      # Раньше я не представлял, что такое SyntaxError: bad input... Теперь очень даже представляю (ошибка токенайзера: не удалось распознать ТИП токена)
      # Правильнее сказать, bad input - это тип токена, который недопустим после типа предущего токена (например, 2 числа подряд - нельзя)

      match code:
        case 10..13 | 15..17 | 29..30 | 39: # byte
          write(bytes(data)) # code, reg
        case 28 | 31 | 34: # byte_type
          w_byte(code)
          w_byte(data[1]) # reg
          write2(type_d[data[2]]) # type
        case 45..49 | 68..81 | 144..175: # pair3
          # assert len(data) == 4
          write(bytes(data)) # code, a, b, c
        case 33 | 123..143 | 176..207: # pair
          w_byte(code)
          w_byte(data[2] << 4 | data[1]) # pair
        case 32 | 35: # pair_type
          pair = data[1]
          w_byte(code)
          w_byte(pair[1] << 4 | pair[0])
          write2(type_d[data[2]]) # type
        # case 62..67 | 115 | 121..122 | 227..249: # unused
        case _:
          raise Exception("  ERROR: Bytecode %s unused!" % data)



        case 0: # nop
          Type = data[1]
          w_byte(0)
          w_byte(Type)
          match Type:
            case 0: continue # nop
            case 1: # packed-switch
              try: off = PackedSwitch[line]
              except KeyError:
                raise Exception("nop_packed-switch-data_error: " + str(PackedSwitch))
              arr = data[3]
              write2(len(arr))
              write4(data[2])
              for i in arr: write4(i - off)

            case 2: # sparse-switch
              try: off = SparseSwitch[line]
              except KeyError:
                raise Exception("nop_sparse-switch-data_error: " + str(SparseSwitch))
              arr = data[2]
              write2(len(arr))
              keys, values = zip(*arr)
              for i in keys: write4(i)
              for i in values: write4(i - off)

            case 3: # array
              arr = data[3]
              # n_size = max(1 if i < 256 else 2 if i < 0x10000 else 4 if i < 0x100000000 else 8 for i in arr)
              # sizeE = data[2]
              # if n_size != sizeE:
              #   print("• new size array elements:", sizeE, "->", n_size)
              #   print("  arr:", arr)
              #   print("      ", n_size)
              n_size = data[2]

              write2(n_size)
              write4(len(arr))

              match n_size:
                case 1:
                  for i in arr: w_byte(i)
                  if len(arr) & 1 == 1: w_byte(0) # pad
                case 2:
                  for i in arr: write2(i)
                case 4:
                  for i in arr: write4(i)
                case 8:
                  for i in arr: write8(i)
                case _:
                  raise Exception("nop_len_array-data_error: %s" % n_size)

            case _:
              raise Exception("nop_type_error: %s" % Type)

        case 1..9: # move
          a = data[1]
          b = data[2]
          T1, T2 = divmod(code - 1, 3)
          if a < 16 and b < 16: T2 = 0
          elif a < 256: T2 = 1
          else: T2 = 2

          n_code = T2 + T1 * 3 + 1
          if n_code != code: print("!!!", code, "->", n_code, data)

          w_byte(n_code)
          if T2 == 0:
            w_byte(b << 4 | a)
          elif T2 == 1:
            w_byte(a)
            write2(b)
          else:
            write2(a)
            write2(b)
            w_byte(0) # pad

        case 14: # return-void
          write(b"\x0e\0")

        case 18..21: # int_const
          a = data[1]
          b = data[2]
          if a in range(16) and b in range(-8, 8): n_code = 18
          elif b in range(-0x8000, 0x8000): n_code = 19
          elif b & 0xffff == 0: n_code = 21
          else: n_code = 20

          if n_code != code: print("!!!", code, "->", n_code, data)

          w_byte(n_code)
          if n_code == 18: w_byte(b << 4 | a)
          else:
            w_byte(a)
            if n_code == 19: write2(b)
            elif n_code == 20: write4(b)
            else: write2(b >> 16)

        case 22..23: # wide_const
          a = data[1]
          b = data[2]
          n_code = 22 if b in range(-0x8000, 0x8000) else 23

          if n_code != code: print("!!!", code, "->", n_code, data)

          w_byte(n_code)
          w_byte(a)
          if n_code == 22: write2(b)
          else: write4(b)

        case 24..25: # long_const
          reg = data[1]
          num = data[2]
          if type(num) is str: num = float(num)

          buff = BytesIO()
          buff.pack("<q", num)
          num = buff.getvalue()
          n_code = 25 if num[:6] == b"\0\0\0\0\0\0" else 24

          if n_code != code: print("!!!", code, "->", n_code, data)

          w_byte(code)
          w_byte(reg)
          write(num if n_code == 24 else num[6:])

        case 26..27: # str_const
          _str = data[2]
          idx = str_d[_str]
          n_code = 26 if idx < 0x10000 else 27

          if n_code != code: print("!!!", code, "->", n_code, data)

          w_byte(n_code)
          w_byte(data[1]) # reg
          if n_code == 26: write2(idx)
          else: write4(idx)

        case 36: # filled_new_array
          regs = data[2]
          L = len(regs)
          w_byte(36)
          w_byte(L << 4 | regs[4] if L > 4 else L << 4)
          write2(type_d[data[1]])
          w_byte(regs[1] << 4 | regs[0] if L > 1 else regs[0] if L else 0)
          w_byte(regs[3] << 4 | regs[2] if L > 3 else regs[2] if L > 2 else 0)

        case 37: # filled_new_array_range
          start = data[1]
          w_byte(37)
          w_byte(data[2] - start + 1) # count
          write2(type_d[data[3]])
          write2(start)

        case 38: # fill_array_data
          w_byte(38)
          w_byte(data[1]) # reg
          write4(data[2] - line) # off

        case 40..42: # goto
          a = data[1] - line # off
          n_code = 40 if a in range(-128, 128) else 41 if a in range(-0x8000, 0x8000) else 42

          if n_code != code: print("!!!", code, "->", n_code, data)

          w_byte(n_code)
          if n_code == 40: w_byte(a)
          else:
            w_byte(0) # pad
            if n_code == 41: write2(a)
            else: write4(a)

        case 43..44: # switch
          off = data[2]
          (PackedSwitch if code == 43 else SparseSwitch)[off] = line
          w_byte(code)
          w_byte(data[1]) # reg
          write4(off - line)

        case 50..55: # pair_goto
          pair = data[1]
          w_byte(code)
          w_byte(pair[1] << 4 | pair[0])
          write2(data[2] - line) # off

        case 56..61: # byte_goto
          w_byte(code)
          w_byte(data[1]) # reg
          write2(data[2] - line) # off

        case 82..95: # iget_iput
          pair = data[1]
          w_byte(code)
          w_byte(pair[1] << 4 | pair[0])
          write2(field_d[data[2]]) # field

        case 96..109: # sget_sput
          w_byte(code)
          w_byte(data[1]) # reg
          write2(field_d[data[2]]) # data

        case 110..114: # invoke
          regs = data[2]
          L = len(regs)
          w_byte(code)
          w_byte(L << 4 | regs[4] if L > 4 else L << 4)
          write2(method_d[data[1]]) # method
          w_byte(regs[1] << 4 | regs[0] if L > 1 else regs[0] if L else 0)
          w_byte(regs[3] << 4 | regs[2] if L > 3 else regs[2] if L > 2 else 0)

        case 116..120: # invoke_range
          start = data[1]
          w_byte(code)
          w_byte(data[2] - start + 1) # count
          write2(method_d[data[3]]) # method
          write2(start)

        case 208..226: # math
          pair = data[1]
          c = data[2]
          T = code - 208 if code < 216 else code - 216
          n_code = T + 216 if T > 7 or c in range(-128, 128) else T + 208

          if n_code != code: print("!!!", code, "->", n_code, data)

          w_byte(n_code)
          if n_code < 216:
            w_byte(pair[1] << 4 | pair[0])
            write2(c)
          else:
            w_byte(pair[0])
            w_byte(pair[1])
            w_byte(c)



        # 250-255 команды (экзотические) до сих пор неоттестированы,
        # да и не понадобятся они мне, т.к. я использую версию DEX с поддержкой от 4-ой версии андроида,
        # где использование этих команд приведёт к поломке ClassLoader

        case 250: # invoke_polymorphic
          _, (name, regs), idx = data
          L = len(regs)
          w_byte(250)
          w_byte(L << 4 | regs[4] if L > 4 else L << 4)
          write2(method_d[name])
          w_byte(regs[1] << 4 | regs[0] if L > 1 else regs[0] if L else 0)
          w_byte(regs[3] << 4 | regs[2] if L > 3 else regs[2] if L > 2 else 0)
          write2(proto_d[idx])

        case 251: # invoke_polymorphic_range
          _, start, end, idx, idx2 = data
          w_byte(251)
          w_byte(end - start + 1) # count
          write2(method_d[idx])
          write2(start)
          write2(proto_d[idx2])

        case 252: # invoke_custom
          _, name, regs = data
          L = len(regs)
          # regs += (0,) * (5 - L) долго, да и в целом - странно
          w_byte(252)
          w_byte(L << 4 | regs[4] if L > 4 else L << 4)
          write2(name) # call_site_id ???
          w_byte(regs[1] << 4 | regs[0] if L > 1 else regs[0] if L else 0)
          w_byte(regs[3] << 4 | regs[2] if L > 3 else regs[2] if L > 2 else 0)

        case 253: # invoke_custom_range
          _, start, end, name = data
          w_byte(253)
          w_byte(end - start + 1)
          write2(name) # call_site_id ???
          write2(start)

        case 254: # const_method_handle
          _, a, b = data
          w_byte(254)
          w_byte(a)
          write2(b)

        case 255: # const_method_type
          _, a, b = data
          w_byte(255)
          w_byte(a)
          write2(proto_d[b])

        #case _: # old
         # disp_table[code]()

    size = (tell() - begin) >> 1
    if size & 1: write2(0) # pad
    end = tell()

    seek(begin - 4)
    write4(size)

    seek(end) # важно!

  return main





class Mark:
  def __init__(self, pos):
    self.pos = pos
    self.raz = False
  def __repr__(self): return "Mark(%s)" % self.pos

Mark0 = Mark(0)

class Blockerson:
  file = None
  insts = []
  Map = [(0, 1, 0)]
  map_d = {0: (1, 0)}

  def __init__(self, data = None):
    data = BytesIO() if data is None else data
    self.marks = []
    self.arr = []
    self.hook = []

    self.w_byte = data.writeByte
    self.write2 = data.writeShort
    self.write4 = data.writeInt
    self.write8 = data.writeLong
    self.write  = data.write
    self.uleb128 = data.write_uleb128
    self.sleb128 = data.write_sleb128

    self.size  = data.size
    self.pack  = data.pack
    self.MUTF8 = data.write_MUTF8

    self.seek = data.seek
    self.tell = data.tell
    if type(data) is BytesIO: self.getvalue = data.getvalue

    self.arr_append = self.arr.append
    self.uleb128_h  = self.hook.append

    Blockerson.insts.append(self)

  def writeMark(self, mark):
    assert type(mark) is Mark
    if mark != Mark0:
      self.marks.append([self.tell(), mark])
    self.write(b"\0\0\0\0")

  # def write4orMark(self, mark):
  #   (self.write4 if type(mark) is int else self.writeMark)(mark)

  def pos(self):
    pos = Mark(self.tell())
    self.arr_append(pos)
    return pos

  def pos2(self):
    res = self.pos()
    self.uleb128_h((res,))
    return res

  def apply(self, pad, Type, conc = None):
    file = Blockerson.file

    file.write(b"\0" * (-file.tell() % pad))

    for num in self.hook:
      T = type(num)
      # print(num, T, T is Mark)
      if T is Mark:
        if not num.raz: raise Exception("Не все позиции обработаны, что были поданы в uleb128_h")
        num = num.pos
      elif T is tuple:
        num[0].pos += self.tell()
        continue
      self.uleb128(num)

    offset = file.tell()
    value = self.getvalue()
    file.write(value)

    size = len(value) // conc if conc else len(self.arr)
    self.Map.append((Type, size, offset))
    self.map_d[Type] = size, offset

    for mark in self.arr:
      mark.pos += offset
      mark.raz = True
    for mark in self.marks:
      mark[0] += offset

  def final():
    seek   = Blockerson.file.seek
    write4 = Blockerson.file.writeInt
    for inst in Blockerson.insts:
      for item in inst.marks:
        offset, mark = item
        #print(offset, mark.pos)
        seek(offset)
        write4(mark.pos)





def descExtractor(desc):
  types = []; app = types.append
  pos = desc.index("(") + 1
  lock = 0
  while True:
    value = desc[pos]
    if value == ")": return tuple(types)
    elif value == "L":
      posN = pos
      while desc[pos] != ";": pos += 1
      app(desc[posN : pos + 1])
    elif value in "BZCDFLSIJ": app(value)
    elif value == "[":
      PosN2 = pos
      while desc[pos + 1] == "[": pos += 1
      lock = 2
    else:
      raise Exception("descExtractorValueError: " + value)
    if lock == 1: types[-1] = desc[PosN2 : pos + 1]
    if lock > 0: lock -= 1
    pos += 1

# print(descExtractor("(ISIDCLjava/lang/Thread;F[[[[[Landroid/widget/Toast;C[[[DZB)V"))
# exit()



class Pooler:
  def __init__(self):
    # формирование Индекса:
    self.Strs, self.Types = set(), set()
    self.Protos, self.Fields, self.Methods = {}, {}, {}
    self.type_list_arr = []
    self.type_list_d = {}

    # ускорители операций:
    self.addStr   = self.Strs.add
    self._addType = self.Types.add
    self._T_list_app = self.type_list_arr.append

  # добавление ресурсов в Индекс:

  def addType(self, Type):
    # Type = TypeRenamer(Type)
    # self.addStr(Type)
    self._addType(Type)

  def addTypeList(self, types):
    if not types: return

    addType = self.addType
    dict = self.type_list_d

    for T in types: addType(T)

    key = "|".join(types)
    try: dict[key]
    except KeyError:
      dict[key] = None
      self._T_list_app(types)

  def addProto(self, proto):
    try: self.Protos[proto]; return
    except KeyError: pass
    assert proto[0] == "(", "Начало Proto неправильное"
    types = descExtractor(proto)
    exType = proto.split(")", 1)[1]
    shorty = "L" if len(exType) > 1 else exType
    self.addTypeList(types)
    for Type in types:
      if len(Type) > 1: Type = "L"
      shorty += Type
    self.addType(exType)
    self.Strs.add(shorty)
    self.Protos[proto] = proto, shorty, types, exType

  def addField(self, field):
    try: self.Fields[field]; return
    except KeyError: pass
    classType, field2 = field.split("->", 1)
    name, fieldType = field2.split(":", 1)
    self.addType(classType)
    self.addStr(name)
    self.addType(fieldType)
    self.Fields[field] = field, classType, name, fieldType

  def addMethod(self, method):
    try: self.Methods[method]; return
    except KeyError: pass
    classType, method2 = method.split("->", 1)
    name, proto = method2.split("(", 1)
    proto = "(" + proto
    self.addType(classType)
    self.addStr(name)
    self.addProto(proto)
    self.Methods[method] = method, classType, name, proto

  # конвертация Индекса в отсортированные пулы

  def sorting(self):
    def comp_type(Type):
      count = Type.count("[")
      return count, Type[count:]
    def comp_proto(proto):
      full, shorty, desc, extype = proto
      L = extype.count("[")
      return (type_d[extype], *(type_d[type] for type in desc))
    def comp_field(field):
      full, Class, name, Type = field
      return type_d[Class], str_d[name], type_d[Type]
    def comp_method(method):
      full, Class, name, proto = method
      return type_d[Class], str_d[name], proto_d[proto]

    # переименовывание

    renamed = set()
    renames = {}
    add = renamed.add
    addStr = self.addStr
    for name in self.Types:
      name2 = TypeRenamer(name)
      renames[name2] = name
      add(name2)
      addStr(name2)
    assert len(self.Types) == len(renamed)

    # сортировка

    self.str_arr = sorted(self.Strs)
    self.str_d = str_d = {Str : i for i, Str in enumerate(self.str_arr)}

    self.type_arr = sorted(renamed, key = comp_type)
    self.type_d = type_d = {renames[Type] : i for i, Type in enumerate(self.type_arr)}

    self.proto_arr = sorted(self.Protos.values(), key = comp_proto)
    self.proto_d = proto_d = {Proto[0] : i for i, Proto in enumerate(self.proto_arr)}
    self.proto_check = [(shorty, "(" + ''.join(desc) + ")" + extype) for full, shorty, desc, extype in self.proto_arr]

    self.field_arr = sorted(self.Fields.values(), key = comp_field)
    self.field_d = {Field[0] : i for i, Field in enumerate(self.field_arr)}

    self.method_arr = sorted(self.Methods.values(), key = comp_method)
    self.method_d = {Method[0] : i for i, Method in enumerate(self.method_arr)}

  # запись пулов в целевой файл

  def write_strs(self, file):
    str_data_b = Blockerson()
    pos = str_data_b.pos
    MUTF8 = str_data_b.MUTF8
    for str in self.str_arr:
      pos() # генерирует метку, что здесь начинается строка
      MUTF8(str)

    sb = Blockerson()
    writeMark = sb.writeMark
    for mark in str_data_b.arr:
      writeMark(mark) # вынимает эти самые метки

    self.file = file
    self.str_b = sb
    self.str_data_b = str_data_b

  def write_types(self):
    self.type_b = tb = Blockerson()
    write4 = tb.write4
    str_d = self.str_d

    for T in self.type_arr: write4(str_d[T])

  def write_protos(self):
    self.type_list_b = tlb = Blockerson()
    tla = self.type_list_arr
    str_d = self.str_d
    type_d = self.type_d
    type_list_d = self.type_list_d

    # помещает в конец элемент с нечётным количеством входящих аргументов
    i = len(tla) - 1
    while i >= 0:
      if len(tla[i]) & 1: break
      i -= 1
    if i >= 0: tla.append(tla.pop(i))

    write2 = tlb.write2
    write4 = tlb.write4
    left = len(tla)
    for types in tla:
      L = len(types)
      type_list_d[types] = tlb.pos()
      write4(L)
      for T in types: write2(type_d[T])
      left -= 1
      if L & 1 == 1 and left: write2(0)

    self.proto_b = pb = Blockerson()
    write4    = pb.write4
    writeMark = pb.writeMark
    for proto, shorty, types, exType in self.proto_arr:
      write4(str_d[shorty])
      write4(type_d[exType])
      writeMark(type_list_d[types] if types else Mark0)

  def write_fields(self):
    self.field_b = fb = Blockerson()
    write2 = fb.write2
    write4 = fb.write4
    str_d = self.str_d
    type_d = self.type_d

    for full, Class, name, Type in self.field_arr:
      write2(type_d[Class])
      write2(type_d[Type])
      write4(str_d[name])

  def write_methods(self):
    self.method_b = mb = Blockerson()
    write2 = mb.write2
    write4 = mb.write4
    str_d = self.str_d
    type_d = self.type_d
    proto_d = self.proto_d

    for full, Class, name, proto in self.method_arr:
      write2(type_d[Class])
      write2(proto_d[proto])
      write4(str_d[name])

  # вытягивает ВСЕ пул-ресурсы из класса

  def collector(self):
    # annotations

    def collectAnnot(annot):
      T, items = annot
      addType(T)
      for TypeV, name, value in items:
        addStr(name)
        encodedValue(TypeV, value)

    # encoded values

    def encodedValue(TypeV, value):
      match TypeV:
        case 23: addStr(value[1:-1])
        case 24: addType(value)
        case 25: addField(value)
        case 26: addMethod(value)
        case 27:
          assert value.startswith(".enum "), "EncodedValue 27 с неправильным началом"
          addField(value[6:])
        case 28:
          for TypeV, value in value:
            encodedValue(TypeV, value)
        case 29:
          collectAnnot(value)

    # code values

    addStr = self.addStr
    addType = self.addType
    addTypeList = self.addTypeList
    addProto = self.addProto
    addField = self.addField
    addMethod = self.addMethod

    # main collector

    def collect(classObj):
      className, accessF, superName, interfaces, sourceStr, classAnnots, allFM = classObj
      addType(className)
      if superName is not None: addType(superName)
      addTypeList(interfaces)
      if sourceStr is not None: addStr(sourceStr)
      for annot in classAnnots: collectAnnot(annot)

      for group_n, name, accessFM, value, elements, codeObj, debug in allFM:
        is_method = group_n >= 2

        (addMethod if is_method else addField)(className + "->" + name)
        if value is not None:
          encodedValue(*value)
        for element in elements: collectAnnot(element)
        if codeObj is not None:
          registers, ins, outs, insns, code_data, tries = codeObj

          if type(code_data) is dict: code_data = code_data.values()
          for data in code_data:
            match data[0]:
              case 26..27:               addStr(data[2])
              case 28 | 31..32 | 34..35: addType(data[2])
              case 36:       addType(data[1])
              case 37:       addType(data[3])
              case 82..109:  addField(data[2])
              case 110..114: addMethod(data[1])
              case 116..120: addMethod(data[3])
              case 250:
                addMethod(data[0][0])
                addProto(data[2])
              case 251:
                addMethod(data[3])
                addProto(data[4])
              case 255:      addProto(data[2])
              case _ | 121..249: continue # искусствено переключил sparse в packed

          for trie in tries:
            for Type, addr in trie[2]: addType(Type)

    return collect





def DexWriter(dex_classes):
  Pool = Pooler()
  # Pool.addStr("string")
  # Pool.addStr("meow!")
  # Pool.addStr("текст 🗿 из 👍 суррогатных 🔥 пар 🎉")
  # Pool.addStr("woof!")

  print("\nСбор пулов")
  collect = Pool.collector()
  for N, classObj in enumerate(dex_classes, 1):
    name = classObj[0]
    print("%04s %s" % (N, name))
    collect(classObj)
  Pool.sorting()
  # Pool.sort_FM(class_arr)



  def write_map(Map, map_d):
    file.seek(0, 2)
    mapO = file.tell()
    Map.append((0x1000, 1, mapO))
    map_d[0x1000] = 1, mapO
    count = len(None for _, size, _ in Map if size)
    file.write4(count)
    for T, size, offset in Map:
      if size: file.pack("<HHLL", T, 0, size, offset)
    return mapO

  def write_classes():
    print("\nЗапаковка классов")
    write4    = class_b.write4
    writeMark = class_b.writeMark
    str_d       = Pool.str_d
    type_d      = Pool.type_d
    type_list_d = Pool.type_list_d

    for N, classObj in enumerate(dex_classes, 1):
      className, accessF, superName, interfaces, sourceStr, classAnnots, allFM = classObj
      print("%4s %s" % (N, className))

      annot_idx = Mark0 # dir_annotation(class_data)
      class_idx, static_fields = write_class_data(className, allFM)
      values_idx = Mark0 # write_values(static_fields)

      write4(type_d[className])
      write4(accessF)
      write4(-1 if superName is None else type_d[superName])
      writeMark(type_list_d["|".join(interfaces)] if interfaces else Mark0)
      write4(-1 if sourceStr is None else str_d[sourceStr])
      writeMark(annot_idx)
      writeMark(class_idx)
      writeMark(values_idx)

  def write_class_data(className, allFM):
    groups = ([], [], [], [])
    g_appends = tuple(group.append for group in groups)
    for FM in allFM: g_appends[FM[0]](FM)

    res_g = ([], [], [], [])
    res_appends = tuple(res.append for res in res_g)
    field_d = Pool.field_d
    method_d = Pool.method_d

    for group, res_append in zip(groups, res_appends):
      pred_id = 0
      for group_n, name, accessFM, _, _, codeObj, debug in group:
        is_method = group_n >= 2

        name = className + "->" + name
        nameId = (method_d if is_method else field_d)[name]
        delta = nameId - pred_id
        if delta < 0:
          print((Pool.method_arr if is_method else Pool.field_arr)[pred_id][0])
          print(name)
          raise Exception("Дельта не должна быть меньше нуля (ошибка сортировщика полей & методов)! delta = %s" % delta)
        if is_method: res_append((delta, accessFM, write_codes(codeObj, debug)))
        else: res_append((delta, accessFM))
        pred_id = nameId

    if sum(map(len, res_g)) == 0: return 0, ()

    res = class_data_b.pos2()
    uleb128 = class_data_b.uleb128_h

    for group in res_g: uleb128(len(group))
    for group in res_g:
      for FM in group:
        for i in FM: uleb128(i)

    static_fields = tuple(res_g[0])
    return res, static_fields

  static_values_d = {}
  def write_values(static_fields):
    if not static_fields: return 0

    values = tuple(field[4] for field in static_fields)
    try: return static_values_d[values]
    except KeyError: pass
    static_values_d[values] = pos = value_b.pos()
    # write_encoded_arr(values, value_b)
    return pos

  def write_codes(codeObj, debug):
    if codeObj is None: return 0

    registers, ins, outs, insns, code_data, tries = codeObj

    res = codes_b.pos()
    TL = len(tries)

    write2 = codes_b.write2
    write4 = codes_b.write4
    tell = codes_b.tell
    seek = codes_b.seek
    sleb128 = codes_b.sleb128
    uleb128 = codes_b.uleb128

    write2(registers)
    write2(ins)
    write2(outs)
    write2(TL)
    write4(0) # write4(write_debug(debug))

    dalvikAssembler(code_data)

    if not TL: return res

    # Запись try-блоков:

    start = tell()
    seek(TL * 8, 1)
    posH = tell()
    seek(1, 1)
    offs, catch_d = [], {}
    offs_app = offs.append

    type_d = Pool.type_d

    for _, _, Catch, CatchAllAddr in tries:
      key = (Catch, CatchAllAddr)
      try:
        offs_app(catch_d[key])
        continue
      except KeyError: pass

      off = tell() - posH
      catch_d[key] = off
      offs_app(off)

      all = CatchAllAddr is not None
      L = len(Catch)
      sleb128(-L if all else L)
      for Type, addr in Catch:
        uleb128(type_d[Type])
        uleb128(addr)
      if all: write2(CatchAllAddr)

    #print(offs, len(catch_d))
    codes_b.write(b"\0" * (-tell() % 4))
    end = tell()

    seek(start)
    for trie, off in zip(tries, offs):
      startAddr, insnCount, _, _ = trie
      write4(startAddr)
      write2(insnCount)
      write2(off)
    codes_b.w_byte(len(catch_d))

    seek(end) # важно!
    return res

  """
  def write_encoded_arr(arr, file):
    file.uleb128(len(arr))
    for i in arr: write_enc_value(i, file)
  def write_enc_value(value, file):
    Type, par = value
    if type(par) is str:
      if par.startswith("0x"): par = int(par[2:], 16)
      elif par.startswith("-0x"): par = -int(par[3:], 16)

    if Type == 0: data = pack("<b", par)
    elif Type == 2: data = pack("<h", par)
    elif Type == 3: data = pack("<H", par)
    elif Type == 4: data = pack("<l", par)
    elif Type == 6:
      if par in ("nan", "inf", "-inf"): par = float(par)
      data = pack("<q", par)
    elif Type == 16: data = pack("<f", par)
    elif Type == 17: data = pack(">d", par)
    elif Type == 23: data = pack("<L", Pool.str_d[par[1:-1]])
    elif Type == 24: data = pack("<L", Pool.type_d[par])
    elif Type == 25: data = pack("<L", Pool.field_d[par])
    elif Type == 26: data = pack("<L", Pool.method_d[par])
    elif Type == 27:
      if not par.startswith(".enum "): raise wtf
      data = pack("<L", Pool.field_d[par[6:]])

    if Type < 28:
      while len(data) > 1 and data[-1] == 0: data = data[:-1]
      value = Type + 32 * (len(data) - 1)
      file.w_byte(value)
      file.write(data)
    elif Type == 28:
      file.w_byte(28)
      write_encoded_arr(par, file)
    elif Type == 29:
      file.w_byte(29)
      write_enc_annot2(par, file)
    elif Type == 30: file.w_byte(30)
    elif Type == 31: file.w_byte(31 + 32 if par else 31)
    else:
      print("•", Type, par)
      raise wtf
  """

  """
  annot_d, enc_annot_d, ref_annot_d = {}, {}, {}
  def write_enc_annot2(annot, file):
    Type, elements = annot
    file.uleb128(Pool.type_d[Type])
    file.uleb128(len(elements))
    for TypeV, name, value in elements:
      file.uleb128(Pool.str_d[name])
      write_enc_value((TypeV, value), file)
    #print("•", annot)
  def write_enc_annot(annot):
    print("ANNOT:", annot)
    key = str(annot)
    try: return enc_annot_d[key]
    except KeyError: pass
    enc_annot_d[key] = res = annot_b.pos()
    visibility = annot[-1]
    annot_b.w_byte(("build", "runtime", "system").index(visibility))
    write_enc_annot2(annot[:-1], annot_b)
    return res
  def write_annotation(annots):
    key = str(annots)
    try: return annot_d[key]
    except KeyError: pass
    asb = annot_set_b
    annot_d[key] = res = asb.pos()
    asb.write4(len(annots))
    for annot in annots: asb.write4(write_enc_annot(annot))
    return res
  def write_ref_annot(refs):
    key = str(refs)
    try: return ref_annot_d[key]
    except KeyError: pass
    asbr = annot_set_ref_b
    ref_annot_d[key] = res = asbr.pos()
    asbr.write4(len(refs))
    for ref in refs: asbr.write4(write_annotation(ref))
    return res
  annot_dirs = {}
  def dir_annotation(class_data):
    adb = annot_dir_b
    className, _, _, _, _, classAnnots, allFM = class_data
    groups = [[], [], [], []]
    F, M, P = [], [], []
    for FM in allFM: groups[FM[0]].append(FM)
    for group in groups:
      for group_n, diff, _, _, elements, _, debug in group:
        is_method = group_n >= 2
        diff = className + "->" + diff
        diffId = (Pool.method_d if is_method else Pool.field_d)[diff]
        if elements:
          el = (diffId, write_annotation(elements))
          (M if is_method else F).append(el)
        p_arr, p_arr2 = [], []
        for Dbg in debug.values():
          for line in Dbg:
            if type(line) is not str: p_arr2.append(line)
            elif line == ".end param" and p_arr2:
              p_arr.append(p_arr2)
              p_arr2 = []
        if p_arr: P.append((diffId, write_ref_annot(p_arr)))
    C = write_annotation(classAnnots) if classAnnots else 0
    arr = [C, len(F), len(M), len(P)]
    app = arr.append
    for idx, ann in F: app(idx); app(ann)
    for idx, ann in M: app(idx); app(ann)
    for idx, ann in P: app(idx); app(ann)
    arr = tuple(arr)
    #print(arr)
    try: return annot_dirs[arr]
    except KeyError: pass
    if len(arr) == 4 and arr[0] == 0: return 0
    annot_dirs[arr] = pos = adb.pos()
    for i in arr: adb.write4(i)
    return pos
  """



  linkS = linkO = mapO = stringIS = stringIO = typeIS = typeIO = protoIS = protoIO = fieldIS = fieldIO = methodIS = methodIO = classDefsIS = classDefsIO = dataIS = dataIO = 0

  annot_b = Blockerson()
  annot_set_b = Blockerson()
  annot_set_ref_b = Blockerson()
  annot_dir_b = Blockerson()
  value_b = Blockerson()
  debug_b = Blockerson()
  codes_b = Blockerson()
  class_b = Blockerson()
  class_data_b = Blockerson()

  dalvikAssembler = DalvikAssembler(codes_b, Pool)

  # with open(filename, "wb") as file:
  with BytesIO() as file:
    Blockerson.file = file
    file = Blockerson(file) # !!! единственный Blockerson с указанным аргументом конструктора

    Pool.write_strs(file)
    Pool.write_types()
    Pool.write_protos()
    Pool.write_fields()
    Pool.write_methods()

    file.write(b"dex\n035\x00")
    file.seek(36)
    file.write4(7 * 16)
    file.write(b"\x78\x56\x34\x12") # little-endian
    file.seek(4 * 17, 1)
    Pool.str_b.apply(4, 1, 4)
    Pool.type_b.apply(4, 2, 4)
    Pool.proto_b.apply(4, 3, 12)
    Pool.field_b.apply(4, 4, 8)
    Pool.method_b.apply(4, 5, 8)

    write_classes()

    class_b.apply(4, 6, 32)

    codes_b.apply(4, 0x2001)
    debug_b.apply(1, 0x2003)
    Pool.type_list_b.apply(4, 0x1001)
    Pool.str_data_b.apply(2, 0x2002)

    annot_b.apply(1, 0x2004)
    class_data_b.apply(1, 0x2000) # не может стоять до codes_b.apply
    value_b.apply(1, 0x2005)

    annot_set_b.apply(4, 0x1003)
    annot_set_ref_b.apply(4, 0x1002)
    annot_dir_b.apply(4, 0x2006)

    Blockerson.final()
    Map = Blockerson.Map
    map_d = Blockerson.map_d
    # print("map:")
    # for item in Map: print("  ", item)
    mapO = write_map(Map, map_d)

    stringIS, stringIO = map_d.get(1, (0, 0))
    typeIS,   typeIO   = map_d.get(2, (0, 0))
    protoIS,  protoIO  = map_d.get(3, (0, 0))
    fieldIS,  fieldIO  = map_d.get(4, (0, 0))
    methodIS, methodIO = map_d.get(5, (0, 0))
    classDefsIS, classDefsIO = map_d.get(6, (0, 0))
    _,        dataIO   = map_d.get(7, (0, 0))

    dataIS = file.tell() - dataIO

    file.seek(44)
    for i in (linkS, linkO, mapO, stringIS, stringIO, typeIS, typeIO, protoIS, protoIO, fieldIS, fieldIO, methodIS, methodIO, classDefsIS, classDefsIO, dataIS, dataIO):
      file.write4(i)

    file_size = file.size()
    file.seek(32)
    file.write4(file_size)
    print("\nfile_size:", file_size)

    file.seek(32)
    Hash = sha1(file.file.read()).digest()
    file.seek(12)
    file.write(Hash)
    print("sha1:", Hash.hex())

    file.seek(12)
    Hash = adler32(file.file.read())
    file.seek(8)
    file.write4(Hash)
    print("adler32:", Hash)

  return file.getvalue()



#   Поскольку я в оригинальном коде переименовал все классы с маленькой буквы на большую,
# то здесь, ClassLoader уже будет загружать не из сгенерированного .dex файла, а из основного приложения,
# т.е. эффект влияния изменений в генерированном .dex файле попусту пропадёт.
#   TypeRenamer это явно исправляет

def TypeRenamer(type):
  # if type.startswith("Lpbi/secured/"):
  #   type = "Ltest/classes" + type[12:]
  return type





import test_classes # test_classes, TheGreatestBeginning, test_Wrap

dexData = DexWriter(test_classes)
with open("/sdcard/Check.dex", "wb") as file:
  file.write(dexData)
print("ok!")

# всего 78 ms на создание dex файла с полноценным процессором моего движка + все pbi.secured.* никуда не делись



# TheGreatestBeginning(dexData)
# test_Wrap(dexData)
