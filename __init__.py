from . import icon_menu

bl_info = {
    "name": "BlenderToolSet",
    "author": "Felix Worseck",
    "description": "Some usefull Functions to make Blender less anoying",
    "blender": (2, 80, 0),
    "version": (2026, 5, 0),
    "category": "Outliner",
}


def register():
    icon_menu.register()


def unregister():
    icon_menu.unregister()
    