
MODULE_PATH = '/where/ever/you/put/the/yinyang/module'
MODULE_PATH = '/home/ismael/Projects/my-python-modules/enabled'

import sys
if MODULE_PATH not in sys.path:
  sys.path.append(MODULE_PATH)

import yinyang
from yinyang import GimpRenderer, gbpdc2gvs
image = gimp.image_list()[0]
iwidth, iheight = image.width, image.height
iradius = .5 * min(iwidth, iheight)
radius = .95 * iradius
dot_radius = radius / 6.
gvyin = pdb.gimp_vectors_new(image, "Yin")
pdb.gimp_image_insert_vectors(image, gvyin, None, 0)
gvyin.visible = gvyin.linked = True
gvyang = pdb.gimp_vectors_new(image, "Yang")
pdb.gimp_image_insert_vectors(image, gvyang, None, 1)
gvyang.visible = gvyang.linked = True
gbshapes = yinyang.gimp_yinyang(radius, dot_radius)

for (gbpd, gbpc) in gbshapes[0]:
  yinyang.gbpdc2gvs(gvyin,gbpd,gbpc)

for (gbpd, gbpc) in gbshapes[1]:
  yinyang.gbpdc2gvs(gvyang,gbpd,gbpc)
