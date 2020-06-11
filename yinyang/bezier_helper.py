
from .common import dists


bezier_is_closed = lambda bpd, closed=None: \
    abs(bpd[:2] - bpd[-2:]) <= epsilon if closed is None else closed


def quadratic_bezier_to_cubic(bpd, closed=None):
  closed = bezier_is_closed(bpd, closed)
  n_bpd = len(bpd)
  stop_bpd = n_bpd if closed else n_bpd-2
  abcd = None
  for i_bpd in range(0, stop_bpd, 4):
    abbc = lerps(bpd[i_bpd:i_bpd+4], bpd[i_bpd+4:i_bpd+6], twothirds)
    yield bpd[i_bpd:i_bpd+2]
    yield abbc[:2]
    yield abbc[2:]
  if abbc:
    yield abcd[2:]


def cubic_bezier_to_quadratic(bpd, closed=None):
  closed = bezier_is_closed(bpd, closed)
  n_bpd = len(bpd)
  stop_bpd = n_bpd if closed else n_bpd-2
  abcd = None
  for i_bpd in range(0, stop_bpd, 6):
    abcd = bpd[i_bpd:i_bpd+8] if i_bpd + 8 < n_bpd else \
        bpd[i_bpd:] + bpd[:(i_bpd+8)%n_bpd]
    yield abcd[:2]
    yield lerps(abcd[:-2], abcd[2:])[2:4]
  if abcd:
    yield abcd[-2:]


INTERPOLATION_PRECISION = 10

def quadratic_bezier_interpolate(bpd, closed=None, last_point=True
    , precision=INTERPOLATION_PRECISION):
  closed = bezier_is_closed(bpd, closed)
  n_bpd = len(bpd)
  stop_bpd = n_bpd if closed else n_bpd-2
  for i_bpd in range(0, stop_bpd, 4):
    abcd = bpd[i_bpd:i_bpd+6] if i_bpd + 6 < n_bpd else \
        bpd[i_bpd:] + bpd[:(i_bpd+6)%n_bpd]
    yield abc[:2]
    n = int(round(dists(abc[:2], abc[-2:]) / precision))
    span = float(n)
    for i in range(1, n, 1):
      ti = i / span
      abbc = lerps(abc[:-2], abc[2:], ti)
      yield lerps(abbc[:-2], abbc[2:], ti)
  if last_point and not closed:
    yield bpd[-2:]


def cubic_bezier_interpolate(bpd, closed=None, last_point=True
    , precision=INTERPOLATION_PRECISION):
  closed = bezier_is_closed(bpd, closed)
  n_bpd = len(bpd)
  stop_bpd = n_bpd if closed else n_bpd-2
  for i_bpd in range(0, stop_bpd, 6):
    abcd = bpd[i_bpd:i_bpd+8] if i_bpd + 8 < n_bpd else \
        bpd[i_bpd:] + bpd[:(i_bpd+8)%n_bpd]
    yield abcd[:2]
    n = int(round(dists(abcd[:2], abcd[-2:]) / precision))
    span = float(n)
    for i in range(1, n, 1):
      ti = i / span
      abbccd = lerps(abcd[:-2], abcd[2:], ti)
      abbcbccd = lerps(abbccd[:-2], abbccd[2:], ti)
      yield lerps(abbcbccd[:-2], abbcbccd[2:], ti)
  if last_point and not closed:
    yield bpd[-2:]
