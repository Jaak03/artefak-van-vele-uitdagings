from base import console_message as out
from base.environment import Environment
from base.extract import ImagePipeline
from base.feature import FeaturePipeline
from base.image_utils import openImage, showImage

import os
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
                if( key == dataset.payload ):
                    ImagePipeline( e, f'{os.getcwd()}/images/', dataset.payload )
        except:
            out.error( 'Extracting failed' )

if( out.confirm( 'Would you like to add a feature?' ).success ):
    dataset = out.ask( 'What dataset would you like to use?' )
    if( dataset.success ):
        try:
            for key in e.paths.content.keys():
                if( key == dataset.payload ):
                    features_pipe = FeaturePipeline( e, f'{os.getcwd()}/images/{ dataset.payload }' )
                    feature_files = features_pipe.getFeatureFiles()
        except:
            out.error( 'Failed to add feature to the dataset.' )
