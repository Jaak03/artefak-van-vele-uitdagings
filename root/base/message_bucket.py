class TestMessage:
    """
        This is a bucket class for sending around status messages of the functions for the tests to pick up on.

        instance variables:
            - success: boolean value for the execution success of the function.
            - payload: string message that is sent back to be displayed to the user.
    """
    def __init__( self, success: bool, payload, line: int = None ):
        if( isinstance( success,bool ) ):
            self.success = bool( success )
            self.payload = payload
        else:
            self.success = False
            self.payload = 'Received the wrong arguments.'

        if( line != None ):
            self.line = line
        else:
            self.line = -1
    
    def __str__( self ):
        return f'Returned {self.success} with message : [{self.line}] : {self.payload}'