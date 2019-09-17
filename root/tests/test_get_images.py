import unittest

class TestGetImages( unittest.TestCase ):
    def test_imageUtils( self ):
        """
            Test whether the program sees the relevant image and is able to read the image.
        """
        from base.image_utils import openImage

        image = openImage( 'image','images/tests/cvl_test.tif' )
        self.assertEqual( 
            image.success,
            True,
            'Checking whether the test image has been opened successfully.'
        )
