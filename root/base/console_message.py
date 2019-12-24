from termcolor import colored
import json
import fileinput

# This part is to account for the possible difference in working directory
if __name__ == "__main__":
    from message_bucket import TestMessage
else:
    from .message_bucket import TestMessage

def showPrint( msg: str, msg_type: str ,colour: str ):
    if( isinstance(msg, dict) or isinstance( msg, list ) ):
        new_message = '[ '+ msg_type +' ]\t' + str( json.dumps( msg ) )
        print( colored( new_message, colour, attrs=[ 'bold' ] ))
    else:
        if( msg_type == '[ QUESTION ]' ):
            text = colored( msg_type +'\t'+ msg, colour, attrs=[ 'bold' ] )
            print( f'{text} ', end='' )
        else:
            text = colored( msg_type +'\t'+ msg, colour, attrs=[ 'bold' ] )
            print( text )

def comment( msg: str ):
    try:
        showPrint( msg, '[ COMMENT ]', 'magenta' )
        return TestMessage( True, 'Successfully printed a comment.' )
    except:
        return TestMessage( False, 'Failed to print a comment.' )

def warn( msg: str ):
    try:
        showPrint( msg, '[ WARN ]', 'yellow' )
        return TestMessage( True, 'Successfully printed a warning.' )
    except:
        return TestMessage( False, 'Failed to print a warning.' )
    
def error( msg: str ):
    try:
        showPrint( msg, '[ ERROR ]', 'red' )
        return TestMessage( True, 'Successfully printed an error.' )
    except:
        return TestMessage( False, 'Failed to print an error.' )
    
def state( msg: str ):
    try:
        showPrint( msg, '\n[ STATE ]', 'green' )
        return TestMessage( True, 'Successfully printed a state message.' )
    except:
        return TestMessage( False, 'Failed to print a state message.' )

def confirm( msg:str, res:str ):
    try:
        showPrint( f'{msg} [Y/n]: ', '[ QUESTION ]', 'blue' )
        choice = res.strip()
        if( choice != 'n' ):
            return TestMessage( True, 'The user confirmed the choice.' )
        else:
            return TestMessage( False, 'The user rejected the choice.' )
    except:
        return TestMessage( False, 'Failed to print a question.' )

def ask( msg: str, res:str=None ):
    try:
        showPrint( f'{msg}', '[ QUESTION ]', 'blue' )

        # Check whether the question has an answer already
        choice = ''
        if(res == None):
            choice = input();
        else:
            choice = res.strip()
        print() # add a newline after asking the question.
        if( choice != '' ):
            return TestMessage( True, choice )
        else:
            return TestMessage( False, 'The user failed to enter a choice.' )
    except:
        return TestMessage( False, 'Failed to print a question.' )
# this is run when you execute this particular class.
if __name__ == "__main__":
    comment( 'Message one to test comments.' )
    warn( 'Message two to test warnings.' )
    error( 'Message three to test error messages.' )
    state( 'Message four to test state messages.' )
    ask( 'Message five to test the question.' )