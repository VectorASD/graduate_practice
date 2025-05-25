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



#T = time()
import myGL
import myGLclasses
# print("ok!", time() - T) 0.016 s.



class myRenderer:
  glVersion = 2

  def __init__(self, activity, view):
    self.activity  = activity
    self.view      = view

    # Camera
    self.yaw, self.pitch, self.roll = 180, 0, 0
    self.camX, self.camY, self.camZ = 0, 0, -3.5
    self.camera = 0, 0, -3.5
    self.CW_mode = False

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
    self.colorDimension = False
    self.clickHandlerQueue = []

    # Timers
    self.eventN = 0
    self.time, self.td = time(), 0
    self.moveTd = 0
    self.moveTd2 = 0

    # Hooks
    self.camMoveEvent = lambda: None

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
      if self.CW_mode: text = "fps: %s\ncam: %.2f %.2f %.2f\nrot: %.2f %.2f %.2f" % (S, self.camX, self.camY, self.camZ, self.yaw, self.pitch, self.roll)
      else: text = "fps: %s" % S
      # self.glyphs.setText(self.fpsText, text, self.W / 16)
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

    skybox_labeled = __resource("skybox_labeled.png")
    skyboxLabeled = newTexture2(skybox_labeled)

    # все шейдерные программы в одном месте

    self.skyboxes = (
      skyBoxLoader(d2textureProgram(skyboxLabeled, (1, 6), self), (0, 1, 2, 3, 4, 5)),
      None,
    )

    # настройка шейдерных программ

    self.skyboxN       = 0
    self.currentSkybox = self.skyboxes[self.skyboxN]

    # загрузка моделей

    self.models = ()

    # первый сигнал перерасчёта матриц модели во всей иерархии моделей

    self.calcViewMatrix()

    self.ready = True

  def calcMVPmatrix(self):
    MVPmatrix = self.MVPmatrix
    multiplyMM(MVPmatrix, 0, self.projectionM, 0, self.viewM, 0)
    # print("MVP:", self.MVPmatrix[:])
    multiplyMM(self.VPmatrix,  0, self.projectionM, 0, self.viewNotTranslatedM, 0)
    self.updMVP = False

    for model in self.models: model.recalc(MVPmatrix)

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

    self.ready2 = True



  def drawScene(self):
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    skybox = self.currentSkybox
    if skybox is not None: skybox.draw()

  def drawColorDimension(self):
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if not self.CW_mode:
      self.colorama.draw(self.SolarSystem)

  def readPixel(self, x, y):
    buffer = MyBuffer.allocateDirect(4)
    buffer._m_order(MyBuffer.nativeOrder)
    glReadPixels(round(x), round(y), 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, buffer)
    arr = BYTE.new_array(buffer._m_remaining())
    buffer._m_get(arr)
    return bytes(arr)

  def onDrawFrame(self, gl10):
    if not self.ready2: return

    self.frames += 1
    T = time()
    self.td = T - self.time
    self.time = T

    #print("📽️ onDraw", gl)

    self.fps()

    if self.updMVP: self.calcMVPmatrix()

    if self.skyboxN == 1:
      self.drawColorDimension()
    else: self.drawScene()

    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)



  def move(self, dx, dy):
    if not self.ready2: return
    self.yaw -= dx * 0.5
    self.pitch = max(-90, min(self.pitch - dy * 0.5, 90))
    self.calcViewMatrix()

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



  def event(self, up, down, misc):
    self.eventN = up | down << 1 | misc << 2

  def getTByPosition(self, x, y):
    if not self.ready2: return -1
    return -1
    # return self.gridProgram.checkPosition(x / self.W, y / self.H)

  reverse = {
    "cr": onSurfaceCreated,
    "ch": onSurfaceChanged,
    "df": onDrawFrame,
  }





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
    self.eventA = set()
    self.eventB = set()
    self.eventC = set()

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
        if t == 1: self.eventA.add(id)
        elif t == 2: self.eventB.add(id)
        elif t == 3: self.eventC.add(id)
        renderer.event(bool(self.eventA), bool(self.eventB), bool(self. eventC))
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
      self.eventA.remove(id)
      self.eventB.remove(id)
      self.eventC.remove(id)
      renderer.event(bool(self.eventA), bool(self.eventB), bool(self.eventC))

      xx, yy, t, ok = startXYT[id]
      if ok and (xx - x) ** 2 + (yy - y) ** 2 < 100:
        renderer.click(xx, yy, T - t)
    elif action == ACTION_CANCEL:
      self.eventA.clear()
      self.eventB.clear()
      self.eventC.clear()
      renderer.event(False, False, False)
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
