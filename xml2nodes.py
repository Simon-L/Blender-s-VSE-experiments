import bpy
import xml.etree.ElementTree as ET

tree = ET.parse('xmlol7.xml')
root = tree.getroot()

# Pick a strip to reconstruct
stripName = "6397.001"
# Retrieve corresponding XML element
movieSequences = root.findall('./scenes/Scene/sequence_editor/SequenceEditor/sequences_all/MovieSequence')
for movieStrip in movieSequences :  
    if movieStrip.attrib['name'] == stripName :
# xmlMovieSequence is the result
        xmlMovieSequence = movieStrip
        break
        
# Retrieve possible FCurves associated to the strip
fcurves = []
for fcurve in root.findall(".//FCurve") :
    
    if fcurve.attrib['data_path'].startswith('sequence_editor.sequences_all["' + xmlMovieSequence.attrib['name'] + '"]'):
        fcurves.append(fcurve)

# Create an Image datablock to use for the Image node (Convenience variable)
image_block = bpy.data.images.load(xmlMovieSequence.attrib['filepath'])

# Create Image node
image = bpy.context.scene.node_tree.nodes.new('IMAGE')
image.image = image_block # Sets the image datablock as Image element
image.frame_duration = int(xmlMovieSequence.attrib['frame_final_duration']) # Copy parameters from xml to node
image.frame_offset = int(xmlMovieSequence.attrib['frame_offset_start']) # idem
#~ image.frame_start = int(xmlMovieSequence.attrib['frame_final_start']) # idem

# Create Viewer node
viewer = bpy.context.scene.node_tree.nodes.new('VIEWER')
viewer.location = ( 600 , 0 ) # Set location on Comp canevas

# Links sockets
image_out_socket = image.outputs['Image'] # Convenience
viewer_in_socket = viewer.inputs['Image'] # idem
bpy.context.scene.node_tree.links.new(image_out_socket, viewer_in_socket) # Linking
