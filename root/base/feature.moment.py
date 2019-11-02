from PIL import Image
import numpy as np
import cv2

if __name__ == "__main__":
    import sys, os
    sys.path.append( os.getcwd() )

from base.console_message import comment, state, error, warn
from base.feature import Feature
class Moment( Feature ):
    def __init__(self, env, image = None):
        self.env = env;

        if( image.all() != None ):
            self.getMoment( image )
    
    def getMoment( self, image ):
        try:
            if( np.shape( image )[2] == 3):
                image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
        except:
            pass
        
        height, width = np.shape( image )
        y = height / 2
        x = width / 2

        demo = image  
        for h in range( height ):
            for w in range( width ):
                demo = image 

                if( image[h][w] < 200 ):
                    colour_scale = ( ( 255 - image[h][w] ) / 255 )

                    if( round(x) != h ):
                        tmp_y = ( h + y ) / 2
                        y = y + ( tmp_y - y ) * colour_scale
                    
                    if( round(y) != w ):
                        tmp_x = ( w + x ) / 2
                        x = x + ( tmp_x - x ) * colour_scale
        
        self.value = {
                        'x': x,
                        'y': y 
                    }