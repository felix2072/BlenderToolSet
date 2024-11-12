import bpy

class OBJECT_OT_unhide_All(bpy.types.Operator):
    """Unhide all selected objects """
    bl_label = "Unhide All"
    bl_idname = "object.unhide_all"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        unhideSelectedObjects()
                
        #bpy.ops.object.select_all(action= 'DESELECT')
        return {'FINISHED'}

#for Viewport / Eyeball / Render
def unHideAll():
    # Iterate through all objects in the scene
    for obj in bpy.data.objects:
        obj.hide_viewport = False  # Unhide the object in the viewport
        obj.hide_set(0)
        obj.hide_render = False


def unHideChildren():
    # Get the active object (assumed to be the selected parent)
    parent_obj = bpy.context.active_object

    if parent_obj is not None:
        # Define a function to recursively unhide all children
        def unhide_children(obj):
            obj.hide_viewport = False  # Unhide the object in the viewport
            for child in obj.children:
                unhide_children(child)  # Recursively unhide all children

        # Unhide the parent and all of its children
        unhide_children(parent_obj)
    else:
        print("No active object selected.")


def toggleHide():
    # Get the active object (assumed to be the selected parent)
    parent_obj = bpy.context.active_object

    if parent_obj is not None:
        # Determine the current hide state of the parent (we'll toggle based on this)
        toggle_hide = not parent_obj.hide_viewport

        # Define a function to recursively toggle hide_viewport for all children
        def toggle_hide_children(obj, hide_state):
            obj.hide_viewport = hide_state  # Set the hide state based on the toggle
            for child in obj.children:
                toggle_hide_children(child, hide_state)  # Recursively apply to all children

        # Toggle the visibility of the parent and all of its children
        toggle_hide_children(parent_obj, toggle_hide)
    else:
        print("No active object selected.")

def unhideSelectedObjects():
    override_context = bpy.context.copy()

    area = [area for area in bpy.context.screen.areas if area.type == "OUTLINER"][0]
    override_context['area'] = area
    override_context['region'] = area.regions[-1]
    
    with bpy.context.temp_override(**override_context):
        for obj in bpy.context.selected_ids:
            #print(obj.is_property_hidden)
            print([o for o in bpy.context.selected_ids if type(o) == bpy.types.Object])

addon_keymaps = []

def register():
    bpy.utils.register_class(OBJECT_OT_unhide_All)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type= 'VIEW_3D')
        kmi = km.keymap_items.new("object.unhide_all", type= 'U', value= 'PRESS', shift= True)
        addon_keymaps.append((km, kmi))
    


def unregister():
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(OBJECT_OT_unhide_All)         

    
if __name__ == "__main__":
    register()
    
    bpy.ops.wm.dialogop('INVOKE_DEFAULT')