if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  load_codes("Mazers.py")
  main("mazers", False, ("/sdcard/my_code3.asd", "/sdcard/my_debug3.asd"))
  exit()

###~~~### mazers

import common # dex, context
import DexWriter # DexWriter
import test_classes # test_classes, TheGreatestBeginning, test_Wrap



dexData = DexWriter(test_classes)
with open("/sdcard/Check.dex", "wb") as file:
  file.write(dexData)
print("ok!")

# TheGreatestBeginning(dexData)
test_Wrap(dexData)
