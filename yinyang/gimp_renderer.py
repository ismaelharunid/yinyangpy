
from .renderer import Renderer
from .common import *


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
