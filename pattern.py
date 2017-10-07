__author__ = 'tbrooks'
import numpy as np


class DF_Pattern:
    def __init__(self, df=np.zeros((8, 24, 3), dtype=np.uint8)):
        self.debug = False

        self.df = df
        self.state = False

        self.ROWS = 8
        self.COLS = 24
        self.max_dim = max([self.ROWS, self.COLS])

        self.x_vel = 1
        self.y_vel = 1
        self.vel_counter = 0
        self.vel_duration = 10

        self.square_counter = 0
        self.square_freq = 10

    def step(self):
        print('No step function set')