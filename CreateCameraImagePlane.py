bl_info={"name": "Create Camera Image Plane", "author": "Christophe SEUX", "category":"Object" }

import os
import bpy
from bpy.types import Operator
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       FloatProperty,
                       CollectionProperty,
                       )


def createMeshFromData(name, origin, verts, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    
    # Link object to scene and make active
    scn = bpy.context.scene
    scn.objects.link(ob)
 
    # Create mesh from given verts, faces.
    me.from_pydata(verts, [], faces)
    # Update mesh with new data
    me.update()    
    
    me.uv_textures.new("UVMap")
    return ob


class CreateCameraImagePlane(Operator):
    """Create mesh plane(s) from image files with the appropiate aspect ratio"""
    bl_idname = "create_camera_image.plane"
    bl_label = "Create Camera Image Plane"
    bl_options = {'REGISTER', 'UNDO'}

    # -----------
    # File props.
    files = CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})

    directory = StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})

    def SetupOffsetDriver(self,plane,shape,key,expression):
        spDriver = shape.driver_add('value')
        spDriver.driver.type = 'SCRIPTED'
        spDriver.driver.expression = expression

        var = spDriver.driver.variables.new()
        var.name = 'var'
        var.type = 'SINGLE_PROP'
        var.targets[0].id = plane
        var.targets[0].data_path='["%s"]'%(key)
        

    def SetupDriver(self,plane,image,camera):
        drivers = []
        
        driver1 = plane.driver_add('scale',1).driver
        driver1.type = 'SCRIPTED'
        driver1.expression ="depth*tan(camAngle/2)*%s"%(str(image.size[1])+'/'+str(image.size[0]))
        driver2 = plane.driver_add('scale',0).driver
        driver2.type= 'SCRIPTED'
        driver2.expression ="depth*tan(camAngle/2)"
        
        drivers = [driver1,driver2]
        
        for driver in drivers :
            camAngle = driver.variables.new()
            camAngle.name = 'camAngle'
            camAngle.type = 'SINGLE_PROP'
            camAngle.targets[0].id = camera
            camAngle.targets[0].data_path="data.angle"
           
            depth = driver.variables.new()
            depth.name = 'depth'
            depth.type = 'LOC_DIFF'
            depth.targets[0].id = plane    
            depth.targets[1].id = camera  
            depth.targets[0].data_path = 'location'
            depth.targets[0].transform_type = 'LOC_Z'



    def execute(self, context):
        import_list, directory = self.generate_paths()
        
        #Guess the good camera
        if bpy.context.object :
            if bpy.context.object.type == 'CAMERA':
                camera = bpy.context.object
        
        elif bpy.context.scene.camera :
            camera = bpy.context.scene.camera

        else :
            cameraList = []
            for ob in bpy.data.objects :
                if ob.type == 'CAMERA' and ob.users!=0:
                    cameraList.append(ob)
            
                elif ob.type == 'CAMERA' and ob.users==0 and ob.name == 'Camera':
                    ob.name="Camera.001"           
            
            if len(cameraList) == 1:
                camera = cameraList[0]
            
            else :
                cam = bpy.data.cameras.new('Camera')
                camera = bpy.data.objects.new('Camera', cam)
                camera.location = (0,-3,1.7)
                camera.rotation_euler = (1.5708,0,0)
                scn = bpy.context.scene
                scn.objects.link(camera)              
                bpy.context.scene.camera = camera
                
        offset = 8
        for path in import_list :
            image =0
            for i in bpy.data.images :
                if i.filepath == directory+path :
                    image = i
                    break
            
            if image ==0 :
                image = bpy.data.images.load(directory+path)
                image.name = os.path.splitext(path)[0]
            
            X=1
            Y=1
            
            origin = (0,0,0)
            verts = [(-X,-Y,0), (-X,Y,0), (X,Y,0),(X,-Y,0)]
            faces = [(0,3,2,1)]
            
            plane = createMeshFromData(image.name, origin, verts, faces)            
            
            self.SetupDriver(plane,image,camera)
            plane.parent = camera
            plane.location[2]-= offset
            plane['X']=0.0
            plane['Y']=0.0
            plane['size']=0.0
            plane.lock_location[0] = True
            plane.lock_location[1] = True
            
            for spName in['Basis','X','-X','Y','-Y','bigger','smaller'] :
                plane.shape_key_add(spName)
                shape = plane.data.shape_keys.key_blocks.get(spName)
                if spName == 'X' :
                    self.SetupOffsetDriver(plane,shape,'X','var*0.0002')
                if spName == '-X' :
                    self.SetupOffsetDriver(plane,shape,'X','var*-0.0002')
                if spName == 'Y' :
                    self.SetupOffsetDriver(plane,shape,'Y','var*0.0002')
                if spName == '-Y' :
                    self.SetupOffsetDriver(plane,shape,'Y','var*-0.0002')            
                if spName == 'bigger' :
                    self.SetupOffsetDriver(plane,shape,'size','var*0.0001')              
                if spName == 'smaller' :
                    self.SetupOffsetDriver(plane,shape,'size','var*-0.01')             
            
            step = 100
            for data in plane.data.shape_keys.key_blocks['X'].data :
                data.co[0]+=step

            for data in plane.data.shape_keys.key_blocks['-X'].data :
                data.co[0]-=step
                
            for data in plane.data.shape_keys.key_blocks['Y'].data :
                data.co[1]+=step
                
            for data in plane.data.shape_keys.key_blocks['-Y'].data :
                data.co[1]-=step  

            for data in plane.data.shape_keys.key_blocks['smaller'].data :
                data.co=(0,0,0)

            plane.data.shape_keys.key_blocks['bigger'].data[0].co[0]-=step
            plane.data.shape_keys.key_blocks['bigger'].data[0].co[1]-=step
            
            plane.data.shape_keys.key_blocks['bigger'].data[1].co[0]-=step
            plane.data.shape_keys.key_blocks['bigger'].data[1].co[1]+=step

            plane.data.shape_keys.key_blocks['bigger'].data[2].co[0]+=step
            plane.data.shape_keys.key_blocks['bigger'].data[2].co[1]+=step

            plane.data.shape_keys.key_blocks['bigger'].data[3].co[0]+=step
            plane.data.shape_keys.key_blocks['bigger'].data[3].co[1]-=step


            offset +=2
            
            # set the image on the UV editor
            for uv_face in plane.data.uv_textures.active.data:
                uv_face.image = image

            # set the material
            plane.show_transparent = True
            plane.show_wire = True
            mat = bpy.data.materials.new(name=image.name)

            if plane.data.materials:
                plane.data.materials[0] = mat
            else:
                plane.data.materials.append(mat)
            
            mat.use_shadeless = True
            mat.use_transparency = True
            mat.alpha = 0
            mat.use_shadows= False
            mat.use_cast_shadows = False
            mat.use_cast_buffer_shadows = False
            
            
            #create texture
            if bpy.data.textures.get(image.name) :
                texture = bpy.data.textures.get(image.name)
            else :
                texture =  bpy.data.textures.new(name=image.name, type = 'IMAGE')
            texture.image = image
            
            mtex = mat.texture_slots.add()
            mtex.texture = texture
            mtex.use_map_alpha = True
            
        bpy.context.scene.update()
            
        return {'FINISHED'}

    def invoke(self, context, event):
        #self.update_extensions(context)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

   
    def generate_paths(self):
        return (fn.name for fn in self.files), self.directory

def menu_func(self, context):
    self.layout.operator(CreateCameraImagePlane.bl_idname, icon='FILE_IMAGE')
 
def register():
    bpy.utils.register_class(CreateCameraImagePlane)
    bpy.types.INFO_MT_mesh_add.append(menu_func)
 
def unregister():
    bpy.utils.unregister_class(CreateCameraImagePlane)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)  

if __name__ == "__main__":
    register()