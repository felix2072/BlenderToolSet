import bpy


class WM_OT_dialogop(bpy.types.Operator):
    """Custom Operator - Add txt here """
    bl_label = "Add Cube Menu"
    bl_idname = "wm.dialogop"
    
    name = bpy.props.StringProperty(name= "Name", default= "")
    scale = bpy.props.FloatVectorProperty(name= "Scale: X,Y,Z", default= (1,1,1))
    bool = bpy.props.BoolProperty(name= "Array?", default= False)
    array = bpy.props.IntProperty(name= "Array Count", default = 1)
    bool2 = bpy.props.BoolProperty(name= "Rotate?", default= False)
    
    
    
    def execute(self, context):
        
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.transform.translate(value= (2,0,0))
        bpy.ops.transform.rotate(value= 0.3, orient_axis = 'X')
                
        bpy.ops.object.select_all(action= 'DESELECT')
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

addon_keymaps = []

def register():
    bpy.utils.register_class(WM_OT_dialogop)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type= 'VIEW_3D')
        kmi = km.keymap_items.new("wm.dialogop", type= 'J', value= 'PRESS', shift= True)
        addon_keymaps.append((km, kmi))
    


def unregister():
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(WM_OT_dialogop)         

    
if __name__ == "__main__":
    register()
    
    bpy.ops.wm.dialogop('INVOKE_DEFAULT')