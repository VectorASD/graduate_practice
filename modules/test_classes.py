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

nan = float("nan")





wrap_class = ('Lpbi/secured/Wrap;',
 ACCESS_PUBLIC,
 'Ljava/lang/Object;',
 (), "GreatSource.java", (), # всё равно будет Unknown Source пишет в traceBack, как если бы я просто оставил None здесь
 ((IS_INSTANCE_FIELD, 'data:J', ACCESS_PRIVATE, None, (), None, {}),
  (IS_INSTANCE_FIELD, 'mul:J', ACCESS_PRIVATE, None, (), None, {}),
  (IS_INSTANCE_FIELD, 'orig:J', ACCESS_PRIVATE, None, (), None, {}),
  (IS_INSTANCE_FIELD, 'shift:J', ACCESS_PRIVATE, None, (), None, {}),
  (IS_DIRECT_METHOD, '<init>()V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, (),
   (3, 1, 3, 9,
    ((112, 'Ljava/lang/Object;-><init>()V', (2,)),
     (22, 0, 0),
     (112, 'Lpbi/secured/Wrap;->first(J)V', (2, 0, 1)),
     (14,)
    ), ()), {}),
  (IS_DIRECT_METHOD, '<init>(J)V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, (),
   (4, 3, 3, 7,
    ((112, 'Ljava/lang/Object;-><init>()V', (1,)),
     (112, 'Lpbi/secured/Wrap;->first(J)V', (1, 2, 3)),
     (14,)
    ), ()), {}),
  (IS_DIRECT_METHOD, 'first(J)V', ACCESS_PRIVATE, None, (),
   (6, 3, 3, 26,
    ((18, 0, 3),
     (19, 1, 32),
     (113, 'Lpbi/secured/Wrap;->randint(II)I', (0, 1)),
     (10, 0),
     (129, 0, 0),
     (90, (0, 3), 'Lpbi/secured/Wrap;->mul:J'),
     (19, 0, 10),
     (20, 1, 1000000),
     (113, 'Lpbi/secured/Wrap;->randint(II)I', (0, 1)),
     (10, 0),
     (129, 0, 0),
     (90, (0, 3), 'Lpbi/secured/Wrap;->shift:J'),
     (110, 'Lpbi/secured/Wrap;->set(J)V', (3, 4, 5)),
     (14,)
    ), ()), {}),
  (IS_DIRECT_METHOD, 'randint(II)I', ACCESS_STATIC | ACCESS_PRIVATE, None, (),
   (6, 2, 0, 13,
    ((113, 'Ljava/lang/Math;->random()D', ()),
     (11, 0),
     (145, 2, 5, 4),
     (216, (2, 2), 1),
     (131, 2, 2),
     (205, 0, 2),
     (138, 0, 0),
     (176, 0, 4),
     (15, 0)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'dec(J)V', ACCESS_PUBLIC, None, [('Ldalvik/annotation/Throws;', [(28, 'value', [(24, 'Ljava/lang/Exception;')])], 'system')],
   (6, 3, 3, 9,
    ((110, 'Lpbi/secured/Wrap;->secured_get()J', (3,)),
     (11, 0),
     (188, 0, 4),
     (110, 'Lpbi/secured/Wrap;->secured_set(J)V', (3, 0, 1)),
     (14,)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'get()J', ACCESS_PUBLIC, None, (),
   (5, 1, 0, 9,
    ((83, (0, 4), 'Lpbi/secured/Wrap;->data:J'),
     (83, (2, 4), 'Lpbi/secured/Wrap;->shift:J'),
     (188, 0, 2),
     (83, (2, 4), 'Lpbi/secured/Wrap;->mul:J'),
     (190, 0, 2),
     (16, 0)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'inc(J)V', ACCESS_PUBLIC, None, [('Ldalvik/annotation/Throws;', [(28, 'value', [(24, 'Ljava/lang/Exception;')])], 'system')],
   (6, 3, 3, 9,
    ((110, 'Lpbi/secured/Wrap;->secured_get()J', (3,)),
     (11, 0),
     (187, 0, 4),
     (110, 'Lpbi/secured/Wrap;->secured_set(J)V', (3, 0, 1)),
     (14,)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'secured_get()J', ACCESS_PUBLIC, None, [('Ldalvik/annotation/Throws;', [(28, 'value', [(24, 'Ljava/lang/Exception;')])], 'system')],
   (5, 1, 2, 19,
    ((110, 'Lpbi/secured/Wrap;->get()J', (4,)),
     (11, 0),
     (83, (2, 4), 'Lpbi/secured/Wrap;->orig:J'),
     (49, 2, 0, 2),
     (56, 2, 18, ':cond_12'),
     (34, 0, 'Ljava/lang/Exception;'),
     (26, 1, 'Нука живо удалил GG и не лезь в ОЗУ!!! XD'),
     (112, 'Ljava/lang/Exception;-><init>(Ljava/lang/String;)V', (0, 1)),
     (39, 0),
     (16, 0)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'secured_set(J)V', ACCESS_PUBLIC, None, (),
   (8, 3, 0, 19,
    ((83, (0, 5), 'Lpbi/secured/Wrap;->mul:J'),
     (189, 0, 6),
     (83, (2, 5), 'Lpbi/secured/Wrap;->mul:J'),
     (158, 2, 0, 2),
     (49, 2, 2, 6),
     (57, 2, 18, ':cond_12'),
     (83, (2, 5), 'Lpbi/secured/Wrap;->shift:J'),
     (187, 0, 2),
     (90, (0, 5), 'Lpbi/secured/Wrap;->data:J'),
     (90, (6, 5), 'Lpbi/secured/Wrap;->orig:J'),
     (14,)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'set(J)V', ACCESS_PUBLIC, None, (),
   (8, 3, 0, 11,
    ((83, (0, 5), 'Lpbi/secured/Wrap;->mul:J'),
     (189, 0, 6),
     (83, (2, 5), 'Lpbi/secured/Wrap;->shift:J'),
     (187, 0, 2),
     (90, (0, 5), 'Lpbi/secured/Wrap;->data:J'),
     (90, (6, 5), 'Lpbi/secured/Wrap;->orig:J'),
     (14,)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'yeah(J)Z', ACCESS_PUBLIC, None, [('Ldalvik/annotation/Throws;', [(28, 'value', [(24, 'Ljava/lang/Exception;')])], 'system')],
   (6, 3, 1, 12,
    ((110, 'Lpbi/secured/Wrap;->secured_get()J', (3,)),
     (11, 0),
     (49, 0, 0, 4),
     (58, 0, 10, ':cond_a'),
     (18, 0, 1),
     (15, 0),
     (18, 0, 0),
     (40, 9, ':goto_9')
    ), ()), {})
  )
)



arr_class = ('Lpbi/secured/Arr;',
 ACCESS_PUBLIC,
 'Ljava/lang/Object;',
 (), None, (),
 ((IS_INSTANCE_FIELD, 'data:[Lpbi/secured/Wrap;', ACCESS_PRIVATE, None, (), None, {}),
  (IS_INSTANCE_FIELD, 'size:Lpbi/secured/Wrap;', ACCESS_PRIVATE, None, (), None, {}),
  (IS_DIRECT_METHOD, '<init>(Lpbi/secured/Root;I)V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, (),
   (7, 3, 3, 31,
    ((112, 'Ljava/lang/Object;-><init>()V', (4,)),
     (34, 0, 'Lpbi/secured/Wrap;'),
     (129, 2, 6),
     (112, 'Lpbi/secured/Wrap;-><init>(J)V', (0, 2, 3)),
     (91, (0, 4), 'Lpbi/secured/Arr;->size:Lpbi/secured/Wrap;'),
     (35, (0, 6), '[Lpbi/secured/Wrap;'),
     (91, (0, 4), 'Lpbi/secured/Arr;->data:[Lpbi/secured/Wrap;'),
     (18, 0, 0),
     (52, (0, 6), 19, ':cond_13'),
     (14,),
     (84, (1, 4), 'Lpbi/secured/Arr;->data:[Lpbi/secured/Wrap;'),
     (34, 2, 'Lpbi/secured/Wrap;'),
     (112, 'Lpbi/secured/Wrap;-><init>()V', (2,)),
     (77, 2, 1, 0),
     (216, (0, 0), 1),
     (40, 16, ':goto_10')
    ), ()), {}),
  (IS_DIRECT_METHOD, 'pack()Ljava/lang/String;', ACCESS_PRIVATE, None, [('Ldalvik/annotation/Throws;', [(28, 'value', [(24, 'Ljava/lang/Exception;')])], 'system')],
   (7, 1, 2, 36,
    ((84, (0, 6), 'Lpbi/secured/Arr;->size:Lpbi/secured/Wrap;'),
     (110, 'Lpbi/secured/Wrap;->secured_get()J', (0,)),
     (11, 0),
     (132, 1, 0),
     (35, (2, 1), '[Ljava/lang/String;'),
     (18, 0, 0),
     (52, (0, 1), 19, ':cond_13'),
     (26, 0, ','),
     (113, 'Ljava/lang/String;->join(Ljava/lang/CharSequence;[Ljava/lang/CharSequence;)Ljava/lang/String;', (0, 2)),
     (12, 0),
     (17, 0),
     (84, (3, 6), 'Lpbi/secured/Arr;->data:[Lpbi/secured/Wrap;'),
     (70, 3, 3, 0),
     (110, 'Lpbi/secured/Wrap;->secured_get()J', (3,)),
     (11, 4),
     (113, 'Ljava/lang/Long;->toString(J)Ljava/lang/String;', (4, 5)),
     (12, 3),
     (77, 3, 2, 0),
     (216, (0, 0), 1),
     (40, 10, ':goto_a')
    ), ()), {}),
  (IS_DIRECT_METHOD, 'print(Ljava/lang/String;)V', ACCESS_STATIC | ACCESS_PRIVATE, None, (),
   (1, 1, 1, 4,
    ((113, 'Lpbi/executor/Main;->print(Ljava/lang/Object;)V', (0,)),
     (14,)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'test()V', ACCESS_PUBLIC, None, (),
   (5, 1, 3, 88,
    ((34, 0, 'Ljava/lang/StringBuilder;'),
     (26, 1, 'size: '),
     (112, 'Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V', (0, 1)),
     (84, (1, 4), 'Lpbi/secured/Arr;->size:Lpbi/secured/Wrap;'),
     (110, 'Lpbi/secured/Wrap;->get()J', (1,)),
     (11, 2),
     (110, 'Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;', (0, 2, 3)),
     (12, 0),
     (26, 1, ' '),
     (110, 'Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;', (0, 1)),
     (12, 0),
     (84, (1, 4), 'Lpbi/secured/Arr;->size:Lpbi/secured/Wrap;'),
     (110, 'Lpbi/secured/Wrap;->secured_get()J', (1,)),
     (11, 2),
     (110, 'Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;', (0, 2, 3)),
     (12, 0),
     (110, 'Ljava/lang/StringBuilder;->toString()Ljava/lang/String;', (0,)),
     (12, 0),
     (113, 'Lpbi/secured/Arr;->print(Ljava/lang/String;)V', (0,)),
     (34, 0, 'Ljava/lang/StringBuilder;'),
     (26, 1, 'data: '),
     (112, 'Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V', (0, 1)),
     (112, 'Lpbi/secured/Arr;->pack()Ljava/lang/String;', (4,)),
     (12, 1),
     (110, 'Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;', (0, 1)),
     (12, 0),
     (110, 'Ljava/lang/StringBuilder;->toString()Ljava/lang/String;', (0,)),
     (12, 0),
     (113, 'Lpbi/secured/Arr;->print(Ljava/lang/String;)V', (0,)),
     (26, 0, '~~~~~~~~~~'),
     (113, 'Lpbi/secured/Arr;->print(Ljava/lang/String;)V', (0,)),
     (14,),
     (13, 0),
     (34, 1, 'Ljava/lang/StringBuilder;'),
     (26, 2, 'ERROR: '),
     (112, 'Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V', (1, 2)),
     (110, 'Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;', (1, 0)),
     (12, 0),
     (110, 'Ljava/lang/StringBuilder;->toString()Ljava/lang/String;', (0,)),
     (12, 0),
     (113, 'Lpbi/secured/Arr;->print(Ljava/lang/String;)V', (0,)),
     (40, 67, ':goto_43')
    ), ((0, 67, [('Ljava/lang/Throwable;', 68)], None),)), {})
  )
)



class3_class = ('Lpbi/secured/Class3;',
 ACCESS_PUBLIC,
 'Ljava/lang/Object;',
 (), None, (),
 ((IS_INSTANCE_FIELD, 'obj:Lpbi/secured/Arr;', ACCESS_PRIVATE, None, (), None, {}),
  (IS_INSTANCE_FIELD, 'obj2:Lpbi/secured/Arr;', ACCESS_PRIVATE, None, (), None, {}),
  (IS_DIRECT_METHOD, '<init>(Lpbi/secured/Root;)V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, (),
   (4, 2, 3, 21,
    ((112, 'Ljava/lang/Object;-><init>()V', (2,)),
     (34, 0, 'Lpbi/secured/Arr;'),
     (18, 1, 5),
     (112, 'Lpbi/secured/Arr;-><init>(Lpbi/secured/Root;I)V', (0, 3, 1)),
     (91, (0, 2), 'Lpbi/secured/Class3;->obj:Lpbi/secured/Arr;'),
     (34, 0, 'Lpbi/secured/Arr;'),
     (19, 1, 10),
     (112, 'Lpbi/secured/Arr;-><init>(Lpbi/secured/Root;I)V', (0, 3, 1)),
     (91, (0, 2), 'Lpbi/secured/Class3;->obj2:Lpbi/secured/Arr;'),
     (14,)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'test()V', ACCESS_PUBLIC, None, (),
   (2, 1, 1, 11,
    ((84, (0, 1), 'Lpbi/secured/Class3;->obj:Lpbi/secured/Arr;'),
     (110, 'Lpbi/secured/Arr;->test()V', (0,)),
     (84, (0, 1), 'Lpbi/secured/Class3;->obj2:Lpbi/secured/Arr;'),
     (110, 'Lpbi/secured/Arr;->test()V', (0,)),
     (14,)
    ), ()), {})
  )
)



class2_class = ('Lpbi/secured/Class2;',
 ACCESS_PUBLIC,
 'Ljava/lang/Object;',
 (), None, (),
 ((IS_INSTANCE_FIELD, 'obj:Lpbi/secured/Class3;', ACCESS_PROTECTED, None, (), None, {}),
  (IS_DIRECT_METHOD, '<init>(Lpbi/secured/Root;)V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, (),
   (3, 2, 2, 11,
    ((112, 'Ljava/lang/Object;-><init>()V', (1,)),
     (34, 0, 'Lpbi/secured/Class3;'),
     (112, 'Lpbi/secured/Class3;-><init>(Lpbi/secured/Root;)V', (0, 2)),
     (91, (0, 1), 'Lpbi/secured/Class2;->obj:Lpbi/secured/Class3;'),
     (14,)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'test()V', ACCESS_PUBLIC, None, (),
   (2, 1, 1, 6,
    ((84, (0, 1), 'Lpbi/secured/Class2;->obj:Lpbi/secured/Class3;'),
     (110, 'Lpbi/secured/Class3;->test()V', (0,)),
     (14,)
    ), ()), {})
  )
)



class1_class = ('Lpbi/secured/Class1;',
 ACCESS_PUBLIC,
 'Ljava/lang/Object;',
 (), None, (),
 ((IS_STATIC_FIELD, 'HEX_DIGITS:[C', ACCESS_FINAL | ACCESS_STATIC, None, (), None, {}),
  (IS_STATIC_FIELD, 'arr_00:[B', ACCESS_FINAL | ACCESS_STATIC | ACCESS_PUBLIC, None, (), None, {}),
  (IS_STATIC_FIELD, 'arr_01:[B', ACCESS_FINAL | ACCESS_STATIC | ACCESS_PUBLIC, None, (), None, {}),
  (IS_STATIC_FIELD, 'arr_1:[B', ACCESS_FINAL | ACCESS_STATIC | ACCESS_PUBLIC, None, (), None, {}),
  (IS_STATIC_FIELD, 'arr_2:[S', ACCESS_FINAL | ACCESS_STATIC | ACCESS_PUBLIC, None, (), None, {}),
  (IS_STATIC_FIELD, 'arr_4:[I', ACCESS_FINAL | ACCESS_STATIC | ACCESS_PUBLIC, None, (), None, {}),
  (IS_STATIC_FIELD, 'arr_8:[J', ACCESS_FINAL | ACCESS_STATIC | ACCESS_PUBLIC, None, (), None, {}),
  (IS_INSTANCE_FIELD, 'obj:Lpbi/secured/Class2;', ACCESS_PUBLIC, None, (), None, {}),
  (IS_DIRECT_METHOD, '<clinit>()V', ACCESS_CONSTRUCTOR | ACCESS_STATIC, None, (),
   (9, 0, 0, 292,
    ((18, 8, 3),
     (19, 7, 10),
     (18, 6, 5),
     (18, 5, 2),
     (18, 4, 1),
     (19, 0, 16),
     (35, (0, 0), '[C'),
     (38, 0, 272, ':array_110'),
     (105, 0, 'Lpbi/secured/Class1;->HEX_DIGITS:[C'),
     (35, (0, 8), '[B'),
     (79, 4, 0, 4),
     (79, 5, 0, 5),
     (105, 0, 'Lpbi/secured/Class1;->arr_00:[B'),
     (35, (0, 8), '[B'),
     (79, 4, 0, 4),
     (79, 5, 0, 5),
     (105, 0, 'Lpbi/secured/Class1;->arr_01:[B'),
     (19, 0, 13),
     (35, (0, 0), '[B'),
     (79, 4, 0, 4),
     (79, 5, 0, 5),
     (79, 6, 0, 8),
     (18, 1, 4),
     (79, 7, 0, 1),
     (19, 1, 126),
     (79, 1, 0, 6),
     (18, 1, 6),
     (19, 2, 127),
     (79, 2, 0, 1),
     (18, 1, 7),
     (18, 2, -1),
     (79, 2, 0, 1),
     (19, 1, 8),
     (18, 2, -2),
     (79, 2, 0, 1),
     (19, 1, 9),
     (18, 2, -5),
     (79, 2, 0, 1),
     (19, 1, -10),
     (79, 1, 0, 7),
     (19, 1, 11),
     (19, 2, -127),
     (79, 2, 0, 1),
     (19, 1, 12),
     (19, 2, -128),
     (79, 2, 0, 1),
     (105, 0, 'Lpbi/secured/Class1;->arr_1:[B'),
     (19, 0, 13),
     (35, (0, 0), '[S'),
     (81, 4, 0, 4),
     (81, 5, 0, 5),
     (81, 6, 0, 8),
     (18, 1, 4),
     (81, 7, 0, 1),
     (19, 1, 32766),
     (81, 1, 0, 6),
     (18, 1, 6),
     (19, 2, 32767),
     (81, 2, 0, 1),
     (18, 1, 7),
     (18, 2, -1),
     (81, 2, 0, 1),
     (19, 1, 8),
     (18, 2, -2),
     (81, 2, 0, 1),
     (19, 1, 9),
     (18, 2, -5),
     (81, 2, 0, 1),
     (19, 1, -10),
     (81, 1, 0, 7),
     (19, 1, 11),
     (19, 2, -32767),
     (81, 2, 0, 1),
     (19, 1, 12),
     (19, 2, -32768),
     (81, 2, 0, 1),
     (105, 0, 'Lpbi/secured/Class1;->arr_2:[S'),
     (19, 0, 13),
     (35, (0, 0), '[I'),
     (75, 4, 0, 4),
     (75, 5, 0, 5),
     (75, 6, 0, 8),
     (18, 1, 4),
     (75, 7, 0, 1),
     (20, 1, 2147483646),
     (75, 1, 0, 6),
     (18, 1, 6),
     (20, 2, 2147483647),
     (75, 2, 0, 1),
     (18, 1, 7),
     (18, 2, -1),
     (75, 2, 0, 1),
     (19, 1, 8),
     (18, 2, -2),
     (75, 2, 0, 1),
     (19, 1, 9),
     (18, 2, -5),
     (75, 2, 0, 1),
     (19, 1, -10),
     (75, 1, 0, 7),
     (19, 1, 11),
     (20, 2, -2147483647),
     (75, 2, 0, 1),
     (19, 1, 12),
     (21, 2, -2147483648),
     (75, 2, 0, 1),
     (105, 0, 'Lpbi/secured/Class1;->arr_4:[I'),
     (19, 0, 13),
     (35, (0, 0), '[J'),
     (22, 2, 1),
     (76, 2, 0, 4),
     (22, 2, 2),
     (76, 2, 0, 5),
     (22, 2, 5),
     (76, 2, 0, 8),
     (18, 1, 4),
     (22, 2, 10),
     (76, 2, 0, 1),
     (24, 2, 9223372036854775806, nan),
     (76, 2, 0, 6),
     (18, 1, 6),
     (24, 2, 9223372036854775807, nan),
     (76, 2, 0, 1),
     (18, 1, 7),
     (22, 2, -1),
     (76, 2, 0, 1),
     (19, 1, 8),
     (22, 2, -2),
     (76, 2, 0, 1),
     (19, 1, 9),
     (22, 2, -5),
     (76, 2, 0, 1),
     (22, 2, -10),
     (76, 2, 0, 7),
     (19, 1, 11),
     (24, 2, -9223372036854775807, -5e-324),
     (76, 2, 0, 1),
     (19, 1, 12),
     (25, 2, -9223372036854775808, -0.0),
     (76, 2, 0, 1),
     (105, 0, 'Lpbi/secured/Class1;->arr_8:[J'),
     (14,),
     (0, 0),
     (0, 3, 2, [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70])
    ), ()), {}),
  (IS_DIRECT_METHOD, '<init>(Lpbi/secured/Root;)V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, (),
   (3, 2, 2, 11,
    ((112, 'Ljava/lang/Object;-><init>()V', (1,)),
     (34, 0, 'Lpbi/secured/Class2;'),
     (112, 'Lpbi/secured/Class2;-><init>(Lpbi/secured/Root;)V', (0, 2)),
     (91, (0, 1), 'Lpbi/secured/Class1;->obj:Lpbi/secured/Class2;'),
     (14,)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'test()V', ACCESS_PUBLIC, None, (),
   (2, 1, 1, 6,
    ((84, (0, 1), 'Lpbi/secured/Class1;->obj:Lpbi/secured/Class2;'),
     (110, 'Lpbi/secured/Class2;->test()V', (0,)),
     (14,)
    ), ()), {})
  )
)



root_class = ('Lpbi/secured/Root;',
 ACCESS_PUBLIC,
 'Ljava/lang/Object;',
 (), None, (),
 ((IS_INSTANCE_FIELD, 'obj:Lpbi/secured/Class1;', ACCESS_PUBLIC, None, (), None, {}),
  (IS_DIRECT_METHOD, '<init>()V', ACCESS_CONSTRUCTOR | ACCESS_PUBLIC, None, (),
   (2, 1, 2, 11,
    ((112, 'Ljava/lang/Object;-><init>()V', (1,)),
     (34, 0, 'Lpbi/secured/Class1;'),
     (112, 'Lpbi/secured/Class1;-><init>(Lpbi/secured/Root;)V', (0, 1)),
     (91, (0, 1), 'Lpbi/secured/Root;->obj:Lpbi/secured/Class1;'),
     (14,)
    ), ()), {}),
  (IS_DIRECT_METHOD, 'checker()V', ACCESS_STATIC | ACCESS_PUBLIC, None, (),
   (1, 0, 1, 9,
    ((34, 0, 'Lpbi/secured/Root;'),
     (112, 'Lpbi/secured/Root;-><init>()V', (0,)),
     (110, 'Lpbi/secured/Root;->test()V', (0,)),
     (14,)
    ), ()), {}),
  (IS_DIRECT_METHOD, 'sum(II)I', ACCESS_STATIC | ACCESS_PUBLIC, None, (),
   (3, 2, 0, 3,
    ((144, 0, 1, 2),
     (144, 0, 0, 2), # для проверки, что вместо (a + b) будет действительно (a + 2b)
     (15, 0)
    ), ()), {}),
  (IS_VIRTUAL_METHOD, 'test()V', ACCESS_PUBLIC, None, (),
   (2, 1, 1, 6,
    ((84, (0, 1), 'Lpbi/secured/Root;->obj:Lpbi/secured/Class1;'),
     (110, 'Lpbi/secured/Class1;->test()V', (0,)),
     (14,)
    ), ()), {})
  )
)



test_classes = (wrap_class, arr_class, class3_class, class2_class, class1_class, root_class)



def TheGreatestBeginning(dexData):
  # dex, context смотрите в модуле common.py
  classLoader = dex(context, dexData)
  root = classLoader("test.classes.Root")
  print(root.methods()) # ЕСТЬ КОНТАКТ!!!!! ClassLoader ПОНЯЛ МЕНЯ!!!!;
  _sum = root._mw_sum(int, int) # аналогично root.methods()["sum(II)"]
  print(_sum)
  print(_sum(123, 64)) # 187 (правка: уже 251 = 123 + 64 + 64)!!!!!
  # ДААААААААА!!!!!!!! ПООООБЕЕЕЕЕДААААА!!!!! 🎇🎆🎇🎆🎇🎆🎇🎆

  # В этой элементарной суммирующей функции вложены годы моей работы,
  # начинающиеся ещё с далёкого 10 моего класса (весь сентябрь 2019 года был отпуск в Новороссийске),
  # когда кроме первого полностью рабочего DexReader'а (в конце отпуска) у меня вообще ничего не было,
  # а собственного Python-движка даже и в планах не было!!! Т.к. тогда я питон (ну и Java, раз на то пошло) толком-то не знал, как сейчас
  # 6 лет хобби-жизни в этих 1053 строчках, пусть и много времени ушло не в данное русло, а в основном: в школу, в развлечения и в универ

  # Я в курсе про существование готовых решений, как jar2dex от google, где аналоги DexReader, DexWriter, JarReader,
  # JarWriter уже созданы (2009-2012 года, 3 года ПО МЕРКАМ ГУГЛА!) ещё когда я только познавал Паскаль с ужасающим ООП и именованием переменных... но хобби - есть хобби

  # Runtime time (от самого запуска приложени и до сюда): 24 ms


def test_Wrap(dexData):
  def check(num):
    fields = inst.fields()

    assert len(fields) == 4
    shift = fields["shift"]
    mul   = fields["mul"]
    data  = fields["data"]
    orig  = fields["orig"]

    print(orig, "*", mul, "+", shift, "=", data)

    assert orig == num
    assert data == num * mul + shift

  classLoader = dex(context, dexData)
  Wrap = classLoader("test.classes.Wrap")

  inst = Wrap((2468).long)
  print(inst)
  check(2468)

  inst._m_inc((125).long)
  check(2593)

  inst._m_dec((216).long)
  check(2377)

  assert inst._m_yeah((2376).long) == True
  assert inst._m_yeah((2377).long) == True
  assert inst._m_yeah((2378).long) == False

  assert inst._m_secured_get() == 2377
  # совершенно нормально, что мой питон (Java-Python мост) позволяет редактировать приватные поля, а также, вызывать приватные методы
  inst._f_orig += 100 # типо накрутил внутриигровую валюту через ОЗУ...
  assert inst._f_orig  == 2477
  assert inst._m_get() == 2377
  try:
    inst._m_secured_get()
    1/0 # при удачном тесте, сюда мы не попадём
  except InvocationTargetError as e:
    assert len(e.args) == 1
    assert e.args[0].startswith("java.lang.Exception: Нука живо удалил GG и не лезь в ОЗУ!!! XD\n\tat test.classes.Wrap.secured_get(Unknown Source:14)\n\tat ")
    # Сообщение в Exception только для примера. Здесь может быть любой бан-хаммер или что-то подобное
    # К слову, GG - приложение, Game Guardian (игровой хранитель) - причина появления подобных защитных классов.
    # Это приложение позволяет редактировать ОЗУ, накручивая различные внутриигровые штуки, но только если есть root-права, и знаешь, что накручиваешь...
  print("TESTED!")

  # Runtime time (от самого запуска приложени и до сюда): 24.4 ms
