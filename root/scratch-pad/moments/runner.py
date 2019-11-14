print('Testing class')

from importlib import import_module
import inspect

test = import_module('c')

t = test.Test('Kyk maar') # werk

# print(dir(t))

method = getattr(test, '__init__')
method('Die is dan die boodskap wat ek wil he...')

import TestPackage

print(dir(TestPackage))