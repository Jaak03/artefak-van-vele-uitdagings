from PIL import Image
import numpy as np
import cv2

class Moment:
    def __init__(self, env):
        self.env = env;
    
    def getMoment( self, image ):
        try:
            if( np.shape( image )[2] == 3):
                image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
        except:
            pass
        
        height, width = np.shape( image )
        y = height / 2
        x = width / 2

        # for pixel in image:
        #     pixel = abs( 255 - pixel )

        demo = image  
        print({
            'y': y, 
            'x': x
        })
        print( image )
        for h in range( height ):
            for w in range( width ):
                if( image[h][w] < 200 ):
                    demo = image 
                    print( f'y: {( h / height )} x {( image[h][w] / 255)} + {y} / 2 = {( ( h / height ) * ( image[h][w] / 255 - 1) + h ) / 2}')
                    print( f'x: {( w / width )} x {( image[h][w] / 255)} + {x} / 2 = {( ( w / width ) * ( image[h][w] / 255 - 1) + w ) / 2}')

                    input()
                    colour_scale = ( ( 255 - image[h][w] ) / 255 );
                    if(( h / height ) * colour_scale > 0 ):
                        x = ( ( h / height ) * colour_scale + x ) / 2
                    if(( w / width ) * colour_scale > 0 ):   
                        y = ( ( w / width ) * colour_scale + y ) / 2
                    # print( f'y:{y} x:{x}' )

                    # demo[int(round(y))][int(round(x))] = 0
                    # cv2.imshow( 'after', demo )
                    # cv2.waitKey( 0 )
                    # cv2.destroyAllWindows()


        print({
            'x': x,
            'y': y 
        })

        image[int(round(y))][int(round(x))] = 0
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

    # image = cv2.imread('images/0050-1_102.tif')

    image = [[255, 255, 0, 255, 255],
             [255, 255, 255, 255, 255],
             [255, 255, 255, 255, 255],
             [255, 255, 255, 255, 255],
             [255, 255, 255, 255, 255]];
    image = cv2.cvtColor(np.array( Image.fromarray( np.asfarray( image )) ), cv2.COLOR_RGB2BGR)
    
    cv2.imshow( 'before', image )
    cv2.waitKey( 0 )
    cv2.destroyAllWindows()

    print( Moment( env ).getMoment( image ) )