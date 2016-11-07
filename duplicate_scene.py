
import bpy

C = bpy.context
D = bpy.data

instance = 5

for scene in bpy.data.scenes :
    if scene != C.scene :
        D.scenes.remove(scene, do_unlink = True)

GroupObjects = {}
for group in bpy.data.groups :
    obList = []
    for ob in group.objects :
        if ob.users_scene :   
            obList.append(ob)
    if not obList :
        D.groups.remove(group, do_unlink = True)
                 
for group in bpy.data.groups :
    obList = []
    for ob in group.objects :
        obList.append(ob)
    GroupObjects[group]= obList

for index in range (0, instance) :
    naming = "_"+"%03d" % index
    
    
    scene = bpy.data.scenes.new(C.scene.name+naming)
    for ob in C.scene.objects :
        newOb = ob.copy()
        

        
        newObName = D.objects.get(ob.name+naming)
        if newObName :
            newObName.name = newObName.name +"_to_clear"
        
        
        newOb.name = ob.name+naming
        scene.objects.link(newOb)
    
    for ob in scene.objects :
        if ob.parent :        
            ob.parent = scene.objects.get(ob.parent.name+naming)
            
        if ob.modifiers :
            for m in ob.modifiers :
                if m.object :
                    m.object = scene.objects.get(m.object.name + naming)
        
        if ob.animation_data :
            for d in ob.animation_data.drivers :
                for v in d.driver.variables :
                    for t in v.targets :
                        t.id = scene.objects.get(t.id.name + naming)
        
        if ob.data.animation_data :
            if len(ob.data.animation_data.drivers)>0 :
                name = ob.data.name
                ob.data = ob.data.copy()
                ob.data.name = name+naming
                
                for d in ob.data.animation_data.drivers :
                    for v in d.driver.variables :
                        for t in v.targets :
                            if t.id :
                                t.id = scene.objects.get(t.id.name + naming)        
                
        
    #reassign group :
    for group in GroupObjects :
        g = bpy.data.groups.new(group.name+ naming)
        for ob in GroupObjects[group]:
            g.objects.link(scene.objects.get(ob.name + naming))
            
