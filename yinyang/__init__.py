
from .generators import cubic_bezier_yinyang, gimp_yinyang
from .renderer import Renderer
from .render_yinyang import render

#from GIFRenderer, SVGRenderer, PILRenderer


try:
  assert 'gimp' in globals() and hasattr(gimp, 'pdb')
  from .gimp_renderer import GimpRenderer
except:
  class GimpRenderer(Renderer):
    def __init__(self, *args, **kwargs):
      raise ModuleNotFoundError('GimpRenderer only works with the gimp ' \
          'environment, try the GIFRenderer or PILRenderer outside of gimp')

