class TestMessage:
    """
        This is a bucket class for sending around status messages of the functions for the tests to pick up on.

        instance variables:
            - success: boolean value for the execution success of the function.
            - msg: string message that is sent back to be displayed to the user.
    """
    def __init__( self, success: bool, msg: str ):
        if( isinstance( success,bool ) and isinstance( msg,str )):
            self.success = bool( success )
            self.msg = str( msg )
        else:
            self.success = False
            self.msg = 'Received the wrong arguments.'
    
    def __get__( self, instance, owner ):
        return { self.success, self.msg }
    
    def __str__( self ):
        return f'Returned {self.success} with message: {self.msg}'