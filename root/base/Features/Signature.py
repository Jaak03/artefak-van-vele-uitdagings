import numpy as np

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
    
    def getMetric(self, image): 
        
        try:
            rows, cols = np.shape(image) 
            open_image = image_utils.Threshold(image, self.env.settings.content['signature']['threshold'])
            
            if open_image.success == False:
                return
            image = open_image.payload

            signature_out = ''

            for cols_counter in range(cols):
            
                signature_total = 0

                for row_counter in range(rows):
                    signature_total += image[row_counter][cols_counter]

                signature_total =  255 - int(round(signature_total / rows))

                signature_out += f'{signature_total}'
                
            return signature_out

        except Exception as e:
            error(e)