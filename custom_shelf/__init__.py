bl_info = {
    "name": "Custom Shelf",
    "author": "Christophe Seux",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "category": "User"}

from . import operators
from . import shelves

import bpy
import os
import glob
from bpy.app.handlers import persistent
from bl_ui.space_info import INFO_HT_header,INFO_MT_editor_menus
import sys
import importlib

class CustomShelfRunFunction(bpy.types.Operator):
    bl_idname = "customshelf.run_function"
    bl_label = "Run Function"


    #variables = {}
    script = bpy.props.StringProperty()
    folder = bpy.props.StringProperty()
    #variables = bpy.props.PointerProperty(type = bpy.types.PropertyGroup)

    Types={
    str : bpy.props.StringProperty,
    int : bpy.props.IntProperty,
    float : bpy.props.FloatProperty,
    list : bpy.props.StringProperty,
    bpy.types.Object : "objects",
    bpy.types.Mesh : "meshes",
    bpy.types.Camera : "cameras",
    bpy.types.Curve : "curves",
    bpy.types.Text : "texts",
    bpy.types.Image : "images",
    bpy.types.Texture : "textures",
    bpy.types.Material : "materials",
    bpy.types.Scene : "scenes",
    bpy.types.World : "worlds",
    bpy.types.ParticleSystems : "particules",
    bpy.types.Action : "actions",
    bpy.types.Armature : "armatures",
    }

    def execute(self,context) :
        exec('from .shelves.%s import %s'%(self.folder,self.script))
        importlib.reload(eval(self.script))


        variables={}
        for v in self.variables :
            variables[v] = context.scene.CustomShelf.variables[v]

        exec('%s.main(%s)'%(self.script,variables))

        return {'FINISHED'}


    def invoke(self, context, event):

        exec('from .shelves.%s import %s'%(self.folder,self.script))
        importlib.reload(eval(self.script))

        print(eval('%s.variables'%self.script))
        self.variables = eval('%s.variables'%self.script)

        #for key,value in context.scene.CustomShelfVars.items() :



        for key,value in self.variables.items() :

            if type(value) in [int,float] :
                Type  = self.Types[type(value)]

                setattr(CustomShelfVariables, key, Type(default = value))
                exec('context.scene.CustomShelf.variables.%s=%s'%(key,value))

            else :
                Type = bpy.props.StringProperty

                if type(value) not in [str,list] :
                     #'Types[type(value)][%s]'%value.name

                    print(type(value))

                    setattr(CustomShelfPropSearch, key, bpy.props.CollectionProperty(type=bpy.types.PropertyGroup))

                    exec('context.scene.CustomShelf.prop_search.%s.clear()'%key)
                    for item in eval('bpy.data.%s'%self.Types[type(value)]):

                        exec('context.scene.CustomShelf.prop_search.%s.add().name = "%s"'%(key,item.name))

                    value = value.name

                elif type(value)  in [list] :
                    value = str(value)

                setattr(CustomShelfVariables, key, Type(default = value))
                exec('context.scene.CustomShelf.variables.%s="%s"'%(key,value))

        #context.scene.CustomShelfVars.a='toto'

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        for key,value in self.variables.items() :
            if type(value) not in [str,int,float,list]:
                col.prop_search(context.scene.CustomShelf.variables, key, context.scene.CustomShelf.prop_search,key,text = key)
            else :

                col.prop(context.scene.CustomShelf.variables, key, expand=True,text = key)



'''
oldPreset = {}
def read_preset():
    preset = {}

    addon_prefs = bpy.context.user_preferences.addons[__name__].preferences.presets
    presetFolder = os.path.join(os.path.dirname(__file__),'shelves')


    pyFile = os.path.join(presetFolder,addon_prefs+'.py')

    with open(pyFile,'r') as text:
        for line in text:
            key = line.split('=')[0]
            value = line.split(';')[0].split('=')[1]
            preset[key] = [v for v in value.split(',')]

    return (preset)
'''

def read_shelves() :
    path = os.path.join(os.path.dirname(__file__),'shelves')
    shelves = {}

    files = glob.glob(path+'/*/*.py')

    for f in files :
        category = os.path.basename(os.path.dirname(f))
        name = os.path.splitext(os.path.basename(f))[0]
        if not shelves.get(category):
            shelves[category] = []
        if name!='__init__' :
            shelves[category].append(name)

    return(shelves)


#Register modified header Class
class my_INFO_HT_header(bpy.types.Header):
    bl_space_type = 'INFO'
    '''
    for key,value in read_shelves().items() :
        items =[]
        for p in value:
            items.append(p)

        itemsSort =[]
        for p in sorted(items):
            exec('%s = bpy.props.BoolProperty(name="%s")'%(p,p))
            #itemsSort.append((p,p,""))
bpy.props.StringProperty()
        #exec('%s = bpy.props.EnumProperty(name="%s",items=itemsSort,description="Call function")'%(key,key))
    '''

    def draw(self, context):
        layout = self.layout

        window = context.window
        scene = context.scene
        rd = scene.render

        row = layout.row(align=True)
        row.template_header()

        INFO_MT_editor_menus.draw_collapsible(context, layout)

        if window.screen.show_fullscreen:
            layout.operator("screen.back_to_previous", icon='SCREEN_BACK', text="Back to Previous")
            layout.separator()
        else:
            layout.template_ID(context.window, "screen", new="screen.new", unlink="screen.delete")
            layout.template_ID(context.screen, "scene", new="scene.new", unlink="scene.delete")

        layout.separator()

        if rd.has_multiple_engines:
            layout.prop(rd, "engine", text="")

        layout.separator()

        layout.template_running_jobs()

        layout.template_reports_banner()

        row = layout.row(align=True)

        if bpy.app.autoexec_fail is True and bpy.app.autoexec_fail_quiet is False:
            row.label("Auto-run disabled", icon='ERROR')
            if bpy.data.is_saved:
                props = row.operator("wm.revert_mainfile", icon='SCREEN_BACK', text="Reload Trusted")
                props.use_scripts = True

            row.operator("script.autoexec_warn_clear", text="Ignore")

            # include last so text doesn't push buttons out of the header
            row.label(bpy.app.autoexec_fail_message)
            return

        row.operator("wm.splash", text="", icon='BLENDER', emboss=False)
        row.label(text='v%s.%s%s'%(bpy.app.version[0],bpy.app.version[1],bpy.app.version_char))
        row.separator()
        row.operator("CustomShelf.display_stats",icon = 'LINENUMBERS_ON',text = '',emboss=False)
        row.separator()

        for key,value in sorted(read_shelves().items()) :
            row = layout.row(align=True)
            #text =' '.join([' ' for a in range(0,len(key))])
            #row.prop(context.scene.CustomShelf,key,emboss = False,text=' ')

            row.label(key+':')
            row.scale_x = 0.7
            row.alignment = 'RIGHT'
            row = layout.row(align=True)
            for s in value :
                func = row.operator("customshelf.run_function",text='',icon = 'SCRIPTWIN')
                func.script = s
                func.folder = key

            #row.prop(context.scene.CustomShelf,'separator',emboss=False)
            subrow = row.row(align=True)
            #subrow.prop(context.scene.CustomShelf,'separator',emboss=False)
            subrow.scale_x = 0.1
            subrow.alignment = 'LEFT'

def apply_UI(register,unregister):

    if unregister == True:
        for pt in bpy.types.Header.__subclasses__():
            if pt.bl_space_type == 'INFO' :
                if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                    bpy.utils.unregister_class(pt)
                    bpy.utils.register_class(INFO_HT_header)


    if register == True :
        for pt in bpy.types.Header.__subclasses__():
            if pt.bl_space_type == 'INFO' :
                if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                    bpy.utils.unregister_class(pt)
                    bpy.utils.register_class(my_INFO_HT_header)

'''
class UiTweakPrefs(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    items =[]
    for p in read_presetList():
        items.append(p)

    itemsSort =[]
    for p in sorted(items):
        itemsSort.append((p,p,""))
launch
    presets = bpy.props.EnumProperty(name="Presets",items=itemsSort,description="Shape",update = update)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "presets")
'''

class CustomShelfPrefs(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__



    localShelf = bpy.props.StringProperty(name="Local path",subtype = 'FILE_PATH')
    globalShelf = bpy.props.StringProperty(name="Global path",subtype = 'FILE_PATH')

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "localShelf")
        layout.prop(self, "globalShelf")


@persistent
def apply_UI_handler(dummy):
    apply_UI(True,True)

class CustomShelfVariables(bpy.types.PropertyGroup) :
    pass

class CustomShelfPropSearch(bpy.types.PropertyGroup) :
    pass

class CustomShelfSettings(bpy.types.PropertyGroup) :
    statistics = bpy.props.BoolProperty(default = False,description='Display scene statistics')
    variables = bpy.props.PointerProperty(type= CustomShelfVariables)
    prop_search = bpy.props.PointerProperty(type= CustomShelfPropSearch)




def register():
    #bpy.utils.unregister_class(INFO_HT_header)
    bpy.utils.register_class(CustomShelfVariables)
    bpy.utils.register_class(CustomShelfPropSearch)
    bpy.utils.register_class(CustomShelfRunFunction)
    bpy.utils.register_class(operators.DisplayStatistics)
    bpy.utils.register_class(CustomShelfPrefs)
    bpy.utils.register_class(CustomShelfSettings)


    bpy.types.Scene.CustomShelf = bpy.props.PointerProperty(type= CustomShelfSettings)
    #bpy.types.Scene.CustomShelfVars = bpy.props.PointerProperty(type= CustomShelfVariables)

    try :
        apply_UI(True,True)
    except :
        pass

    bpy.app.handlers.load_post.append(apply_UI_handler)



def unregister():
    del bpy.types.Scene.CustomShelf
    #del bpy.types.Scene.CustomShelfVars
    apply_UI(False,True)

    bpy.utils.unregister_class(CustomShelfVariables)
    bpy.utils.unregister_class(CustomShelfPropSearch)
    bpy.utils.unregister_class(CustomShelfPrefs)
    bpy.utils.unregister_class(CustomShelfSettings)
    bpy.utils.unregister_class(operators.DisplayStatistics)
    bpy.utils.unregister_class(CustomShelfRunFunction)
    bpy.app.handlers.load_post.remove(apply_UI_handler)
