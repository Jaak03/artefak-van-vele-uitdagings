from base import console_message as out
from base.environment import Environment
from base.extract import ImagePipeline
import os
from base.image_utils import openImage, showImage
import cv2
import numpy as np
from PIL import Image

out.state( 'Running the main application.' )
e = Environment( out, os.getcwd() )

if( out.confirm( 'Extract words from images' ).success ):
    dataset = out.ask( 'What dataset would you like to use?' )
    if( dataset.success ):
        try:
            for key in e.paths.content.keys():
                print( key )
            # ImagePipeline( e, )
            print( e['env_paths'].keys )
        except:
            print( 'werk nie')
