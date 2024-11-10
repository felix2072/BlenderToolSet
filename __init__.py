from . import addCube
from . import deleteAll

bl_info = {
    "name": "BlenderToolSet",
    "author": "Felix Worseck",
    "description": "Some usefull Functions to make Blender less anoying",
    "blender": (2, 80, 0),
    "version": (2024, 11, 0),
    "category": "Outliner",
}


def register():
    addCube.register()
    deleteAll.register()


def unregister():
    addCube.unregister()
    deleteAll.unregister()