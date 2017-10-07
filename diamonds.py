from random import randint
import numpy as np

from pattern import DF_Pattern
import helpers as help

off = 0
offset = lambda x: (x+off) % 16

COLOR_BUFFER = 6


class Diamonds(DF_Pattern):
    def __init__(self, *args, **kargs):
        DF_Pattern.__init__(self, *args, **kargs)
        # import pdb; pdb.set_trace()
        self.iteration = 0
        self.h = 0.
        self.dh = 0.05
        self.colors = np.zeros((COLOR_BUFFER, 3), 'uint')
        # self.data = np.zeros((self.ROWS*self.COLS*3), 'uint8')
        print 'init'

    def change_velocity(self):
        self.x_vel = randint(-1, 1)
        self.y_vel = randint(-1, 1)
        if self.x_vel == 0 and self.y_vel == 0:
                self.x_vel = 1

    def step(self):
        # print "Center at r:%d c:%d\n" % (ROWS/2, COLS/2)
        r, g, b = 0., 0., 0.
        r, g, b = help.hsv_rgb(r, g, b, self.h)

        self.colors[0][0] = r
        self.colors[0][1] = g
        self.colors[0][2] = b

        # pick color for 'ring'
        for i in range(COLOR_BUFFER-1, 0, -1):
            self.colors[i] = self.colors[i-1]

        # calculate (x, y) of each square in 'ring'
        for j in range(self.COLS):
            for i in range(self.ROWS):
                # j = (j + off) % 16
                # distance from center
                dist = abs(i-self.ROWS/2.) + abs(j-self.COLS/2.)
                self.df = help.set_pixel(self.df,  # mod_data
                                         (i+self.iteration) % self.ROWS,  # y
                                         (j+self.iteration) % self.COLS,  # x
                                         self.colors[dist % COLOR_BUFFER])  # color

        self.h += self.dh
        if self.h > 1:
            self.h = 0

        self.iteration += 1
        return self.df

    def set_color(self, mod_data, y, x, color):
        i = (self.COLS*y+x)*3
        mod_data[i] = color[0]  # (color >> 16) & 0xFF
        mod_data[i+1] = color[1]  # (color >> 8) & 0xFF
        mod_data[i+2] = color[2]  # color & 0xFF
        return mod_data