import random

"""
Over the course of the years, Python has made changes to how their random module works.
The functions overrided, provide accurate function to Python 2.4 TTO.
Use this if you want to to make random functions behave exactly like Toontown Online.
"""

class Random(random.Random):

    def seed(self, a=None):
        from os import urandom as _urandom
        from hashlib import sha512 as _sha512
        if a is None:
            try:
                a = int.from_bytes(_urandom(2500), 'big')
            except NotImplementedError:
                import time
                a = int(time.time() * 256)
        super().seed(a)

    def randrange(self, start, stop=None, step=1, _int=int, default=None):
        istart = _int(start)
        if istart != start:
            raise ValueError("non-integer arg 1 for randrange()")
        if stop is default:
            if istart > 0:
                return _int(self.random() * istart)
            raise ValueError("empty range for randrange()")
        istop = _int(stop)
        if istop != stop:
            raise ValueError("non-integer stop for randrange()")
        width = istop - istart
        if step == 1 and width > 0:
            return _int(istart + _int(self.random()*width))
        if step == 1:
            raise ValueError("empty range for randrange() (%d,%d, %d)" % (istart, istop, width))
        istep = _int(step)
        if istep != step:
            raise ValueError("non-integer step for randrange()")
        if istep > 0:
            n = (width + istep - 1) // istep
        elif istep < 0:
            n = (width + istep + 1) // istep
        else:
            raise ValueError("zero step for randrange()")
        if n <= 0:
            raise ValueError("empty range for randrange()")
        return istart + istep*_int(self.random() * n)

    def choice(self, seq):
        return seq[int(self.random() * len(seq))]

_inst = Random()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
choices = _inst.choices
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits
