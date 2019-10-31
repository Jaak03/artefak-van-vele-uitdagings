import os, sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
import json
from PIL import Image
from math import ceil

sys.path.append( os.getcwd() )
print( sys.path )

from base.console_message import comment, state, error, warn, ask, confirm

#Skryf dalk 'n ekstra klas wat na 'n dir kan kyk en al die beelde in die folder na die klas toe kan stuur om verwerk te word.
'''
    - This class processes the image initially. The pre-processing includes:
        1) opening the image
        2) showing the image
        3) getting the opened image
        4) extracting the textlines from the image
        5) extracting the words from the text lines.
    
    - The __init__ for this class opens a single image that is then sent through all of the extraction steps.

    -ARGUMENTS: 
        > self: is used to setup the environment for the precess.
'''
class ProcessImage:
    def __init__( self, image_path, env ):
        state( 'Opening image...' )
        self.env = env
        if( self.setImage( image_path ) ):
            comment( '- Image opened successfully.')
        else:
            error( 'Could not set image from path in ProcessImage.' )  
    def setImage( self, path ):
        try:
            comment( 'Reading image.' )
            comment( '- Loading from path: {0}'.format( path ) )
            self.image = cv2.imread( path )

            comment( '- Flattening image into matrix.' )
            # Flattening and reshaping the array
            self.matrix = np.array( cv2.cvtColor( self.image, cv2.COLOR_RGB2GRAY ))
            x, y = np.shape( self.matrix )
            self.dimensions = [ x, y ]

            comment( '- Matrix shape: {0}'.format( str( self.dimensions )))

            return True
        except:
            return False
    def getImage( self ):
        return self.image
    def showImage( self, image ):
        cv2.imshow( 'Image', image )
        cv2.waitKey( 0 )
        cv2.destroyAllWindows()

    # Extract the text lines from the document image.
    def getLines( self ):
        print(  )
        extract_buffer = self.env.settings.content[ 'extract' ][ 'buffer']
        kernel_size = self.env.settings.content[ 'extract' ][ 'kernel_size']
        comment( 'Extracting text lines.' )
        threshold = self.env.settings.content[ 'extract' ][ 'threshold']

        # This is the structuring element that will be used in the dilation of the mask.
        comment( '- Creating structuring element with a kernel size of {0}.'.format( kernel_size ) )
        kernel = cv2.getStructuringElement( cv2.MORPH_DILATE, ( kernel_size, kernel_size ) ) 

        # Eroding image
        self.image = cv2.cvtColor( self.image, cv2.COLOR_BGR2GRAY )
        ret, mask = cv2.threshold( self.image, threshold, 255, cv2.THRESH_BINARY )
        comment( '- Dilating image.' )
        mask = cv2.bitwise_not( mask )
        original_mask = mask
        mask = cv2.dilate( mask, kernel, iterations= 1 )

        # Setting up run-length array 
        comment( '- Extracting text lines.' )
        self.matrix = np.array( mask )
        regions = []
        totals = []
        region_flag = False

        # Extracting line regions by using horizontal projections
        for x in range( 0, self.dimensions[ 0 ] ):
            total = 0
            for y in range( 0, self.dimensions[ 1 ]):
                total += self.matrix[ x ][ y ]/255
            
            totals.append( total )

            if( total > extract_buffer and region_flag != True):
                begin_region = x
                region_flag = True
            elif( total <= self.env.settings.content[ 'extract' ][ 'buffer'] and region_flag == True ):
                """
                    - If you reach the end of the one region the boundaries and sub-image is stored in the regions array to be returned by the function.
                    - The extra if-statement is to ensure that only relevant segments are stored.
                """
                [ seg_width, seg_height ] = np.shape( self.image[ begin_region:x, 0:self.dimensions[ 1 ] ] ) 

                if( seg_width > self.env.settings.content[ 'extract' ][ 'tolerance' ] ):

                    # resizing the image height to be consistent for the neural network
                    dim = ( seg_height, self.env.settings.content[ 'extract' ][ 'height' ] )
                    resized_image = cv2.resize( 
                        self.image[ begin_region:x, 0:self.dimensions[ 1 ] ] , 
                        dim, 
                        interpolation = cv2.INTER_AREA 
                    )
                    resized_mask = cv2.resize( 
                        original_mask[ begin_region:x, 0:self.dimensions[ 1 ] ] , 
                        dim, 
                        interpolation = cv2.INTER_AREA 
                    )

                    regions.append({ 
                        'begin': begin_region, 
                        'end': x, 
                        'image': resized_image, 
                        'mask': resized_mask
                    })

                region_flag = False

        return regions
    def getWords( self, line ):
        ( rows, cols ) = np.shape( line[ 'image' ] )

        # Erode the mask again to get more gaps in the text.
        extract_buffer = self.env.settings.content[ 'extract' ][ 'buffer']

        comment( '- Extracting words from line.' )
        mask = np.array( line[ 'mask' ] )
        words = []
        word_flag = False
        for c in range( 0, cols ):
            total = 0
            for r in range( 0, rows ):
                total += mask[ r ][ c ]/255

            if( total > extract_buffer and word_flag == False ):
                word_flag = True
                begin_word = c
            elif( total == 0 and word_flag == True ):
                word_flag = False

                # Divide the word image into smaller segments if possible
                word = line[ 'image' ][ 0:rows, begin_word:c ]
                word_mask = mask[ 0:rows, begin_word:c ] 

                ( height, width ) = np.shape( word )
                word_length = c - begin_word
                if( word_length + ( self.env.settings.content[ 'extract' ][ 'buffer'] ) <= self.env.settings.content[ 'extract' ][ 'width'] ):
                    resized_word_image = cv2.resize( 
                        word, 
                        ( height, self.env.settings.content[ 'extract' ][ 'width'] ), 
                        interpolation = cv2.INTER_AREA 
                    )
                    resized_word_mask = cv2.resize( 
                        word_mask, 
                        ( height, self.env.settings.content[ 'extract' ][ 'width'] ), 
                        interpolation = cv2.INTER_AREA 
                    )
                    words.append({ 
                        'begin': begin_word, 
                        'end': c, 
                        'image': resized_word_image, 
                        'mask': resized_word_mask
                    })
                else:
                    div = ceil( width / self.env.settings.content[ 'extract' ][ 'width'] )
                    count = 0
                    while( count < width - ( width / div ) ):
                        seg = word[ 0:rows, count: count + int( width / div ) ]
                        seg_mask = mask[ 0:rows, count: count + int( width / div ) ]
                        if( np.shape( seg )[1] == 0): print( count, width )
                        words.append({ 
                            'begin': count, 
                            'end': count + int( width / div ), 
                            'image': seg, 
                            'mask': seg_mask
                        })
                        count += int( width / div )

                    # If there are still some pixels left for the whole word to be extracted.
                    seg = word[ 0:rows, count: width ]
                    seg_mask = mask[ 0:rows, count: width ]
                    if( np.shape( seg )[1] > 0 ):
                        words.append({ 
                            'begin': count, 
                            'end': width, 
                            'image': seg, 
                            'mask': seg_mask
                        })                

        return words

"""
    Write the files to a directory with the same name. After the preprocessing phase there should be a list of directories, each having their own extracted word data and the features captured in a json file with the same name that is also present in the directory.
"""
class Files:
    def __init__( self, path, env ):
        os.chdir( path )
        self.env = env
    
    '''
        - After dividing the sentence into the words, each word image is further divided into fixed dimensions. This is needed for the neural network.
        - Afte dividing the word image into further segments the buff() function just takes the segment and places it in the middel of an empty image of the appropriate size, rather the stretching the smaller image.

        - ARGUMENTS:
            > Self: is used to get the dimensions from the constructor environmental variable.
            > small_image: the smaller image is copied into a larger image of the correct dimensions.

        - RETURNS:
            > big_image: a 2D array with the pixel grey levels. The result is a numpy array.
        
        - ERROR HANDLING:
            --NONE--
    '''
    def buff( self, small_image ):
        comment( '- Buffing image.' )
        big_image = Image.fromarray( 
            np.uint8( 
                np.full([
                    self.env.settings.content[ 'extract' ][ 'height'],
                    self.env.settings.content[ 'extract' ][ 'width']
                ], 
                255) 
            )
        )

        small_dim = np.shape( np.array( small_image ) )
        big_dim = np.shape( np.array( big_image ) )

        coordinates = []

        # werk eers op die eerste as.
        s_ax = small_dim[ 0 ]
        b_ax = big_dim[ 0 ]

        if( s_ax == b_ax ):
            coordinates.append( 0 )
            pass
        elif( s_ax > b_ax):
            coordinates.append( 0 )
        else:
            coordinates.append( int( ( b_ax/2 ) - ( s_ax/2 ) ) )
        
        # werk dan op die tweede as
        s_ax = small_dim[ 1 ]
        b_ax = big_dim[ 1 ]

        if( s_ax == b_ax ):
            coordinates.append( 0 )
            pass
        elif( s_ax > b_ax):
            coordinates.append( 0 )
        else:
            coordinates.append( int( ( b_ax/2 ) - ( s_ax/2 ) ) )
       
        big_image.paste( Image.fromarray( small_image ), ( coordinates[ 1 ], coordinates[ 0 ]) )
        big_image = np.asarray( big_image ) 
        return big_image
    
    '''
        - Each extracted word is written to a .tiff file.
        - The feature .json file, that holds a record for all of the images and their features is also written in this function.

        - ARGUMENTS:
            > Self: is used to get the dimensions from the constructor environmental variable.
            > name: is the name of the file. This name is used to create a directory with the same name for each image.
            > words: this is a list of the words that were extracted from the sentence image.
            > filename: this is the file that the word image is to be saved to, this is almost the same as the name.

        - RETURNS:
            > TestMessage: with true and message if successful.

        - ERROR HANDLING:
            > Tries to write the image and displays a message in the console if this is not successful.
    '''
    def writeWords( self, name, words, filename ):
        os.makedirs( name )
        os.chdir( name ) 
        output_file = { 'author': filename.split('-')[0], 'word_count':0, 'words': [], 'features': [] }   

        word_count = 0
        for line in words:
            for word in line:
                image = word[ 'image' ]
                if( np.shape( image )[1] > 0 and np.shape( image )[0] > 0 ):
                    if( np.shape( word[ 'image' ] )[ 1 ] < self.env.settings.content[ 'extract' ][ 'width'] ):
                        image = self.buff( image )                      

                    output_filename = '{0}_{1}.tif'.format( filename, word_count )

                    try:
                        cv2.imwrite( output_filename, image )
                    except:
                        error( f'Could not write {output_filename} to a file.' )

                    output_file[ 'words' ].append( '{0}_{1}.tif'.format( filename, word_count ) )
                    word_count += 1

        output_file[ 'word_count' ] = word_count
        open( '{0}.json'.format( filename ), 'a' ).write( json.dumps( output_file, indent=4, sort_keys = True ) )
        os.chdir( '..' )  

        return    
    
    '''
        - Each extracted line is written to a .tiff file.
        - The feature .json file, that holds a record for all of the sentence images.

        - ARGUMENTS:
            > Self: -- not used --
            > name: is the name of the file. This name is used to create a directory with the same name for each image.
            > lines: this is a list of the sentences that were extracted from the sentence image.
            > filename: this is the file that the line image is to be saved to, this is almost the same as the name.

        - RETURNS:
            > TestMessage: with true and message if successful.

        - ERROR HANDLING:
            > Tries to write the image and displays a message in the console if this is not successful.
    '''
    def writeLines( self, name, lines, filename ):
        os.makedirs( name )
        os.chdir( name )    
        count = 1

        output_file = { 'author': filename.split('-')[0], 'line_count':0, 'lines': [], 'features': [] }
        for line in lines:
            output_file[ 'lines' ].append( '{0}_{1}.tif'.format( filename, count ) )
            try:
                cv2.imwrite( '{0}_{1}.tif'.format( filename, count ), line[ 'image' ])
                count += 1
            except:
                error( f'Could not write line to {filename}_{count}.tif')
        output_file[ 'line_count' ] = count-1
        open( '{0}.json'.format( filename ), 'a' ).write( json.dumps( output_file, indent = 4, sort_keys = True ) )
        os.chdir( '..' )  

state( 'Cropping and preparing images:' )

class ImagePipeline:
    def __init__( self, env, directory, dataset ):
        self.env = env
        try:
            self.processImages( f'{directory}{dataset}/', 'tif' )
        except:
            error( 'Could not process selected dataset.' )       

    '''
        This function adds the '.' before the given extension if one is needed. After this step the getFiles() function is called and the list of files is then passed on the the extraction class. Finally the results from the extraction class is written to actual directories and files on the system.

        - ARGUMENTS
            > self: is used to read the env variable from the class.
            > dir: the directory that is searched for the relevant files.
            > extension: of the files that you are looking for. If the extension does not include a ., one will be added inside this function.
        
        - RETURNS
            A TestMessage should be sent back if this function is successful.
    '''
    def processImages( self, dir, extension ):
        if( '.' in extension ):
            files_list = self.getFiles( dir, extension )
        else:
            files_list = self.getFiles( dir, f'.{extension}' )

        for path in files_list:
            _p = ProcessImage( path, self.env )

            lines = self.extractLines( _p )
            words = self.extractWords( _p, lines )

            # Creating bundle to write
            class Bundle:
                def __init__( self ):
                    self.p = _p
                    self.lines = lines
                    self.words = words
                    self.folder_name = os.path.basename( path ).split( '.' )[0]
                    self.working_dir = dir
                
                def getPath( self ):
                    return f'{self.working_dir}{self.folder_name}'

            self.writeFiles( Bundle() )
            
    '''
        Read all of the files in the given directory that en with the given extension. The extension that is given at this stage should include the '.???'.

        - ARGUMENTS
            > self: -- not used --
            > dir: the directory that is searched for the relevant files.
            > extension: the function will send back the files in the directory that end with this extension. It should include the . at this stage.

        - RETURNS
            Returns a list of the absolute paths to each of the files inside the directory ending with the appropriate extensions.

        - ERROR HANDLING
            > It does not handel any errors at this stage. Adjust this function to return a TestMessage as soon as it is added to the main project.
            > An error that you can look out for is if the function returns noting or an empty list.
    '''
    def getFiles( self, dir, extension ):
        tmp_files_list = []
        for file in os.listdir( dir ):
            if( file.endswith( extension )):
                path_to_file = f'{dir}{file}';
                tmp_files_list.append( path_to_file )

        return tmp_files_list;            

    def extractLines( self, _p ):
        return _p.getLines()
    
    def extractWords( self, _p, lines ):
        tmp_words = []
        for line in lines:
            tmp_words.append( _p.getWords( line ) )

        return tmp_words 

    def writeFiles( self, bundle ):
        try:
            os.makedirs( bundle.getPath() )
            os.chdir( bundle.getPath() )
            files = Files( bundle.getPath() , self.env )
            comment( '- Writing content for subdirectories.' )
            files.writeWords( 'words', bundle.words, bundle.folder_name )
            files.writeLines( 'lines', bundle.lines, bundle.folder_name )
        except:
            error( 'Directory already exists.' )
            rm_file = input( 'Do you want to remove the directory [Y/n]?' )
            if( rm_file.upper() == 'Y' or rm_file == '' ):
                os.system( f'rm { bundle.getPath() } -r')
                os.makedirs( bundle.getPath() )
                os.chdir( bundle.getPath() )
                files = Files( bundle.getPath(), self.env )
                comment( '- Writing content for subdirectories.' )
                files.writeWords( 'words', bundle.words, bundle.folder_name )
                files.writeLines( 'lines', bundle.lines, bundle.folder_name )

if __name__ == "__main__":
    from base import console_message as out
    from base.environment import Environment

    e = Environment( out, os.getcwd() )

    choice = ask( 'What dataset would you like to use?' )
    ImagePipeline( e, f'{os.getcwd()}/images/', choice.payload )
