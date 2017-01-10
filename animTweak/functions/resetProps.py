from .insertKeyframe import insert_keyframe

import bpy

NonZeroValue={

'pose.bones["torso"]["pivot_slide"]': 0.333,
'pose.bones["spine"]["bend_alpha"]': 0.5,
'pose.bones["spine"]["bend_alpha"]': 1.0,
'pose.bones["upper_arm.fk.L"]["stretch_length"]' :1,
'pose.bones["upper_arm.fk.R"]["stretch_length"]':1,
'pose.bones["thigh.fk.L"]["stretch_length"]':1,
'pose.bones["thigh.fk.R"]["stretch_length"]':1,
}

def reset_props(bone,insertKeyframe):
    if bone.rotation_mode =='QUATERNION':
        bone.rotation_quaternion = 1,0,0,0

    if bone.rotation_mode == 'AXIS_ANGLE':
        bone.rotation_axis_angle = 0,0,1,0

    else :
        bone.rotation_euler = 0,0,0

    bone.location = 0,0,0
    bone.scale = 1,1,1

    for key,value in bone.items() :
        if key != '_RNA_UI':

            if 'pose.bones["%s"]["%s"]'%(bone.name,key) in NonZeroValue :

                bone[key] = NonZeroValue['pose.bones["%s"]["%s"]'%(bone.name,key)]

            else :
                if type(value)== int :
                    bone[key]=0
                else :
                    bone[key]=0.0


    if insertKeyframe == 1 :
        insert_keyframe(bone)
