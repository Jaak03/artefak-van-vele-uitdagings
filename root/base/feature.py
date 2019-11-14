import sys
import os
import json
import fileinput
import re # regular expression om die magice functions uit te haal.


sys.path.append( os.getcwd() )

from base.console_message import comment, state, error, warn, ask
from base.message_bucket import TestMessage

from base import Features

readInput = fileinput.input()

class FeaturePipeline:
    def __init__( self, env, feature:str, path = None):
        state( 'Setting up the image pipeline.' )
        self._e = env

        if( path != None ):
            directories = self.getDirectories( path )
            if( directories.success ):
                # Inside each sample folder there are images for lines and words, which are folders.
                self.subject = ask('Would you like to use [words] or [lines]?', readInput.readline())
                while( not(self.subject.payload == 'words' or self.subject.payload == 'lines' )):
                    self.subject = ask('Type either [words] or [lines]?', readInput.readline())

                tmp_create_paths = self.setPaths( self.subject.payload )
                if( tmp_create_paths.success ):
                    comment( tmp_create_paths.payload )
                    feature_files = self.getFeatureFiles()        
                    
                    available_features = self.getListOfAvailableFeatures()
                    for feature_class in available_features:
                        self.save(self.generateFeatures(feature_files, feature_class))
                else:
                    error( tmp_create_paths.payload )
                    raise IOError( tmp_create_paths.payload )
            else:
                error( directories.payload )

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
        tmp_list = []
        for dir in self._directory_list:
            tmp_json = HandleJSON(dir)
            tmp_list.append({
                "feature_json": tmp_json.file,
                "directory": dir,
                "filepath": tmp_json.filepath
            })

        return tmp_list

    def save(self, file):
        outfile = open(file['filepath'], 'w')
        outfile.write(json.dumps(file['feature_json'], indent=4))
        outfile.close() 
        comment(f'Successfully added feature.')   

    def getDirectories(self, path):
        comment('Reading directories in dataset.')
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
        except Exception as e:
            return TestMessage( False, f'{e}', 22 )

    def getListOfAvailableFeatures(self):
        # Regex vir al die woorde wat nie __*__ in het nie
        ex = re.compile("^((?!__).(?!__))*$")
        return list(filter(ex.match, dir(Features)));

    def generateFeatures(self, feature_files: any, feature_class:str):
        for file in feature_files:
            tmp_feature = []
            for image_file in file['feature_json'][self.subject.payload]:
                feature = getattr(Features, feature_class)
                # print(dir(feature))

                # Gaan kyk hier
                # https://stackoverflow.com/questions/40588239/may-init-be-used-as-normal-method-for-initialization-not-as-constructor

                # metric = feature(self._e, file['directory']+f'/{image_file}')
                # moment = Features.Moment(self._e, file['directory']+f'/{image_file}')
                tmp_feature.append({image_file: metric.getValue()})
            file['feature_json']['features'].append({f'{feature.getName()}': tmp_feature})
        return file

class Feature:
    def __init__(self, env, name):
        self.env = env
        self._feature_name = name

    def setValue(self, value):
        self._value = value
    
    def getValue(self):
        return self._value

    def getName(self):
        return self._feature_name
class FeatureJSON:
    def __init__(self):
        self.author = ""
        self.features = []
        self.word_count = 0
        self.words = []
    
    def __str__(self):
        tmp2write = {}
        tmp2write["author"] = self.author
        tmp2write["features"] = self.features
        tmp2write["word_count"] = self.word_count
        tmp2write["words"] = self.words

        return str(json.dumps(tmp2write))

class HandleJSON:
    def __init__(self, path: str):
        self.filepath = self.getJson(path)
        self.file = self.parseJson()

    def getJson(self, path: str):
        try:
            for file in os.listdir(path):
                if file.endswith('.json'):
                    path_to_file = f'{path}/{file}'
                    return path_to_file
        except:
            error(f"Could not find a .json file in {path}")

    def parseJson(self):      
        with open(self.filepath) as json_file:
            file = dict(json.load(json_file))
            return file

if __name__ == "__main__":
    # warn( 'You have to inherit feature.' )
    from base import console_message as out
    from base.environment import Environment
    e = Environment( out, os.getcwd() )

    dataset = out.ask('What dataset would you like to use?', readInput.readline())
    if( dataset.success ):
    # if( True ):   
        # try:
            for key in e.paths.content.keys():
                if( key == dataset.payload ):
                    FeaturePipeline( e, 'moment', f'{os.getcwd()}/images/{ dataset.payload }')
        # except:
        #     error( 'Failed to add feature to the dataset.' )
