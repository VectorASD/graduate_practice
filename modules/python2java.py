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

def DVM_name(class_name):
  return "L%s;" % class_name.replace('.', '/')



def builder(ClassName, inputs, py_codes, local_consts):
  registers = 6
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
      (34, 1, 'Lpbi/executor/exceptions/NameError;'), # new-instance v1, Lpbi/executor/exceptions/NameError;
      (26, 2, "name 'regs:%s' is not defined" % py_reg), # const-string v2, "name 'regs:{py_reg}' is not defined"
      (112, 'Lpbi/executor/exceptions/NameError;-><init>(Ljava/lang/String;)V', (1, 2)), # invoke-direct {v1, v2}, Lpbi/executor/exceptions/NameError;-><init>(Ljava/lang/String;)V
      (39, 1), # throw v1
    ))

  def get_reg(reg, py_reg):
    try:
      const = local_consts[py_reg]
      field_name = "%s->c%s:Lpbi/executor/types/Base;" % (ClassName, const)
      append((98, reg, field_name)) # sget-object v{reg}, {...}
      return
    except KeyError: pass
    extend((
      (18, reg, py_reg), # const v{reg} = v{py_reg}
      (70, reg, 0, reg), # aget-object v{reg} = v0[v{reg}]
    ))
    reg_is_null(reg, py_reg)

  codes = [
    # (7, 0, p1), # move-object v0, p1
    # (84, (0, 0), 'Lpbi/executor/RegLocs;->regs:[Lpbi/executor/types/Base;'), # iget-object v0, v0, Lpbi/executor/RegLocs;->regs:[Lpbi/executor/types/Base;
    (84, (0, p0), ClassName + '->globals:[Lpbi/executor/types/Base;'), # iget-object v0, p0, {ClassName}->globals:[Lpbi/executor/types/Base;
  ]
  extend = codes.extend
  append = codes.append

  for line in py_codes:
    match line[0]:
      case 43: # return
        extend((
          (98, 0, 'Lpbi/executor/Main;->None:Lpbi/executor/types/NoneType;'), # sget-object v0, Lpbi/executor/Main;->None:Lpbi/executor/types/NoneType;
          (17, 0), # return-object v0
        ))

      case 60: # v%0 = reg v%1
        append((18, 1, line[1])) # const v1 = {line[1]}
        get_reg(2, line[2]) # const v2 = regs[line[2]]
        append((77, 2, 0, 1)) # aput-object v0[v1] = v2

      case 93: # v%0 = v%1(%2_args)   (37)
        out = line[1]
        _in = line[2]
        args = line[3]
        if args:
          extend((
            (18, 1, len(args)), # const v1 = {len(args)}
            (35, (1, 1), '[Lpbi/executor/types/Base;'),  # new-array v1, v1, [Lpbi/executor/types/Base;
          ))
          for i, arg in enumerate(args):
            append((18, 2, i)) # const v2 = {i}
            get_reg(3, arg) # const v3 = regs[arg]
            append((77, 3, 1, 2)) # aput-object v1[v2] = v3
        else: append((98, 1, ClassName + '->void_arr:[Lpbi/executor/types/Base;')) # sget-object v1, {ClassName}->void_arr:[Lpbi/executor/types/Base;
        extend((
          (18, 2, _in), # const v2 = {_in}
          (70, 2, 0, 2), # aget-object v2 = v0[v2]
          (98, 3, ClassName + '->void_map:Ljava/util/Map;'), # sget-object v3, {ClassName}->void_map:Ljava/util/Map;
          (110, 'Lpbi/executor/types/Base;->__call__([Lpbi/executor/types/Base;Ljava/util/Map;)Lpbi/executor/types/Base;', (2, 1, 3)), # invoke-virtual {v2, v1, v3}, Lpbi/executor/types/Base;->__call__([Lpbi/executor/types/Base;Ljava/util/Map;)Lpbi/executor/types/Base;
          (12, 1), # move-result-object v1
          (18, 2, out), # const v2 = {out}
          (77, 1, 0, 2), # aput-object v0[v2] = v1
        ))

      case _: raise Exception("code_%s not supported!" % line[0])

  # for line in codes: print(line)

  tries = ()
  return (registers, inputs, outsSize, None, codes, tries)



def apply_consts(ClassName, extend, consts, end):
  fields = []; field_add = fields.append
  for c_num, const in enumerate(consts):
    T = type(const)
    name = "c%s" % c_num
    field_name = name + ":Lpbi/executor/types/Base;"
    if T is int:
      label = ":array_" + name
      b_arr = const.to_bytes(None, "little", True)
      end((-1, label))
      end((0, 3, 1, b_arr))
      extend((
        (34, 0, 'Lpbi/executor/types/BigInt;'), # new-instance v0, Lpbi/executor/types/BigInt;
        (18, 1, len(b_arr)), # const v1 = {len(b_arr)}
        (35, (1, 1), '[B'), # new-array v1, v1, [B
        (38, 1, label), # fill_array_data v1, {label}
        (112, 'Lpbi/executor/types/BigInt;-><init>([B)V', (0, 1)), # invoke-direct {v0, v1}, Lpbi/executor/types/BigInt;-><init>([B)V
        (105, 0, '%s->%s' % (ClassName, field_name)), # sput-object v0, {...}
      ))
    elif T is tuple: # уже давно как, tuple у меня попадает под свёртку констант, а вот range, enumerate и прочее, увы, пока нет, т.к. я недавно это заметил в оригинальном питоне
      extend((
        (18, 0, len(const)), # const v0 = {len(const)}
        (35, (0, 0), '[Lpbi/executor/types/Base;'), # new-array v0, v0, [Lpbi/executor/types/Base;
      ))
      for n, const in enumerate(const):
        field2_name = "%s->c%s:Lpbi/executor/types/Base;" % (ClassName, const)
        extend((
          (18, 1, n), # const v1 = {n}
          (98, 2, field2_name), # sget-object v2, {...}
          (77, 2, 0, 1), # aput-object v0[v1] = v2
        ))
      extend((
        (34, 1, 'Lpbi/executor/types/Tuple;'), # new-instance v1, Lpbi/executor/types/Tuple;
        (112, 'Lpbi/executor/types/Tuple;-><init>([Lpbi/executor/types/Base;)V', (1, 0)), # invoke-direct {v1, v0}, Lpbi/executor/types/Tuple;-><init>([Lpbi/executor/types/Base;)V
        (105, 1, '%s->%s' % (ClassName, field_name)), # sput-object v1, {...}
      ))
    else: 1/0
    field_add((IS_STATIC_FIELD, field_name, ACCESS_STATIC | ACCESS_PRIVATE, None, (), None, {}))
  return fields



def python2java(code):
  jClassName = "pbi.eval.Main"
  ClassName = DVM_name(jClassName)

  defs, b_links, consts = code
  print("b_links:", b_links)
  print("consts:", consts)
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
    print("tries:", tries)
    print("local_consts:", local_consts)

    assert id == 0

    inputs = 1
    module_func = builder(ClassName, inputs, codes, local_consts)

  print("~" * 53)

  global_regs = defs[0][0][0]
  annot = ('Ldalvik/annotation/Throws;', ((28, 'value', ((24, 'Lpbi/executor/exceptions/RuntimeError;'),)),), 'system')

  clinit_codes = [
    (34, 0, 'Ljava/util/HashMap;'),              # new-instance v0, Ljava/util/HashMap;
    (112, 'Ljava/util/HashMap;-><init>()V', (0,)), # invoke-direct {v0}, Ljava/util/HashMap;-><init>()V
    (105, 0, ClassName + '->void_map:Ljava/util/Map;'), # sput-object v0, {ClassName}->void_map:Ljava/util/Map;
    (18, 0, 0), # const v0 = 0
    (35, (0, 0), '[Lpbi/executor/types/Base;'),  # new-array v0, v0, [Lpbi/executor/types/Base;
    (105, 0, ClassName + '->void_arr:[Lpbi/executor/types/Base;'), # sput-object v0, {ClassName}->void_arr:[Lpbi/executor/types/Base;
  ]
  extend = clinit_codes.extend
  append = clinit_codes.append
  end = []; end_append = end.append
  const_fields = apply_consts(ClassName, extend, consts, end_append)
  append((14,)) # return-void
  extend(end)

  p0 = 4 - 1
  init_codes = [
    (112, 'Ljava/lang/Object;-><init>()V', (p0,)), # invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    (18, 0, global_regs), # const v0 = {global_regs}
    (35, (0, 0), '[Lpbi/executor/types/Base;'),  # new-array v0, v0, [Lpbi/executor/types/Base;
    (91, (0, p0), ClassName + '->globals:[Lpbi/executor/types/Base;'), # iput-object v0, p0, {ClassName}->globals:[Lpbi/executor/types/Base;
  ]
  extend = init_codes.extend
  append = init_codes.append
  if b_links: append((98, 1, 'Lpbi/executor/Main;->builtins_arr:[Lpbi/executor/types/Base;')) # sget-object v1, Lpbi/executor/Main;->builtins_arr:[Lpbi/executor/types/Base;
  for idx, reg in b_links:
    extend((
      (18, 2, idx), # const/4 v2, {idx}
      (18, 3, reg), # const/4 v3, {reg}
      (70, 2, 1, 2), # aget-object v2 = v1[v2]
      (77, 2, 0, 3), # aput-object v0[v3] = v2
    ))
  append((14,)) # return-void

  test_class = (ClassName,
   ACCESS_PUBLIC,
   'Ljava/lang/Object;',
   (), None, (),
   (
    *const_fields,
    (IS_STATIC_FIELD, 'void_arr:[Lpbi/executor/types/Base;', ACCESS_STATIC | ACCESS_PRIVATE, None, (), None, {}),
    (IS_STATIC_FIELD, 'void_map:Ljava/util/Map;', ACCESS_STATIC | ACCESS_PRIVATE, None, (('Ldalvik/annotation/Signature;', ((28, 'value', ((23, '"Ljava/util/Map"'), (23, '"<"'), (23, '"Ljava/lang/String;"'), (23, '"Lpbi/executor/types/Base;"'), (23, '">;"'))),), 'system'),), None, {}),
    (IS_INSTANCE_FIELD, 'globals:[Lpbi/executor/types/Base;', ACCESS_NOFLAGS, None, (), None, {}),
    (IS_DIRECT_METHOD, '<clinit>()V', ACCESS_CONSTRUCTOR | ACCESS_STATIC, None, (),
     (4, 0, 2, None, clinit_codes, ()), {}),
    (IS_DIRECT_METHOD, '<init>()V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, (),
     (4, 1, 1, None, init_codes, ()), {}),
    (IS_VIRTUAL_METHOD, 'module()Lpbi/executor/types/Base;', ACCESS_NOFLAGS, None, (annot,), module_func, {})
   )
  )

  dexData = DexWriter((test_class,))
  with open("/sdcard/Check.dex", "wb") as file:
    file.write(dexData)

  classLoader = dex(context, dexData)
  return classLoader(jClassName)



""" Результат декомпиляции "polygon.py":
//
// Decompiled by Jadx - 2232ms
//
package pbi.eval;

import java.util.HashMap;
import java.util.Map;
import pbi.executor.exceptions.NameError;
import pbi.executor.exceptions.RuntimeError;
import pbi.executor.types.Base;
import pbi.executor.types.BigInt;
import pbi.executor.types.Tuple;

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

    public Main() {
        Base[] baseArr = new Base[8];
        this.globals = baseArr;
        baseArr[3] = pbi.executor.Main.builtins_arr[0];
    }

    Base module() throws RuntimeError {
        Base[] baseArr = this.globals;
        baseArr[2] = c0;
        Base[] baseArr2 = new Base[1];
        Base base = baseArr[2];
        if (base == null) {
            throw new NameError("name 'regs:2' is not defined");
        }
        baseArr2[0] = base;
        baseArr[0] = baseArr[3].__call__(baseArr2, void_map);
        baseArr[0] = baseArr[3].__call__(void_arr, void_map);
        baseArr[0] = baseArr[3].__call__(new Base[]{c9}, void_map);
        return pbi.executor.Main.None;
    }
}
"""



""" Вывод в консоль моего движка:
heap: 0.0001461505889893
zlib: 0.0021228790283203
reader: 0.008105993270874
b_links: ((0, 3),)
consts: (123, 1, 2, 3, 127, 128, -1, -128, -129, (1, 2, 3, 4, 5, 6, 7, 8))
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
id: 0
rln_count: 8
names: ()
args: ((), None, None)
• (60, 2, 6)
• (93, 0, 3, (2,))
• (93, 0, 3, ())
• (93, 0, 3, (7,))
• (43,)
labels: ()
tries: ()
local_consts: {6: 0, 7: 9}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Сбор пулов
   1 Lpbi/eval/Main;

Запаковка классов
   1 Lpbi/eval/Main;
!!! 18 -> 19 (18, 0, 8)
!!! 18 -> 19 (18, 0, 8)

file_size: 2300
sha1: 0b43c065cce1466ba301501e8b0005884e05d5cb
adler32: 4106631436
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
• module: pbi.eval.Main
{'void_map': <object 'java.util.HashMap' at 0x0>, 'c9': (1, 2, 3, 127, 128, -1, -128, -129), 'c8': -129, 'c3': 3, 'c2': 2, 'c1': 1, 'c0': 123, 'c7': -128, 'c6': -1, 'c5': 128, 'c4': 127, 'globals': '$non-static$', 'void_arr': <object '[Lpbi.executor.types.Base;' at 0x7e43be8>}
{'module()': <methoder 'pbi.eval.Main'.module() at 0x7a8e2e7>}
• inst: pbi.eval.Main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
123

(1, 2, 3, 127, 128, -1, -128, -129)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
• returned: None
runtime: 0.0361521244049072
"""
