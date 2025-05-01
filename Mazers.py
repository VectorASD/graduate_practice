if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  load_codes("Mazers.py")
  n = 1
  main(("mazers", "time-tests", "optimizer-check")[n], False, ("/sdcard/my_code3.asd", "/sdcard/my_debug3.asd"))
  exit()

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

###~~~### time-tests

def time_test():
  data = tuple((0, "5") for i in range(100000))
  td_sum = td2_sum = count = 0
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

    td_sum += td
    td2_sum += td2
    count += 1
    res = td_sum / count, td2_sum / count

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
  StopIteration теперь не в виде исключения, а в виде __next__() = null... возможно, плохая идея;
  range теперь имеет ускоренную версию range-int за счёт int вместо BigInteger
    """
    print(*res)    # 0.0372 vs 0.0289 (странненько, они приблизились)

    # print(100000 / td, 100000 / td2)

# замеры на QPython3 (это же устройство):
#    0.02744 vs 0.0112
# я довольно-таки близок к тому, чтобы обогнать его!
# при том QPython3 на .so-библиотеке, т.е. этот тот же CPython, у меня - чистая Java

def time_test2():
  while True:
    T = time()
    for i in range(1000000): pass
    print(1000000 / (time() - T))

Thread(time_test).start()

###~~~### mazers

import common # adler32, sha1

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
      print(num, T, T is Mark)
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
# exit(0)



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
    self.addStr(Type)
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

    self.str_arr = sorted(self.Strs)
    self.str_d = str_d = {Str : i for i, Str in enumerate(self.str_arr)}

    self.type_arr = sorted(self.Types, key = comp_type)
    self.type_d = type_d = {Type : i for i, Type in enumerate(self.type_arr)}

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

  def collector(self, classObj):
    def collectAnnot(annot):
      T, items = annot
      addType(T)
      for TypeV, name, value in items:
        addStr(name)
        encodedValue(TypeV, value)

    def disp_27(value):
      assert value.startswith(".enum "), "EncodedValue 27 с неправильным началом"
      addField(value[6:])
    def disp_28(value):
      for TypeV, value in value: encodedValue(TypeV, value)
    dispatch = (
      *(lambda value: None,) * 23, # 0 - 22
      lambda value: addStr(value[1:-1]), # 23
      lambda value: addType(value), # 24
      lambda value: addField(value), # 25
      lambda value: addMethod(value), # 26
      disp_27, # 27
      disp_28, # 28
      collectAnnot, # 29
      *(lambda value: None,) * 2, # 30 - 31
    )

    def encodedValue(TypeV, value):
      dispatch[TypeV](value)

    addStr = self.addStr
    addType = self.addType
    addProto = self.addProto
    addField = self.addField
    addMethod = self.addMethod

    className, accessF, superName, interfaces, sourceStr, classAnnots, allFM = classObj
    self.addType(className)
    if superName is not None: addType(superName)
    self.addTypeList(interfaces)
    if sourceStr is not None: addStr(sourceStr)
    for annot in classAnnots: collectAnnot(annot)

    for group_n, name, accessFM, value, elements, codeObj, debug in allFM:
      is_method = group_n >= 2

      (addMethod if is_method else addField)(className + "->" + name)
      if value is not None:
        encodedValue(*value)
      for element in elements: collectAnnot(element)
      if codeObj is not None:
        registers, ins, outs, insns, codeD, tries3 = codeObj





def DexWriter(filename, dex_classes):
  Pool = Pooler()
  # Pool.addStr("string")
  # Pool.addStr("meow!")
  # Pool.addStr("текст 🗿 из 👍 суррогатных 🔥 пар 🎉")
  # Pool.addStr("woof!")
  for N, classObj in enumerate(dex_classes, 1):
    name = classObj[0]
    print("%04s %s" % (N, name))
    Pool.collector(dex_class)
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
        if is_method: res_append((delta, accessFM, 0)) # write_codes(name, codeObj, debug)))
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

  with open(filename, "wb") as file:
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
    print("map:")
    Map = Blockerson.Map
    map_d = Blockerson.map_d
    for item in Map: print("  ", item)
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
    print("file_size:", file_size)

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





ACCESS_PUBLIC       =     0x1 # class | field | method
ACCESS_PRIVATE      =     0x2 # class | field | method
ACCESS_PROTECTED    =     0x4 # class | field | method
ACCESS_STATIC       =     0x8 # class | field | method
ACCESS_FINAL        =    0x10 # class | field | method
# ACCESS_SUPER      =    0x20 # class |  ---  |  ----
ACCESS_SYNCHRONIZED =    0x20 #  ---  |  ---  | method
ACCESS_VOLATILE     =    0x40 #  ---  | field |  ----
ACCESS_BRIDGE       =    0x40 #  ---  |  ---  | method
ACCESS_TRANSIENT    =    0x80 #  ---  | field |  ----
ACCESS_VARARGS      =    0x80 #  ---  |  ---  | method
ACCESS_NATIVE       =   0x100 #  ---  |  ---  | method
ACCESS_INTERFACE    =   0x200 # class |  ---  |  ----
ACCESS_ABSTRACT     =   0x400 # class |  ---  | method
ACCESS_STRICT       =   0x800 #  ---  |  ---  | method
ACCESS_SYNTHETIC    =  0x1000 # class | field | method
ACCESS_ANNOTATION   =  0x2000 # class |  ---  |  ----
ACCESS_ENUM         =  0x4000 # class | field |  ----
ACCESS_UNKNOWN      =  0x8000 #  ---  |  ---  |  ----
ACCESS_CONSTRUCTOR  = 0x10000 #  ---  |  ---  | method (только и всегда <clinit> и <init>)
ACCESS_DECL_SYNC    = 0x20000 #  ---  |  ---  | method (работает также, как и обычный synchronized)

IS_STATIC_FIELD   = 0 # static
IS_INSTANCE_FIELD = 1
IS_DIRECT_METHOD  = 2 # static or constructor
IS_VIRTUAL_METHOD = 3

dex_class = ('Lpbi/secured/root;',
 ACCESS_PUBLIC,
 'Ljava/lang/Object;',
 [],
 None,
 [],
 [(IS_INSTANCE_FIELD, 'obj:Lpbi/secured/class1;', ACCESS_PUBLIC, None, [], None, {}),
  (IS_DIRECT_METHOD, '<init>()V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, [],
   (2, 1, 2, 11,
    {0: (112, 'Ljava/lang/Object;-><init>()V', (1,)),
     3: (34, 0, 'Lpbi/secured/class1;'),
     5: (112, 'Lpbi/secured/class1;-><init>(Lpbi/secured/root;)V', (0, 1)),
     8: (91, (0, 1), 'Lpbi/secured/root;->obj:Lpbi/secured/class1;'),
     10: (14,)
    }, []), {}),
  (IS_DIRECT_METHOD, 'checker()V', ACCESS_STATIC | ACCESS_PUBLIC, None, [],
   (1, 0, 1, 9,
    {0: (34, 0, 'Lpbi/secured/root;'),
     2: (112, 'Lpbi/secured/root;-><init>()V', (0,)),
     5: (110, 'Lpbi/secured/root;->test()V', (0,)),
     8: (14,)
    }, []), {}),
  (IS_DIRECT_METHOD, 'sum(II)I', ACCESS_STATIC | ACCESS_PUBLIC, None, [],
   (3, 2, 0, 3,
    {0: (144, 0, 1, 2),
     2: (15, 0)
    }, []), {}),
  (IS_VIRTUAL_METHOD, 'test()V', ACCESS_PUBLIC, None, [],
   (2, 1, 1, 6,
    {0: (84, (0, 1), 'Lpbi/secured/root;->obj:Lpbi/secured/class1;'),
     2: (110, 'Lpbi/secured/class1;->test()V', (0,)),
     5: (14,)
    }, []), {})
  ]
)

DexWriter("/sdcard/Check.dex", (dex_class,))
print("ok!")
