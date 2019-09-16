import unittest

class TestGetImages( unittest.TestCase ):
    def test_openImage( self ):
        """
            Test whether the program sees the relevant image and is able to read the image.
        """
        from base.image_utils import openImage
        import cv2, numpy as np

        image = openImage( 'image','tests/cvl_test.tif' )
        x, y = np.shape( image )
        self.assertTrue( 
            x > 0 and y > 0,
            'Checking whether the test image has been opened successfully.'
        )