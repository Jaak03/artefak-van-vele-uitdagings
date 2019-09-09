from termcolor import colored;
import json;

def showPrint( msg, msg_type ,colour ):
    if( isinstance(msg, dict) or isinstance( msg, list ) ):
        new_message = '[ '+ msg_type +' ]\t' + str( json.dumps( msg ) );
        print( colored( new_message, colour, attrs=[ 'bold' ] ));
    else:
        text = colored( msg_type +'\t'+ msg, colour, attrs=[ 'bold' ] );
        print( text );

def comment( msg ):
    showPrint( msg, '[ COMMENT ]', 'magenta' );

def warn( msg ):
    showPrint( msg, '[ WARN ]', 'yellow' );
    
def error( msg ):
    showPrint( msg, '[ ERROR ]', 'red' );

def state( msg ):
    showPrint( msg, '\n[ STATE ]', 'green' );