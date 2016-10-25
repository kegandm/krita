import pykrita
import os
import sys

from .api import *
from .decorators import *
from .dockwidgetfactory import *
from PyKrita import krita

krita_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, krita_path)
print("%s added to PYTHONPATH" % krita_path, file=sys.stderr)

# Look for PyQt
try:
    from PyQt5 import QtCore
except ImportError:
    print("Python cannot find the Qt5 bindings.", file=sys.stderr)
    print("Please make sure, that the needed packages are installed.", file=sys.stderr)
    raise

# Shows nice looking error dialog if an unhandled exception occures.
import excepthook
excepthook.install()

# Import helper modules
from scripter_hooks import MenuHooks
from mikro import create_pyqt_object, Error as MiKroError

import builtins
builtins.Krita = krita.Krita.instance()

def qDebug(text):
    '''Use KDE way to show debug info

        TODO Add a way to control debug output from partucular plugins (?)
    '''
    plugin = sys._getframe(1).f_globals['__name__']
    pykrita.qDebug('{}: {}'.format(plugin, text))


@pykritaEventHandler('_pluginLoaded')
def on_load(plugin):
    if plugin in init.functions:
        # Call registered init functions for the plugin
        init.fire(plugin=plugin)
        del init.functions[plugin]
    return True


@pykritaEventHandler('_pluginUnloading')
def on_unload(plugin):
    if plugin in unload.functions:
        # Deinitialize plugin
        unload.fire(plugin=plugin)
        del unload.functions[plugin]
    return True


@pykritaEventHandler('_pykritaLoaded')
def on_pykrita_loaded():
    qDebug('PYKRITA LOADED')
    return True


@pykritaEventHandler('_pykritaUnloading')
def on_pykrita_unloading():
    qDebug('UNLOADING PYKRITA')
    return True

