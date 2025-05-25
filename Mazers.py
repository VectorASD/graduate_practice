if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  load_codes("Mazers.py")
  main("mazers", False, ("/sdcard/my_code3.asd", "/sdcard/my_debug3.asd"))
  exit()

###~~~### mazers

import python2java # python2java

module = python2java(__code("polygon.py"))

print("~" * 53)

print("• module:", module)
print("F:", module.fields())
print("M:", module.methods())

print("~" * 53)
res = module._m_module()
print("~" * 53)
print("• returned:", res)
