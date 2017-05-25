import bpy

class SEQUENCER_QT_INTEGRATION(bpy.types.Panel):
    bl_label = 'Qt'
    bl_category = "XILAM"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        window_btn = layout.operator('qt_window.event_loop')
