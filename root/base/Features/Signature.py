from PIL import Image
import numpy as np
import cv2

if __name__ == "__main__":
    import sys, os
    sys.path.append( os.getcwd() )

from base.console_message import comment, state, error, warn
from base.feature import Feature
from base import image_utils

class Signature( Feature ):
    def __init__(self, env, image = None):
        super().__init__(env, 'signature')

        if type(image) == str:
            image = image_utils.openImage('image', image).payload

        if( image.all() != None ):
            metric = self.getMetric( image )
            self.setValue(metric)
    
    def getMetric( self, image ):     
        return -1