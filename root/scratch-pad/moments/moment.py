from PIL import Image
import numpy as np
import cv2

class Moment:
    def __init__(self, env, image = None):
        self.env = env;

        if( image.all() != None ):
            self.value = self.getMoment( image )
    
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
        # print({
        #     'y': y, 
        #     'x': x
        # })
        # print( image )
        # print( '( ( w / width ) * colour_scale + y ) / 2' )
        for h in range( height ):
            for w in range( width ):
                # vervang die met die threshold
                demo = image 

                if( image[h][w] < 200 ):
                    # input()
                    colour_scale = ( ( 255 - image[h][w] ) / 255 )
                    # print( f'\nh:{h} w:{w}' )            
                    # print( f'Colour scale: {colour_scale}' )

                    if( round(x) != h ):
                        # print({'h':h, 'w': w})
                        # print( f'x: {h+y} / 2 = {( h + y ) / 2} x {(1-colour_scale )} = {( h + y ) / 2 * (1-colour_scale )}')
                        # x = ( ( h / height ) * colour_scale + x ) / 2
                        tmp_y = ( h + y ) / 2
                        y = y + ( tmp_y - y ) * colour_scale
                        # y *= ( 1 - colour_scale )
                        # y = ( h + y ) / 2
                    
                    
                    if( round(y) != w ):
                        # print({'h':h, 'w': w})
                        # print( f'y: {w+x} / 2 = {( w + x ) / 2} x {(1-colour_scale )} = {( w + x ) / 2 * (1-colour_scale )}')
                        # y = ( ( w / width ) * colour_scale + y ) / 2
                        tmp_x = ( w + x ) / 2
                        x = x + ( tmp_x - x ) * colour_scale
                        # x *= ( 1 - colour_scale )
                        # x = ( w + x ) / 2

                    # print( f'y:{y} x:{x}' )

                    # demo[int(round(y))][int(round(x))] = 0
                    # cv2.imshow( 'after', demo )
                    # cv2.waitKey( 0 )
                    # cv2.destroyAllWindows()


        # print({
        #     'x': x,
        #     'y': y 
        # })

        # image[int(round(y))][int(round(x))] = 0
        # cv2.imshow( 'before', image )
        # cv2.waitKey( 0 )
        # cv2.destroyAllWindows()

        
        return {
            'x': x,
            'y': y 
        }


if __name__ == "__main__":
    env = {
        'parameters': {
            'moments': {
                'msg': 'Toets die env.'
            }
        }
    }

    image = cv2.imread('images/0050-1_102.tif')

    # image = [[255, 255, 0, 255, 0],
    #          [255, 255, 255, 255, 255],
    #          [255, 255, 255, 255, 255],
    #          [255, 255, 255, 255, 255],
    #          [255, 255, 255, 100, 255]];
    # image = cv2.cvtColor(np.array( Image.fromarray( np.asfarray( Moment( env, image ).value )) ), cv2.COLOR_RGB2BGR)
    
    # cv2.imshow( 'before', image )
    # cv2.waitKey( 0 )
    # cv2.destroyAllWindows()

    print( Moment( env, image ).value )