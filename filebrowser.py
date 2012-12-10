import bpy
import re
import xml.etree.ElementTree as ET

#############
#  Refaire la routine en checkant
#  ligne 2.startswith() == "<!-- BXML - Blender XML interchange format" avant de faire quoique ce soit
#  Enum en boutons switch == win !



bpy.types.Scene.XmlModeEnum = bpy.props.EnumProperty( \
                                                            items = [('whole', 'Whole file', 'Imports whole file'),\
                                                ('filter', 'Filter import', 'Filter scenes and strips to import')],\
                                                name = 'Mode', default = 'whole')


class XmlPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "BXML Import options"
    bl_idname = "FILEBROWSER_PT_xml"
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'CHANNELS'

    def draw(self, context):
        filename = context.screen.areas[5].spaces[0].params.filename
        
        if filename.endswith('.xml') :
            
            self.layout.label(text=filename, icon='FILE' )
            #~ try :
                #~ filehandle = open(context.screen.areas[5].spaces[0].params.directory + filename)
                #~ filehandle.readline()
                #~ filehandle.readline()
                #~ a = filehandle.readline()
                #~ self.layout.label(text="Containing : " + re.findall(r'[^"]+/(.+\.blend)"',a)[0])
            #~ except :
                #~ print("lol")
            
            row = self.layout.row(align=True)
            row.alignment = 'EXPAND'
            #~ row.operator("xml.mode", text="Whole Blend file")
            #~ row.operator("xml.mode", text="Filter import")
            self.layout.row().prop(context.scene,'XmlModeEnum', expand=True)
            
            if context.scene.XmlModeEnum == 'filter':
                
                row = self.layout.row()
                box = row.box()
                
                try :
                    root = ET.parse(context.screen.areas[5].spaces[0].params.directory + filename).getroot()
                    scenes = root.findall('./scenes//Scene')
                    #~ if len(scenes) == 0 :
                        #~ box.separator()
                        
                    for scene in scenes :
                        box.label(text=scene.get('name'))
                except :
                    box.label('')
                
            else :
                self.layout.separator()
             
            row = self.layout.row(align=True)
            row.operator("xml.import", text="IMPORT")
             
        else :
            self.layout.label(text="Please select a BXML file", icon='ERROR' )

            
class OBJECT_OT_XmlModeButton(bpy.types.Operator):
    bl_idname = "xml.mode"
    bl_label = "XML Mode"
 
    def execute(self, context):
        
        print("Xml mode button clicked")
        
        return{'FINISHED'} 
        
        
class OBJECT_OT_XmlImportButton(bpy.types.Operator):
    bl_idname = "xml.import"
    bl_label = "XML Import"
 
    def execute(self, context):
        
        print("Import button clicked ")
        print("Import mode = ", context.scene.XmlModeEnum)
        
        return{'FINISHED'}
            
bpy.utils.register_class(XmlPanel)
bpy.utils.register_class(OBJECT_OT_XmlModeButton)
bpy.utils.register_class(OBJECT_OT_XmlImportButton)
print('lol')
