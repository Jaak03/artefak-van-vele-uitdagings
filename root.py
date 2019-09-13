import os
os.chdir( os.path.dirname( __file__ ) )
cout = __import__( './base/c_outputs.py' )
# from base import c_outputs as cout

# from features.feature import LoadFeatures;
from base.load import LoadFeatures;

cout.state( 'Running root script for the artefact.' );

"""
    -  Loading environmental variables from ./base/config.json file.
"""
from base.environment import Environment as env;
_e = env( cout, os.path.dirname( __file__ ) );


"""
    - Calculate the custom features for a class of images.
    - image_class stores the keys for the settings that have been saved in the config file.
"""
image_class = [ 'test', 
                'cvl'];
LoadFeatures( cout, _e, image_class[ 0 ] );
