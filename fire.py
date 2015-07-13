import numpy as np
from pattern import DF_Pattern

rows, cols = 16, 16
bitmap_buffer = np.zeros((rows, cols, 3), 'uint8')


class Fire(DF_Pattern):
    def __init__(self, rows=16, cols=16, *args, **kargs):
        DF_Pattern.__init__(self, *args, **kargs)
        self.rows = rows
        self.cols = cols
        
        self.fire_buffer = np.zeros((self.rows, self.cols), 'uint8')
        self.color_buffer = np.zeros((self.rows*self.cols*1, 3), 'uint8')

        for i in range(len(self.fire_buffer)):
            self.fire_buffer[i] = self.rows
            
        for i in range(64):
            self.color_buffer[i]     = (i*4, 0, 0)
            self.color_buffer[i+64]  = (255, i*4, 0)
            self.color_buffer[i+128] = (255, 255, i*4)
            self.color_buffer[i+192] = (255-i*4, 255-i*4, 255)
            
        self.buff = self.rows*self.cols*3
       
    def step(self):
        for y in range(self.rows):
            self.fire_buffer[:][y] = (np.random.rand() % 2) * 255
            
        for x in range(self.cols):
            for y in range(self.rows):
                color = self.fire_buffer[x][y]
                
                for i in range(y-1, y+1):  # add current and prior
                    # print (i+self.rows) % self.rows
                    color += self.fire_buffer[x][(i+self.rows) % self.rows]
                    
                color /= 3  # changes intensity of the redness, higher numbers get darker
                color -= 2
                if color < 0:
                    color = 0
                if color > 255:
                    color = 255
                    
                self.fire_buffer[x][y] = color
                self.df[x][y] = self.color_buffer[color]

        return self.df