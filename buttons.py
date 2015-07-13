from nodebox.graphics import *


def default_fxn():
    print('I am the default function!')


class Button(Layer):
    def __init__(self, function=default_fxn, function_args=[], *args, **kwargs):
        Layer.__init__(self, *args, **kwargs)
        self.clr = Color(0.8)
        if len(function_args) > 0:
            self.function = function(*function_args)
        else:
            self.function = function

    def draw(self):
        rect(0, 0, self.width, self.height, fill=self.clr)

    def on_mouse_press(self, mouse):
        self.clr = Color(random())

    def copy(self):
        button = Layer.copy(self)
        button.clr = self.clr.copy()
        return button


class PlayPause(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self.clr = Color(0.8)
        self.state = True

    def on_mouse_press(self, mouse):
        self.state = not self.state
        return self.function()

    def on_mouse_release(self, mouse):
        pass

    def draw(self):
        # print 'cat'
        mid_x = self.width / 2
        mid_y = self.height / 2

        if self.state:  # play
            rect(0, 0, self.width, self.height, fill=self.clr)
        else:  # pause
            rect(0, 0, self.width, self.height, fill=Color(0.3))

        fill(Color(1))
        # play
        triangle(self.width*0.2, self.height*0.1,  # point 1
                 self.width*0.2, self.height*0.9,  # point 2
                 self.width*0.4, mid_y)  # point 3
        # slash
        line(mid_x-5, mid_y-5, mid_x+5, mid_y+5)

        # equals
        # top
        rect(self.width*0.6, self.height*0.6,
             self.width*0.25, self.height*0.15)
        # bottom
        rect(self.width*0.6, self.height*0.2,
             self.width*0.25, self.height*0.15)


class ClearButton(Button):
    def __init__(self, df_obj, *args, **kargs):
        Button.__init__(self, *args, **kargs)
        self.clr = Color(0.2)
        self.df_obj = df_obj

    def on_mouse_press(self, mouse):
        self.df_obj.clear_df()

    def draw(self):
        rect(0, 0, self.width, self.height, fill=self.clr)
        fill(1)
        Text('Clear',
             x=self.width/2, y=self.height/2,
             width=None, height=None, align=CENTER,
             fill=Color(1))


class PatternButton(Button):
    def __init__(self, df_obj, algorithm, *args, **kargs):
        Button.__init__(self, *args, **kargs)
        self.clr = Color(0.2)
        self.df_obj = df_obj
        self.algorithm = algorithm

    def on_mouse_press(self, mouse):
        self.df_obj.set_algorithm(self.algorithm)
