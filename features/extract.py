import os, sys;
import numpy as np;
import cv2;
from matplotlib import pyplot as plt;
import json;

# Feature = imp.import_module( os.path.join() );
sys.path.append( '/run/media/user/c508845f-6045-4466-9585-40b22f040f83/user/git/projek-2018-9/artefak/M-artefak/');
print( sys.path );

from base.c_outputs import comment, state, error, warn;

class ProcessImage:
    def __init__( self, image_path, env ):
        state( 'Opening image...' );
        self.env = env;
        if( self.setImage( image_path ) ):
            comment( '- Image opened successfully.');
        else:
            error( 'Could not set image from path.' );  
    
    def setImage( self, path ):
        try:
            comment( 'Reading image.' );
            self.image = cv2.imread( path );

            comment( '- Flattening image into matrix.' );
            # Flattening and reshaping the array
            self.matrix = np.array( cv2.cvtColor( self.image, cv2.COLOR_RGB2GRAY ));
            x, y = np.shape( self.matrix );
            self.dimensions = [ x, y ];

            comment( '- Matrix shape: {0}'.format( str( self.dimensions )));

            return True;
        except:
            return False;
    def getImage( self ):
        return self.image;
    
    def showImage( self, image ):
        cv2.imshow( 'Image', image );
        cv2.waitKey( 0 );
        cv2.destroyAllWindows();

    # Extract the text lines from the document image.
    def getLines( self ):
        extract_buffer = self.env[ 'settings' ][ 'extract' ][ 'buffer'];
        kernel_size = self.env[ 'settings' ][ 'extract' ][ 'kernel_size'];
        comment( 'Extracting text lines.' );
        threshold = self.env[ 'settings' ][ 'extract' ][ 'threshold'];

        # This is the structuring element that will be used in the dilation of the mask.
        comment( '- Creating structuring element with a kernel size of {0}.'.format( kernel_size ) );
        kernel = cv2.getStructuringElement( cv2.MORPH_DILATE, ( kernel_size, kernel_size ) ); 

        # Eroding image
        self.image = cv2.cvtColor( self.image, cv2.COLOR_BGR2GRAY );
        ret, mask = cv2.threshold( self.image, threshold, 255, cv2.THRESH_BINARY );
        comment( '- Dilating image.' );
        mask = cv2.bitwise_not( mask );
        original_mask = mask;
        mask = cv2.dilate( mask, kernel, iterations= 1 );

        # Setting up run-length array 
        comment( '- Extracting text lines.' );
        self.matrix = np.array( mask );
        regions = [];
        totals = [];
        region_flag = False;
        previous_total = 0;
        for x in range( 0, self.dimensions[ 0 ] ):
            total = 0;
            for y in range( 0, self.dimensions[ 1 ]):
                total += self.matrix[ x ][ y ]/255;
            
            totals.append( total );

            if( total > extract_buffer and region_flag != True):
                begin_region = x;
                region_flag = True;
            elif( total == 0 and region_flag == True ):
                """
                    - If you reach the end of the one region the boundaries and sub-image is stored in the regions array to be returned by the function.
                """
                regions.append({ 'begin': begin_region, 'end': x, 'image': self.image[ begin_region:x, 0:self.dimensions[ 1 ] ], 'mask': original_mask[ begin_region:x, 0:self.dimensions[ 1 ] ] });
                region_flag = False;
        
        plt.plot( totals );
        plt.show();
        return regions;

    def getWords( self, line ):
        rows, cols = np.shape( line[ 'image' ] );

        # Erode the mask again to get more gaps in the text.
        extract_buffer = self.env[ 'settings' ][ 'extract' ][ 'buffer'];

        comment( '- Extracting words from line.' );
        mask = np.array( line[ 'mask' ] );
        words = [];
        word_flag = False;
        for c in range( 0, cols ):
            total = 0;
            for r in range( 0, rows ):
                total += mask[ r ][ c ]/255;


            # Hier moet jy dit net reg maak as jy met regte images begin werk
            if( total > extract_buffer and word_flag == False ):
                word_flag = True;
                begin_word = c;
            elif( total == 0 and word_flag == True ):
                word_flag = False;
                words.append({ 'begin': begin_word, 'end': c, 'image': line[ 'image' ][ 0:rows, begin_word:c ], 'mask': mask[ 0:rows, begin_word:c ] });

        return words;

class Files:
    def __init__( self, path ):
        os.chdir( path );
    
    def writeWords( self, name, words, filename ):
        os.makedirs( name );
        os.chdir( name ); 
        count = 1;
        output_file = { 'word_count':0, 'words': [], 'features': [] };   
        for line in words:
            word_count = 1;
            for words in line:
                cv2.imwrite( '{0}_{1}_{2}.tif'.format( filename, count, word_count ), words[ 'image' ]);
                word_count += 1;
            count += 1;
        output_file[ 'word_count' ] = count-1;
        open( '{0}.json'.format( filename ), 'a' ).write( json.dumps( output_file, indent=4, sort_keys = True ) );
        os.chdir( '..' );  
    
    def writeLines( self, name, lines, filename ):
        os.makedirs( name );
        os.chdir( name );    
        count = 1;
        output_file = { 'word_count':0, 'words': [], 'features': [] };
        for line in lines:
            output_file[ 'words' ].append( '{0}_{1}.tif'.format( filename, count ) );
            cv2.imwrite( '{0}_{1}.tif'.format( filename, count ), line[ 'image' ]);
            count += 1;
        output_file[ 'word_count' ] = count-1;
        open( '{0}.json'.format( filename ), 'a' ).write( json.dumps( output_file, indent=4, sort_keys = True ) );
        # print( json.dumps( output_file, indent=4, sort_keys = True ));
        os.chdir( '..' );  

state( 'Cropping and preparing images:' );

# Open the image: /run/media/user/c508845f-6045-4466-9585-40b22f040f83/user/git/projek-2018-9/toets_materiaal/extract/0041-1.tif
file = '/run/media/user/c508845f-6045-4466-9585-40b22f040f83/user/git/projek-2018-9/toets_materiaal/extract/0041-1.tif';
_p = ProcessImage(  file, {'settings': {'extract': {'buffer': 10, 'kernel_size': 3, 'erode_difference': 2, 'threshold': 240}}});
# _p.showImage();
lines = _p.getLines();
words = [];
filename = os.path.basename( file );
path = os.path.dirname( file );

comment( 'Extracting words from text lines.' );
for line in lines:
    words.append( _p.getWords(( line )) );

try:
    os.makedirs( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) );
    os.chdir( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) );
    files = Files( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) );
    comment( '- Writing content for subdirectories.' );
    files.writeWords( 'words', words );
    files.writeLines( 'lines', lines );
except Exception as e:
    error( 'File already exists.' );
    rm_file = input( 'Do you want to remove the directory [Y/n]?' );
    if( rm_file.upper() == 'Y' or rm_file == '' ):
        os.system( 'rm {0} -r'.format('{0}/{1}'.format( path, filename.split('.')[ 0 ] )));
        os.makedirs( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) );
        os.chdir( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) );
        files = Files( '{0}/{1}'.format( path, filename.split('.')[ 0 ] ) );
        comment( '- Writing content for subdirectories.' );
        files.writeWords( 'words', words, filename.split('.')[ 0 ] );
        files.writeLines( 'lines', lines, filename.split('.')[ 0 ] );
        
