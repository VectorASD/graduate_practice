import common # dex, context
import DexWriter # DexWriter
# import test_classes # test_classes, TheGreatestBeginning, test_Wrap

"""
dexData = DexWriter(test_classes)
with open("/sdcard/Check.dex", "wb") as file:
  file.write(dexData)
print("ok!")

# TheGreatestBeginning(dexData)
test_Wrap(dexData)
"""

def python2java(code):
  defs, rln_count, names = code
  print("rln_count:", rln_count)
  print("names:", names)
  for id, (counts, args, codes, labels, tries, consts) in enumerate(defs):
    print("~" * 53)
    print("id:", id)
    print("counts:", counts)
    print("args:", args)
    for line in codes:
      print("•", line)
    print("labels:", labels)
    print("tries:", tries)
    print("consts:", consts)
