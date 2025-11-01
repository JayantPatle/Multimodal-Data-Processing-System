import sys
import os
import importlib

print('cwd=', os.getcwd())
print('sys.path[0]=', sys.path[0])
print('dirs=', os.listdir('.'))
print('isdir extractors', os.path.isdir('extractors'))
print('isdir Extractors', os.path.isdir('Extractors'))

for name in ('extractors', 'Extractors'):
    try:
        importlib.import_module(name)
        print('imported', name)
    except Exception as e:
        print('err', name, type(e).__name__ + ':', e)
