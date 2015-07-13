__author__ = 'tbrooks and Ben Vaughn'
from itertools import chain


def c_scale(r=0, g=0, b=0):
    return r/255.0, g/255.0, b/255.0


def hsv_rgb(r=0, g=0, b=0, h=0, s=1, v=0.5):
    if s == 0:
        r, g, b = 0, 0, 0
    else:
        _h = h*6.
        i = int(_h)

        double_1 = v * (1.0 - s)
        double_2 = v * (1.0 - s * (_h - i))
        double_3 = v * (1.0 - s * (1.0 - (_h - i)))

        if i == 0:
            _r, _g, _b = v, double_3, double_1
        elif i == 1:
            _r, _g, _b = double_2, v, double_1
        elif i == 2:
            _r, _g, _b = double_1, v, double_3
        elif i == 3:
            _r, _g, _b = double_1, double_2, v
        elif i == 4:
            _r, _g, _b = double_3, double_1, v
        else:
            _r, _g, _b = v, double_1, double_2

        return int(_r * 255), int(_g * 255), int(_b * 255)


class InvalidData(Exception):
    pass


def set_pixel(df, x, y, color):
    df[x, y, 0] = color[0]
    df[x, y, 1] = color[1]
    df[x, y, 2] = color[2]
    return df


def convert_array(arr):
    arr = arr.tostring()
    try:
        iter(arr[0])
        arr = list(chain.from_iterable(arr))
    except TypeError:
        pass
    data = list('DANCEFLOOR') + [1] + arr

    return bytearray(data)


def color_at(pattern, y, x):
    x = (x + pattern.COLS) % pattern.COLS
    y = (y + pattern.ROWS) % pattern.ROWS

    i = (pattern.COLS*y + x) * 3

    color = pattern.df[i] << 16   # Red
    color += pattern.df[i+1] << 8 # Green
    color += pattern.df[i+2]      # Blue

    return color


def validate_array(arr):
    size = 16*16
    if not len(arr) in (size, size * 3):
        raise InvalidData('array must be length 64 or 192')
    if len(arr) == size:
        for el in arr:
            if len(el) != 3:
                raise InvalidData('Element %s not length 3' % el)
            for i in el:
                if not 255 >= i >= 0:
                    raise InvalidData('Invalid RGB value %s', str(i))