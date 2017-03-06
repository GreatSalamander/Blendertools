import bpy
import blf
import bgl

def draw_stats(self,context) :
    font_size = 12
    if context.scene.CustomShelf.statistics :
        width = context.region.width
        height = context.region.height

        stat = context.scene.statistics().split('|')
        stat[0]= stat[-1]
        stat.pop(-1)

        blf.enable(1,blf.SHADOW)
        space=0
        for index,s in enumerate(stat) :

            text = s.split(':')
            font_id = 1
            blf.size(font_id, font_size, 72)
            if len(text)>1:
                #bgl.glColor3f(.13,.55,.31)
                #bgl.glColor3f(.5,.7,.8)
                bgl.glColor4f(1,.667,.251,1)

            else :
                bgl.glColor4f(.9,.9,.9,1)

            Dimension = blf.dimensions(font_id, context.scene.statistics())
            dimension = blf.dimensions(font_id, text[0])

            #blf.position(1, (width - dimension[0]-10), (height-dimension[1]-4), 0)
            blf.position(font_id, (width/2-Dimension[0]/2+space), (height-font_size-2), 0)
            if len(text)>1:
                typo = text[0]+':'
            else :
                typo = text[0]

            blf.shadow(font_id, 3, 0, 0, 0, .6)
            blf.draw(font_id,typo)
            space+= dimension[0]+10

            if len(text)>1:
                bgl.glColor4f(.8,.8,.8,1)
                dimension = blf.dimensions(font_id, text[1])
                #blf.position(1, (width - dimension[0]-10), (height-dimension[1]-4), 0)
                blf.position(font_id, (width/2-Dimension[0]/2+space), (height-font_size-2), 0)
                blf.shadow(font_id, 3, 0, 0, 0, .6)
                blf.draw(font_id, text[1])
                space+= dimension[0]

    blf.disable(1,blf.SHADOW)

class DisplayStatistics(bpy.types.Operator):
    bl_idname = "customshelf.display_stats"
    bl_label = "Display Statistics"

    _handle = None

    def modal(self, context, event):

        context.area.tag_redraw()
        if not context.scene.CustomShelf.statistics :
            try :
                bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            except :
                pass

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.scene.CustomShelf.statistics = not context.scene.CustomShelf.statistics


        args = (self, context)
        #if self.stat == True :
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_stats, args, 'WINDOW', 'POST_PIXEL')


        context.window.cursor_modal_set('DEFAULT')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
