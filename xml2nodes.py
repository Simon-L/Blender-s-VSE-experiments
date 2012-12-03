import bpy
import xml.etree.ElementTree as ET

tree = ET.parse('xmlol7.xml')
root = tree.getroot()

mix = False

# Pick a strip to reconstruct
stripName = "6397.001"
# Retrieve corresponding XML element
movieSequences = root.findall('./scenes/Scene/sequence_editor/SequenceEditor/sequences_all/MovieSequence')
for movieStrip in movieSequences :  
    if movieStrip.get('name') == stripName :
# xmlMovieSequence is the result
        xmlMovieSequence = movieStrip
        break
        
# Retrieve possible FCurves associated to the strip
fcurves = []
for fcurve in root.findall(".//FCurve") :
    
    if fcurve.attrib['data_path'].startswith('sequence_editor.sequences_all["' + xmlMovieSequence.attrib['name'] + '"]'):
        fcurves.append(fcurve)

# Create an Image datablock to use for the Image node (Convenience variable)
image_block = bpy.data.images.load(xmlMovieSequence.get('filepath'))

# Create Image node
image = bpy.context.scene.node_tree.nodes.new('IMAGE')
image.image = image_block # Sets the image datablock as Image element
image.frame_duration = int(xmlMovieSequence.get('frame_final_duration')) # Copy parameters from xml to node
image.frame_offset = int(xmlMovieSequence.get('frame_offset_start')) # idem
#~ image.frame_start = int(xmlMovieSequence.attrib['frame_final_start']) # idem
image_out_socket = image.outputs['Image'] # Convenience

# Add keyframes
for fcurve in fcurves :
    #~ print("inside the for fcurve")
    if fcurve.attrib['data_path'].endswith('.blend_alpha') : # If opacity fcurve
        #~ print("if fcurve.attrib")
        mix = True
        mixNode = bpy.context.scene.node_tree.nodes.new('MIX_RGB') # Add Mix node
        mixNode.location = ( 300 , 0 ) # Set location on Comp canevas
        mixNode_output = mixNode.outputs['Image']
        mixNode_inputs = mixNode.inputs
        mixNode_inputs[1].default_value = (0,0,0,1) # Sets input to Black
        bpy.data.actions.new('SceneAction')
        bpy_fcurve = bpy.data.actions['SceneAction'].fcurves.new('mixNode.inputs[0].default_value')
        start_frame = int(xmlMovieSequence.attrib['frame_final_start'])
        print(start_frame)
        for keyframe in fcurve.findall('./keyframe_points/Keyframe') : 
            #~ print(keyframe)
            print('avant bla !')
            frame = int(keyframe.get('co').split()[0])
            print('bla')
            if frame >= start_frame : # Offsets accordingly to relocate around 0
                bpy_keyframe = bpy_fcurve.keyframe_points.insert(frame - start_frame,int(keyframe.get('co').split()[1]))
            else :
                bpy_keyframe = bpy_fcurve.keyframe_points.insert(start_frame - frame,int(keyframe.get('co').split()[1]))                
            bpy_keyframe.handle_left = (float(keyframe.get('handle_left').split()[0]),float(keyframe.get('handle_left').split()[1])) # Sets parameters according to XML
            bpy_keyframe.handle_right = (float(keyframe.get('handle_right').split()[0]),float(keyframe.get('handle_right').split()[1]))
            bpy_keyframe.handle_left_type = keyframe.get('handle_left_type')
            bpy_keyframe.handle_right_type = keyframe.get('handle_right_type')
            bpy_keyframe.interpolation = keyframe.get('interpolation')            
            
# Create Viewer node
viewer = bpy.context.scene.node_tree.nodes.new('VIEWER')
viewer.location = ( 600 , 0 ) # Set location on Comp canevas
viewer_in_socket = viewer.inputs['Image'] # idem

# Links sockets
if mix :
    bpy.context.scene.node_tree.links.new(image_out_socket, mixNode_inputs[2]) # Link Image to Mix
    bpy.context.scene.node_tree.links.new(mixNode_output, viewer_in_socket) # Link Mix to Viewer
    
else :

    bpy.context.scene.node_tree.links.new(image_out_socket, viewer_in_socket) # Linking
    
