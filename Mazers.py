if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  load_codes("Mazers.py")
  main("mazers", False, ("/sdcard/my_code3.asd", "/sdcard/my_debug3.asd"))
  exit()

###~~~### mazers

"""
import python2java # python2java

#module = python2java(__code("polygon.py"))
module = python2java(__code("../TimeTests.py"))

print("~" * 53)

print("• module:", module)
print("F:", module.fields())
print("M:", module.methods())

print("~" * 53)
res = module._m_module()
print("~" * 53)
print("• returned:", res)
"""



# T = time()
import myGL
import myGLclasses
import myGLtext
# print("ok!", time() - T) # 0.02 s.



face2delta = (
  ( 0, +1,  0), # top    / верх   (+Y)
  ( 0,  0, +1), # south  / юг     (+Z)
  (-1,  0,  0), # west   / запад  (-X)
  ( 0,  0, -1), # north  / север  (-Z)
  (+1,  0,  0), # east   / восток (+X)
  ( 0, -1,  0), # bottom / дно    (-Y)
)
ids_for_build = 0, 1, 2, 3, 4, 5, 6, 10, 11

def ClickProvider(data):
  def click():
    renderer, x, y, z, face = data
    # print(x, y, z, face)
    dx, dy, dz = face2delta[face]
    id = renderer.selected_tile
    if id:
      x += dx
      y += dy
      z += dz
    level.setblock(x, y, z, id)
  return click



ChunkSX = ChunkSY = ChunkSZ = 8

class Chunk:
  def __init__(self, level, my_pos):
    self.level = level
    self.data = tuple(tuple(
    	 [0] * ChunkSX
      for y in range(ChunkSY))
      for z in range(ChunkSZ))
    self.model = None
    self.dirty = False
    self.mat = None
    self.my_pos = my_pos
    self.colors = []

  def build(self):
    renderer = self.level.renderer
    next_color = renderer.colorama.next

    def add_block(x, y, z, id, faces):
      x2 = x + 1
      y2 = y + 1
      z2 = z + 1

      v, u = divmod(15 - id, 4)
      u1 = 0.75 - u / 4
      u2 = u1 + 0.25
      v1 = v / 4
      v2 = v1 + 0.25

      # мой extend теперь позволяет передавать несколько элементов без tuple!
      for face in faces:
        color = next_color(ClickProvider((renderer, x, y, z, face)))
        match face:
          case 0: # top    / верх   (+Y)
            a = (x,  y2, z,  u1, v1, *color)
            b = (x2, y2, z,  u2, v1, *color)
            c = (x,  y2, z2, u1, v2, *color)
            d = (x2, y2, z2, u2, v2, *color)
            extend((b, a, c), (b, c, d))
          case 1: # south  / юг     (+Z)
            a = (x,  y2, z2, u1, v1, *color)
            b = (x2, y2, z2, u2, v1, *color)
            c = (x,  y,  z2, u1, v2, *color)
            d = (x2, y,  z2, u2, v2, *color)
            extend((b, a, c), (b, c, d))
          case 2: # west   / запад  (-X)
            a = (x, y2, z,  u1, v1, *color)
            b = (x, y2, z2, u2, v1, *color)
            c = (x, y,  z,  u1, v2, *color)
            d = (x, y,  z2, u2, v2, *color)
            extend((b, a, c), (b, c, d))
          case 3: # north  / север  (-Z)
            a = (x2, y2, z, u1, v1, *color)
            b = (x,  y2, z, u2, v1, *color)
            c = (x2, y,  z, u1, v2, *color)
            d = (x,  y,  z, u2, v2, *color)
            extend((b, a, c), (b, c, d))
          case 4: # east   / восток (+X)
            a = (x2, y2, z2, u1, v1, *color)
            b = (x2, y2, z,  u2, v1, *color)
            c = (x2, y,  z2, u1, v2, *color)
            d = (x2, y,  z,  u2, v2, *color)
            extend((b, a, c), (b, c, d))
          case 5: # bottom / дно    (-Y)
            a = (x,  y, z2, u1, v1, *color)
            b = (x2, y, z2, u2, v1, *color)
            c = (x,  y, z,  u1, v2, *color)
            d = (x2, y, z,  u2, v2, *color)
            extend((b, a, c), (b, c, d))
        add_color(color)

    self.remove()

    faces = []
    extend = faces.extend
    add_color = self.colors.append

    my_x, my_y, my_z = self.my_pos
    my_x *= ChunkSX
    my_y *= ChunkSY
    my_z *= ChunkSZ

    for y, mat in enumerate(self.data, my_y):
      for z, row in enumerate(mat, my_z):
        for x, id in enumerate(row, my_x):
          if id:
            add_block(x, y, z, id, range(6))

    if not faces:
      self.model = None
      return # Чисто-воздушный чанк...

    VBOdata, IBOdata = buildModel(faces)
    self.model = Model(VBOdata, IBOdata, renderer.colorama, False)

    mat = self.mat
    if mat: self.model.recalc(mat)



  def setblock(self, x, y, z, id):
    self.data[y][z][x] = id
    self.dirty = True

  def getblock(self, x, y, z):
    return self.data[y][z][x]



  def recalc(self, mat):
    model = self.model
    if model: model.recalc(mat)
    self.mat = mat

  def draw(self):
    if self.dirty:
      self.build()
      self.dirty = False
    model = self.model
    if model: model.draw()
    else: self.delete()

  def restart(self):
    self.dirty = self.model is not None
    self.model = None
    self.colors.clear()

  def remove(self):
    model = self.model
    if model: model.delete(False)
    colors = self.colors
    if colors:
      self.level.renderer.colorama.clear(colors)
      colors.clear()

  def delete(self):
    self.remove()
    level = self.level
    level.chunks.pop(self.my_pos)
    if not level.chunks:
      level.default()

  def pack(self, file):
    file.pickle(self.my_pos)
    write = file.write
    for mat in self.data:
      for row in mat:
        write(bytes(row))

  def unpack(self, file):
    self.my_pos = my_pos = file.unpickle()
    read = file.read
    for mat in self.data:
      for row in mat:
        row[:] = read(ChunkSX)
    self.dirty = True



class Level:
  def __init__(self, path):
    self.chunks = {}
    self.mat = None
    self.renderer = None

    self.path = path
    self.save_time = None

    try: self.load()
    except OSError: self.default()

  def setblock(self, x, y, z, id):
    chunk_x, x = divmod(x, ChunkSX)
    chunk_y, y = divmod(y, ChunkSY)
    chunk_z, z = divmod(z, ChunkSZ)
    chunk_pos = chunk_x, chunk_y, chunk_z
    try: chunk = self.chunks[chunk_pos]
    except KeyError:
      chunk = self.chunks[chunk_pos] = Chunk(self, chunk_pos)
      mat = self.mat
      if mat: chunk.recalc(mat)
    chunk.setblock(x, y, z, id)
    self.save_time = time() + 3

  def getblock(self, x, y, z):
    chunk_x, x = divmod(x, ChunkSX)
    chunk_y, y = divmod(y, ChunkSY)
    chunk_z, z = divmod(z, ChunkSZ)
    chunk_pos = chunk_x, chunk_y, chunk_z
    try: chunk = self.chunks[chunk_pos]
    except KeyError: return 0 # воздух
    return chunk.getblock(x, y, z)



  def recalc(self, mat):
    self.mat = mat
    for chunk in self.chunks.values():
      chunk.recalc(mat) 

  def draw(self):
    save_time = self.save_time
    if save_time and save_time <= time():
      self.save_time = None
      self.save()

    for chunk in self.chunks.values():
      chunk.draw()

  def restart(self):
    for chunk in self.chunks.values():
      chunk.restart()

  def default(self):
    for z in range(2):
      for x in range(3):
        self.setblock(x, 0, z, 8 if x == 1 and z == 1 else 1)

  # пока временная мера просто всё подряд без структурирования поместить в файл

  def pack(self, file):
    for chunk in self.chunks.values():
      chunk.pack(file)

  def unpack(self, file):
    chunks = self.chunks
    for chunk in chunks.values(): chunk.delete()
    while not file.eof():
      chunk = Chunk(self, None)
      chunk.unpack(file)
      print("LOADED:", chunk.my_pos)
      chunks[chunk.my_pos] = chunk

  def save(self):
    with open(self.path, "wb") as file:
      self.pack(file)

  def load(self):
    with open(self.path, "rb") as file:
      self.unpack(file)



level = Level("/sdcard/TEST.chunk")



class myRenderer:
  glVersion = 2

  def __init__(self, activity, view):
    self.activity  = activity
    self.view      = view

    # Camera
    self.yaw, self.pitch, self.roll = 0, -45, 0
    self.camX, self.camY, self.camZ = 0, 3.5, 3.5
    self.camera = 0, 3.5, 3.5
    self.CW_mode = False
    self.skyboxN = 0

    # FPS
    self.frames    = self.last_frames = 0
    self.last_time = time() + 0.1
    self.frame_pos = 0
    self.frame_arr = []
    self.fpsS      = "?"

    # Window
    self.W = self.H = self.WH_ratio = -1
    self.FBO = None
    self.ready = False
    self.ready2 = False

    # Click system
    self.clickHandlerQueue = []

    # Timers
    self.eventN = set()
    self.time, self.td = time(), 0
    self.moveTd = 0
    self.moveTd2 = 0

    # Hooks
    self.camMoveEvent = lambda: None

    # Editor
    self.selected_tile = 1

  def fps(self):
    T = time()
    arr = self.frame_arr
    if T >= self.last_time:
      self.last_time = T + 0.1
      fd = self.frames - self.last_frames
      self.last_frames = self.frames
      if len(arr) < 10: self.frame_arr.append(fd)
      else:
        pos = self.frame_pos
        arr[pos] = fd
        self.frame_pos = (pos + 1) % 10
      self.fpsS = S = sum(arr) * 10 // len(arr)
      if self.CW_mode:
        text = "fps: %s\ncam: %.2f %.2f %.2f\nrot: %.2f %.2f %.2f" % (S, self.camX, self.camY, self.camZ, self.yaw, self.pitch, self.roll)
      else:
        text = "fps: %s\nchunks: %s%s" % (S, len(level.chunks), "\nsaved" if level.save_time is None else "")
      self.glyphs.setText(self.fpsText, text, self.W / 16)
    return self.fpsS



  def onSurfaceCreated(self, gl10, config):
    self.ready = self.ready2 = False
    print("📽️ onSurfaceCreated", gl10, config)

    self.time, self.td = time(), 0
    self.clickHandlerQueue.clear()

    # основные настройки по умолчанию

    # glClearColor(0.9, 0.95, 1, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glActiveTexture(GL_TEXTURE0) и так по умолчанию

    # матрицы

    self.viewM       = FLOAT.new_array(16)
    self.projectionM = FLOAT.new_array(16)
    self.MVPmatrix   = FLOAT.new_array(16)
    self.VPmatrix    = FLOAT.new_array(16)

    # все негенерированные (из ресурсника) текстуры в одном месте

    textures = __resource("textures.png")
    skybox_labeled = __resource("skybox_labeled.png")

    self.mainTexture = mainTextures = newTexture2(textures)
    skyboxLabeled = newTexture2(skybox_labeled)

    # __resource - bult-in функция моего компилятора. Она не может поддерживать переменные, только строки
    tiles = (
      __resource("tiles/tile_0.png"),
      __resource("tiles/tile_1.png"),
      __resource("tiles/tile_2.png"),
      __resource("tiles/tile_3.png"),
      __resource("tiles/tile_4.png"),
      __resource("tiles/tile_5.png"),
      __resource("tiles/tile_6.png"),
      __resource("tiles/tile_7.png"),
      __resource("tiles/tile_8.png"),
      __resource("tiles/tile_9.png"),
      __resource("tiles/tile_10.png"),
      __resource("tiles/tile_11.png"),
    )
    tiles = tuple(map(newTexture3, tiles))

    # все шейдерные программы в одном месте

    self.program = firstProgram = FirstProgram(self)
    self.gridProgram = gridProgram = d2textureProgram(mainTextures, (8, 64), self)
    self.skyboxes = (
      skyBoxLoader(d2textureProgram(skyboxLabeled, (1, 6), self), (0, 1, 2, 3, 4, 5)),
      None,
    )
    self.glyphs = glyphTextureGenerator(self)
    self.colorama = Colorama(self)
    self.textureChain = TextureChain(self)

    combine = TextureChain(self)
    for i, tile in enumerate(tiles):
      y, x = divmod(i, 4)
      combine.add_texture(tile, x, y, 4)
    self.atlas = atlas = combine.draw_to_texture(64, 64, 1, GL_NEAREST)
    dbgTextures = (atlas, tiles[0])

    self.gridProgram2 = gridProgram2 = d2textureProgram(atlas, (4, 4), self)

    # настройка шейдерных программ

    gridProgram.setUp(0.25)
    gridProgram.add(160, 0.25, 5.5,  8, 1, lambda: 1 in self.eventN)
    gridProgram.add(142, 0.25, 6.75, 8, 2, lambda: 2 in self.eventN)
    gridProgram.add(45,  6.75, 6.75, 8, 3, lambda: 3 in self.eventN)

    gridProgram2.setDirection(1)

    for i, id in enumerate(ids_for_build):
      y, x = divmod(i, 4)
      v, u = divmod(id, 4)
      # пока в моём python НЕ сохраняются состояния конкретно текущей итерации for для scope'ов
      def add(id):
        func = lambda: self.selected_tile != id
        gridProgram2.add(15 - (v << 2 | (3 - u)), 5 + 1.25 * x, 0.25 + 1.25 * y, 10, i + 4, func)
      add(id)

    self.currentSkybox = self.skyboxes[self.skyboxN]

    # загрузка моделей

    triangles, cube, sphere = figures(firstProgram)
    fboTex = lambda: self.FBO[1]
    self.Models = UnionModel((
      TranslateModel(NoCullFaceModel(triangles), (0, 0, -7.5)),
      TexturedModel(TranslateModel(ScaleModel(cube, (0.5, 1, 0.5)), (2.5, 0, -7.5)), fboTex),
      *(
      	  TexturedModel(TranslateModel(ScaleModel(cube.clone(), (1, 1, 0.5)), (0.5 - 2.5 * i, 0, -7.5)), dbg)
      	  for i, dbg in enumerate(dbgTextures)
      ),
      TexturedModel(TranslateModel(sphere, (0, 3, -7.5)), fboTex),
    ))

    # первый сигнал перерасчёта матриц модели во всей иерархии моделей

    self.calcViewMatrix()

    level.renderer = self
    level.recalc(identity_mat)

    self.ready = True

  def calcMVPmatrix(self):
    MVPmatrix = self.MVPmatrix
    multiplyMM(MVPmatrix, 0, self.projectionM, 0, self.viewM, 0)
    # print("MVP:", self.MVPmatrix[:])
    multiplyMM(self.VPmatrix,  0, self.projectionM, 0, self.viewNotTranslatedM, 0)
    self.updMVP = False

    self.Models.recalc(MVPmatrix)

  def calcViewMatrix(self):
    q = Quaternion.fromYPR(self.yaw, self.pitch, self.roll)
    q2 = q.conjugated()
    self.viewNotTranslatedM = mat = q2.toMatrix()

    translateM2(self.viewM, 0, mat, 0, -self.camX, -self.camY, -self.camZ)

    self.updMVP = True
    self.forward = q.rotatedVector(0, 0, -1)
    self.camMoveEvent()



  def onSurfaceChanged(self, gl10, width, height):
    if not self.ready: return
    print("📽️ onSurfaceChanged", gl10, width, height)
    if width == self.W and height == self.H: return

    glViewport(0, 0, width, height)
    self.W, self.H, self.WH_ratio = width, height, width / height

    perspectiveM(self.projectionM, 0, 90, self.WH_ratio, 0.01, 1000000)
    self.calcMVPmatrix()

    if self.FBO is not None: deleteFrameBuffer(self.FBO)
    self.FBO = newFrameBuffer(width, height, True)

    # настройка glyphs

    glyphs = self.glyphs
    glyphs.printer = False
    glyphs.setDirection(1)
    glyphs.setHeight(self.W / 16)
    glyphs.setColor(0xadddff)
    self.fpsText = glyphs.add(0, 0, 1, "fps: ?")

    self.ready2 = True



  def drawScene(self):
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)

    # Skybox
    skybox = self.currentSkybox
    if skybox is not None: skybox.draw()

    # Стартовые модельки
    program = self.program
    enableProgram(program.program)
    self.Models.draw()

    # Модели
    self.colorama.mode(False)
    glBindTexture(GL_TEXTURE_2D, self.atlas)
    self.colorama.draw(level)

    # GUI
    self.gridProgram.draw(self.WH_ratio)
    self.gridProgram2.draw(self.WH_ratio)
    self.glyphs.draw(self.WH_ratio)

  def drawColorDimension(self, gui = False):
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glDisable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)

    # Модели
    self.colorama.mode(True)
    self.colorama.draw(level)

    # GUI
    if gui:
      self.gridProgram.draw(self.WH_ratio)
      self.gridProgram2.draw(self.WH_ratio)
      self.glyphs.draw(self.WH_ratio)

  def readPixel(self, x, y):
    buffer = MyBuffer.allocateDirect(4)
    buffer._m_order(MyBuffer.nativeOrder)
    glReadPixels(round(x), round(y), 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, buffer)
    arr = BYTE.new_array(buffer._m_remaining())
    buffer._m_get(arr)
    return bytes(arr)

  # Основная отрисовочная петля
  def onDrawFrame(self, gl10):
    if not self.ready2: return

    self.frames += 1
    T = time()
    self.td = T - self.time
    self.time = T

    #print("📽️ onDraw", gl)

    self.fps()
    self.eventHandler()

    if self.updMVP: self.calcMVPmatrix()

    glBindFramebuffer(GL_FRAMEBUFFER, self.FBO[0])
    queue = self.clickHandlerQueue
    cbs = []
    if queue:
      self.drawColorDimension()
      for x, y in queue:
        rgba = self.readPixel(x, self.H - y)
        cb = self.colorama.to_n(rgba)
        # print("👆 click CB:", cb)
        if cb is not None: cbs.append(cb)
      self.clickHandlerQueue.clear()

    if self.skyboxN == 1:
      self.drawColorDimension(True)
    else: self.drawScene()

    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    if cbs:
      for cb in cbs: cb()

    self.textureChain.postprocessing(self.FBO[1])
    #print("🫢", glGetError())



  def move(self, dx, dy):
    def wrap():
      if not self.ready2: return
      self.yaw -= dx * 0.5
      self.pitch = max(-90, min(self.pitch - dy * 0.5, 90))
      self.calcViewMatrix()
    runOnGLThread(self.view, wrap)

  def event(self, t, active):
    (self.eventN.add if active else self.eventN.remove)(t)
  def clear_events(self):
    self.eventN.clear()

  def getTByPosition(self, x, y):
    if not self.ready2: return -1
    x /= self.W
    y /= self.H
    result = self.gridProgram.checkPosition(x, y)
    if result != -1: return result
    return self.gridProgram2.checkPosition(x, y)

  def click(self, x, y, click_td):
    if not self.ready2: return
    if click_td > 0.5: return
    t = self.getTByPosition(x, y)
    if t == -1:
      self.clickHandlerQueue.append((x, y))
    elif t == 3:
      self.skyboxN = N = (self.skyboxN + 1) % len(self.skyboxes)
      self.currentSkybox = self.skyboxes[N]
    elif t in range(4, 13):
      id = ids_for_build[t - 4]
      self.selected_tile = id
    # print("🐾 click:", x, y, t)

  def eventHandler(self):
    td, event = self.td, self.eventN
    if 1 in event or 2 in event:
      if 2 in event: td = -td
      x, y, z = self.forward

      td *= 10
      self.moveCam(x * td, y * td, z * td)



  def setCamPos(self, x, y, z):
    self.camX = x
    self.camY = y
    self.camZ = z
    self.camera = x, y, z
    self.calcViewMatrix()
  def moveCam(self, dx, dy, dz):
    self.camX += dx
    self.camY += dy
    self.camZ += dz
    self.camera = self.camX, self.camY, self.camZ
    self.calcViewMatrix()

  def restart(self):
    print2("~" * 53)
    self.ready = self.ready2 = False
    self.W = self.H = self.WH_ratio = -1
    self.FBO = None
    SkyBox.restart()
    self.findNearestPlanet = lambda: None
    level.restart()

  reverse = {
    "cr": onSurfaceCreated,
    "ch": onSurfaceChanged,
    "df": onDrawFrame,
  }





# Отрисовывается, если в инициализации что-то крашнется:
main_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView
        android:textSize="29dp"
        android:textColor="#40ad80"
        android:layout_gravity="center"
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="TEXT"/>
</LinearLayout>
""".strip()

class activityHandler:
  def onCreate(self, activity):
    global HALT
    def halt(message = None):
      try:
        activity._m_finish()
        renderer.ready = renderer.ready2 = False
      except: pass
      exit(message)
    HALT = halt

    print("onCreate", self, repr(activity))
    # for meth in sorted(activity.methods().values(), key = str): print(meth)

    ctx = activity._m_getApplicationContext().cast(Context)

    activity._m_requestWindowFeature(FEATURE_NO_TITLE) # Remove title bar
    activity._m_getWindow()._m_setFlags(FLAG_FULLSCREEN, FLAG_FULLSCREEN) # Remove notification bar

    view = GLSurfaceView(ctx)
    renderer = myRenderer(activity, view)
    # renderer = gpuRenderer(activity, view)
    renderer2 = rm.renderer(renderer)
    print("V:", view)
    print("R:", renderer2)
    view._m_setEGLContextClientVersion(renderer.glVersion)
    view._m_setRenderer(renderer2)
    activity._mw_setContentView(View)(view)

    self.viewResume = view._mw_onResume()
    self.viewPause = view._mw_onPause()
    self.renderer = renderer
    self.prevXY = {}
    self.startXYT = {}
    self.events = {}

    return True # lock setContentView

  def onStart(self): print("onStart")
  def onRestart(self):
    print("onRestart")
    self.renderer.restart()
  def onResume(self):
    print("onResume")
    self.viewResume()
  def onPause(self):
    print("onPause")
    self.viewPause()
  def onStop(self): print("onStop")
  def onDestroy(self): print("onDestroy")
  def onTouchEvent(self, e):
    action = e._m_getAction()
    getX = e._mw_getX(int)
    getY = e._mw_getY(int)
    getPointerId = e._mw_getPointerId(int)
    prevXY, startXYT, renderer = self.prevXY, self.startXYT, self.renderer
    actionN = action >> 8
    action &= 255
    T = time()
    if action in ACTION_DOWN:
      x, y, id = getX(actionN), getY(actionN), getPointerId(actionN)
      t = renderer.getTByPosition(x, y)
      if t > 0:
        prevXY[id] = None
        try: ev = self.events[t]
        except KeyError: ev = self.events[t] = set()
        ev.add(id)
        renderer.event(t, True)
      else: prevXY[id] = x, y
      startXYT[id] = [x, y, T, True]
    elif action == ACTION_MOVE:
      for p in range(e._m_getPointerCount()):
        x, y, id = getX(p), getY(p), getPointerId(p)
        prevv = prevXY[id]
        if prevv is None: continue
        prevX, prevY = prevv
        prevXY[id] = x, y
        self.renderer.move(x - prevX, y - prevY)

        xx, yy, t, ok = startXYT[id]
        if ok and (xx - x) ** 2 + (yy - y) ** 2 > 100: startXYT[id][3] = False
    elif action in ACTION_UP:
      x, y, id = getX(actionN), getY(actionN), getPointerId(actionN)
      prevXY[id] = 0, 0 # del prevXY[id] пока нет :/
      for t, ev in self.events.items():
        ev.remove(id)
        if not ev: renderer.event(t, False)

      xx, yy, t, ok = startXYT[id]
      if ok and (xx - x) ** 2 + (yy - y) ** 2 < 100:
        renderer.click(xx, yy, T - t)
    elif action == ACTION_CANCEL:
      self.events.clear()
      renderer.clear_events()
    return True
  def onKeyDown(self, num, e):
    print("onKeyDown", num, e)
    return True
  def onKeyUp(self, num, e):
    print("onKeyUp", num, e)
    return True
  reverse = {
    "cr": onCreate,
    "st": onStart,
    "re": onRestart,
    "res": onResume,
    "pa": onPause,
    "sto": onStop,
    "de": onDestroy,
    "to": onTouchEvent,
    "kd": onKeyDown,
    "ku": onKeyUp,
  }



rm = ctxResources = None
# ctxResources пока не используется
def Activity():
  global rm, ctxResources
  rm = ResourceManager()
  rm.xml("main", "main.xml", main_xml)
  #print("•", rm)
  ress = rm.release()
  ctx = ress.ctx
  ctxResources = ctx._m_getResources()
  #print("•", ress, ctx)

  activityManager = ctx._m_getSystemService(ACTIVITY_SERVICE)
  config = activityManager._m_getDeviceConfigurationInfo()
  #print("•", activityManager, config)
  #for name in config.methods().keys(): print(name)
  vers = config._f_reqGlEsVersion
  a, b, c = vers >> 16, vers >> 8 & 255, vers & 255
  print("GL: v%s.%s.%s" % (a, b, c))
  if a < 2:
    print("GLv2 not supported :/")
    return
  print("~" * 53)

  H = activityHandler()
  ress.activity("layout/main", H)

Activity()
