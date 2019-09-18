import numpy as np
from PIL import Image
import cv2

BIG = 100
SMALL = 27

big_image = Image.fromarray( np.uint8( np.full([BIG,BIG], 255) ))
small_image = Image.fromarray( np.uint8( np.full([SMALL,36], 0) ))

def pasteIn( small_image, big_image ):
    small_dim = np.shape( np.array( small_image ) )
    big_dim = np.shape( np.array( big_image ) )

    coordinates = []

    print( small_dim )
    print( big_dim )

    # werk eers op die eerste as.
    s_ax = small_dim[ 0 ]
    b_ax = big_dim[ 0 ]

    if( s_ax == b_ax ):
        print( 'Dimension stays the same.' )
        coordinates.append( 0 )
        pass
    elif( s_ax > b_ax):
        coordinates.append( 0 )
        print( 'Resize the image.' )
    else:
        coordinates.append( int( ( b_ax/2 ) - ( s_ax/2 ) ) )
    
    # werk dan op die tweede as
    s_ax = small_dim[ 1 ]
    b_ax = big_dim[ 1 ]

    if( s_ax == b_ax ):
        print( 'Dimension stays the same.' )
        coordinates.append( 0 )
        pass
    elif( s_ax > b_ax):
        print( 'Resize the image.' )
        coordinates.append( 0 )
    else:
        coordinates.append( int( ( b_ax/2 ) - ( s_ax/2 ) ) )
    
    print( f"Paste image here { coordinates }" )

    big_image.paste( small_image, ( coordinates[ 1 ], coordinates[ 0 ]) )

    return big_image;

pasteIn( small_image, big_image ).show()
