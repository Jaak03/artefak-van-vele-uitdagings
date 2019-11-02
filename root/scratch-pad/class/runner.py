print('Testing class')

from importlib import import_module

test = import_module('c')

t = test.Test() # werk

method = getattr(t, 'boom')
method()
