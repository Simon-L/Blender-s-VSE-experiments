import bpy
import re

class XmlPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "BXML Options"
    bl_idname = "FILEBROWSER_PT_xml"
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'CHANNELS'

    def draw(self, context):
        filename = bpy.context.screen.areas[5].spaces[0].params.filename
        
        if filename.endswith('.xml') :
            
            self.layout.label(text=filename, icon='FILE' )
            try :
                filehandle = open(bpy.context.screen.areas[5].spaces[0].params.directory + filename)
                filehandle.readline()
                filehandle.readline()
                a = filehandle.readline()
                #~ print("ligne : ",a)
                self.layout.label(text="Containing : " + re.findall(r'[^"]+/(.+\.blend)"',a)[0])
                #~ print("result : ", re.findall(r'[^"]+/(.+\.blend)"',a))
            except :
                print("lol")
            
            row = self.layout.row(align=True)
            row.alignment = 'EXPAND'
            row.operator("xml.mode", text="Whole Blend file")
            row.operator("xml.mode", text="Filter import")
            
            #~ self.layout.label(text="")
            
            row = self.layout.row(align=True)
            row.operator("xml.import", text="IMPORT")
            
        else :
            self.layout.label(text="Please select a BXML file", icon='ERROR' )

            
class OBJECT_OT_XmlModeButton(bpy.types.Operator):
    bl_idname = "xml.mode"
    bl_label = "XML Mode"
 
    def execute(self, context):
        
        print("Hello world!")
        
        return{'FINISHED'} 
        
        
class OBJECT_OT_XmlImportButton(bpy.types.Operator):
    bl_idname = "xml.import"
    bl_label = "XML Import"
 
    def execute(self, context):
        
        print("Hello world! 2")
        
        return{'FINISHED'}
            
bpy.utils.register_class(XmlPanel)
bpy.utils.register_class(OBJECT_OT_XmlModeButton)
bpy.utils.register_class(OBJECT_OT_XmlImportButton)
