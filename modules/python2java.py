ACCESS_NOFLAGS      =     0x0 # аналогичен ACCESS_PRIVATE
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

IS_STATIC_FIELD   = 0 # static or constructor (<clinit>)
IS_INSTANCE_FIELD = 1
IS_DIRECT_METHOD  = 2 # static or constructor (<init>)
IS_VIRTUAL_METHOD = 3



import common # dex, context
import DexWriter # DexWriter



NOT_CHECK_REGS_IN_ARGS = True

# Типы

CoreType = "Lpbi/executor/Main;"

BaseType = "Lpbi/executor/types/Base;"
BaseArrType = "[" + BaseType
NoneType = "Lpbi/executor/types/NoneType;"
BooleanType = "Lpbi/executor/types/pBoolean;"
BigIntType = "Lpbi/executor/types/BigInt;"
FloatType = "Lpbi/executor/types/pFloat;"
StringType = "Lpbi/executor/types/pString;"
BytesType = "Lpbi/executor/types/Bytes;"
ListType = "Lpbi/executor/types/List;"
TupleType = "Lpbi/executor/types/Tuple;"
JavaWrapType = "Lpbi/executor/types/JavaWrap;"

# Исключения

NameErrorType = "Lpbi/executor/exceptions/NameError;"
ValueErrorType = "Lpbi/executor/exceptions/ValueError;"
StopIterationType = "Lpbi/executor/exceptions/StopIteration;"
PyExceptionType = "Lpbi/executor/exceptions/PyException;"

# Поля

GlobalsField = "->globals:" + BaseArrType
VoidArrField = "->void_arr:" + BaseArrType
VoidMapField = "->void_map:Ljava/util/Map;"
LastExcField = "->last_exc:" + BaseType

BuiltinsField = "%s->builtins_arr:%s" % (CoreType, BaseArrType)
NoneField = "%s->None:%s" % (CoreType, NoneType)
TrueField = "%s->True:%s" % (CoreType, BooleanType)
FalseField = "%s->False:%s" % (CoreType, BooleanType)

# КонструкТОРы типов

BigIntCtor = BigIntType + "-><init>([B)V"
FloatCtor = FloatType + "-><init>(D)V"
StringCtor = StringType + "-><init>(Ljava/lang/String;)V"
BytesCtor = BytesType + "-><init>([B)V"
ListCtor = ListType + "-><init>()V"
ListCtor2 = ListType + "-><init>(Ljava/util/ArrayList;)V"
ListCtor3 = ListType + "-><init>(I)V"
TupleCtor = "%s-><init>(%s)V" % (TupleType, BaseArrType)
JavaWrapCtor = JavaWrapType + "-><init>(Ljava/lang/String;)V"

# КонструкТОРы исключений

NameErrorCtor = NameErrorType + "-><init>(Ljava/lang/String;)V"
ValueErrorCtor = ValueErrorType + "-><init>(Ljava/lang/String;)V"



# Методы арифметики

maths = ("__add__", "__sub__", "__mul__", "__matmul__", "__truediv__", "__mod__", "__and__", "__or__", "__xor__", "__lshift__", "__rshift__", "__pow__", "__floordiv__", "__lt", "__gt", "__eq", "__ge", "__le", "__ne")
unars = ("__pos__", "__neg__", "__invert__")

BinaryMethods = tuple('%s->%s(%s)%s' % (BaseType, operation, BaseType, BaseType) for operation in maths)
UnaryMethods = tuple('%s->%s()%s' % (BaseType, operation, BaseType) for operation in unars)

# Остальные методы

CallerMethod = "%s->__call__(%sLjava/util/Map;)%s" % (BaseType, BaseArrType, BaseType)
ContainsMethod = "%s->__contains__(%s)%s" % (BaseType, BaseType, BooleanType)
SetItemMethod = "%s->__setitem__(I%s)V" % (BaseType, BaseType)
SetItemMethod2 = "%s->__setitem__(%s%s)V" % (BaseType, BaseType, BaseType)
GetItemMethod = "%s->__getitem__(I)%s" % (BaseType, BaseType)
GetItemMethod2 = "%s->__getitem__(%s)%s" % (BaseType, BaseType, BaseType)
GetAttrMethod = "%s->__getattr__(Ljava/lang/String;)%s" % (BaseType, BaseType)
LenMethod = BaseType + "->__len()I"
BoolMethod = BaseType + "->__bool()Z"
IterMethod = "%s->__iter__()%s" % (BaseType, BaseType)
NextMethod = "%s->__next__()%s" % (BaseType, BaseType)
AppendMethod = "%s->append(%s)V" % (BaseType, BaseType)
EnterMethod = "%s->__enter__()%s" % (BaseType, BaseType)
ExitMethod = "%s->__exit__(%s%s)%s" % ((BaseType,) * 4)
RaiseMethod = "%s->__raise__()%s" % (BaseType, BaseType)

""" TODOs:
Разделить вызов функций на их вызов и присвоение в регистр результата вызова (например, у всех print бессмысленное присвоение их None-результата в regs[0])
Заменить regs-массив на регистры DVM, не затрагивает только те элементы, в которых хранятся bult-ins, а также, использования глобала в других функциях
  Ещё понадобится реализовать сжимающий (+перемешивающий) механизм, чтобы не было неиспользуемых регистров
"""



def DVM_name(class_name):
  return "L%s;" % class_name.replace('.', '/')

def builtins():
  class_name, field = BuiltinsField.split("->", 1)
  field_name, field_type = field.split(":", 1)
  # print(class_name, field_name, field_type)
  return getattr(__import__(class_name), "_f_" + field_name)
  # Иногда даже у getattr появляется смысл существования... Т.к. не все имена атрибутов возможно обфусцировать ;"-}

def bultin_expections():
  PET = __import__(PyExceptionType)
  return {i : DVM_name(str(item().source))
    for i, item in enumerate(builtins())
    if type(item) is type and PET.isAssignableFrom(__import__(item))
  }
bultin_expections = bultin_expections()



def builder(ClassName, inputs, py_codes, py_tries, local_consts, analysis):
  def reg_is_null(reg, py_reg):
    # проверяется reg-регистр на null
    # 4 + 4 + 4 + 6 + 6 + 4 + 6 + 6 + 2 + 4 + 6 + 2 = 54 bytes
    # new: 4 + 4 + 4 + 6 + 2 = 20 bytes!
    """
      (34, 1, 'Ljava/lang/StringBuilder;'), # new-instance v1, Ljava/lang/StringBuilder;
      (26, 2, "name 'regs:"), # const-string v2, "name 'regs:"
      (112, 'Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V', (1, 2)), # invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
      (110, 'Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;', (1, 3)), # invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;
      # (12, 1), # move-result-object v1 (StringBuilder через append сам себя возвращает)
      (26, 2, "' is not defined"), # const-string v2, "' is not defined"
      (110, 'Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;', (1, 2)), # invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
      # (12, 1), # move-result-object v1 (StringBuilder через append сам себя возвращает)
      (110, 'Ljava/lang/StringBuilder;->toString()Ljava/lang/String;', (1,)), # invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
      (12, 2), # move-result-object v2
    """ # Что я сразу не подумал-то?! Получается свёртка констант на уровне данного генератора кода 👍👍👍 Это понял только после JaDX-декомпилятора
    extend((
      (57, reg, 10), # if-nez v{reg}, :{+10 * 2 bytes}
      (34, 1, NameErrorType), # new-instance v1, Lpbi/executor/exceptions/NameError;
      (26, 2, "name 'regs:%s' is not defined" % py_reg), # const-string v2, "name 'regs:{py_reg}' is not defined"
      (112, NameErrorCtor, (1, 2)), # invoke-direct {v1, v2}, Lpbi/executor/exceptions/NameError;-><init>(Ljava/lang/String;)V
      (39, 1), # throw v1
    ))

  def get_reg(reg, py_reg, tmp = None, is_args = False):
    try:
      const = local_consts[py_reg]
      field_name = "%s->c%s:%s" % (ClassName, const, BaseType)
      if tmp is not None: append((18, tmp, py_reg)) # const v{tmp} = {py_reg}
      append((98, reg, field_name)) # sget-object v{reg}, {...}
      return
    except KeyError: pass
    if tmp is None: tmp = reg
    extend((
      (18, tmp, py_reg), # const v{tmp} = {py_reg}
      (70, reg, 0, tmp), # aget-object v{reg} = v0[v{tmp}]
    ))
    if is_args and NOT_CHECK_REGS_IN_ARGS: return
    reg_is_null(reg, py_reg)

  def put_reg(idx, reg):
    tmp = 2 - int(reg == 2)
    extend((
      (18, tmp, idx), # const v{tmp} = {idx}
      (77, reg, 0, tmp), # aput-object v0[v{tmp}] = v{reg}
    ))

  def put_var(idx, reg):
    if type(idx) is int:
      put_reg(idx, reg)
      return
    print("var:", idx, reg); 1/0
    #match reg & 7:
    #  case 2: 
    #  case _: print(idx >> 3, idx & 7); 1/0

  def make_base_array(args):
    extend((
      (18, 1, len(args)), # const v1 = {len(args)}
      (35, (1, 1), BaseArrType),  # new-array v1, v1, [Lpbi/executor/types/Base;
    ))
    for i, arg in enumerate(args):
      append((18, 2, i)) # const v2 = {i}
      get_reg(3, arg, None, True) # const v3 = regs[arg]
      append((77, 3, 1, 2)) # aput-object v1[v2] = v3

  def string_builder(items, reg):
    append((34, reg, 'Ljava/lang/StringBuilder;')) # new-instance v{reg}, Ljava/lang/StringBuilder;
    first = True
    tmp = reg + 1
    for item in items:
      if type(item) is str:
        append((26, tmp, item)) # const-string v{tmp}, {item}
        if first:
          append((112, 'Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V', (reg, tmp))) # invoke-direct {v{reg}, v{tmp}}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
          first = False
        else: append((110, 'Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;', (reg, tmp))) # invoke-virtual {v{reg}, v{tmp}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
        # append((12, 1)) # move-result-object v1 (StringBuilder через append сам себя возвращает)
      else: # type(item) is int (регистр)
        if first:
          append((112, 'Ljava/lang/StringBuilder;-><init>()V', (reg,))) # invoke-direct {v{reg}}, Ljava/lang/StringBuilder;-><init>()V
          first = False
        append((110, 'Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;', (reg, item))) # invoke-virtual {v{reg}, v{item}}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;
        # append((12, 1)) # move-result-object v1 (StringBuilder через append сам себя возвращает)
    extend((
      (110, 'Ljava/lang/StringBuilder;->toString()Ljava/lang/String;', (reg,)), # invoke-virtual {v{reg}}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
      (12, reg), # move-result-object v{reg}
    ))
    # высчитывание байтового размера:
    # 4 + 10 * strings + 6 * integers + 6 + 2 + 6 * (если type(items[0]) is int)
    # = 12 + 10 * strings + 6 * (integers + (если type(items[0]) is int)) 



  registers = 5
  outsSize = 3 # пока не разобрался, как ЭТО правильно считать...

  p0 = registers - inputs # экземпляр pbi.eval.Main
  # p1 = p0 + 1 # аргумент pbi.executor.RegLocs

  # v8 - i_arr (здесь: массив констант)
  # v19 - pos (счётчик команд)
  # v21 - regs (здесь: v0)
  # v22 - scope (здесь: ?)
  # v23 - i0data (здесь: const)
  # v24 - i1data (здесь: const)
  # v25 - i2data (здесь: const)
  # v26 - void_hash_map

  codes = [
    # (7, 0, p1), # move-object v0, p1
    # (84, (0, 0), 'Lpbi/executor/RegLocs;->regs:[Lpbi/executor/types/Base;'), # iget-object v0, v0, Lpbi/executor/RegLocs;->regs:[Lpbi/executor/types/Base;
    (84, (0, p0), ClassName + GlobalsField), # iget-object v0, p0, {ClassName}->globals:[Lpbi/executor/types/Base;
  ]
  extend = codes.extend
  append = codes.append

  tries = []
  try_add = tries.append

  # LINKS = {4: 3, 7: 2, 9: 1, 58: 2, 65: 4, 67: 3, 98: 4, 99: 3}
  # for pos, line in enumerate(py_codes):
  #   try: print(line, pos + line[LINKS[line[0]]])
  #   except KeyError: pass

  starts = {}
  for item in py_tries:
    ts = item[2]
    if ts:
      start = item[0]
      try: items = starts[start]
      except KeyError: items = starts[start] = []
      items.extend(ts)
  exc_types = {}
  for pos, line in enumerate(py_codes):
    try:
      items = starts[pos]
      try: exc_types[pos] = {reg : analysis[reg] for reg, label in items}
      except KeyError: raise Exception("Тип исключения не обнаружен (reg:%s)" % reg)
    except KeyError: pass
    try:
      match line[0]:
        case 59: # %0 <- "package%1"
          analysis[line[1]] = line[2]
        case 60: # v%0 = reg v%1
          analysis[line[1]] = analysis[line[2]]
    except KeyError: pass

  for a, b, ts, to in py_tries:
    ts = tuple((exc_types[a][reg], -label) for reg, label in ts)
    try_add((-a, -b, ts, -to if to >= 0 else None))
    # print("tries:", -a, -b, ts, -to if to >= 0 else None)

  for pos, line in enumerate(py_codes):
    # Коды оставшихся операций:
    # 12, 13, 41, 42, 44, 46, 47, 50,
    # 56, 57, 58, 61, 62, 63, 64, 65, 66, 68, 70, 98, 99
    match line[0]:
      case -1: # label
        append((-1, -pos))
        print("label:", -pos)

      case 0: # v%0 = [%1 None-items]     makelist
        extend((
          (34, 1, ListType), # new-instance v1, Lpbi/executor/types/List;
          (18, 2, line[2]), # const v2 = {line[2]}
          (112, ListCtor3, (1, 2)), # invoke-direct {v1, v2}, Lpbi/executor/types/List;-><init>(Ljava/util/ArrayList;)V
        ))
        put_reg(line[1], 1) # regs[line[1]] = v1

      case 1: # v%0[%1] = v%2
        get_reg(1, line[1]) # const v1 = regs[line[1]]
        append((18, 2, line[2])) # const v2 = {line[2]}
        get_reg(3, line[3]) # const v3 = regs[line[3]]
        append((110, SetItemMethod, (1, 2, 3))) # invoke-virtual {v1, v2, v3}, Lpbi/executor/types/Base;->__setitem__(ILpbi/executor/types/Base;)V

      case 2: # v%0 = list()
        extend((
          (34, 1, ListType), # new-instance v1, Lpbi/executor/types/List;
          (112, ListCtor, (1,)), # invoke-direct {v1}, Lpbi/executor/types/List;-><init>()V
        ))
        put_reg(line[1], 1) # regs[line[1]] = v1

      case 3: # v%0 = v%0.__iter__()
        get_reg(1, line[1], 2) # const v2 = {line[1]}, v1 = regs[v2]
        extend((
          (110, IterMethod, (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__iter__()Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
          (77, 1, 0, 2), # aput-object v0[v2] = v1
        ))

      # 4 реализовано внутри 67

      case 5: # test tuple & size %0: v%1
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        size = line[1]
        extend((
          (110, LenMethod, (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__len()I
          (10, 1), # move-result v1
          (18, 2, size), # const v2 = {size}

          (55, (1, 2), 10), # if-le v1, v2, :{+10 * 2 bytes}   4+4+4+6+2 = 20 bytes
          (34, 1, ValueErrorType), # new-instance v1, Lpbi/executor/exceptions/ValueError;
          (26, 2, "too many values to unpack (expected %s)" % size), # const-string v2, {const}
          (112, ValueErrorCtor, (1, 2)), # invoke-direct {v1, v2}, Lpbi/executor/exceptions/ValueError;-><init>(Ljava/lang/String;)V
          (39, 1), # throw v1

          (53, (1, 2), 27), # if-ge v1, v2, :{+27 * 2 bytes}   4+38+4+6+2 = 54 bytes
        ))
        # (26, 2, "not enough values to unpack (expected %s)" % size), # const-string v2, {const}
        string_builder(("not enough values to unpack (expected %s, got" % size, 1, ")"), 2) # v2 = "..." + v1 + ")"     12+10*2+6*1 = 38 bytes
        extend((
          (34, 1, ValueErrorType), # new-instance v1, Lpbi/executor/exceptions/ValueError;
          (112, ValueErrorCtor, (1, 2)), # invoke-direct {v1, v2}, Lpbi/executor/exceptions/ValueError;-><init>(Ljava/lang/String;)V
          (39, 1), # throw v1
        ))

      case 6: # v%0 = v%1[%2]
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        extend((
          (18, 2, line[3]), # const v2 = {line[3]}
          (110, GetItemMethod, (1, 2)), # invoke-virtual {v1, v2}, Lpbi/executor/types/Base;->__getitem__(I)Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
        ))
        put_reg(line[1], 1) # regs[line[1]] = v1

      case 7: # ifn v%0: goto %1
        get_reg(1, line[1]) # const v1 = regs[line[1]]
        off = -(pos + line[2])
        extend((
          (110, BoolMethod, (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__bool()Z
          (10, 1), # move-result v1
          (56, 1, (off,)), # if-eqz v1, :{off}
        ))

      case 8: # v%0.append(v%1)
        get_reg(1, line[1]) # const v1 = regs[line[1]]
        get_reg(2, line[2]) # const v2 = regs[line[2]]
        append((110, AppendMethod, (1, 2))) # invoke-virtual {v1, v2}, Lpbi/executor/types/Base;->append(Lpbi/executor/types/Base;)V

      case 9: # goto %0
        off = -(pos + line[1])
        assert off < 0, "off = %s" % off
        append((40, off)) # goto :{off}

      case 10..11: 1/0

      # 12..13

      case 14..32: # v%0 {maths}= v%1
        code, in1, in2 = line
        get_reg(1, in1, 3) # const v3 = {in1}, v1 = regs[v3] (Левый операнд)
        get_reg(2, in2) # const v2 = regs[in2] (Правый операнд)
        extend((
          (110, BinaryMethods[code - 14], (1, 2)), # invoke-virtual {v1, v2}, Lpbi/executor/types/Base;->__add__(Lpbi/executor/types/Base;)Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
          (77, 1, 0, 3), # aput-object v0[v3] = v1
        ))

      case 33: # v%0 = v%0 in v%1
        get_reg(1, line[1], 3) # const v3 = {line[1]}, v1 = regs[v3]
        get_reg(2, line[2]) # const v2 = regs[line[2]]
        extend((
          (110, ContainsMethod, (2, 1)), # invoke-virtual {v2, v1}, Lpbi/executor/types/Base;->__contains__(Lpbi/executor/types/Base;)Lpbi/executor/types/pBoolean;
          (12, 1), # move-result-object v1
          (77, 1, 0, 3), # aput-object v0[v3] = v1
        ))

      case 34: # v%0 = v%0 is v%1
        get_reg(1, line[1], 3) # const v3 = line[1], v1 = regs[v3]
        get_reg(2, line[2]) # const v2 = regs[line[2]]
        extend((
          (51, (1, 2), 5), # if-ne v1, v2, :{+5 * 2 bytes}   4+4+2 = 10 bytes
          (98, 2, TrueField), # sget-object v2, Lpbi/executor/Main;->True:Lpbi/executor/types/pBoolean;
          (40, 3), # goto :{+3 * 2 bytes}   2+4 = 6 bytes
          (98, 2, FalseField), # sget-object v2, Lpbi/executor/Main;->False:Lpbi/executor/types/pBoolean;
          (77, 2, 0, 3), # aput-object v0[v3] = v2
        ))

      # 35 реализовано внутри 92

      case 36: # v%0 = v%1[v%2]
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        get_reg(2, line[3]) # const v2 = regs[line[3]]
        extend((
          (110, GetItemMethod2, (1, 2)), # invoke-virtual {v1, v2}, Lpbi/executor/types/Base;->__getitem__(Lpbi/executor/types/Base;)Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
        ))
        put_reg(line[1], 1) # regs[line[1]] = v1

      # 37 реализовано внутри 93

      case 38: # v%0 = v%1.%2
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        extend((
          (26, 2, line[3]), # const-string v2, {line[3]}
          (110, GetAttrMethod, (1, 2)), # invoke-virtual {v1, v2}, Lpbi/executor/types/Base;->__getattr__(Ljava/lang/String;)Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
        ))
        put_reg(line[1], 1) # regs[line[1]] = v1

      case 39: # v%0 = [v%0]     makelist
        get_reg(1, line[1], 3) # const v3 = {line[1]}, v1 = regs[v3]
        extend((
          (34, 2, 'Ljava/util/ArrayList;'), # new-instance v2, Ljava/util/ArrayList;
          (112, 'Ljava/util/ArrayList;-><init>()V', (2,)), # invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V
          (110, 'Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z', (2, 1)), # invoke-virtual {v2, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
          (34, 1, ListType), # new-instance v1, Lpbi/executor/types/List;
          (112, ListCtor2, (1, 2)), # invoke-direct {v1, v2}, Lpbi/executor/types/List;-><init>(Ljava/util/ArrayList;)V
          (77, 1, 0, 3), # aput-object v0[v3] = v1
        ))

      case 40: # v%0[v%1] = v%2
        get_reg(1, line[1]) # const v1 = regs[line[1]]
        get_reg(2, line[2]) # const v2 = regs[line[2]]
        get_reg(3, line[3]) # const v3 = regs[line[3]]
        append((110, SetItemMethod2, (1, 2, 3))) # invoke-virtual {v1, v2, v3}, Lpbi/executor/types/Base;->__setitem__(Lpbi/executor/types/Base;Lpbi/executor/types/Base;)V

      # 41..42

      case 43: # return
        extend((
          (98, 0, NoneField), # sget-object v0, Lpbi/executor/Main;->None:Lpbi/executor/types/NoneType;
          (17, 0), # return-object v0
        ))

      # 44

      case 45: # v%0 = tuple(v%1_args)
        starred = any(is_star for reg, is_star in line[2])
        if starred: 1/0
        args = tuple(item[0] for item in line[2])
        make_base_array(args) # v1 = new Base[] {...arg_regs}
        extend((
          (34, 2, TupleType), # new-instance v2, Lpbi/executor/types/Tuple;
          (112, TupleCtor, (2, 1)), # invoke-direct {v2, v1}, Lpbi/executor/types/Tuple;-><init>([Lpbi/executor/types/Base;)V
        ))
        put_reg(line[1], 2) # regs[line[1]] = v2

      # 46..47

      case 48: # %0 = last_exception
        append((84, (1, p0), ClassName + LastExcField)) # iget-object v1, p0, {ClassName}->last_exc:Lpbi/executor/types/Base;
        put_var(line[1], 1) # var(line[1]) = v1
        extend((
          (98, 1, NoneField), # sget-object v1, Lpbi/executor/Main;->None:Lpbi/executor/types/NoneType;
          (91, (1, p0), ClassName + LastExcField), # iput-object v1, p0, {ClassName}->last_exc:Lpbi/executor/types/Base;
        ))

      case 49: # raise v%0
        get_reg(1, line[1]) # const v1 = regs[line[1]]
        append((110, RaiseMethod, (1,))) # invoke-virtual {v1}, Lpbi/executor/types/Base;->__raise__()Lpbi/executor/types/Base;

      # 50

      case 51..53: # v%0 = {unars}v%0
        code, inout = line
        get_reg(1, inout, 3) # const v3 = {inout}, v1 = regs[v3] (Правый операнд)
        extend((
          (110, UnaryMethods[code - 51], (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__neg__()Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
          (77, 1, 0, 3), # aput-object v0[v3] = v1
        ))

      case 54: # v%0 = v%1.__enter__()
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        extend((
          (110, EnterMethod, (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__enter__()Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
        ))
        put_reg(line[1], 1) # regs[line[1]] = 1

      case 55: # ifn v%0.__exit__(type(last_exception), last_exception, None): raise last_exception
        # (84, (0, p0), ClassName + LastExcField), # iget-object v0, p0, {ClassName}->last_exc:Lpbi/executor/types/Base;
        # (91, (0, p0), ClassName + LastExcField), # iput-object v0, p0, {ClassName}->last_exc:Lpbi/executor/types/Base;
        L = len(codes)
        no_throw = L + 1
        get_reg(1, line[1]) # const v1 = regs[line[1]]
        extend((
          (84, (2, p0), ClassName + LastExcField), # iget-object v2, p0, {ClassName}->last_exc:Lpbi/executor/types/Base;
          (32, (3, 2), PyExceptionType), # instance-of v3, v2, Lpbi/executor/exceptions/PyException;

          (56, 3, (L,)), # if-eqz v3, :{L}
          (31, 2, PyExceptionType), # check-cast v2, Lpbi/executor/exceptions/PyException;
          (110, 'Lpbi/executor/exceptions/PyException;->__type__()Lpbi/executor/types/Type;', (2,)), # invoke-virtual {v2}, Lpbi/executor/exceptions/PyException;->__type__()Lpbi/executor/types/Type;
          (12, 3), # move-result-object v3
          (110, ExitMethod, (1, 3, 2)), # invoke-virtual {v1, v3, v2}, Lpbi/executor/types/Base;->__exit__(Lpbi/executor/types/Base;Lpbi/executor/types/Base;)Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
          (110, BoolMethod, (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__bool()Z
          (10, 1), # move-result v1
          (57, 1, (no_throw,)), # if-nez v1, :{L}
          (84, (1, 2), 'Lpbi/executor/exceptions/PyException;->err:Lpbi/executor/exceptions/RuntimeError;'), # iget-object v1, v2, Lpbi/executor/exceptions/PyException;->err:Lpbi/executor/exceptions/RuntimeError;
          (39, 1), # throw v1

          (-1, L),
          (98, 2, NoneField), # sget-object v2, Lpbi/executor/Main;->None:Lpbi/executor/types/NoneType;
          (110, ExitMethod, (1, 2, 2)), # invoke-virtual {v1, v2, v2}, Lpbi/executor/types/Base;->__exit__(Lpbi/executor/types/Base;Lpbi/executor/types/Base;)Lpbi/executor/types/Base;

          (-1, no_throw),
        ))

      # 56

      case 57: # last_exception = None
        extend((
          (98, 1, NoneField), # sget-object v1, Lpbi/executor/Main;->None:Lpbi/executor/types/NoneType;
          (91, (1, p0), ClassName + LastExcField), # iput-object v1, p0, {ClassName}->last_exc:Lpbi/executor/types/Base;
        ))

      # 58

      case 59: # %0 <- "package%1"
        extend((
          (26, 2, line[2]), # const-string v2, {line[2]}
          (34, 1, JavaWrapType), # new-instance v1, Lpbi/executor/types/JavaWrap;
          (112, JavaWrapCtor, (1, 2)), # invoke-direct {v1, v2}, Lpbi/executor/types/JavaWrap;-><init>(Ljava/lang/String;)V
        ))
        put_var(line[1], 1) # var(line[1]) = v1

      case 60: # v%0 = reg v%1
        append((18, 1, line[1])) # const v1 = {line[1]}
        get_reg(2, line[2]) # const v2 = regs[line[2]]
        append((77, 2, 0, 1)) # aput-object v0[v1] = v2

      # 61..66

      case 4 | 67:
        # 4: try: v%0 = v%1.__next__()\nexcept StopIteration: goto %2
        # 67: try: %0 = v%1.__next__()\nexcept StopIteration: goto %2
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        L = len(codes)
        try_start = L # метки могут быть, вполне, и просто числами
        try_end = L + 1
        catch = -(pos + line[3])
        extend((
          (-1, try_start),
          (110, NextMethod, (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__next__()Lpbi/executor/types/Base;
          (-1, try_end),
          (12, 1), # move-result-object v1
        ))
        if line[0] == 4: put_reg(line[1], 1) # regs[line[1]] = v1
        else: put_var(line[1], 1) # var(line[1]) = v1

        # Гениально!!! goto в случае StopIteration использовать напрямую в качестве catch-блока! 
        # Интересно, что будет с JaDX после этого?! По опыту говорю, что try-catch-finally-конструкции для него - боль
        # Вывод: надо же... JaDX умеет использовать while (true) { ... }, чтобы имитировать поведение goto внутри catch-смещения
        try_add((try_start, try_end, ((StopIterationType, catch),), None))

      # 68

      case 69: # v%0 = v%1.__iter__()   (3)
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        extend((
          (110, IterMethod, (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__iter__()Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
        ))
        put_reg(line[1], 1) # regs[line[1]] = 1

      # 70

      case 71..89: # v%0 = v%1 {maths} v%2   (14..32)
        code, out, in1, in2 = line
        # print("math:", line, maths[code - 71])
        get_reg(1, in1) # const v1 = regs[in1] (Левый операнд)
        get_reg(2, in2) # const v2 = regs[in2] (Правый операнд)
        extend((
          (110, BinaryMethods[code - 71], (1, 2)), # invoke-virtual {v1, v2}, Lpbi/executor/types/Base;->__add__(Lpbi/executor/types/Base;)Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
          (18, 2, out), # const v2 = {out}
          (77, 1, 0, 2), # aput-object v0[v2] = v1
        ))

      case 90: # v%0 = v%1 in v%2   (33)
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        get_reg(2, line[3]) # const v2 = regs[line[3]]
        extend((
          (110, ContainsMethod, (2, 1)), # invoke-virtual {v2, v1}, Lpbi/executor/types/Base;->__contains__(Lpbi/executor/types/Base;)Lpbi/executor/types/pBoolean;
          (12, 1), # move-result-object v1
        ))
        put_reg(line[1], 1) # regs[line[1]] = v1

      case 91: # v%0 = v%1 is v%2   (34)
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        get_reg(2, line[3]) # const v2 = regs[line[3]]
        extend((
          (51, (1, 2), 5), # if-ne v1, v2, :{+5 * 2 bytes}   4+4+2 = 10 bytes
          (98, 1, TrueField), # sget-object v1, Lpbi/executor/Main;->True:Lpbi/executor/types/pBoolean;
          (40, 3), # goto :{+3 * 2 bytes}   2+4 = 6 bytes
          (98, 1, FalseField), # sget-object v1, Lpbi/executor/Main;->False:Lpbi/executor/types/pBoolean;
        ))
        put_reg(line[1], 1) # regs[line[1]] = v1

      case 35 | 92:
        # 35: v%0 = not v%0
        # 92: v%0 = not v%1   (35)
        inout = line[0] == 35
        if inout: get_reg(1, line[1], 3) # const v3 = {line[1]}, v1 = regs[v3]
        else: get_reg(1, line[2]) # const v1 = regs[line[2]]
        extend((
          (110, BoolMethod, (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__bool()Z
          (10, 1), # move-result v1
          (56, 1, 5), # if-eqz v1, :{+5 * 2 bytes}   4+4+2 = 10 bytes
          (98, 1, FalseField), # sget-object v1, Lpbi/executor/Main;->False:Lpbi/executor/types/pBoolean;
          (40, 3), # goto :{+3 * 2 bytes}   2+4 = 6 bytes
          (98, 1, TrueField), # sget-object v1, Lpbi/executor/Main;->True:Lpbi/executor/types/pBoolean;
          (18, 2, line[1]), # const v2 = {line[1]}
          (77, 1, 0, 3 if inout else 2), # aput-object v0[v2|v3] = v1
        ))

      case 37 | 93:
        # 37: v%0 = v%0(%1_args)
        # 93: v%0 = v%1(%2_args)   (37)
        if line[0] == 37:
          out = _in = line[1]
          args = line[2]
        else:
          out = line[1]
          _in = line[2]
          args = line[3]
        if args: make_base_array(args) # v1 = new Base[] {...arg_regs}
        else: append((98, 1, ClassName + VoidArrField)) # sget-object v1, {ClassName}->void_arr:[Lpbi/executor/types/Base;
        extend((
          (18, 2, _in), # const v2 = {_in}
          (70, 2, 0, 2), # aget-object v2 = v0[v2]
          (98, 3, ClassName + VoidMapField), # sget-object v3, {ClassName}->void_map:Ljava/util/Map;
          (110, CallerMethod, (2, 1, 3)), # invoke-virtual {v2, v1, v3}, Lpbi/executor/types/Base;->__call__([Lpbi/executor/types/Base;Ljava/util/Map;)Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
          (18, 2, out), # const v2 = {out}
          (77, 1, 0, 2), # aput-object v0[v2] = v1
        ))

      case 94: # v%0 = [v%1]     makelist   (39)
        get_reg(1, line[2]) # const v1 = regs[line[2]]
        extend((
          (34, 2, 'Ljava/util/ArrayList;'), # new-instance v2, Ljava/util/ArrayList;
          (112, 'Ljava/util/ArrayList;-><init>()V', (2,)), # invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V
          (110, 'Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z', (2, 1)), # invoke-virtual {v2, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
          (34, 1, ListType), # new-instance v1, Lpbi/executor/types/List;
          (112, ListCtor2, (1, 2)), # invoke-direct {v1, v2}, Lpbi/executor/types/List;-><init>(Ljava/util/ArrayList;)V
        ))
        put_reg(line[1], 1) # regs[line[1]] = v1

      case 95..97: # v%0 = {unars}v%1   (51..53)
        code, out, _in = line
        # print("unar:", line, unars[line[0] - 95])
        get_reg(1, _in) # const v1 = regs[_in] (Правый операнд)
        extend((
          (110, UnaryMethods[code - 95], (1,)), # invoke-virtual {v1}, Lpbi/executor/types/Base;->__neg__()Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
          (18, 2, out), # const v2 = {out}
          (77, 1, 0, 2), # aput-object v0[v2] = v1
        ))

      # 98..99

      case _: raise Exception("code_%s not supported!" % line[0])

  # for line in codes: print(line)

  return (registers, inputs, outsSize, None, codes, tries)



def apply_consts(ClassName, extend, append, consts, end):
  fields = []; field_add = fields.append
  for c_num, const in enumerate(consts):
    T = type(const)
    name = "c%s" % c_num
    field_name = "%s:%s" % (name, BaseType)
    if T is int:
      b_arr = const.to_bytes(None, "little", True)
      end((-1, c_num))
      end((0, 3, 1, b_arr))
      extend((
        (34, 0, BigIntType), # new-instance v0, Lpbi/executor/types/BigInt;
        (18, 1, len(b_arr)), # const v1 = {len(b_arr)}
        (35, (1, 1), '[B'), # new-array v1, v1, [B
        (38, 1, c_num), # fill_array_data v1, {c_num}
        (112, BigIntCtor, (0, 1)), # invoke-direct {v0, v1}, Lpbi/executor/types/BigInt;-><init>([B)V
        (105, 0, '%s->%s' % (ClassName, field_name)), # sput-object v0, {...}
      ))
    elif T is tuple: # уже давно как, tuple у меня попадает под свёртку констант, а вот range, enumerate и прочее, увы, пока нет, т.к. я недавно это заметил в оригинальном питоне
      extend((
        (18, 0, len(const)), # const v0 = {len(const)}
        (35, (0, 0), BaseArrType), # new-array v0, v0, [Lpbi/executor/types/Base;
      ))
      for n, const in enumerate(const):
        field2_name = "%s->c%s:%s" % (ClassName, const, BaseType)
        extend((
          (18, 1, n), # const v1 = {n}
          (98, 2, field2_name), # sget-object v2, {...}
          (77, 2, 0, 1), # aput-object v0[v1] = v2
        ))
      extend((
        (34, 1, TupleType), # new-instance v1, Lpbi/executor/types/Tuple;
        (112, TupleCtor, (1, 0)), # invoke-direct {v1, v0}, Lpbi/executor/types/Tuple;-><init>([Lpbi/executor/types/Base;)V
        (105, 1, '%s->%s' % (ClassName, field_name)), # sput-object v1, {...}
      ))
    elif T is str:
      extend((
        (34, 0, StringType), # new-instance v0, Lpbi/executor/types/pString;
        (26, 1, const), # const-string v1, {const}
        (112, StringCtor, (0, 1)), # invoke-direct {v0, v1}, Lpbi/executor/types/pString;-><init>(Ljava/lang/String;)V
        (105, 0, '%s->%s' % (ClassName, field_name)), # sput-object v0, {...}
      ))
    elif T is bytes:
      end((-1, c_num))
      end((0, 3, 1, const))
      extend((
        (34, 0, BytesType), # new-instance v0, Lpbi/executor/types/Bytes;
        (18, 1, len(const)), # const v1 = {len(b_arr)}
        (35, (1, 1), '[B'), # new-array v1, v1, [B
        (38, 1, c_num), # fill_array_data v1, {c_num}
        (112, BytesCtor, (0, 1)), # invoke-direct {v0, v1}, Lpbi/executor/types/Bytes;-><init>([B)V
        (105, 0, '%s->%s' % (ClassName, field_name)), # sput-object v0, {...}
      ))
    elif T is bool:
      if const: append((98, 0, TrueField)) # sget-object v0, Lpbi/executor/Main;->True:Lpbi/executor/types/pBoolean;
      else: append((98, 0, FalseField)) # sget-object v0, Lpbi/executor/Main;->False:Lpbi/executor/types/pBoolean;
      append((105, 0, '%s->%s' % (ClassName, field_name))) # sput-object v0, {...}
    elif T is float: # Пропустил случайно float - потерял 2 часа на попытках понять, почему sin(pi * 1.5) не работает... Получалось: sin(pi * None) => sin(NotImplemented)
      extend((
        (34, 0, FloatType), # new-instance v0, Lpbi/executor/types/pFloat;
        (24, 1, const), # const-wide v1, {const}
        (112, FloatCtor, (0, 1, 2)), # invoke-direct {v0, v1, v2}, Lpbi/executor/types/pFloat;-><init>(D)V
        (105, 0, '%s->%s' % (ClassName, field_name)), # sput-object v0, {...}
      ))
    else:
      assert const is None, "type: %s" % T
      extend((
        (98, 0, NoneField), # sget-object v0, Lpbi/executor/Main;->None:Lpbi/executor/types/NoneType;
        (105, 0, '%s->%s' % (ClassName, field_name)), # sput-object v0, {...}
      ))
    field_add((IS_STATIC_FIELD, field_name, ACCESS_STATIC | ACCESS_PRIVATE, None, (), None, {}))
  return fields



def python2java(code):
  jClassName = "pbi.eval.Main"
  ClassName = DVM_name(jClassName)

  defs, b_links, consts = code
  print("b_links:", b_links)
  print("consts:", consts)

  analysis = {}
  for idx, reg in b_links:
    try: analysis[reg] = bultin_expections[idx]
    except KeyError: pass

  for id, (counts, args, codes, labels, tries, local_consts) in enumerate(defs):
    rln_count, names = counts
    local_consts = {k: v for k, v in local_consts}

    print("~" * 53)
    print("id:", id)
    print("rln_count:", rln_count)
    print("names:", names)
    print("args:", args)
    for line in codes:
      print("•", line)
    print("labels:", labels)
    # print("tries:", tries)
    print("local_consts:", local_consts)

    assert id == 0

    inputs = 1
    module_func = builder(ClassName, inputs, codes, tries, local_consts, analysis)

  print("~" * 53)

  global_regs = defs[0][0][0]
  annot = ('Ldalvik/annotation/Throws;', ((28, 'value', ((24, 'Lpbi/executor/exceptions/RuntimeError;'),)),), 'system')

  clinit_codes = [
    (34, 0, 'Ljava/util/HashMap;'),              # new-instance v0, Ljava/util/HashMap;
    (112, 'Ljava/util/HashMap;-><init>()V', (0,)), # invoke-direct {v0}, Ljava/util/HashMap;-><init>()V
    (105, 0, ClassName + VoidMapField), # sput-object v0, {ClassName}->void_map:Ljava/util/Map;
    (18, 0, 0), # const v0 = 0
    (35, (0, 0), BaseArrType),  # new-array v0, v0, [Lpbi/executor/types/Base;
    (105, 0, ClassName + VoidArrField), # sput-object v0, {ClassName}->void_arr:[Lpbi/executor/types/Base;
  ]
  extend = clinit_codes.extend
  append = clinit_codes.append
  end = []; end_append = end.append
  const_fields = apply_consts(ClassName, extend, append, consts, end_append)
  # print(*clinit_codes, sep = "\n")
  append((14,)) # return-void
  extend(end)

  p0 = 4 - 1
  init_codes = [
    (112, 'Ljava/lang/Object;-><init>()V', (p0,)), # invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    (18, 0, global_regs), # const v0 = {global_regs}
    (35, (0, 0), BaseArrType),  # new-array v0, v0, [Lpbi/executor/types/Base;
    (91, (0, p0), ClassName + GlobalsField), # iput-object v0, p0, {ClassName}->globals:[Lpbi/executor/types/Base;
    (98, 1, NoneField), # sget-object v1, Lpbi/executor/Main;->None:Lpbi/executor/types/NoneType;
    (91, (1, p0), ClassName + LastExcField), # iput-object v1, p0, {ClassName}->last_exc:Lpbi/executor/types/Base;
  ]
  extend = init_codes.extend
  append = init_codes.append
  if b_links: append((98, 1, BuiltinsField)) # sget-object v1, Lpbi/executor/Main;->builtins_arr:[Lpbi/executor/types/Base;
  for idx, reg in b_links:
    extend((
      (18, 2, idx), # const/4 v2, {idx}
      (18, 3, reg), # const/4 v3, {reg}
      (70, 2, 1, 2), # aget-object v2 = v1[v2]
      (77, 2, 0, 3), # aput-object v0[v3] = v2
    ))
  append((14,)) # return-void

  class_obj = (ClassName,
   ACCESS_PUBLIC,
   'Ljava/lang/Object;',
   (), None, (),
   (
    *const_fields,
    (IS_STATIC_FIELD, VoidArrField[2:], ACCESS_STATIC | ACCESS_PRIVATE, None, (), None, {}),
    (IS_STATIC_FIELD, VoidMapField[2:], ACCESS_STATIC | ACCESS_PRIVATE, None, (('Ldalvik/annotation/Signature;', ((28, 'value', ((23, '"Ljava/util/Map"'), (23, '"<"'), (23, '"Ljava/lang/String;"'), (23, '"%s"' % BaseType), (23, '">;"'))),), 'system'),), None, {}),
    (IS_INSTANCE_FIELD, GlobalsField[2:], ACCESS_NOFLAGS, None, (), None, {}),
    (IS_INSTANCE_FIELD, LastExcField[2:], ACCESS_NOFLAGS, None, (), None, {}),
    (IS_DIRECT_METHOD, '<clinit>()V', ACCESS_CONSTRUCTOR | ACCESS_STATIC, None, (),
     (4, 0, 3, None, clinit_codes, ()), {}),
    (IS_DIRECT_METHOD, '<init>()V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, (),
     (4, 1, 1, None, init_codes, ()), {}),
    (IS_VIRTUAL_METHOD, 'module()' + BaseType, ACCESS_NOFLAGS, None, (annot,), module_func, {})
   )
  )

  dexData = DexWriter((class_obj,))
  with open("/sdcard/Check.dex", "wb") as file:
    file.write(dexData)

  classLoader = dex(context, dexData)
  return classLoader(jClassName)



""" Результат декомпиляции "polygon.py":
//
// Decompiled by Jadx - 1446ms
//
package pbi.eval;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import pbi.executor.exceptions.NameError;
import pbi.executor.exceptions.RuntimeError;
import pbi.executor.exceptions.ValueError;
import pbi.executor.types.Base;
import pbi.executor.types.BigInt;
import pbi.executor.types.Bytes;
import pbi.executor.types.List;
import pbi.executor.types.Tuple;
import pbi.executor.types.pString;

public class Main {
    Base[] globals;
    private static Map<String, Base> void_map = new HashMap();
    private static Base[] void_arr = new Base[0];
    private static Base c0 = new BigInt(new byte[]{123});
    private static Base c1 = new BigInt(new byte[]{1});
    private static Base c2 = new BigInt(new byte[]{2});
    private static Base c3 = new BigInt(new byte[]{3});
    private static Base c4 = new BigInt(new byte[]{Byte.MAX_VALUE});
    private static Base c5 = new BigInt(new byte[]{0, Byte.MIN_VALUE});
    private static Base c6 = new BigInt(new byte[]{-1});
    private static Base c7 = new BigInt(new byte[]{Byte.MIN_VALUE});
    private static Base c8 = new BigInt(new byte[]{-1, Byte.MAX_VALUE});
    private static Base c9 = new Tuple(new Base[]{c1, c2, c3, c4, c5, c6, c7, c8});
    private static Base c10 = new BigInt(new byte[]{4, -46});
    private static Base c11 = new BigInt(new byte[]{0});
    private static Base c12 = new Tuple(new Base[]{c1, c2, c3});
    private static Base c13 = new pString("Пора добавить оставшиеся типы констант:\nстрока");
    private static Base c14 = new Bytes(new byte[]{98, 121, 116, 101, 115});
    private static Base c15 = pbi.executor.Main.None;
    private static Base c16 = pbi.executor.Main.True;
    private static Base c17 = pbi.executor.Main.False;
    private static Base c18 = new BigInt(new byte[]{5});
    private static Base c19 = new BigInt(new byte[]{4});
    private static Base c20 = new BigInt(new byte[]{6});
    private static Base c21 = new Tuple(new Base[]{c19, c18, c20});
    private static Base c22 = new BigInt(new byte[]{7});
    private static Base c23 = new BigInt(new byte[]{8});
    private static Base c24 = new BigInt(new byte[]{9});
    private static Base c25 = new Tuple(new Base[]{c22, c23, c24});
    private static Base c26 = new BigInt(new byte[]{-2});
    private static Base c27 = new BigInt(new byte[]{-5});

    public Main() {
        Base[] baseArr = new Base[52];
        this.globals = baseArr;
        Base[] baseArr2 = pbi.executor.Main.builtins_arr;
        baseArr[17] = baseArr2[0];
        baseArr[18] = baseArr2[17];
        baseArr[19] = baseArr2[10];
        baseArr[20] = baseArr2[11];
        baseArr[21] = baseArr2[12];
    }

    Base module() throws RuntimeError {
        Base[] baseArr = this.globals;
        baseArr[0] = baseArr[17].__call__(new Base[]{c0}, void_map);
        baseArr[0] = baseArr[17].__call__(void_arr, void_map);
        baseArr[0] = baseArr[17].__call__(new Base[]{c9}, void_map);
        baseArr[1] = c0.__add__(c5);
        baseArr[2] = c0.__sub__(c5);
        baseArr[3] = c0.__mul__(c5);
        baseArr[4] = c5.__truediv__(c2);
        baseArr[5] = c0.__floordiv__(c2);
        baseArr[6] = c10.__mod__(c0);
        baseArr[7] = c0.__pow__(c3);
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[1], baseArr[2], baseArr[3], baseArr[4], baseArr[5], baseArr[6], baseArr[7]}, void_map);
        baseArr[1] = c10.__and__(c4);
        baseArr[2] = c10.__xor__(c5);
        baseArr[3] = c10.__or__(c5);
        baseArr[4] = c10.__lshift__(c3);
        baseArr[5] = c10.__rshift__(c3);
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[1], baseArr[2], baseArr[3], baseArr[4], baseArr[5]}, void_map);
        baseArr[1] = c10.__pos__();
        baseArr[2] = c10.__neg__();
        baseArr[3] = c10.__invert__();
        baseArr[4] = c10.__bool() ? pbi.executor.Main.False : pbi.executor.Main.True;
        baseArr[5] = c11.__bool() ? pbi.executor.Main.False : pbi.executor.Main.True;
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[1], baseArr[2], baseArr[3], baseArr[4], baseArr[5]}, void_map);
        baseArr[1] = c1.__lt(c2);
        baseArr[2] = c1.__eq(c2);
        baseArr[3] = c1.__gt(c2);
        baseArr[4] = c1.__le(c2);
        baseArr[5] = c1.__ne(c2);
        baseArr[6] = c1.__ge(c2);
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[1], baseArr[2], baseArr[3], baseArr[4], baseArr[5], baseArr[6]}, void_map);
        baseArr[1] = baseArr[19].__call__(new Base[]{c10}, void_map);
        Base base = baseArr[1];
        if (base == null) {
            throw new NameError("name 'regs:1' is not defined");
        }
        Base base2 = baseArr[20];
        if (base2 == null) {
            throw new NameError("name 'regs:20' is not defined");
        }
        baseArr[1] = base == base2 ? pbi.executor.Main.True : pbi.executor.Main.False;
        baseArr[2] = baseArr[19].__call__(new Base[]{c10}, void_map);
        Base base3 = baseArr[2];
        if (base3 == null) {
            throw new NameError("name 'regs:2' is not defined");
        }
        Base base4 = baseArr[18];
        if (base4 == null) {
            throw new NameError("name 'regs:18' is not defined");
        }
        baseArr[2] = base3 == base4 ? pbi.executor.Main.True : pbi.executor.Main.False;
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[1], baseArr[2]}, void_map);
        baseArr[1] = c12.__contains__(c2);
        baseArr[2] = c12.__contains__(c4);
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[1], baseArr[2]}, void_map);
        baseArr[0] = baseArr[17].__call__(new Base[]{c13, c14, c15, c16, c17}, void_map);
        baseArr[12] = new List();
        Base base5 = c1;
        ArrayList arrayList = new ArrayList();
        arrayList.add(base5);
        baseArr[16] = new List(arrayList);
        baseArr[0] = new List(3);
        Base base6 = baseArr[0];
        if (base6 == null) {
            throw new NameError("name 'regs:0' is not defined");
        }
        base6.__setitem__(0, c1);
        Base base7 = baseArr[0];
        if (base7 == null) {
            throw new NameError("name 'regs:0' is not defined");
        }
        base7.__setitem__(1, c2);
        Base base8 = baseArr[0];
        if (base8 == null) {
            throw new NameError("name 'regs:0' is not defined");
        }
        base8.__setitem__(2, c3);
        Base base9 = baseArr[0];
        if (base9 == null) {
            throw new NameError("name 'regs:0' is not defined");
        }
        baseArr[10] = base9;
        Base base10 = baseArr[10];
        if (base10 == null) {
            throw new NameError("name 'regs:10' is not defined");
        }
        baseArr[0] = base10.__getitem__(-1);
        Base base11 = baseArr[0];
        if (base11 == null) {
            throw new NameError("name 'regs:0' is not defined");
        }
        baseArr[0] = base11.__mul__(c18);
        Base base12 = baseArr[10];
        if (base12 == null) {
            throw new NameError("name 'regs:10' is not defined");
        }
        Base base13 = baseArr[0];
        if (base13 == null) {
            throw new NameError("name 'regs:0' is not defined");
        }
        base12.__setitem__(0, base13);
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[12], baseArr[16], baseArr[10]}, void_map);
        Base base14 = baseArr[10];
        if (base14 == null) {
            throw new NameError("name 'regs:10' is not defined");
        }
        int __len = base14.__len();
        if (__len > 3) {
            throw new ValueError("too many values to unpack (expected 3)");
        }
        if (__len < 3) {
            throw new ValueError("not enough values to unpack (expected 3, got" + __len + ")");
        }
        Base base15 = baseArr[10];
        if (base15 == null) {
            throw new NameError("name 'regs:10' is not defined");
        }
        baseArr[14] = base15.__getitem__(0);
        Base base16 = baseArr[10];
        if (base16 == null) {
            throw new NameError("name 'regs:10' is not defined");
        }
        baseArr[13] = base16.__getitem__(1);
        Base base17 = baseArr[10];
        if (base17 == null) {
            throw new NameError("name 'regs:10' is not defined");
        }
        baseArr[15] = base17.__getitem__(2);
        baseArr[11] = new Tuple(new Base[]{baseArr[14], baseArr[13], baseArr[13], baseArr[15], baseArr[13], baseArr[14], baseArr[15]});
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[11]}, void_map);
        baseArr[2] = baseArr[21].__call__(new Base[]{c2, c6}, void_map);
        Base base18 = baseArr[11];
        if (base18 == null) {
            throw new NameError("name 'regs:11' is not defined");
        }
        Base base19 = baseArr[2];
        if (base19 == null) {
            throw new NameError("name 'regs:2' is not defined");
        }
        baseArr[1] = base18.__getitem__(base19);
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[1]}, void_map);
        baseArr[2] = baseArr[21].__call__(new Base[]{c1, c2}, void_map);
        Base base20 = baseArr[10];
        if (base20 == null) {
            throw new NameError("name 'regs:10' is not defined");
        }
        Base base21 = baseArr[2];
        if (base21 == null) {
            throw new NameError("name 'regs:2' is not defined");
        }
        base20.__setitem__(base21, c21);
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[10]}, void_map);
        baseArr[2] = baseArr[21].__call__(new Base[]{c26, c27, c6}, void_map);
        Base base22 = baseArr[10];
        if (base22 == null) {
            throw new NameError("name 'regs:10' is not defined");
        }
        Base base23 = baseArr[2];
        if (base23 == null) {
            throw new NameError("name 'regs:2' is not defined");
        }
        base22.__setitem__(base23, c25);
        baseArr[0] = baseArr[17].__call__(new Base[]{baseArr[10]}, void_map);
        return pbi.executor.Main.None;
    }
}
"""



""" Вывод в консоль моего движка:
heap: 0.000669002532959
zlib: 0.0063240528106689
reader: 0.0153951644897461
b_links: ((0, 17), (17, 18), (10, 19), (11, 20), (12, 21))
consts: (123, 1, 2, 3, 127, 128, -1, -128, -129, (1, 2, 3, 4, 5, 6, 7, 8), 1234, 0, (1, 2, 3), 'Пора добавить оставшиеся типы констант:\nстрока', b'bytes', None, True, False, 5, 4, 6, (19, 18, 20), 7, 8, 9, (22, 23, 24), -2, -5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
id: 0
rln_count: 52
names: ()
args: ((), None, None)
• (93, 0, 17, (49,))
• (93, 0, 17, ())
• (93, 0, 17, (44,))
• (71, 1, 49, 35)
• (72, 2, 49, 35)
• (73, 3, 49, 35)
• (75, 4, 35, 43)
• (83, 5, 49, 43)
• (76, 6, 46, 49)
• (82, 7, 49, 33)
• (93, 0, 17, (1, 2, 3, 4, 5, 6, 7))
• (77, 1, 46, 47)
• (79, 2, 46, 35)
• (78, 3, 46, 35)
• (80, 4, 46, 33)
• (81, 5, 46, 33)
• (93, 0, 17, (1, 2, 3, 4, 5))
• (95, 1, 46)
• (96, 2, 46)
• (97, 3, 46)
• (92, 4, 46)
• (92, 5, 39)
• (93, 0, 17, (1, 2, 3, 4, 5))
• (84, 1, 41, 43)
• (86, 2, 41, 43)
• (85, 3, 41, 43)
• (88, 4, 41, 43)
• (89, 5, 41, 43)
• (87, 6, 41, 43)
• (93, 0, 17, (1, 2, 3, 4, 5, 6))
• (93, 1, 19, (46,))
• (34, 1, 20)
• (93, 2, 19, (46,))
• (34, 2, 18)
• (93, 0, 17, (1, 2))
• (90, 1, 43, 34)
• (90, 2, 47, 34)
• (93, 0, 17, (1, 2))
• (93, 0, 17, (40, 38, 31, 42, 36))
• (2, 12)
• (94, 16, 41)
• (0, 0, 3)
• (1, 0, 0, 41)
• (1, 0, 1, 43)
• (1, 0, 2, 33)
• (60, 10, 0)
• (6, 0, 10, -1)
• (16, 0, 32)
• (1, 10, 0, 0)
• (93, 0, 17, (12, 16, 10))
• (5, 3, 10)
• (6, 14, 10, 0)
• (6, 13, 10, 1)
• (6, 15, 10, 2)
• (45, 11, ((14, False), (13, False), (13, False), (15, False), (13, False), (14, False), (15, False)))
• (93, 0, 17, (11,))
• (93, 2, 21, (43, 48))
• (36, 1, 11, 2)
• (93, 0, 17, (1,))
• (93, 2, 21, (41, 43))
• (40, 10, 2, 51)
• (93, 0, 17, (10,))
• (93, 2, 21, (50, 37, 48))
• (40, 10, 2, 45)
• (93, 0, 17, (10,))
• (43,)
labels: ()
tries: ()
local_consts: {32: 18, 33: 3, 34: 12, 35: 5, 36: 17, 37: 27, 38: 14, 39: 11, 40: 13, 41: 1, 42: 16, 43: 2, 44: 9, 45: 25, 46: 10, 47: 4, 48: 6, 49: 0, 50: 26, 51: 21, 31: 15}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Сбор пулов
   1 Lpbi/eval/Main;

Запаковка классов
   1 Lpbi/eval/Main;

file_size: 7716
sha1: 4cc5bc14f90ec2e998c5b173cf81086c0709f7f2
adler32: 722536282
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
• module: pbi.eval.Main
{'c18': 5, 'c19': 4, 'c12': (1, 2, 3), 'c13': 'Пора добавить оставшиеся типы констант:\nстрока', 'c10': 1234, 'c11': 0, 'c16': True, 'c17': False, 'c14': b'bytes', 'c15': None, 'void_map': <object 'java.util.HashMap' at 0x0>, 'globals': '$non-static$', 'c4': 127, 'c5': 128, 'c6': -1, 'c7': -128, 'c0': 123, 'c1': 1, 'c2': 2, 'c3': 3, 'c8': -129, 'c9': (1, 2, 3, 127, 128, -1, -128, -129), 'c21': (4, 5, 6), 'c20': 6, 'c23': 8, 'c22': 7, 'c25': (7, 8, 9), 'c24': 9, 'c27': -5, 'c26': -2, 'void_arr': <object '[Lpbi.executor.types.Base;' at 0xe6d2fa7>}
{'module()': <methoder 'pbi.eval.Main'.module() at 0xdc07cf2>}
• inst: pbi.eval.Main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
123

(1, 2, 3, 127, 128, -1, -128, -129)
251 -5 15744 64.0 61 4 1860867
82 1106 1234 9872 154
1234 -1234 -1235 False True
True False False True True False
True False
True False
Пора добавить оставшиеся типы констант:
строка b'bytes' None True False
[] [1] [15, 2, 3]
(15, 2, 2, 3, 2, 15, 3)
(2, 3, 2, 15)
num: 1 range(1, 2)
[15, 4, 5, 6, 3]
num: 3 range(3, 0, -1)
num: 2 range(3, 0, -1)
num: 1 range(3, 0, -1)
[15, 9, 8, 7, 3]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
• returned: None
runtime: 0.1082241535186768
"""
