import bpy

C = bpy.context
D = bpy.data

action = C.object.animation_data.action


Fcurve={}
keyPose =[]
for fcurve in action.fcurves :
    keyList=[]    
    for key in fcurve.keyframe_points :
        if key.co[0] not in keyPose :
            keyPose.append(key.co[0])
        keyList.append(key.co[0])


    Fcurve[fcurve]=keyList


print(keyPose)
print(Fcurve)
for fcurve in action.fcurves :
    for key in keyPose :
        if key not in Fcurve[fcurve] :
            C.object.keyframe_insert(fcurve.data_path,fcurve.array_index,key)
