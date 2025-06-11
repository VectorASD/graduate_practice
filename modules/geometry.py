
def buildModel(faces):
  VBOdata = []
  VBOdict = {}
  IBOdata = []
  VBOextend = VBOdata.extend
  IBOextend = IBOdata.extend
  for xyz, xyz2, xyz3 in faces:
    try: index = VBOdict[xyz]
    except KeyError:
      index = VBOdict[xyz] = len(VBOdict)
      VBOextend(xyz)
    try: index2 = VBOdict[xyz2]
    except KeyError:
      index2 = VBOdict[xyz2] = len(VBOdict)
      VBOextend(xyz2)
    try: index3 = VBOdict[xyz3]
    except KeyError:
      index3 = VBOdict[xyz3] = len(VBOdict)
      VBOextend(xyz3)
    IBOextend((index, index2, index3))
  return VBOdata, IBOdata



def figures(shaderProgram):
  ratio = (2 ** 2 - 1) ** 0.5
  ratio2 = ratio * 0.6

  triangles = Model((
      0,  ratio, 4, 1, 0, 0, 1, -1, -1,
     -2, -ratio, 4, 0, 1, 0, 1, -1, -1,
      2, -ratio, 4, 0, 0, 1, 1, -1, -1,
   -1.6,  ratio, 4, 1, 1, 0, 1, -1, -1,
   -1.2, ratio2, 4, 1, 0, 1, 1, -1, -1,
     -2, ratio2, 4, 0, 1, 1, 1, -1, -1,
   -1.2,  ratio, 4, 0, 0, 0, 0, -1, -1,
  ), (
    0, 2, 1, 3, 4, 5, 0, 4, 6, # старые 3 треугольника
  ), shaderProgram)

  cube = Model((
    -1, -1, -1,   1, 1, 1, 1,   -1, -1, #  0
     1, -1, -1,   1, 0, 0, 1,   -1, -1, #  1
     1, -1,  1,   1, 1, 0, 1,   -1, -1, #  2
    -1, -1,  1,   0, 0, 1, 1,   -1, -1, #  3
    -1,  1, -1,   0, 1, 0, 1,   -1, -1, #  4
     1,  1, -1,   0, 1, 1, 1,   -1, -1, #  5
     1,  1,  1,   0, 0, 0, 0,   -1, -1, #  6
    -1,  1,  1,   1, 0, 1, 1,   -1, -1, #  7
    -1, -1, -1,   1, 1, 1, 1,    1, 0, # 8
     1, -1, -1,   1, 0, 0, 1,    0, 0, # 9
    -1,  1, -1,   0, 1, 0, 1,    1, 1, # 10
     1,  1, -1,   0, 1, 1, 1,    0, 1, # 11
  ), (
     0,  1,  2,  0,  2,  3, # дно куба
   # 0,  4,  1,  1,  4,  5, # фронт
     8, 10,  9,  9, 10, 11, # фронт
     1,  5,  2,  2,  5,  6, # правый бок
     2,  7,  3,  2,  6,  7, # тыл
     3,  7,  0,  0,  7,  4, # левый бок
     4,  7,  5,  5,  7,  6, # верх куба
  ), shaderProgram)

  gridN = 8
  gridRange = range(gridN)
  faces = []
  facesAppend = faces.append
  for x in gridRange:
    for z in gridRange:
      x1, x2 = x / gridN * 2 - 1, (x + 1) / gridN * 2 - 1
      z1, z2 = z / gridN * 2 - 1, (z + 1) / gridN * 2 - 1
      a, b, c, d = (x1, -1, z1, x1, z1), (x1, -1, z2, x1, z2), (x2, -1, z1, x2, z1), (x2, -1, z2, x2, z2)
      facesAppend((a, c, b))
      facesAppend((b, c, d))
      a, b, c, d = (x1, 1, z1, x1, z1), (x1, 1, z2, x1, z2), (x2, 1, z1, x2, z1), (x2, 1, z2, x2, z2)
      facesAppend((a, b, c))
      facesAppend((b, d, c))
      a, b, c, d = (-1, x1, z1, x1, z1), (-1, x1, z2, x1, z2), (-1, x2, z1, x2, z1), (-1, x2, z2, x2, z2)
      facesAppend((a, b, c))
      facesAppend((b, d, c))
      a, b, c, d = (1, x1, z1, x1, z1), (1, x1, z2, x1, z2), (1, x2, z1, x2, z1), (1, x2, z2, x2, z2)
      facesAppend((a, c, b))
      facesAppend((b, c, d))
      a, b, c, d = (x1, z1, -1, x1, z1), (x1, z2, -1, x1, z2), (x2, z1, -1, x2, z1), (x2, z2, -1, x2, z2)
      facesAppend((a, b, c))
      facesAppend((b, d, c))
      a, b, c, d = (x1, z1, 1, x1, z1), (x1, z2, 1, x1, z2), (x2, z1, 1, x2, z1), (x2, z2, 1, x2, z2)
      facesAppend((a, c, b))
      facesAppend((b, c, d))
  VBOdata, IBOdata = buildModel(faces)
  VBOdata2 = []
  VBOextend = VBOdata2.extend
  for n in range(0, len(VBOdata), 5):
    x, y, z, U, V = VBOdata[n : n + 5]
    L = (x * x + y * y + z * z) ** 0.5
    # r, g, b = (sin(n * 3) + 2) / 3, (sin(n * 4) + 2) / 3, (sin(n * 5) + 2) / 3
    # L = 1 / L * 0.5 + L * 0.5
    L = 1 / L
    VBOextend((x / L, y / L, z / L, 0, 0, 0, 0, (U + 1) / 2, (V + 1) / 2))
  sphere = Model(VBOdata2, IBOdata, shaderProgram)
  return triangles, cube, sphere





def make_arrow(color1, color2, color3):
  T = time()
  n = 64
  cycle = 2 * pi
  sequence = tuple(cycle * (i / n) if i < n else 0 for i in range(n + 1))
  sin_seq = tuple(map(sin, sequence))
  cos_seq = tuple(map(cos, sequence))

  n4 = n // 4
  n5_16 = n * 5 // 16
  n2 = n // 2
  n_m1 = n - 1

  R = 0.05
  R2 = 0.025
  R3 = 0.1
  R4 = 0.025
  R5 = 0.025

  z = R
  circles = [
    (sin_seq[i] * R, z + (1 - cos_seq[i]) * R)
    for i in range(n4 + 1)]
  append = circles.append
  z = circles[-1][1]
  z += 0.6
  for i in range(n4 + 1):
    append((R + (1 - cos_seq[i]) * R2, z + sin_seq[i] * R2))
  z = circles[-1][1]
  for i in range(n5_16 + 1):
    append((R3 + sin_seq[i] * R4, z + (1 - cos_seq[i]) * R4))
  z = circles[-1][1]
  z -= (1 - cos_seq[n5_16]) * R5
  z += (circles[-1][0] - sin_seq[n5_16] * R5) * 3
  for i in range(n5_16, n2 + 1):
    append((sin_seq[i] * R5, z + (1 - cos_seq[i]) * R5))

  circles.extend((R, -z) for R, z in circles[::-1])

  T2 = time()

  faces = []
  IBOdata = []
  append = faces.append

  color1 = tuple(i / 255 for i in color1)
  color2 = tuple(i / 255 for i in color2)
  _rand = tuple(color1 if bit else color2 for bit in rand_bits(67)) * 100
  _rand_i = iter(_rand)

  def halo(R, z):
    nonlocal _rand_i
    dn = len(faces) // 9
    extend = faces.extend
    rand = _rand_i.__next__
    cr, cb, cg = color3
    for i in range(n):
      try: r, g, b = rand()
      except StopIteration:
        _rand_i = iter(_rand)
        rand = _rand_i.__next__
        r, g, b = rand()
      extend(sin_seq[i] * R, cos_seq[i] * R, z, r, g, b, cr, cb, cg)
    return dn

  def lid(z, swap): # крышка
    dn = last_dn
    dot = len(faces) // 9

    r, g, b = color1 if random_bool() else color2
    cr, cb, cg = color3
    faces.extend(0, 0, z, r, g, b, cr, cb, cg)

    extend = IBOdata.extend
    if swap:
      for i in range(dn, dn + n_m1):
        extend(i, dot, i + 1)
      extend(dn + n_m1, dot, dn)
    else:
      for i in range(dn, dn + n_m1):
        extend(dot, i, i + 1)
      extend(dot, dn + n_m1, dn)

  def tube(R, z): # туба
    nonlocal last_dn
    dn = last_dn
    dn2 = last_dn = halo(R, z)

    extend = IBOdata.extend
    for i in range(n_m1):
      a = dn + i
      b = a + 1
      c = dn2 + i
      extend(b, a, c,   b, c, c + 1)
    extend(dn, dn + n_m1, dn2 + n_m1,   dn, dn2 + n_m1, dn2)

  a = circles[0]
  b = circles[1]
  last_dn = halo(*b)
  lid(a[1], False)
  for i in range(2, len(circles) - 1):
    b = circles[i]
    tube(*b)
  a = circles[-1]
  lid(a[1], True)

  T3 = time()
  # VBOdata, IBOdata = buildModel(faces)
  VBOdata = faces

  T4 = time()
  """
  VBOdata2 = []
  extend = VBOdata2.extend
  rand = rand_bits(67)
  for i in range(0, len(VBOdata), 3):
    x, y, z = VBOdata[i : i+3]
    r, g, b = color1 if rand[i % 67] else color2
    extend(x, y, z, r, g, b, 1, 1, 1)
  отправилось, как часть функции "halo"
  """

  T5 = time()
  # print(round(T2 - T, 5), "+", round(T3 - T2, 5), "+", round(T4 - T3, 5), "+", round(T5 - T4, 5))
  # print(len(VBOdata) // 9, len(IBOdata) // 3) # количество вершин и полигонов
  return VBOdata, IBOdata





class ArrowedStar:
  def cb(self, delta_vec):
    prev_xy = None
    def handler(x, y):
      nonlocal prev_xy
      if prev_xy is None:
        prev_xy = x, y
        return

      renderer = self.renderer
      star = self.get_pos()
      unprojected = renderer.unproject(*prev_xy)
      t0 = find_closest_point_on_line1(star, delta_vec, renderer.camera, unprojected)
      unprojected = renderer.unproject(x, y)
      t1 = find_closest_point_on_line1(star, delta_vec, renderer.camera, unprojected)
      
      prev_xy = x, y
      # renderer.marker.update2(pos)
      x, y, z = star
      dx, dy, dz = delta_vec
      t1 = t1 - t0
      dx *= t1
      dy *= t1
      dz *= t1
      # self.set_pos((x + dx, y + dy, z + dz))
      level = renderer.choosed_level
      if level is not None: level.move(dx, dy, dz)

    return handler

  def __init__(self, renderer):
    self.renderer = renderer

    T = time()
    colorama = renderer.colorama
    arrow_data_X = make_arrow((170, 0, 0), (255, 85, 85), colorama.next_cb(lambda: self.cb((1, 0, 0))))
    arrow_data_Y = make_arrow((0, 170, 0), (85, 255, 85), colorama.next_cb(lambda: self.cb((0, 1, 0))))
    arrow_data_Z = make_arrow((0, 0, 170), (85, 85, 255), colorama.next_cb(lambda: self.cb((0, 0, 1))))
    # print("•••", time() - T)
    # было:  0.00032 + 0.00725 + 0.28886 + 0.02229 = 0.31872 секунд (buildModel как всегда самый требовательный)
    # стало: 0.00042 + 0.01368 + 0.0     + 0.0     = 0.0141  секунд
    # 22.6x-кратный прирост!
    # Оба замера при n = 64, что соответствует 4226 вершинам и 8448 полигонам

    arrow_X = Model(*arrow_data_X, colorama)
    arrow_Y = Model(*arrow_data_Y, colorama)
    arrow_Z = Model(*arrow_data_Z, colorama)
    arrow_X = RotateModel(arrow_X, (90, 0, 0))
    arrow_Y = RotateModel(arrow_Y, (0, 90, 0))
    star = UnionModel((arrow_X, arrow_Y, arrow_Z))
    scaled = ScaleModel(star, (1, 1, 1))
    translated = TranslateModel(scaled, (0, 3, -3.5))

    self.arrow = arrow = translated
    arrow.recalc(identity_mat)
    self.draw = arrow.draw
    self.get_pos = lambda: translated.translate

    self.set_scale = scaled.update2
    self.set_pos = translated.update2
    self.set_mat = arrow.recalc

    def camMoveEvent():
      cx, cy, cz = renderer.camera
      mat = scaled.mat
      L = lengthVec(cx - mat[12], cy - mat[13], cz - mat[14])
      L /= 4
      self.set_scale((L, L, L))
    renderer.camMoveEvent = camMoveEvent





EPSILON = 1e-9
def find_closest_point_on_line1(star, delta, camera, unprojected):
  x, y, z = star
  dx, dy, dz = delta
  cx, cy, cz = camera
  cx2, cy2, cz2 = unprojected
  dx2 = cx2 - cx
  dy2 = cy2 - cy
  dz2 = cz2 - cz
  delta_x = x - cx
  delta_y = y - cy
  delta_z = z - cz
  a = dx * dx + dy * dy + dz * dz
  b = dx * dx2 + dy * dy2 + dz * dz2
  c = dx2 * dx2 + dy2 * dy2 + dz2 * dz2
  d = dx * delta_x + dy * delta_y + dz * delta_z
  e = dx2 * delta_x + dy2 * delta_y + dz2 * delta_z
  denominator = b * b - a * c
  if abs(denominator) < EPSILON: # Линии параллельны или коллинеарны
    t1 = -d / a
  else:
    t1 = (c * d - e * b) / denominator
  return t1
  # return x + dx * t1, y + dy * t1, z + dz * t1

# встраивается в любой класс, содержащий camera=(x, y, z), W, H, near и MVPmatrix
def _unproject(self, x, y):
  x = x / self.W * 2 - 1
  y = 1 - y / self.H * 2
  z = 1 - self.near * 2 # долго искал зависимость, но нашёл
  inv = FLOAT.new_array(16)
  invertM(inv, 0, self.MVPmatrix, 0)
  pos = (x, y, z, 1)._a_float
  pos2d = FLOAT.new_array(4)
  multiplyMV(pos2d, 0, inv, 0, pos, 0)
  x, y, z, w = pos2d
  assert w, "здесь 0 недопустим"
  w = 1 / w
  return x * w, y * w, z * w
