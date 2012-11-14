import bpy, rna_xml, random
import xml.etree.ElementTree as ET

tempfilename = '.rna2xmltemp_' + str(hex(random.randrange(5000)))[2:] + '.xml'
filehandle = open(tempfilename, 'w')

root_rna = bpy.data
fw = filehandle.write
rna_xml.rna2xml(fw, root_rna=root_rna, skip_classes=(bpy.types.WindowManager,
													bpy.types.Operator,
													bpy.types.Panel,
													bpy.types.KeyingSet,
													bpy.types.Header,
													bpy.types.Screen,
													bpy.types.Texture,
													bpy.types.Armature,
													bpy.types.Brush,
													bpy.types.Camera,
													bpy.types.VectorFont,
													bpy.types.GreasePencil,
													bpy.types.Lamp,
													bpy.types.Material,
													bpy.types.Mesh,
													bpy.types.Object,
													bpy.types.ParticleSettings,
													bpy.types.Speaker),
													method = 'ATTR')
filehandle.close()

skipdata = [ 'cameras', 'objects', 'materials', 'meshes', \
        'lamps', 'screens', 'window_managers','lattices', \
         'metaballs', 'fonts', 'textures', 'brushes', 'shape_keys',\
          'scripts', 'texts', 'speakers', 'sounds', 'armatures', 'particles','grease_pencil', 'worlds']
skipscenesdata = [ 'tool_settings', 'unit_settings', 'render', 'game_settings',\
                    'view_settings', 'display_settings', 'cycles', 'object_bases', 'objects', 'orientations' ]
                    
tree = ET.parse(tempfilename)
root = tree.getroot()                    
for skipped in skipdata :   
    root.remove(root.find(skipped)) 
    
sceneslist = root.findall('scenes/Scene')
for scene in sceneslist :                   
    for skipped in skipscenesdata : 
        scene.remove(scene.find(skipped))

images = root.find('images')
for image in images :	
	del image.attrib['pixels']

allxmlout = ET.tostring(root, encoding="unicode")

outputfilename = 'xmlol5.xml'
outhandle = open(outputfilename, 'w')

outhandle.write(str("<!-- BXML - Blender XML interchange format\nBlender version " + bpy.app.version_string + "\n-->\n<?xml version=\"1.0\"?>\n"))
outhandle.write(allxmlout)
outhandle.close()



