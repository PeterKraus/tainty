import weakref
import math


def _sos(*args):
    return sum([i ** 2 for i in args])


class tufloat(object):
    def __init__(self, n: float, s: float, refs=None):
        self._nominal_value = n
        self._abs_dev = s
        self._rel_dev = s / n
        self._refs = weakref.WeakKeyDictionary()
        self._refs[self] = True
        if refs is not None:
            # assert isinstance(refs, weakref.WeakKeyDictionary), f"{type(refs)}"
            self._refs.update(refs)

    @property
    def nominal_value(self):
        return self._nominal_value

    @property
    def abs_dev(self):
        return self._abs_dev

    @property
    def rel_dev(self):
        return self._rel_dev

    @property
    def refs(self):
        return self._refs

    n = nominal_value
    s = abs_dev
    r = rel_dev

    def __bool__(self):
        return self.n != 0 or self.s != 0

    def __repr__(self):
        return f"{self.n:f}+/-{self.s:f}"

    def __add__(self, b):
        if isinstance(b, tufloat):
            newn = self.n + b.n
            news = _sos(self.s, b.s) ** 0.5
            ret = tufloat(newn, news, self.refs | b.refs)
            return ret
        elif isinstance(b, (float, int)):
            newn = self.n + b
            news = self.s
            ret = tufloat(newn, news, self.refs)
            return ret
        else:
            raise TypeError

    def __radd__(self, b):
        return self.__add__(b)

    def __sub__(self, b):
        if isinstance(b, tufloat):
            newn = self.n - b.n
            newv = _sos(self.s, b.s)
            if b in self.refs or self in b.refs:
                newv -= 2 * self.s * b.s
            news = newv ** 0.5
            ret = tufloat(newn, news, self.refs | b.refs)
            return ret
        elif isinstance(b, (int, float)):
            newn = self.n - b
            news = self.s
            ret = tufloat(newn, news, self.refs)
            return ret
        else:
            raise TypeError

    def __rsub__(self, b):
        if isinstance(b, tufloat):
            return b.__sub__(self)
        elif isinstance(b, (int, float)):
            newn = b - self.n
            news = self.s
            ret = tufloat(newn, news, self.refs)
            return ret
        else:
            raise TypeError

    def __mul__(self, b):
        if isinstance(b, tufloat):
            newn = self.n * b.n
            newv = _sos(self.r, b.r)
            if b in self.refs or self in b.refs:
                newv += 2 * self.s * b.s / (self.n * b.n)
            newr = newv ** 0.5
            ret = tufloat(newn, abs(newn) * newr, self.refs | b.refs)
            return ret
        elif isinstance(b, (int, float)):
            newn = self.n * b
            news = self.s * b
            ret = tufloat(newn, abs(news), self.refs)
            return ret
        else:
            raise TypeError

    def __rmul__(self, b):
        return self.__mul__(b)

    def __truediv__(self, b):
        if isinstance(b, tufloat):
            newn = self.n / b.n
            newv = _sos(self.r, b.r)
            if b in self.refs or self in b.refs:
                newv -= 2 * self.s * b.s / (self.n * b.n)
            newr = newv ** 0.5
            ret = tufloat(newn, abs(newn) * newr, self.refs | b.refs)
            return ret
        elif isinstance(b, (int, float)):
            newn = self.n / b
            newr = self.r
            ret = tufloat(newn, abs(newn) * newr, self.refs)
            return ret
        else:
            raise TypeError

    def __rtruediv__(self, b):
        if isinstance(b, tufloat):
            return b.__div__(self)
        elif isinstance(b, (int, float)):
            newn = b / self.n
            newr = self.r
            ret = tufloat(newn, abs(newn) * newr, self.refs)
            return ret
        else:
            raise TypeError

    def __pow__(self, b):
        if isinstance(b, tufloat):
            newn = self.n ** b.n
            newv = _sos(b.n * self.r, math.log(self.n) * b.s)
            if b in self.refs or self in b.refs:
                newv += 2 * b.n * math.log(self.n) / self.n
            newr = newv ** 0.5
            ret = tufloat(newn, abs(newn) * newr, self.refs | b.refs)
            return ret
        elif isinstance(b, (int, float)):
            newn = self.n ** b
            news = newn * b * self.r
            ret = tufloat(newn, news, self.refs)
            return ret
        else:
            raise TypeError

    def __rpow__(self, b):
        if isinstance(b, tufloat):
            return b.__pow__(self)
        elif isinstance(b, (int, float)):
            newn = b ** self.n
            news = abs(newn) * abs(math.log(b) * self.s)
            ret = tufloat(newn, news, self.refs)
            return ret
        else:
            raise TypeError

    def __abs__(self):
        ret = tufloat(abs(self.n), self.s, self.refs)
        return ret

    def __floordiv__(self):
        print("stub floordiv")
        return None

    def __rfloordiv__(self):
        print("stub rfloordiv")
        return

    def __mod__(self):
        print("stub mod")
        return None

    def __rmod__(self):
        print("stub rmod")
        return None

    def __eq__(self, b):
        if isinstance(b, tufloat) and self.__hash__() == b.__hash__():
            return True
        else:
            return False

    def __lt__(self, b):
        if isinstance(b, tufloat):
            comp = b.n
        elif isinstance(b, int):
            comp = float(b)
        elif isinstance(b, float):
            comp = b
        return self.n < comp

    def __gt__(self, b):
        if isinstance(b, tufloat):
            comp = b.n
        elif isinstance(b, int):
            comp = float(b)
        elif isinstance(b, float):
            comp = b
        return self.n > comp

    def __le__(self, b):
        return self.__eq__(b) or self.__lt__(b)

    def __ge__(self, b):
        return self.__eq__(b) or self.__gt__(b)

    def __hash__(self):
        return hash((self.n, self.s))
