import sys, os
sys.path.append( os.getcwd() )

from base.console_message import comment, state, error, warn, ask
from base.message_bucket import TestMessage

class FeaturePipeline:
    def __init__( self, env, path = None ):
        state( 'Setting up the image pipeline.' )
        self._e = env

        if( path != None ):
            directories = self.getDirectories( path )
            if( directories.success ):
                # Inside each sample folder there are images for lines and words, which are folders.
                subject = ask( 'Would you like to use [words] or [lines]?' )
                while( not(subject.payload == 'words' or subject.payload == 'lines' )):
                    subject = ask( 'Type either [words] or [lines]?' )

                tmp_create_paths = self.setPaths( subject.payload )
                if( tmp_create_paths.success ):
                    comment( tmp_create_paths.payload )
                    getJson();
                else:
                    error( tmp_create_paths.payload )
                    raise IOError( tmp_create_paths.payload )
            else:
                error( directories.payload )

    # def getPaths( ):
    def setPaths( self, subject: str ):
        try:
            comment('Setting paths for image directories.')

            for i in range( len(self._directory_list) ):
                self._directory_list[i] = f'{ self._directory_list[ i ] }/{ subject }'
            
            return TestMessage(True, 'Complete list of paths created for feature extraction.')
        except IOError as ioe:
            return TestMessage(False, ioe)
        except:
            return TestMessage(False, 'Could not add subject type to path variables')

    def getFeatureFiles( self ):
        comment( 'Reading files.' )
        for dir in self._directory_list:
            print( dir )

    def getDirectories( self, path ):
        comment( 'Reading directories in dataset.' )
        try:
            samples = []
            for dir in os.scandir( path ):
                if( os.DirEntry.is_dir( dir ) ):
                    samples.append( dir.path )
            if( samples != [] ):
                self._directory_list = samples
                return TestMessage( True, 'Successfully compiled a list of directories for the sample.', 7 )
            else:
                self._directory_list = samples
                return TestMessage( False, 'There was no relevant sample directories in this path.', 7 )
        except:
            return TestMessage( False, 'Could not compile a list of sample directories for the dataset.', 22 )

        
class Feature:
    def __init__( self, directory ):
        self._imageDir = directory
        print( directory )
       
if __name__ == "__main__":
    # warn( 'You have to inherit feature.' )
    from base import console_message as out
    from base.environment import Environment
    e = Environment( out, os.getcwd() )

    dataset = out.ask( 'What dataset would you like to use?' )
    if( dataset.success ):
    # if( True ):   
        try:
            for key in e.paths.content.keys():
                if( key == dataset.payload ):
                    FeaturePipeline( e, f'{os.getcwd()}/images/{ dataset.payload }' )
        except:
            error( 'Failed to add feature to the dataset.' )
