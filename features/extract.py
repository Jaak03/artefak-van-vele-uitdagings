import os, sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
import json
from PIL import Image

# Feature = imp.import_module( os.path.join() )
sys.path.append( '/run/media/user/c508845f-6045-4466-9585-40b22f040f83/user/git/M-artefak/')
sys.path.append( '/home/mother/git/artefak-van-vele-uitdagings/')
print( sys.path )

from base.c_outputs import comment, state, error, warn

class ProcessImage:
    def __init__( self, image_path, env ):
        state( 'Opening image...' )
        self.env = env
        if( self.setImage( image_path ) ):
            comment( '- Image opened successfully.')
        else:
            error( 'Could not set image from path.' )  
    
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
        extract_buffer = self.env[ 'settings' ][ 'extract' ][ 'buffer']
        kernel_size = self.env[ 'settings' ][ 'extract' ][ 'kernel_size']
        comment( 'Extracting text lines.' )
        threshold = self.env[ 'settings' ][ 'extract' ][ 'threshold']

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
            elif( total <= self.env[ 'settings' ][ 'extract' ][ 'buffer' ] and region_flag == True ):
                """
                    - If you reach the end of the one region the boundaries and sub-image is stored in the regions array to be returned by the function.
                    - The extra if-statement is to ensure that only relevant segments are stored.
                """
                [ seg_height, seg_width ] = np.shape( self.image[ begin_region:x, 0:self.dimensions[ 1 ] ] ) 

                if( seg_height > self.env[ 'settings' ][ 'extract' ][ 'tolerance' ] ):

                    # resizing the image height to be consistent for the neural network
                    dim = ( seg_width, self.env[ 'settings' ][ 'extract' ][ 'width' ] )
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
                    Image.fromarray( resized_mask ).show()

                    regions.append({ 
                        'begin': begin_region, 
                        'end': x, 
                        'image': resized_image, 
                        'mask': resized_mask
                    })

                region_flag = False

        return regions
    def getWords( self, line ):
        rows, cols = np.shape( line[ 'image' ] )

        # Erode the mask again to get more gaps in the text.
        extract_buffer = self.env[ 'settings' ][ 'extract' ][ 'buffer']

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
                words.append({ 
                    'begin': begin_word, 
                    'end': c, 
                    'image': line[ 'image' ][ 0:rows, begin_word:c ], 
                    'mask': mask[ 0:rows, begin_word:c ] 
                })

        return words

    # def pasteIn( small_image ):
    #     big_image = Image.fromarray( np.uint8( np.full([BIG,BIG], 255) ))

    #     small_dim = np.shape( np.array( small_image ) )
    #     big_dim = np.shape( np.array( big_image ) )

    #     # coordinates = []

    #     # print( small_dim )
    #     # print( big_dim )

    #     # # werk eers op die eerste as.
    #     # s_ax = small_dim[ 0 ]
    #     # b_ax = big_dim[ 0 ]

    #     # if( s_ax == b_ax ):
    #     #     print( 'Dimension stays the same.' )
    #     #     coordinates.append( 0 )
    #     #     pass
    #     # elif( s_ax > b_ax):
    #     #     coordinates.append( 0 )
    #     #     print( 'Resize the image.' )
    #     # else:
    #     #     coordinates.append( int( ( b_ax/2 ) - ( s_ax/2 ) ) )
        
    #     # # werk dan op die tweede as
    #     # s_ax = small_dim[ 1 ]
    #     # b_ax = big_dim[ 1 ]

    #     # if( s_ax == b_ax ):
    #     #     print( 'Dimension stays the same.' )
    #     #     coordinates.append( 0 )
    #     #     pass
    #     # elif( s_ax > b_ax):
    #     #     print( 'Resize the image.' )
    #     #     coordinates.append( 0 )
    #     # else:
    #     #     coordinates.append( int( ( b_ax/2 ) - ( s_ax/2 ) ) )
        
    #     # print( f"Paste image here { coordinates }" )

    #     # big_image.paste( small_image, ( coordinates[ 1 ], coordinates[ 0 ]) )

    #     return big_image;

class Files:
    def __init__( self, path ):
        os.chdir( path )
    
    def writeWords( self, name, words, filename ):
        os.makedirs( name )
        os.chdir( name ) 
        count = 1
        output_file = { 'word_count':0, 'words': [], 'features': [] }   

        word_count = 0
        for line in words:
            for words in line:
                cv2.imwrite( '{0}_{1}-{2}.tif'.format( filename, count, word_count ), words[ 'image' ])
                output_file[ 'words' ].append( '{0}_{1}-{2}.tif'.format( filename, count, word_count ) )
                word_count += 1
        # comment( f"- Wrote {str( word_count )} words for {filename}." )
        output_file[ 'word_count' ] = word_count
        open( '{0}.json'.format( filename ), 'a' ).write( json.dumps( output_file, indent=4, sort_keys = True ) )
        os.chdir( '..' )  
    
    def writeLines( self, name, lines, filename ):
        os.makedirs( name )
        os.chdir( name )    
        count = 1

        output_file = { 'line_count':0, 'lines': [], 'features': [] }
        for line in lines:
            output_file[ 'lines' ].append( '{0}_{1}.tif'.format( filename, count ) )
            cv2.imwrite( '{0}_{1}.tif'.format( filename, count ), line[ 'image' ])
            count += 1
        # comment( f"- Wrote {str( count - 1 )} lines for {filename}." )
        output_file[ 'line_count' ] = count-1
        open( '{0}.json'.format( filename ), 'a' ).write( json.dumps( output_file, indent = 4, sort_keys = True ) )
        os.chdir( '..' )  

state( 'Cropping and preparing images:' )

# Open the image: /run/media/user/c508845f-6045-4466-9585-40b22f040f83/user/git/projek-2018-9/toets_materiaal/extract/0041-1.tif
# file = '/run/media/user/c508845f-6045-4466-9585-40b22f040f83/user/git/M-artefak/toets_materiaal/extract/toets_demo.tif'

file = '/home/mother/git/artefak-van-vele-uitdagings/toets_materiaal/extract/toets_demo.tif'
_p = ProcessImage(  file, {
        'settings': {
            'extract': {
                'buffer': 10, 
                'kernel_size': 3, 
                'erode_difference': 2, 
                'threshold': 240, 
                'tolerance': 3, 
                'height': 50, 
                'width': 50 
            }
        }
    })
# _p.showImage()
lines = _p.getLines()
words = []
filename = os.path.basename( file )
path = os.path.dirname( file )

comment( 'Extracting words from text lines.' )
for line in lines:
    words.append( _p.getWords(( line )) )

try:
    os.makedirs( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) )
    os.chdir( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) )
    files = Files( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) )
    comment( '- Writing content for subdirectories.' )
    files.writeWords( 'words', words, filename.split('.')[ 0 ] )
    files.writeLines( 'lines', lines, filename.split('.')[ 0 ] )
except Exception as e:
    print( e )
    error( 'File already exists.' )
    rm_file = input( 'Do you want to remove the directory [Y/n]?' )
    if( rm_file.upper() == 'Y' or rm_file == '' ):
        os.system( 'rm {0} -r'.format('{0}/{1}'.format( path, filename.split('.')[ 0 ] )))
        os.makedirs( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) )
        os.chdir( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) )
        files = Files( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) )
        comment( '- Writing content for subdirectories.' )
        files.writeWords( 'words', words, filename.split('.')[ 0 ] )
        files.writeLines( 'lines', lines, filename.split('.')[ 0 ] )
        
