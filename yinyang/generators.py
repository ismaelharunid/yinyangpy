
from .common import *


def cubic_bezier_yinyang(radius=1.0
    , dot_radius=0.6, dot_align=0.5, angle=0.0, ratio=0.5):
  #TODO: add dots and docs
  top_radius, bottom_radius = ratio * radius, (1.0-ratio) * radius
  top_offset, bottom_offset = -bottom_radius, top_radius
  topdot_offset = -lerp(dot_radius, 2*top_radius-dot_radius, dot_align)
  print dot_radius, top_radius, dot_align, topdot_offset
  bottomdot_offset = lerp(dot_radius, 2*bottom_radius-dot_radius, dot_align)
  print dot_radius, bottom_radius, dot_align, bottomdot_offset
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
  dot = \
      ( 0.,                       dot_radius
      , circle4k*dot_radius,      dot_radius
      , dot_radius,               circle4k*dot_radius
      , dot_radius,               0.
      , dot_radius,               -circle4k*dot_radius
      , circle4k*dot_radius,      -dot_radius
      , 0.,                       -dot_radius
      , -circle4k*dot_radius,     -dot_radius
      , -dot_radius,              -circle4k*dot_radius
      , -dot_radius,              0.
      , -dot_radius,              circle4k*dot_radius
      , -circle4k*dot_radius,     dot_radius
      , 0.,                       dot_radius )
  # yin outer goes bottom to right to top
  yin = inner[:-2] + \
      ( 0.,                       radius
      , circle4k*radius,          radius
      , radius,                   circle4k*radius
      , radius,                   0.
      , radius,                   -circle4k*radius
      , circle4k*radius,          -radius
      , 0.,                       -radius )
  yindot = adds(dot, (0, topdot_offset))
  # yang outer goes bottom to left to top
  yang = \
      ( 0.,                       radius
      , -circle4k*radius,         radius
      , -radius,                  circle4k*radius
      , -radius,                  0.
      , -radius,                  -circle4k*radius
      , -circle4k*radius,         -radius
      , 0.,                       -radius )[:-2] + inner
  yangdot = adds(dot, (0, bottomdot_offset))
  return ( ((yin, True),(yindot, True),(yangdot, True)), ((yang, True),(yangdot, True),(yindot, True)) )


def gimp_yinyang(radius=1.0
    , dot_radius=0.6, dot_align=0.5, angle=0.0, ratio=0.5):
  return tuple( \
      tuple(bpd2gbpd(*bpsc) for bpsc in shape) \
    for shape in cubic_bezier_yinyang(radius, dot_radius, dot_align, angle, ratio))
