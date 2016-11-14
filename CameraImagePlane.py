bl_info = {
    "name": "Camera Image Plane",
    "author": "Christophe Seux",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "description": "Adds an image plane on the active camera",
    "warning": "",
    "wiki_url": "",
    "category": "User",
    }

import bpy
import os

from bpy.types import Menu, Panel, UIList, PropertyGroup
from bpy.props import StringProperty, BoolProperty, FloatProperty, CollectionProperty, BoolVectorProperty, PointerProperty

C = bpy.context
D = bpy.data

empty = ''
plane =''

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

def create_empty(name):
    empty =bpy.data.objects.new(name+"_target",None)
    empty.empty_draw_size = 0.1
    empty.empty_draw_type= 'SPHERE'
    empty.lock_location = True,True,False
    C.scene.objects.link(empty)
    
    return (empty)
    
def SetupOffsetDriver(self,plane,shape,key,expression):
    spDriver = shape.driver_add('value')
    spDriver.driver.type = 'SCRIPTED'
    spDriver.driver.expression = expression

    var = spDriver.driver.variables.new()
    var.name = 'var'
    var.type = 'SINGLE_PROP'
    var.targets[0].id = plane
    var.targets[0].data_path='["%s"]'%(key)
        

def SetupDriver(ob,image,camera):
    
    driver1 = ob.driver_add('scale',1).driver
    driver1.type = 'SCRIPTED'
    driver1.expression ="depth*tan(camAngle/2)*%s"%(str(image.size[1])+'/'+str(image.size[0]))
    driver2 = ob.driver_add('scale',0).driver
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
        depth.targets[0].id = ob    
        depth.targets[1].id = camera  
        depth.targets[0].data_path = 'location'
        depth.targets[0].transform_type = 'LOC_Z'


class CreateCameraImagePlane(bpy.types.Operator):
    """Create mesh plane(s) from image files with the appropiate aspect ratio"""
    bl_idname = "create.camera_image_plane"
    bl_label = "Create Camera Image Plane"
    bl_options = {'REGISTER', 'UNDO'}

    # -----------
    # File props.
    files = CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})

    directory = StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})
    
    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'CAMERA' or context.space_data.region_3d.view_perspective == 'CAMERA')

    def execute(self, context):
        import_list, directory = self.generate_paths()
            
        camera = bpy.context.scene.camera
        offset = 8
        
        X,Y = 1,1        
        origin = (0,0,0)
        verts = [(-X,-Y,0), (-X,Y,0), (X,Y,0),(X,-Y,0)]
        faces = [(0,3,2,1)]

        for path in import_list :
            image =0
            for i in bpy.data.images :
                if i.filepath == directory+path :
                    image = i
                    break
            
            if image ==0 :
                image = bpy.data.images.load(directory+path)
                image.name = os.path.splitext(path)[0]
            
            plane = createMeshFromData(image.name, origin, verts, faces)            
            
            empty = create_empty(camera.name)

            
            bpy.context.scene.update()
            
            SetupDriver(empty,image,camera)
            
            plane.parent = empty
            empty.parent = camera
            empty.location[2]-= offset
            plane['X']=0.0
            plane['Y']=0.0
            plane['size']=0.0
            plane.lock_location = False,False,True
            
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


class CIP_ImagesSettings(PropertyGroup):
    show_image = BoolProperty(name="Show Image", default=True)
    show_expanded = BoolProperty(name="Show Expanded", default=True)
    thumbnail = BoolProperty(name="Thumbnail", default=False)


class CameraMoviePlanePanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Image Plane"
        
    bpy.types.Scene.CIP_distance = FloatProperty(default=5.0,min = 0, max = 100)
    bpy.types.Scene.CIP_size = FloatProperty(default=0.0,min = 0, max = 100)
    bpy.types.Scene.CIP_offsetX = FloatProperty(default=5.0,min = 0, max = 100)
    bpy.types.Scene.CIP_offsetY = FloatProperty(default=5.0,min = 0, max = 100)
    bpy.types.Scene.CIP_thumbnail = BoolProperty(default=False)

    @classmethod
    def poll(self, context):
        return (context.object and context.object.type == 'CAMERA' or context.space_data.region_3d.view_perspective == 'CAMERA')

    def draw_header(self, context):
        view = context.space_data

        self.layout.prop(view, "show_background_images", text="")

    def draw(self, context):
        layout = self.layout
    
        row = layout.row()
        row.operator("create.camera_image_plane", emboss=True, text="Add Camera Plane",icon="RENDER_RESULT")
        box = layout.box()
        col = box.column()
        row = col.row(align=True)

        if context.scene.imagePlaneSetting.show_expanded == True :
            show_icon = "TRIA_DOWN"
        else :
            show_icon = "TRIA_RIGHT"
        
        
        row.prop(context.scene.imagePlaneSetting,"show_expanded" ,emboss=False, text="",icon = show_icon)
        row.label(text = "lalala")

        if context.scene.imagePlaneSetting.thumbnail == True :
            show_icon = "FULLSCREEN_EXIT"
        else :
            show_icon = "FULLSCREEN_ENTER"
        
        row.prop(context.scene.imagePlaneSetting,"thumbnail" ,emboss=False, text="",icon = show_icon)
        
        if context.scene.imagePlaneSetting.show_image == True :
            show_icon = "RESTRICT_VIEW_OFF"
        else :
            show_icon = "RESTRICT_VIEW_ON"
            
            
        row.prop(context.scene.imagePlaneSetting,"show_image" ,emboss=False, text="",icon = show_icon)
        row.operator("object.move_operator", emboss=False, text="",icon = "X")
        
        
        if context.scene.imagePlaneSetting.show_expanded == True :
            #col.prop(empty,"location",text = "Distance")

            col.prop(context.scene,"CIP_size",text = "Size")
            row = col.row()
            row.prop(context.scene,"CIP_offsetX",text = "X")
            row.prop(context.scene,"CIP_offsetY",text = "Y")




def register():
    
    bpy.utils.register_module(__name__)
    bpy.types.Scene.imagePlaneSetting = PointerProperty(type=CIP_ImagesSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.imagePlaneSetting


if __name__ == "__main__":  
    register()  
    
