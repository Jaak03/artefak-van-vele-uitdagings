import unittest

from base.console_message import state, comment, warn, error

class TestConsoleMessage( unittest.TestCase ):
    def test_comment( self ):
        """
            Test whether a successfull comment can be made to the console.
        """
        self.assertEqual( 
            comment( 'Testing a comment message' ).success,
            True,
            'A successful comment message should return a success status of True.'
        )

    def test_state( self ):
        """
            Test whether a successfull state message can be made to the console.
        """
        self.assertEqual( 
            state( 'Testing a state message' ).success,
            True,
            'A successful state message should return a success status of True.'
        )
    
    def test_warn( self ):
        """
            Test whether a successfull warning can be made to the console.
        """
        self.assertEqual( 
            warn( 'Testing a warning message' ).success,
            True,
            'A successful warning message should return a success status of True.'
        )

    def test_error( self ):
        """
            Test whether a successfull error message can be made to the console.
        """
        self.assertEqual( 
            error( 'Testing a error message' ).success,
            True,
            'A successful error message should return a success status of True.'
        )
    