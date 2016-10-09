import bpy

SCALE_bones = []
armature = bpy.context.active_object.data

for bone in bpy.context.active_object.data.edit_bones :
    if not bone.name.startswith("MASTER") :
      
        SCALE_bones.append(bone)


for bone in SCALE_bones :
    try :
        tailParent = armature.edit_bones.get(bone["tailParent"])
        headParent = armature.edit_bones.get(bone["headParent"])
        
        bone.tail = (tailParent.tail-tailParent.head) * bone["tail"]+tailParent.head
        bone.head = (tailParent.tail-tailParent.head) * bone["head"]+headParent.head
        
    except :
        pass
    
    try :    
        bone.roll = headParent.roll - bone["roll"]
        
    except :
        pass