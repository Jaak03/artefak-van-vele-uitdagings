from base import console_message as out
from base.environment import Environment
import os
from base.image_utils import openImage, imShow
import cv2
import numpy as np

out.state( 'Running the main application.' )
e = Environment( out, os.getcwd() )

image = openImage( 'image','images/tests/cvl_test.tif' ).payload
imShow( image )