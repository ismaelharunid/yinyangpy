
import warnings
from .renderer import Renderer
from .common import *
from .bezier_helper import *
from collections import OrderedDict

"""
handle PIL envirment stuff so the submodule can load regardless whether \
PIL, Image and ImageDraw are available or not.
"""
try:
  from PIL.ImageDraw import Image as PILImage, ImageDraw as PILImageDraw
  Image = PILImage.Image
except:
  warnings.warn("pil_renderer: PIL module and submodules not available", ImportWarning)
  PILImage = PILImageDraw = Image = Drawable = None

try:
  import aggdraw
except:
  warnings.warn("pil_renderer: aggdraw module not available", ImportWarning)
  aggdraw = None


_BRUSH_CACHE_SIZE = 10
_BRUSH_CACHE = OrderedDict()
def aggdraw_create_brush(fill, opacity=255):
  if fill:
    if len(fill) > 3:
      fill, opacity = fill[:3], fill[3]
    key = (fill, opacity)
    if key in _PEN_CACHE:
      brush = _PEN_CACHE.pop(key)
    else:
      if len(_BRUSH_CACHE) >= _BRUSH_CACHE_SIZE:
        _BRUSH_CACHE.popitem(0)
      brush = aggdraw.Brush(fill, opacity)
    _PEN_CACHE[key] = brush
  else:
    brush = None
  return brush


_PEN_CACHE_SIZE = 10
_PEN_CACHE = OrderedDict()
def aggdraw_create_pen(outline, weight, opacity=255):
  if outline and weight:
    if len(outline) > 3:
      outline, opacity = outline[:3], outline[3]
    key = (outline, weight, opacity)
    if key in _PEN_CACHE:
      pen = _PEN_CACHE.pop(key)
    else:
      if len(_PEN_CACHE) >= _PEN_CACHE_SIZE:
        _PEN_CACHE.popitem(0)
      pen = aggdraw.Pen(outline, weight, opacity)
    _PEN_CACHE[key] = pen
  else:
    pen = None
  return pen


"""
=== aggdraw ===
Draw(image_or_mode, size, color=None)
  Creates a drawing interface object.

  image_or_mode:
    A PIL Image, or a mode string. The following modes are supported: 
    “L”, “RGB”, “RGBA”, “BGR”, “BGRA”.
  size:
    If a mode string was given, this argument gives the image size, 
    as a 2-tuple.
  color:
    An optional background color specifier. If a mode string was given, 
    this is used to initialize the image memory. If omitted, it defaults 
    to white with full alpha.

=== PIL.ImageDraw.ImageDraw ===
Draw(im, mode=None)
  Creates an object that can be used to draw in the given image.

  Note that the image will be modified in place.

  im:
    The image to draw in.
  mode:
    Optional mode to use for color values. For RGB images, this argument 
    can be RGB or RGBA (to blend the drawing into the image). For all other 
    modes, this argument must be the same as the image mode. If omitted, 
    the mode defaults to the mode of the image.
"""

class PILDrawable(PILImageDraw):
  
  _imdraw = None
  _aggdraw = None
  
  def __init__(self, im, *args, **kwargs):
    if is2tuple(im):
      im = PILImage.Image("RGBA", im)
    elif not isinstance(im, PILImage.Image):
      raise ValueError("source must be a PILImage or PILDrawable")
    super(PILDrawable, self).__init__(self, im, *args, **kwargs)
    self._image = im
    self._imdraw = PILImageDraw(im)
    self._aggdraw = None if aggdraw is None else aggdraw.Draw(im)
  
  def cubic_path(self, xy, fill=None, outline=None, weight=0):
    if self._aggdraw:
      path = aggdraw.Path()
      brush = aggdraw_create_brush(fill)
      pen = aggdraw_create_pen(outline, weight)
      self._aggdraw.path(cubic_bezier_to_quadratic(xy), path, pen, brush)
      path = brush = pen = None
    else:
      pd = tuple(cubic_bezier_interpolate(xy))
      if fill:
        self.polygon(pd[:-2], fill)
      if outline and weight >= 0:
        self.line(pd, outline, weight)
  
  def quadratic_path(self, xy, fill=None, outline=None, weight=0):
    if self._aggdraw:
      path = aggdraw.Path()
      brush = aggdraw_create_brush(fill)
      pen = aggdraw_create_pen(outline, weight)
      self._aggdraw.path(xy, path, pen, brush)
      path = brush = pen = None
    else:
      pd = tuple(quadratic_bezier_interpolate(xy))
      if fill:
        self.polygon(pd[:-2], fill)
      if outline and weight >= 0:
        self.line(pd, outline, weight)
  
  def flush(self):
    if self._aggdraw:
      self._aggdraw.flush()


class PILRenderer(Renderer):
  
  _ItemType = PILImage.Image
  
  def __init__(self, name, size, image=None):
    super(PILRenderer, self).__init__(name, size)
  
  def __isvalid__(self, frame):
    return super(PILRenderer, self).__isvalid__(frame) \
        and frame.mode == "RGBA" \
        and frame.size == self.size
  
  def __new_frame__(self, frame_name):
    return PILDrawable("RGBA", self.size)
  
  def flush(self):
    for frame in self._frames:
      frame.flush()
    return tuple(frame._im for frame in self._frames)
  
  def bezier_fill(self, frame_name, shapes, offset, colors
      , stroke_color, stroke_weight):
    frame = self.new_frame(frame_name)
    n_shapes = len(shapes)
    n_colors = len(colors)
    for i_shapes in range(n_shapes):
      color = colors[i_shapes%n_colors]
      n_beziers = len(beziers)
      for i_beziers in range(n_beziers):
        frame.cubic_path(self, bpd, color, stroke_color, stroke_weight)
  
  def save(self, filepath):
    basepath, filename = ospath.split(filepath)
    basename, fileextn = ospath.splitext(filename)
    if not fileextn:
      fileextn = '.gif'
      filepath += fileextn
    if fileextn.lower() == '.xcf':
      raise NotImplementedError('.XCF format is not supported')
    elif fileextn.lower() == '.gif':
      self.frames[0].save(self._name, save_all=True, append_images=self.frames[1:])
    elif fileextn.lower() in ('.png',):
      foldername = ospath.join(basepath, basename)
      if ospath.exists(foldername):
        if not os.path.isdir:
          raise Exception('{:s} exists and is not a directory'.format(foldername))
      else:
        mkdir(foldername)
      # if folder doesn't exist create it
      for frame in self.frames:
        frame.save(ospath.joinext(ospath.join(foldername, frame.name), fileextn))
    else:
      pdb.gimp_file_save(self._image, self._frames[0], filepath, filepath)
