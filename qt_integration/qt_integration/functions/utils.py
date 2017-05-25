import os

def icon_path(image) :
    working_dir = os.path.abspath(os.path.dirname('__FILE__'))
    real_path = os.path.join(working_dir,'resource','icons',image+'.png')

    return real_path.replace('\\','/')

def get_css(css) :
    working_dir = os.path.abspath(os.path.dirname('__FILE__'))
    real_path = os.path.join(working_dir,'resource','css',css+'.css')

    icon_folder = os.path.join(working_dir,'resource','icons').replace('\\','/')

    css_to_string =  open(real_path).read().replace('RESOURCE',icon_folder)


    return css_to_string

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clear_layout(child.layout())
