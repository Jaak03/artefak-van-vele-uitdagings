# Hier is die finale jupyter notebook wat kan resultate gee op die digits.

# https://www.youtube.com/watch?v=lbFEZAXzk0g
# > Die is om net 'n idee te kry van hoe die ding werk en om net 'n klein model
#    aan die gang te kry sodat mens van daar af kan gaan.
# > Ek gaan ook nie die comments insit nie, maar jy kan gaan kyk as jy bietjie
#    onseker is.

# STAP 1: Laai die beelde.

# tutorial goed
import gzip;
import numpy as np;
import os;

# sien wat gelaai en gebruik word.
import matplotlib;
# matplotlib.use('TkAgg');
import matplotlib.pyplot as plt;   


# storage goed sodat mens met die files van drive af kan werk
from IPython.display import Image, display;
from google.colab import drive;
drive.mount('/gdrive', force_remount=True);

# path waar ek die goed in stoor - lyk nie of dit werk nie
path='/gdrive/My Drive/datasets/';

def load_dataset():
    def download(filename, source='http://yann.lecun.com/exdb/mnist/'):
        print ('  Downloading',filename);
        from urllib.request import urlretrieve;
        urlretrieve(source+filename, filename);

    def load_mnist_images(filename):
        if not os.path.exists(filename):
            download(filename);
        else:
            print ('  ',filename,'already exists.');
            
        with gzip.open(filename, 'rb') as f:
            data = np.frombuffer(f.read(), np.uint8, offset=16);
            data = data.reshape(-1,1,28,28);
        return data/np.float32(256);
        

    def load_mnist_labels(filename):
        if not os.path.exists(filename):
            download(filename);
        else:
            print ('  ',filename,'already exists.');
            
        with gzip.open(filename, 'rb') as f:
            data = np.frombuffer(f.read(), np.uint8, offset = 8);
        
        return data;
        
    
    # files wat ek van die mnist site aflaai
    dfiles = ['train-images-idx3-ubyte.gz','train-labels-idx1-ubyte.gz',
         't10k-images-idx3-ubyte.gz', 't10k-labels-idx1-ubyte.gz'];     
    
    # omgewing waarin ek al die files stoor
    env_files = {};
    
    for dfile in dfiles:
        parts = dfile.split('-');
        if parts[1] == 'labels':
            env_files[parts[0]+'_'+parts[1]] = load_mnist_labels( dfile );
        else:
            env_files[parts[0]+'_'+parts[1]] = load_mnist_images( dfile );
    
    return env_files;
  
print ('Retrieving datasets:');
files = load_dataset();

# for key in files.keys():
#     print( key );
    
# train_images
# train_labels
# t10k_images
# t10k_labels

plt.show(plt.imshow(files['train_images'][4][0]));
# print( files['train_images'][1][0] );

# STAP 2: Train die netwerk

try:
    import lasagne;
except:
    os.system( "pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip" );
    import lasagne;
try:
    import theano;
    import theano.tensor as T;
except:
    os.system( "pip install --upgrade https://github.com/Theano/Theano/archive/master.zip" );
    import theano;
    import theano.tensor as T;    



def build_NN( input_var=None ):
    print( 'Building neural network.' );
    
    # input layer
    l_in = lasagne.layers.InputLayer( shape = ( None,1,28,28 ), input_var = input_var );
    
    # dropout layer 1
    l_in_dropout = lasagne.layers.DropoutLayer( l_in, p = 0.2 );
    
    # hidden layer 1
    l_hid1 = lasagne.layers.DenseLayer( l_in_dropout, 
                                   num_units = 800,
                                   nonlinearity = lasagne.nonlinearities.rectify,
                                   W = lasagne.init.GlorotUniform());
    
    # dropout layer for hidden layer 1
    l_hid1_drop = lasagne.layers.DropoutLayer( l_hid1, p = 0.5 );
    
    # hidden layer 2
    l_hid2 = lasagne.layers.DenseLayer( l_hid1_drop, 
                                   num_units = 800,
                                   nonlinearity = lasagne.nonlinearities.rectify,
                                   W = lasagne.init.GlorotUniform());
    
    # dropout layer for hidden layer 2
    l_hid2_drop = lasagne.layers.DropoutLayer( l_hid2, p = 0.5 );

    # final output layer
    l_out = lasagne.layers.DenseLayer( l_hid2_drop, 
                                        num_units = 10,
                                        nonlinearity = lasagne.nonlinearities.softmax);
    
    return l_out;

# nou gaan ons vir die netwerk se hoe om homself te train
input_var = T.tensor4('inputs');
target_var = T.ivector('targets');

network = build_NN( input_var );

# training steps
prediction = lasagne.layers.get_output( network );
loss = lasagne.objectives.categorical_crossentropy( prediction, target_var );

loss = loss.mean();

params = lasagne.layers.get_all_params( network, trainable = True );
updates = lasagne.updates.nesterov_momentum( loss, params, learning_rate = 0.01, momentum = 0.9 );

train_fn = theano.function( [ input_var, target_var ], loss, updates = updates );

num_training_steps = 10;

for step in range( num_training_steps ):
    train_err = train_fn( files[ 'train_images'], files[ 'train_labels'] );
    print( 'Current step is',step );

# STAP 3: Toets die netwerk met een van die toets beelde.

test_prediction = lasagne.layers.get_output( network );
val_fn = theano.function( [ input_var ], test_prediction );

plt.show(plt.imshow(files['t10k_images'][0][0]));
val_fn( [ files[ 't10k_images' ][0] ] )