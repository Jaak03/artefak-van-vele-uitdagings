import unittest

from base.message_bucket import TestMessage

class TestMessageBucket( unittest.TestCase ):
    def test_bucket( self ):
        """
            Send a message and check if it returns a success status of True
        """
        self.assertEqual(
            TestMessage( True, 'Testing the message bucket class.' ).success,
            True,
            'Message bucket must return success code that was sent, True in this case.'
        )
    
    def test_bucket_wrong_parameters( self ):
        """
            This is a test to see how the bucket will handle being sent the wrong arguments
        """
        self.assertEqual(
            TestMessage( 9, 'Testing the message bucket class.' ).success,
            False,
            'Message bucket must return a False if the function arguments are incorrect.'
        )