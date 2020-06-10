
from .common import *


def ti_value(value, i_frames, n_frames, ti, default=None):
  if callable(value):
    return value(i_frames, n_frames, ti, default)
  if is2tuple(value):
    if isinstance(value, Sequence):
      return lerps(value[0], value[1], float(i_frames % n_frames) / n_frames)
    if isinstance(value, Number):
      return lerp(value[0], value[1], float(i_frames % n_frames) / n_frames)
  if value is None: return default
  return value


def render(generator, renderer, size, n_frames, frame_start=0, frame_stop=1
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
    , ratio=0.5):                   # float or callable that returns one
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
    yins, yangs = generator(rad, dotrad, align, ang, rat)
    frame = renderer.new_frame(frame_name)
    if len(fills) >= 1 and fills[0]:
      renderer.bezier_fill(frame_name, yins, off, fills[0])
    if len(fills) >= 2 and fills[1]:
      renderer.bezier_fill(frame_name, yangs, off, fills[1])
    if stroke:
      renderer.bezier_stroke(frame_name, (yins or ()) + (yangs or {}), off, stroke, weight)
