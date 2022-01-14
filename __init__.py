import bpy

bl_info = {
    "name": "Collection Helper Operations",
    "blender": (3, 0, 0),
    "category": "Object",
}

class IsolateCollectionInstance(bpy.types.Operator):
    """Isolate Collection Instance"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "collection_instance.isolate"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Isolate collection instance(s)"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        # The original script
        selected_objects = context.selected_objects
        objects_to_select = []
        for obj in selected_objects:
            if getattr(obj, 'type', '') == 'EMPTY' and obj.instance_collection is not None:
                for lc in context.scene.view_layers['ViewLayer'].layer_collection.children:
                    if lc.collection == obj.instance_collection:
                        lc.exclude = False
                for o in obj.instance_collection.objects:
                    objects_to_select.append(o)
        
        for o in selected_objects:
            o.select_set(False)
        for o in objects_to_select:
            o.select_set(True)
        bpy.ops.view3d.localview()
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

class AttachOrphanCollection(bpy.types.Operator):
    """Append orphan collection"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "collection_instance.attach_orphan"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Attach orphan collection(s)"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.
        # The original script
        destination_collection = bpy.data.collections['Collection']
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            is_found = False
            if getattr(obj, 'type', '') == 'EMPTY' and  obj.instance_collection is not None:
                for item in destination_collection.children:
                    if obj.instance_collection == item:
                        is_found = True
                        break
                if not is_found:
                    destination_collection.children.link(obj.instance_collection)
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(IsolateCollectionInstance.bl_idname)
    self.layout.operator(AttachOrphanCollection.bl_idname)

def draw_menu(self, context):
    layout = self.layout
    selected_objects = context.selected_objects
    found = False
    for obj in selected_objects:
        if getattr(obj, 'type', '') == 'EMPTY' and obj.instance_collection is not None:
            found = True
    if found:
        layout.separator()
        layout.operator(IsolateCollectionInstance.bl_idname, text=IsolateCollectionInstance.bl_label)
        layout.operator(AttachOrphanCollection.bl_idname, text=AttachOrphanCollection.bl_label)

def register():
    bpy.utils.register_class(IsolateCollectionInstance)
    bpy.utils.register_class(AttachOrphanCollection)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_menu)

def unregister():
    bpy.utils.unregister_class(IsolateCollectionInstance)
    bpy.utils.unregister_class(AttachOrphanCollection)
    bpy.types.VIEW3D_MT_object.remove(menu_func)  # Adds the new operator to an existing menu.
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_menu)

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()