
class Color(object):
    _MIN = 0
    _MAX = 255

    def __init__(self, r=100, g=100, b=100):
        self.rgb = []
        for val in (r, g, b):
            if val > self._MAX:
                val = self._MAX
            elif val < self._MIN:
                val = self._MIN
            self.rgb.append(val)

    def __str__(self):
        return "Color{}".format(tuple(self.rgb))

    __repr__ = __str__

    def __add__(self, other):
        r,g,b = [sum(x) for x in zip(self.rgb,other.rgb)]
        return Color(r,g,b)

    def __sub__(self, other):
        r, g, b = [x1 - x2 for (x1, x2) in zip(self.rgb,other.rgb)]
        return Color(r, g, b)

    def __mul__(self, other):
        r, g, b = [v * other for v in self.rgb]
        return Color(r, g, b)

    def __iter__(self):
        for v in self.rgb:
            yield v

    def __getitem__(self, item):
        return self.rgb[item]
