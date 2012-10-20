import bpy, rna_xml

filehandle = open('xmlol2.xml', 'w')
fw = filehandle.write

rna_xml.rna2xml(fw, root_rna=bpy.data.scenes[0].sequence_editor)

filehandle.close()
