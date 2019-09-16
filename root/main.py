from base import console_message as out
from base.environment import Environment
import os

out.state( 'Running the main application.' )
e = Environment( out, os.getcwd() )