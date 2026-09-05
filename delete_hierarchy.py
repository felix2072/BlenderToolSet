import bpy


class SBB_OT_delete_hierarchy(bpy.types.Operator):
    """Delete selected objects including all their children"""

    bl_idname = "object.sbb_delete_hierarchy"
    bl_label = "Delete Hierarchy"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" and bool(context.selected_objects)

    def execute(self, context):
        targets = set()
        for obj in context.selected_objects:
            targets.add(obj)
            targets.update(obj.children_recursive)

        skipped = 0
        removed = 0
        for obj in targets:
            if obj.library is not None or obj.override_library is not None:
                skipped += 1
                continue
            bpy.data.objects.remove(obj, do_unlink=True)
            removed += 1

        if skipped:
            self.report(
                {"WARNING"},
                f"Deleted {removed} object(s), skipped {skipped} linked object(s)",
            )
        else:
            self.report({"INFO"}, f"Deleted {removed} object(s)")

        return {"FINISHED"}


def register():
    bpy.utils.register_class(SBB_OT_delete_hierarchy)


def unregister():
    bpy.utils.unregister_class(SBB_OT_delete_hierarchy)
