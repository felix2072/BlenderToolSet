import cmd
import bpy
import os


# ICON_NAMES is now loaded from icon.csv
def load_icon_names():
    csv_path = os.path.join(os.path.dirname(__file__), "icon.csv")
    with open(csv_path, encoding="utf-8") as f:
        content = f.read()
    # Remove line breaks and split by comma
    return [name.strip() for name in content.replace("\n", "").split(",") if name.strip()]

ICON_NAMES = load_icon_names()

import subprocess

class ICONS_UL_icon_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            op = row.operator("wm.copy_icon_name", text=item.name, icon=item.name)
            op.icon_name = item.name
        elif self.layout_type in {'GRID'}:
            layout.label(text="", icon=item.name)

class ICONS_OT_copy_icon_name(bpy.types.Operator):
    bl_idname = "wm.copy_icon_name"
    bl_label = "Copy Icon Name"
    bl_description = "Copies the icon name to the clipboard"

    icon_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            trimmed = self.icon_name.rstrip('\n')
            subprocess.run(
                ["clip"],
                input=trimmed.encode("utf-16le"),
                check=True
            )
        except Exception as e:
            self.report({'ERROR'}, f'Clipboard Error: {e}')
            return {'CANCELLED'}
        self.report({'INFO'}, f'Icon name "{trimmed}" copied!')
        return {'FINISHED'}

class ICONS_OT_init_icon_list(bpy.types.Operator):
    bl_idname = "wm.init_icon_list"
    bl_label = "Open Icon Dictionary"
    def execute(self, context):
        items = context.scene.icon_name_items
        items.clear()
        for name in ICON_NAMES:
            item = items.add()
            item.name = name
        return {'FINISHED'}

class IconNameItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()

class ICONS_PT_menu(bpy.types.Panel):
    bl_label = "Icons"
    bl_idname = "ICONS_PT_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Icons'

    def draw(self, context):
        layout = self.layout
        if len(context.scene.icon_name_items) == 0:
            layout.operator("wm.init_icon_list", icon='VIEWZOOM')
            return
        box = layout.box()
        row = box.row()
        row.template_list("ICONS_UL_icon_list", "", context.scene, "icon_name_items", context.scene, "icon_name_index", rows=20)

def register():
    bpy.utils.register_class(ICONS_UL_icon_list)
    bpy.utils.register_class(ICONS_OT_copy_icon_name)
    bpy.utils.register_class(ICONS_OT_init_icon_list)
    bpy.utils.register_class(IconNameItem)
    bpy.utils.register_class(ICONS_PT_menu)
    bpy.types.Scene.icon_name_items = bpy.props.CollectionProperty(type=IconNameItem)
    bpy.types.Scene.icon_name_index = bpy.props.IntProperty(name="Icon Index", default=-1)

def unregister():
    bpy.utils.unregister_class(ICONS_UL_icon_list)
    bpy.utils.unregister_class(ICONS_OT_copy_icon_name)
    bpy.utils.unregister_class(ICONS_OT_init_icon_list)
    bpy.utils.unregister_class(IconNameItem)
    bpy.utils.unregister_class(ICONS_PT_menu)
    del bpy.types.Scene.icon_name_items
    del bpy.types.Scene.icon_name_index
