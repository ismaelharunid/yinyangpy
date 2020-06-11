import sys

from math import pi, sqrt
epsilon = sys.float_info.epsilon
sixthpi = pi / 6
quarterpi = .25 * pi
thirdpi = pi / 3
halfpi = .5 * pi
twopi = 2 * pi
circle4k = 0.55191502449
twothirds = 2. / 3.

dist = lambda x, y: sqrt(x*x + y*y)
_dists = lambda a,an, b,bn: sqrt(sum((a[i%an]-b[i%bn])**2 for i in range(max(an,bn))))
dists = lambda a, b=(0,): _dists(a,len(a), b,len(b))
lerp = lambda a, b, t=0.5: a + (b-a) * t
lerps = lambda sa, sb, t=0.5: type(sa)(lerp(sa[i],sb[i],t) for i in range(len(sa)))

inbounce = lambda i,n,s=1: (n-abs(n-float(i)%(2*n)))*s/n

_scales = lambda s, sn, d, dn: (s[i]*d[i%dn] for i in range(sn))
scales = lambda s, d: type(s)(_scales(s, len(s), d, len(d)))

is2tuple = lambda v: type(value) is tuple and len(value) == 2

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

