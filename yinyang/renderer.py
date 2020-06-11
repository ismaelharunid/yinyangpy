
import sys, os
ospath = os.path
vinfo = sys.version_info
#major=3, minor=7, micro=6, releaselevel='final', serial=0
if vinfo.major == 2:
  # for gimp
  from collections import Mapping, MutableMapping, Container as Reversible, Sequence
else:
  from collections.abc import Mapping, MutableMapping, Reversible, Sequence

from .common import *


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
    self._frame_names = {}
    self._frames = {}
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
  


