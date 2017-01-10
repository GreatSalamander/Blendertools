import bpy
import collections
   
class at_poseLib(bpy.types.Panel):
    bl_label = "Pose Lib"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "posemode"

    def getMarkers(self,context):
        armObj = context.object

        ret = {}

        if armObj.pose_library:
            for key,value in armObj.pose_library.pose_markers.items():
                ret[key] = value.frame
        return(collections.OrderedDict(sorted(ret.items(), key=lambda t: t[0])))
        return(ret)

    @classmethod
    def poll(self,context):
        return (context.active_object != None and context.mode == 'POSE')

    def draw(self, context):
        
        layout = self.layout

        layout.template_ID(context.active_object, "pose_library", new="poselib.new", unlink="poselib.unlink")

        for i,(name,frame) in enumerate(self.getMarkers(context).items()):
            if i%4 == 0:
                row = layout.row(align=True)
            row.operator("poselib.apply_pose_custom",text=name).pose_index = frame