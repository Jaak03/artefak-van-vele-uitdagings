from base.message_bucket import TestMessage

# class ImageUtils:
#     def __init__( self ):
#         self.root_path = 'images/';
    
root_path = 'images/'

def openImage( type: str, path: str):
    """
        type:   -image
                -dataset
    """
    import cv2, numpy as np

    if( type == 'image' ):
        image = np.array( cv2.cvtColor( cv2.imread( path ), cv2.COLOR_RGB2GRAY ) )
        # image = cv2.imread( path )
        return TestMessage( True, image )
    else:
        return TestMessage( False, 'The program can not yet process this option.' )

def imShow( image ):
    import matplotlib.pyplot as plt

    plt.imshow( image ) 
    plt.show()  