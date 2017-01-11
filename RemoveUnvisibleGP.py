bl_info = {
    "name": "DeleteHideGP",
    "author": "Christophe Seux",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "description": "Adds a new Mesh Object",
    "category": "User",
    }


import bpy
import mathutils


class GPtools_clearHideGP(bpy.types.Operator):
    """ Clear Hide GP.
    """
    bl_label = "Clear Hide GP"
    bl_idname = "gptools.clear_hide_gp"
    bl_options = {'UNDO'}


    def execute(self, context):
        
        cam = bpy.context.scene.camera
        cam_coord = cam.matrix_world.to_translation()

        GP_layer = bpy.data.grease_pencil['GPencil'].layers['GP_Layer']

        for stroke in GP_layer.active_frame.strokes :   
                
            for point in stroke.points :
                point.select = False
                ray = bpy.context.scene.ray_cast(cam_coord,point.co-cam_coord)[1]
                
                if ray[0] :
                    dif = (point.co-cam_coord)-(ray-cam_coord)
                    
                    if dif.length > 0.1 :
                        point.select =True                    

        bpy.ops.gpencil.delete(type='POINTS')
        
        return {'FINISHED'}


class GPtools_panel(bpy.types.Panel):
    bl_label = "Extra Tools"
    bl_category = "Grease Pencil"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        if context.gpencil_data is None:
            return False

        gpd = context.gpencil_data
        return bool(context.editable_gpencil_strokes) and bool(gpd.use_stroke_edit_mode)

    def draw(self, context):
        layout = self.layout
        is_3d_view = context.space_data.type == 'VIEW_3D'
        
        if is_3d_view:
            layout.operator("gptools.clear_hide_gp")

def register():
    bpy.utils.register_class(GPtools_clearHideGP)
    bpy.utils.register_class(GPtools_panel)

def unregister():
    bpy.utils.unregister_class(GPtools_clearHideGP)
    bpy.utils.unregister_class(GPtools_panel)


if __name__ == "__main__":
    register()
