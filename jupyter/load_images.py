# https://www.youtube.com/watch?v=lbFEZAXzk0g
# > Die is om net 'n idee te kry van hoe die ding werk en om net 'n klein model
#    aan die gang te kry sodat mens van daar af kan gaan.
# > Ek gaan ook nie die comments insit nie, maar jy kan gaan kyk as jy bietjie
#    onseker is.

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