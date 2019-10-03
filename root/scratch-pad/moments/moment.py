from PIL import Image
import numpy as np
import cv2

class Moment:
    def __init__(self, env):
        self.env = env;
    
    def getMoment( self, image ):
        if( np.shape( image )[2] == 3):
            image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
        
        height, width = np.shape( image )
        y = height / 2
        x = width / 2
        image = cv2.bitwise_not( image )
        for h in range( height ):
            for w in range( width ):
                y = ( ( h / height ) * ( image[h][w] / 255 ) + h ) / 2
                x = ( ( w / height ) * ( image[h][w] / 255 ) + w ) / 2


            print({
                'y': y, 
                'x': x
            })

        image[int(round(y))][int(round(x))] = 255;
        
        cv2.imshow( 'before', image )
        cv2.waitKey( 0 )
        cv2.destroyAllWindows()
        return self.env['parameters']['moments']['msg']


if __name__ == "__main__":
    env = {
        'parameters': {
            'moments': {
                'msg': 'Toets die env.'
            }
        }
    }

    image = cv2.imread('images/0050-1_102.tif')

    print( Moment( env ).getMoment( image ) )