import numpy as np
import matplotlib as plt
import cv2
from PIL import Image

from base.console_message import comment, warn, error, state
from base.message_bucket import TestMessage

# class ImageUtils:
#     def __init__( self ):
#         self.root_path = 'images/';
    
root_path = 'images/'

def openImage( type: str, path: str):
    state( f'Opening image from {path}')
    if( type == 'image' ):
        # image = np.array( cv2.cvtColor( cv2.imread( path ), cv2.COLOR_RGB2GRAY ) )
        # image = np.array( cv2.cvtColor( cv2.imread( path ), cv2.COLOR_RGB2GRAY ) )
        image = Image.open( path ).convert('RGB')
        image = np.array( image )
        # image = image[ :, :, ::-1 ].copy()
        image = cv2.cvtColor( image, cv2.COLOR_RGB2GRAY )

        return TestMessage( True, image )
    else:
        return TestMessage( False, 'The program can not yet process this option.' )
def showImage( image: object ):
    state( 'Showing image' )
    try:
        cv2.imshow( 'Showing image', image )
        cv2.waitKey(0)
        return TestMessage( True, 'Image shown successfully.' )
    except:
        return TestMessage( False, 'Could not show image.' )
    # plt.show()  

