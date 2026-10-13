import sys
import os

# Sustituye 'tu_usuario' por tu nombre de usuario en PythonAnywhere
path = '/home/tu_usuario/portal_microapps'
if path not in sys.path:
    sys.path.append(path)

from app import app as application