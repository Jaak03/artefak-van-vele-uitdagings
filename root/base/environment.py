import json

from base.message_bucket import TestMessage

# This is the output class for communication to the user.
out = None

def printTree( JSON ):
    out.comment( '\n'+ json.dumps( JSON, indent=4, sort_keys=True ) )

class Environment:
    def __init__( self, cout, root_directory ):
        try:
            global out
            out = cout
            cout.state( 'Setting up environment.' )
            with open( root_directory + '/base/config.json' ) as file:
                file = json.load( file )
                self.modules = self.installModules( file )
                self.settings = self.Settings( file )
                self.paths = self.Paths( file, root_directory )
                self.datasets = self.Datasets( file )
        except:
            out.error( 'Could not setup environment.' )
    
    # Tries to import the modules in the list. If this fails the modules are not installed so it runs pip install on the module.
    def installModules( self, file ):
        import os

        number_of_modules = 0

        out.state( 'Installing modules.' )
        module_list = file['modules']
        for module in module_list:
            tmp_msg = ""
            try:
                tmp_msg += 'Checking for module: '+ module +' -> '
                exec( 'import '+ module )
                tmp_msg += '[ already installed ]'
                number_of_modules += 1
            except:
                tmp_msg += 'Installing '+ module +' -> '
                os.system( 'pip install '+ module +' --user' )
                tmp_msg += '[ done ]'
                number_of_modules += 1
            finally:
                out.comment( tmp_msg )
        print( number_of_modules )
        return TestMessage( True, f'Successfully installed and imported {number_of_modules} modules.' )

    class Settings:
        def __init__( self, file ):
            try:
                out.state( 'Loading settings.' )
                self.content = file['settings']
                printTree( self.content )
            except:
                # error(   )
                out.error( 'Could not read settings from config file.' )

    class Paths:
        def __init__ (self, file, root_directory ):
            try:
                out.state( 'Reading environment paths.' )
                self.content = file['env_paths']
                self.root_directory = root_directory
                printTree( self.content )
            except:
                out.error( 'Could not read paths from config file.' )
        
        def getLongPath( self, choice ):
            try:
                return self.root_directory + self.content[ choice ]
            except:
                out.error( 'Requested path entry does not exist.' )
                return False
    
    # Reads the characteristics of the datasets from the config file.
    class Datasets:
        def __init__( self, file ):
                out.state( 'Loading dataset characteristics.' )
                self.content = file[ 'datasets' ]
                printTree( self.content )