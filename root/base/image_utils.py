import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

from base.console_message import comment, warn, error, state
from base.message_bucket import TestMessage

# class ImageUtils:
#     def __init__( self ):
#         self.root_path = 'images/';
    
root_path = 'images/'

def openImage(type: str, path: str):
    if( type == 'image' ):
        image = Image.open( path ).convert('RGB')
        image = np.array( image )

        image = cv2.cvtColor( image, cv2.COLOR_RGB2GRAY )

        return TestMessage( True, image )
    else:
        return TestMessage( False, 'The program can not yet process this option.' )
        
def showImage(image: object ):
    try:
        cv2.imshow( 'Showing image', image)
        cv2.waitKey(0)
        return TestMessage( True, 'Image shown successfully.' )
    except Exception as e:
        error(e)
        return TestMessage( False, e )

def Threshold(image: object, threshold: int):
    try:
        return TestMessage(True,cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1])
    except Exception as e:
        return TestMessage(False, e)