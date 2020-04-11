import os
from shutil import copy


def copyImages(subDirectory):
  for file in os.listdir(f'{subDirectory}/words/'):
    print(file)
    if '.tif' in file:
      copy(f'{subDirectory}/words/{file}', f'/home/mother/git/SELF/artefak-van-vele-uitdagings/root/images/pile/{file}')

def getFiles(dir, extension ):
    tmp_files_list = []
    for file in os.listdir(dir):
      if not('.' in file):
        copyImages(f'{os.getcwd()}/{dir}/{file}')

getFiles('images/idcar', '.tif')        
