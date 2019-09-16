import unittest
import os
import base.console_message as out

from base.environment import Environment

e = Environment( out, os.getcwd() )

class TestEnvironment( unittest.TestCase ):
    def test_settings( self ):
        """
            Check whether the settings was read from the config file.
        """
        self.assertIsNotNone( 
            e.settings,
            'Testing whether the environment has a settings characteristic.'
        )
    
    def test_paths( self ):
        """
            Check whether the parameters was read from the config file.
        """
        self.assertIsNotNone( 
            e.paths,
            'Testing whether the environment has a paths characteristic.'
        )
    
    def test_datasets( self ):
        """
            Check whether the datasets was read from the config file.
        """
        self.assertIsNotNone( 
            e.datasets,
            'Testing whether the environment has a datasets characteristic.'
        )
    
    def test_modules( self ):
        """
            Check whether the datasets was read from the config file.
        """
        self.assertEqual( 
            e.modules.success,
            True,
            'Testing whether the environment has a modules characteristic.'
        )