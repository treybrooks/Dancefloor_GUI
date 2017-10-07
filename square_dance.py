from random import randint, choice

import numpy as np

import helpers as h
from pattern import DF_Pattern


# Define basic colors
pink = [200, 25, 25]
red = [255, 0, 0]

orange = [255, 128, 0]
yellow = [255, 255, 0]

green = [0, 255, 0]
turq = [0, 200, 200]
blue = [0, 0, 255]
purple = [150, 20, 102]

black = [0, 0, 0]

# the HULK
rich_purple = [123, 50, 148]  # rather pink
med_purple = [194, 165, 207]  # similar to white
white = [247, 247, 247]  # kind of pink
med_green = [166, 219, 160]
dark_green = [0, 136, 55]

the_hulk = [rich_purple, white, med_green, dark_green]


# halloween
halloween = [green, orange, black, purple]

# color Sea themed colors
under_the_sea = [turq, blue, green, purple]

# Christmas
xmas = [red, green, white]

# Bubble Gum
bubble_gum = [purple, rich_purple, pink, black]

# Martins Wedding
wedding = [purple, white, pink, black]

# The Blues
blues = [turq, blue, orange, black]
# bubble_gum xmas,
schemes = [under_the_sea]


def draw_line(df, x1, y1, x2, y2, color, x_max=24, y_max=8):
    if x1 > x_max:
        x1 = x_max
    elif x1 < 0:
        x1 = 0

    if x2 > x_max:
        x2 = x_max
    elif x2 < 0:
        x2 = 0

    if y1 > y_max:
        y1 = y_max
    elif y1 < 0:
        y1 = 0

    if y2 > y_max:
        y2 = y_max
    elif y2 < 0:
        y2 = 0

    dx = abs(x2-x1)+1
    dy = abs(y2-y1)+1
    d = [dx, dy]

    xpoints = [int(round(p)) for p in np.linspace(x1, x2, max(d))]
    ypoints = [int(round(p)) for p in np.linspace(y1, y2, max(d))]

    for i in range(len(xpoints)):
        x = xpoints[i]
        y = ypoints[i]
        df = h.set_pixel(df, x, y, color)

    return df


def draw_square(df, center, size, color):
    # draw right line
    df = draw_line(df, center[0]-size/2+1, center[1]+size/2,   center[0]+size/2,   center[1]+size/2,   color)
    # draw bottom line
    df = draw_line(df, center[0]+size/2,   center[1]+size/2-1, center[0]+size/2,   center[1]-size/2+1, color)
    # draw left line
    df = draw_line(df, center[0]-size/2+1, center[1]-size/2+1, center[0]+size/2,   center[1]-size/2+1, color)
    # draw top line
    df = draw_line(df, center[0]-size/2+1, center[1]+size/2,   center[0]-size/2+1, center[1]-size/2+1, color)
    return df


def draw_filled_square(df, center, size, color):
    for i in range(size):
        df = draw_line(
            df,
            center[0]-size/2+1+i,
            center[1]+size/2,
            center[0]-size/2+1+i,
            center[1]-size/2+1,
            color
        )
    return df


class SquareDance(DF_Pattern):
    def __init__(self, *args, **kargs):
        DF_Pattern.__init__(self, *args, **kargs)
        self.color_list = choice(schemes)
        # self.df = np.zeros((8, 24, 3), dtype=np.uint8)

    def what_to_draw(self, operation):
        if operation == 0:
            if self.debug:
                print 'square'

            size = randint(3, self.max_dim-2)
            center = [randint(2, self.ROWS-1), randint(2, self.COLS-1)]
            color = choice(self.color_list)
            self.df = draw_square(self.df, center, size, color)

        elif operation == 1:
            if self.debug:
                print 'full square'

            size = randint(3, self.max_dim/3)
            center = [randint(2, self.ROWS-1), randint(2, self.COLS-1)]
            color = choice(self.color_list)
            self.df = draw_filled_square(self.df, center, size, color)

        else:
            if self.debug:
                print 'no action taken'

    def change_velocity(self):
        self.x_vel = randint(-1, 1)
        self.y_vel = randint(-1, 1)
        if self.x_vel == 0 and self.y_vel == 0:
                self.x_vel = 1

    def step(self):
        if self.vel_counter >= self.vel_duration:
            self.change_velocity()
            self.vel_counter = 0

        if self.square_counter >= self.square_freq:
            operation = randint(0, 5)
            self.what_to_draw(operation)
            self.square_counter = 0

        self.df = np.roll(self.df, self.x_vel, axis=1)
        self.df = np.roll(self.df, self.y_vel, axis=0)

        self.vel_counter += 1
        self.square_counter += 1
        return self.df