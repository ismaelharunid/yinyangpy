import sys, os
ospath = os.path
vinfo = sys.version_info
#major=3, minor=7, micro=6, releaselevel='final', serial=0
if vinfo.major == 2:
  # for gimp
  from collections import Mapping, MutableMapping, Container as Reversible, Sequence
else:
  from collections.abc import Mapping, MutableMapping, Reversible, Sequence
from numbers import Number
import numpy as np
from math import *
epsilon = sys.float_info.epsilon
sixthpi = pi / 6
quarterpi = .25 * pi
thirdpi = pi / 3
halfpi = .5 * pi
twopi = 2 * pi
circle4k = 0.55191502449
circle3k = circle4k * 4 / 3
dist = lambda x, y: sqrt(x*x + y*y)
lerp = lambda a, b, t=0.5: a + (b-a) * t
lerps = lambda sa, sb, t=0.5: type(sa)(lerp(sa[i],sb[i],t) for i in range(len(sa)))
inbounce = lambda i,n,s=1: (n-abs(n-float(i)%(2*n)))*s/n
_scales = lambda s, sn, d, dn: (s[i]*d[i%dn] for i in range(sn))
scales = lambda s, d: type(s)(_scales(s, len(s), d, len(d)))
types = lambda s, t: t(c for c in s)
_opapplys = lambda op, sa,na, sb, nb, d: (op(sa[i%na+j],sb[i%nb+j]) \
    for i in range(0,max(na,nb),d) for j in range(d))
opapplys = lambda op, sa, sb, d=2: type(sa)(_opapplys(op, sa,len(sa), sb,len(sb), d=d))
muls = lambda sa, sb, d=2: opapplys(float.__mul__, sa, sb, d=d)
divs = lambda sa, sb, d=2: opapplys(float.__div__, sa, sb, d=d)
mods = lambda sa, sb, d=2: opapplys(float.__mod__, sa, sb, d=d)
adds = lambda sa, sb, d=2: opapplys(float.__add__, sa, sb, d=d)
subs = lambda sa, sb, d=2: opapplys(float.__sub__, sa, sb, d=d)

matmuls = lambda ra,ca,a, rb,cb,b: \
    (cb, ra, tuple(sum(a[i+k*ca]*b[j+i*cb] for i in range(ca)) \
    for k in range(ra) for j in range(cb)))
_bpd2gbpd = lambda bpd, closed: \
    ( bpd[-4:] + bpd[2:-4] if closed else \
    bpd[:2] + bpd + bpd[-2:], closed )
bpd2gbpd = lambda bpd, closed=None: \
    _bpd2gbpd(bpd, abs(bpd[:2] - bpd[-2:]) <= epsilon if closed is None else \
    closed)
is2tuple = lambda v: type(value) is tuple and len(value) == 2


def yinyang_cubic_bezier_points(radius=1.0
    , dot_radius=0.6, dot_align=0.5, angle=0.0, ratio=0.5):
  top_radius, bottom_radius = ratio * radius, (1.0-ratio) * radius
  top_offset, bottom_offset = -bottom_radius, top_radius
  # inner goes top to left to right to bottom
  inner = \
      ( 0.,                     top_offset-top_radius
      , -circle4k*top_radius,   top_offset-top_radius
      , -top_radius,            top_offset-circle4k*top_radius
      , -top_radius,            top_offset
      , -top_radius,            top_offset+circle4k*top_radius
      , -circle4k*top_radius,   top_offset+top_radius
      , 0.,                     top_offset+top_radius
      , circle4k*bottom_radius, top_offset+top_radius   # bottom_offset-bottom_radius
      , bottom_radius,          bottom_offset-circle4k*bottom_radius
      , bottom_radius,          bottom_offset
      , bottom_radius,          bottom_offset+circle4k*bottom_radius
      , circle4k*bottom_radius, bottom_offset+bottom_radius
      , 0.,                     bottom_offset+bottom_radius )
  # yin outer goes bottom to right to top
  yin = inner[:-2] + \
      ( 0.,                       radius
      , circle4k*radius,          radius
      , radius,                   circle4k*radius
      , radius,                   0.
      , radius,                   -circle4k*radius
      , circle4k*radius,          -radius
      , 0.,                       -radius )
  # yang outer goes bottom to left to top
  yang = \
      ( 0.,                       radius
      , -circle4k*radius,         radius
      , -radius,                  circle4k*radius
      , -radius,                  0.
      , -radius,                  -circle4k*radius
      , -circle4k*radius,         -radius
      , 0.,                       -radius )[:-2] + inner
  return ( ((yin, True),), ((yang, True),) )


def ti_value(value, i_frames, n_frames, ti, default=None):
  if callable(value):
    return value(i_frames, n_frames, ti, default)
  if is2tuple(value):
    if isinstance(value, Sequence)
      return lerps(value[0], value[1], float(i_frames % n_frames) / n_frames)
    if isinstance(value, Number):
      return lerp(value[0], value[1], float(i_frames % n_frames) / n_frames)
  if value is None: return default
  return value


def render_yinyang(renderer, size, n_frames, frame_start=0, frame_stop=1
    , make_time=lambda i,n: (i % n) / n
    , offset=None                   # 2-tuple of floats or callable that returns one
    , yin_color=(0,0,0,255)         # 3 or 4-tuple of ints or callable that returns one
    , yang_color=(255,255,255,255)  # 3 or 4-tuple of ints or callable that returns one
    , stroke_color=None             # 3 or 4-tuple of ints or callable that returns one
    , stroke_weight=1               # float or callable that returns one
    , radius=None                   # float or callable that returns one
    , dot_radius=None               # float or callable that returns one
    , dot_align=0.5                 # float or callable that returns one
    , angle=0.0                     # float or callable that returns one
    , ratio=0.5                     # float or callable that returns one
  width, height = renderer.size
  if offset is None: offset = (.5 * width, .5 * height)
  if radius is None: radius = .5 * min(width, height)
  if dot_radius is None: dot_radius = radius / 6.
  for i_frames in range(frame_start, frame_stop, 1):
    frame_name = 'frame={:05d}'.format(i_frames)
    ti = float(make_time(i_frames, n_frames))
    off = ti_value(off, i_frames, n_frames, ti)
    fills = tuple(ti_value(clr, i_frames, n_frames, ti) for clr in colors)
    stroke = ti_value(stroke_color, i_frames, n_frames, ti)
    weight = ti_value(stroke_weight, i_frames, n_frames, ti)
    rad = ti_value(radius, i_frames, n_frames, ti)
    dotrad = ti_value(dot_radius, i_frames, n_frames, ti)
    align = ti_value(dot_align, i_frames, n_frames, ti)
    ang = ti_value(angle_start, i_frames, n_frames, ti)
    rat = ti_value(ratio_start, i_frames, n_frames, ti)
    yins, yangs = yinyang_cubic_bezier_points(rad, dotrad, align, ang, rat)
    frame = renderer.new_frame(frame_name)
    if len(fills) >= 1 and fills[0]:
      renderer.bezier_fill(frame_name, yins, off, fills[0])
    if len(fills) >= 2 and fills[1]:
      renderer.bezier_fill(frame_name, yangs, off, fills[1])
    if stroke:
      renderer.bezier_stroke(frame_name, (yins or ()) + (yangs or {}), off, stroke, weight)


class Renderer(MutableMapping):
  
  _ItemType = None   # class variable
  
  _name = None
  _size = None
  _image = None
  _frame_names = None
  _frames = None
  _background = None
  _overlay = None
  
  @property
  def name(self):
    return self._name
  
  @property
  def size(self):
    return self._size
  
  @property
  def image(self):
    return self._image
  
  def __init__(self, name, size, background=None):
    self._name = name
    self._size = size
    self._frame_names = []
    self._frames = []
    self._background = background
  
  def __contains__(self, key):
    if type(key) is str: return key in self._frame_names
    return key in self._frames
  
  def __delitem__(self, key):
    if type(key) is str: key = self._frame_names.index(key)
    del self._frames[key]
    del self._frame_names[key]
    
  def __getitem__(self, key):
    if type(key) is str: key = self._frame_names[key]
    return self._frames[key]
    
  def __iter__(self):
    for key in range(len(self._frames)):
      yield { self._frame_names[key]: self._frames[key] }
    raise StopIteration('exhausted')
  
  def __eq__(self, value):
    if isinstance(value, Renderer): return self.layers == value.layers
  
  def __len__(self):
    return len(self._frames)
  
  def __isvalid__(self, item):
    type = self.__class__._ItemType
    return type is not None and isinstance(item, type)
  
  def __new_frame__(self, frame_name):
    raise NotImplementedError('please implement __new_frame__')
  
  def __rekey__(self, key):
    if key is None:
      return key
    if type(key) is str:
      index = 0
      if '-' in key:
        i = key.rindex('-')
        if all(c.isdigit() for c in key[i+1:]):
          basekey, index = key[:i], int(key[i+1:])
      else:
        basekey = key
      while key in self.layer_names:
        key = "{:s}-{:05d}".format(basekey, index)
      return key
    raise ValueError('bad layer')
  
  def __reversed__(self):
    for key in range(len(self._frames)-1, -1, -1):
      yield { self._frame_names[key]: self._frames[key] }
    raise StopIteration('exhansted')
  
  def __ne__(self, *args):
    return self.layers != value
  
  def __setitem__(self, key, value):
    if self.__isvalid__(value):
      if key is None: return self.setdefault(value)
      if type(key) is str:
        index, key = len(self._frames), self.__rekey(key)
        self._frames.append(value)
        self._frame_names.append(key)
      elif type(key) is int and 0 <= key and k < len(self._frames):
        self._frames[key] = value
  
  def clear(self):
    self._frame_names.clear()
    self._frames.clear()
  
  def flush(self):
    raise NotImplementedError('please implement flush')
  
  def items(self):
    return list(self._frame_names)
  
  def keys(self):
    return list(self._frame_names)
  
  def new_frame(self, key):
    key = self.__rekey__(key)
    frame = self.__new_frame__(key)
    self._frame_names.append(key)
    self._frames.append(frame)
    return frame
  
  def pop(self, index=None):
    if type(key) is str: key = self._frame_names[key]
    self._frame_names.pop(key)
    return self._frames.pop(key)

  def popitem(self, index=None):
    if type(key) is str: key = self._frame_names[key]
    return (self._frame_names.pop(key), self._frames.pop(key))

  def save(self, filepath):
    raise NotImplementedError('please implement save')

  def setdefault(self, background):
    if not self.__isvalid__(background):
      raise ValueError("bad background")
    self_background = background
  
  def update(self, *pairs, **kwpairs):
    if any(not isinstance(pair, Sequence) \
        or len(pair) != 2 \
        or type(pair[0]) is not str \
        or not self.__isvalid__(pair[1]) \
        for pair in pairs):
      raise ValueError('bad layer')
    if any(type(pair[0]) is not str \
        or not self.__isvalid__(pair[1]) \
        for pair in kwpairs.items()):
      raise ValueError('bad layer')
    for (key, item) in pairs:
      self[key] = item
    for (key, item) in kwpairs.items():
      self[key] = item
  
  def values(self):
    return list((self._frame_names[key], self._frames[key]) \
        for key in range(len(self._frames)))
  


class GimpRenderer(Renderer):
  
  _ItemType = gimp.Layer
  
  _frame_group = None
  
  def __init__(self, name, size, image=None):
    if isinstance(size, gimp.Image):
      image = size
      size = image.width, image.height
    else:
      self._image = pdb.gimp_image_new(size[0], size[1], RGB)
      pdb.gimp_image_set_filename(image, self._name)
    super(GimpRenderer, self).__init__(name, size)
    self._image = image
    self._frame_group = pdb.gimp_layer_group_new(image)
    self._frame_group.name = name
    self._frames = {}
  
  def __isvalid__(self, frame):
    return super(GimpRenderer, self).__isvalid__(frame) \
        and frame.type in (RGB_IMAGE, RGBA_IMAGE) \
        and frame.size == self.size
  
  def __new_frame__(self, frame_name):
    layer = pdb.gimp_layer_new(self.image, self.width, self.height, RGBA_IMAGE, frame_name, 100, 0)
    pdb.gimp_image_insert_layer(image, layer, self._frame_group, len(image.self._frame_group.children))
    return layer
  
  def flush(self):
    return list(self._frames)
  
  def bezier_fill(self, frame_name, yins, offset, yin_color):
    n_beziers = len(beziers)
    layer = pdb.gimp_layer_new(image, width, height, layer_type, frame_name, 100, 0)
    pdb.gimp_image_insert_layer(image, layer, None, i_frames)
    for i_beziers in range(n_beziers):
      vector_name = 'frame={:05d} stroke={:05d}'.format(i_frames, i_beziers)
      vector = pdb.gimp_vectors_new(image, vector_name)
      pdb.gimp_image_insert_vectors(image, vectors, None, 0)
      gbpd,gbpc = bpd2gbpd(beziers[i_beziers], False)
      bpd = muls(bpd,(450.,450.))
      vsid = pdb.gimp_vectors_stroke_new_from_points(vector, VECTORS_STROKE_TYPE_BEZIER
          , len(bpd0), bpd0, False)
      strokes.append(vector)
      color = colors[i_beziers%2]
      if color is not None:
        pdb.gimp_context_set_background(color)
        pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, layer)
        pdb.gimp_edit_bucket_fill(layer, 1, 0, 100, 15.0, False, 0, 0)
    pdb.gimp_selection_none(image)
    if stroke_weight is not None and stroke_weight > 0:
      pdb.gimp_context_set_brush_size(stroke_weight)
      for vector in strokes:
        if stroke_color is None:
          n_pd, pd, pc = pdb.gimp_vectors_stroke_interpolate(vector, vector.strokes[0].ID, 15)
          pdb.gimp_eraser(layer, n_pd, pd, 100, 0)
        else:
          pdb.gimp_edit_stroke_vectors(layer, vector)
  
  def save(self, filepath):
    basepath, filename = ospath.split(filepath)
    basename, fileextn = ospath.splitext(filename)
    if not fileextn:
      fileextn = '.gif'
      filepath += fileextn
    if fileextn.lower() == '.xcf':
      pdb.gimp_xcf_save(2, self._image, self._frames[0], filepath, filepath)
    elif fileextn.lower() == '.gif':
      pdb.file_gif_save(self._image, self._frames[0], filepath, filepath, False, True, 100, 2)
    elif fileextn.lower() == '.png':
      pdb.file_png_save(self._image, self._frames[0], filepath, filepath, False, 9, 0, 0, 0, 0, 0)
    else:
      pdb.gimp_file_save(self._image, self._frames[0], filepath, filepath)
