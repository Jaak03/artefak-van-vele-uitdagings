#! pip install --upgrade https://github.com/Theano/Theano/archive/master.zip
#! pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip

import lasagne;
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
                                   W = lasagne.init.GloroUniform());
    
    # dropout layer for hidden layer 1
    l_hid1_drop = lasagne.layers.DropoutLayer( l_hid1, p = 0.5 );
    
    # hidden layer 2
    l_hid2 = lasagne.layers.DenseLayer( l_hid1_drop, 
                                   num_units = 800,
                                   nonlinearity = lasagne.nonlinearities.rectify,
                                   W = lasagne.init.GloroUniform());
    
    # dropout layer for hidden layer 2
    l_hid1_drop = lasagne.layers.DropoutLayer( l_hid2, p = 0.5 );

build_NN();