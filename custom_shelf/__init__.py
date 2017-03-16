bl_info = {
    "name": "Custom Shelf",
    "author": "Christophe Seux",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "category": "User"}

if "bpy" in locals():
    import importlib
    importlib.reload(operators)
    importlib.reload(panels)
    importlib.reload(functions)

from . import operators
#from functions import read_shelves
from . import shelves
from . import panels
from .panels import CustomShelfSettings

import bpy
import os





def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.CustomShelf = bpy.props.PointerProperty(type= CustomShelfSettings)

def unregister():
    del bpy.types.Scene.CustomShelf
    bpy.utils.unregister_module(__name__)
