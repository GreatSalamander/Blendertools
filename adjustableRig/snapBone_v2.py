import bpy

SCALE_bones = []
armature = bpy.context.active_object.data

#for bone in bpy.context.selected_editable_bones :
for bone in bpy.context.active_object.data.edit_bones :
    if not bone.name.startswith("REF-") :
      
        SCALE_bones.append(bone)

for bone in SCALE_bones :
    if bone.get("head") is not None and bone.get('tail') is not None:
    
        tailParent = armature.edit_bones.get(bone["tailParent"]) if bone.get("tailParent") else print(bone)
        headParent = armature.edit_bones.get(bone["headParent"]) if bone.get("headParent") else print(bone)
 
        bone.tail = (tailParent.tail-tailParent.head) * bone["tail"]+tailParent.head
        bone.head = (headParent.tail-headParent.head) * bone["head"]+headParent.head
        
        bone.roll = headParent.roll - bone["roll"]
            
             
    elif bone.get("head") is  None and bone.get("tail") is not None: 
                
        tailParent = armature.edit_bones.get(bone["tailParent"]) if bone.get("tailParent") else print(bone)
    
        bone.tail = (tailParent.tail-tailParent.head) * bone["tail"]+tailParent.head
        bone.head = (headParent.tail-headParent.head) * bone["tail"]+bone.head
        

    elif bone.get("tail") is  None and bone.get("head") is not None:
        
        headParent = armature.edit_bones.get(bone["headParent"]) if bone.get("headParent") else print(bone)
     
        bone.tail = (headParent.tail-headParent.head) * bone["head"]+headParent.head+bone.tail-bone.head
        bone.head = (headParent.tail-headParent.head) * bone["head"]+headParent.head

        
        
