import bpy

from ..functions import apply_pose
from ..functions import reset_props
from ..functions import insert_keyframe


class ApplyPose(bpy.types.Operator):
    bl_label = "Apply Pose Custom"
    bl_idname = "poselib.apply_pose_custom"

    pose_index = bpy.props.IntProperty()
    opacity = bpy.props.FloatProperty()

    def execute(self,context):
    	print(self.pose_index)
    	apply_pose(self.pose_index,self.opacity,context)
    	return({'FINISHED'})

class ResetProps(bpy.types.Operator) :
    """ Reset Transfrom And Props.
    """
    bl_idname = "pose.reset_props"
    bl_label = "Reset bones transforms and custom propeties"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        if len(bpy.context.selected_pose_bones)==0 :
            bones = bpy.context.object.pose.bones

        else :
            bones = bpy.context.selected_pose_bones

        for bone in bones :
            #0 = no keyframe inserted, 1 = keyframe inserted
            if bpy.context.scene.tool_settings.use_keyframe_insert_auto == False :
                reset_props(bone,0)
            else :
                reset_props(bone,1)

        return {'FINISHED'}

class InsertKeyFrame(bpy.types.Operator):
    """ Add key frame to selected bone on available transforms and properties
    """
    bl_idname = "pose.insert_keyframe"
    bl_label = "Insert Key Frame"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        for bone in bpy.context.selected_pose_bones :
            insert_keyframe(bone)


        return {'FINISHED'}
