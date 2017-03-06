bl_info = {
    "name": "Custom Shelf",
    "author": "Christophe Seux",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "category": "User"}

from . import operators
from . import UI

import bpy
import os
from bpy.app.handlers import persistent


class CustomShelfRunFunction(bpy.types.Operator):
    bl_idname = "customshelf.run_function"
    bl_label = "Run Function"

    script = bpy.props.StringProperty()
    folder = bpy.props.StringProperty()

    def execute(self,context) :
        print(self.folder,self.script)
        #addon_prefs = bpy.context.user_preferences.addons[__name__].preferences.presets
        global_shelves = os.path.join(os.path.dirname(__file__),'shelves')
        pyFile = os.path.join(global_shelves,self.folder,self.script+'.py')



        variables= {}
        def local() :
            exec(open(pyFile).read(), globals())

            print(globals)
            #print (variables) # globals from the someFile module
        local()
        return {'FINISHED'}

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
    Folder = os.path.join(os.path.dirname(__file__),'shelves')
    shelves = {}
    for s in os.listdir(Folder) :
        shelves[s] = [os.path.splitext(p)[0] for p in os.listdir(os.path.join(Folder,s))]


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

        UI.INFO_MT_editor_menus.draw_collapsible(context, layout)

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

        for key,value in read_shelves().items() :
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
                    bpy.utils.register_class(UI.INFO_HT_header)


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

class CustomShelfSettings(bpy.types.PropertyGroup) :
    statistics = bpy.props.BoolProperty(default = False,description='Display scene statistics')
    for key,value in read_shelves().items() :
        items =[]
        for p in value:
            items.append(p)
        separator = bpy.props.StringProperty(name='',default="|")
        itemsSort =[]
        for p in sorted(items):
            exec('%s = bpy.props.BoolProperty(name="%s")'%(p,p))



def register():
    #bpy.utils.unregister_class(INFO_HT_header)
    bpy.utils.register_class(CustomShelfRunFunction)
    bpy.utils.register_class(operators.DisplayStatistics)
    bpy.utils.register_class(CustomShelfPrefs)
    bpy.utils.register_class(CustomShelfSettings)


    bpy.types.Scene.CustomShelf = bpy.props.PointerProperty(type= CustomShelfSettings)

    try :
        apply_UI(True,True)
    except :
        pass

    bpy.app.handlers.load_post.append(apply_UI_handler)



def unregister():
    del bpy.types.Scene.CustomShelf
    apply_UI(False,True)
    bpy.utils.unregister_class(CustomShelfPrefs)
    bpy.utils.unregister_class(CustomShelfSettings)
    bpy.utils.unregister_class(operators.DisplayStatistics)
    #bpy.utils.unregister_class(my_INFO_HT_header)
    bpy.app.handlers.load_post.remove(apply_UI_handler)
