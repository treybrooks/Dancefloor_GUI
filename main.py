from nodebox.graphics import *
import numpy as np
import socket

from buttons import Button, PlayPause, PatternButton, ClearButton
import square_dance as sd
import diamonds as dia

from helpers import c_scale, convert_array

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

LATCH = bytearray(list('DANCEFLOOR') + [2])

port = 21337

u1 = '10.0.0.11'
u2 = '10.0.0.12'
u3 = '10.0.0.13'
u4 = '10.0.0.14'

red = Color(*c_scale(255, 0, 0))
green = Color(*c_scale(0, 255, 0))
blue = Color(*c_scale(0, 0, 255))

mod_width = 300
mod_height = 300

canvas.fps = 30
canvas.size = 800, 800


def split_data_into_quadrants(data):
    h = len(data)
    w = len(data[1])
    data0 = [data[i][:h / 2] for i in range(w / 2)]  # top_left
    data1 = [data[i][h / 2:] for i in range(w / 2)]  # top_right
    data2 = [data[i][:h / 2] for i in range(w / 2, w)]  # bot_left
    data3 = [data[i][h / 2:] for i in range(w / 2, w)]  # bot_right
    return [np.asarray(data0), np.asarray(data1), np.asarray(data2), np.asarray(data3)]


class Light(Layer):
    def __init__(self, clr=Color(0), point=(0,0), *args, **kargs):
        Layer.__init__(self, *args, **kargs)
        self.clr = clr
        self.point = point

    def draw(self):
        border = 1
        fill(self.clr)
        rect(self.x+border, self.y+border, self.height-(2*border), self.width-(2*border))

    def set_color(self, clr):
        self.clr = clr


class Module(Layer):
    def __init__(self, clr=Color(0), ip=None, rows=8, cols=8, *args, **kargs):
        Layer.__init__(self, *args, **kargs)
        self.clr = clr
        self.ip = ip
        self.rows = rows
        self.cols = cols
        self.data = np.zeros((rows, cols, 3), dtype=np.uint8)
        self.lights = []

        width = self.width / self.cols
        height = self.height / self.rows
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                x = self.x + col * width
                y = self.y + row * height
                light = Light(clr=self.clr, point=(row, col), x=x, y=y, width=width, height=height)
                self.lights.append(light)

    def update_data(self, data):
        # update all the colors of the lights inside the module
        self.data = data
        for light in self.lights:
            x, y = light.point
            # make it a nodebox color
            clr = Color(c_scale(*data[x, y]))
            light.set_color(clr)

    def draw(self):
        for light in self.lights:
            light.draw()


class DanceFloor(Layer):
    def __init__(self, df_fps=2, *args, **kargs):
        Layer.__init__(self, *args, **kargs)
        self.data = np.zeros((16, 16, 3), dtype=np.uint8)  # static and properly shouldn't be
        self.df_fps = df_fps
        self.counter = 0

        mod1 = Module(clr=red, ip=u1, x=0, y=mod_height, width=mod_width, height=mod_height)
        mod2 = Module(clr=green, ip=u2, x=mod_width, y=mod_height, width=mod_width, height=mod_height)
        mod3 = Module(clr=blue, ip=u3, x=0, y=0, width=mod_width, height=mod_height)
        mod4 = Module(clr=red, ip=u4, x=mod_width, y=0, width=mod_width, height=mod_height)
        self.modules = [mod1, mod2, mod3, mod4]

        self.play = True
        # self.pattern = sd.SquareDance(self.data)
        self.pattern = dia.Diamonds(self.data)

    def play_pause(self):
        print(('Play', 'Pause')[self.play])
        self.play = not self.play

    def set_algorithm(self, algorithm):
        self.pattern = algorithm

    def clear_df(self):
        zs = np.zeros((16, 16, 3), dtype=np.uint8)  # static and properly shouldn't be
        self.data = zs
        return zs

    def draw(self):
        for module in self.modules:
            module.draw()

    def update(self):
        if self.play:
            if self.counter >= canvas.fps / self.df_fps:
                self.df_write()
                self.counter = 0

                data_list = split_data_into_quadrants(self.data)
                for module, data in zip(self.modules, data_list):
                    module.update_data(data)

            self.data = self.pattern.step()
            self.counter += 1

    def df_write(self):
        # steps need to be separate to avoid syncing issues
        # Write data to module
        for module in self.modules:
            sock.sendto(convert_array(np.asarray(module.data)), (module.ip, port))

        # Latch frame
        for module in self.modules:
            sock.sendto(LATCH, (module.ip, port))


def draw(canvas):
    dance_floor.draw()

dance_floor = DanceFloor(df_fps=10, x=100, y=50)

sq_d_fxn = sd.SquareDance()
dia_fxn = dia.Diamonds()

pause_button = PlayPause(function=dance_floor.play_pause,
                         x=0, y=600, width=100, height=30)

diamonds_button = PatternButton(dance_floor, dia_fxn, x=110, y=600, width=100, height=30)
square_dance_button = PatternButton(dance_floor, sq_d_fxn, x=220, y=600, width=100, height=30)

clear_button = ClearButton(dance_floor, dance_floor.clear_df,
                         x=330, y=600, width=100, height=30)

dance_floor.append(pause_button)
dance_floor.append(diamonds_button)
dance_floor.append(square_dance_button)
dance_floor.append(clear_button)

canvas.append(dance_floor)

# import pdb
# pdb.set_trace()
canvas.run()