
from .common import *


def cubic_bezier_yinyang(radius=1.0
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


def gimp_yinyang(radius=1.0
    , dot_radius=0.6, dot_align=0.5, angle=0.0, ratio=0.5):
  return tuple( \
      tuple(bpd2gbpd(*bpsc) for bpsc in shape) \
    for shape in cubic_bezier_yinyang(radius, dot_radius, dot_align, angle, ratio))
