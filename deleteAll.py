import bpy

class OBJECT_OT_delete_parent_and_children(bpy.types.Operator):
    """Delete Selected Parent and All Children"""
    bl_label = "Delete Parent and Children"
    bl_idname = "object.delete_parent_and_children"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        parent_obj = context.active_object
        
        if parent_obj is not None:
            # Deselect all objects to avoid interference
            bpy.ops.object.select_all(action='DESELECT')
            
            # Recursively select all children of the parent
            def select_all_children(obj):
                obj.select_set(True)  # Select the object
                for child in obj.children:
                    select_all_children(child)
            
            # Select the parent and all its children
            select_all_children(parent_obj)
            
            # Delete selected objects (parent and its children)
            bpy.ops.object.delete()
            
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}

# Register the operator
addon_keymaps = []

def register():
    bpy.utils.register_class(OBJECT_OT_delete_parent_and_children)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        # Access the 3D View keymap
        km = kc.keymaps.get("3D View")
        if km:
            # Find the existing 'X' keymap for deletion in 3D View and remove it
            for kmi in km.keymap_items:
                if kmi.type == "DEL" and kmi.value == "PRESS":
                    km.keymap_items.remove(kmi)
                    break

            # Add new hotkey for the custom delete operator using 'X' key
            kmi = km.keymap_items.new("object.delete_parent_and_children", type="DEL", value="PRESS")
            addon_keymaps.append((km, kmi))

        # Repeat for other editors if needed (e.g., Outliner)
        km_outliner = kc.keymaps.get("Outliner")
        if km_outliner:
            for kmi in km_outliner.keymap_items:
                if kmi.type == "DEL" and kmi.value == "PRESS":
                    km_outliner.keymap_items.remove(kmi)
                    break

            kmi_outliner = km_outliner.keymap_items.new("object.delete_parent_and_children", type="DEL", value="PRESS")
            addon_keymaps.append((km_outliner, kmi_outliner))

def unregister():
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(OBJECT_OT_delete_parent_and_children)

if __name__ == "__main__":
    register()