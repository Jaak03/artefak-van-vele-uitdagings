import sys, os
sys.path.append( os.getcwd() )

from base.console_message import comment, state, error, warn

class Feature:
    def __init__( self, directory ):
        self._imageDir = directory
        print( directory )
        
if __name__ == "__main__":
    warn( 'You have to inherit feature.' )