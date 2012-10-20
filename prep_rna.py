# Python module -- adds the required elements to the collections in RNA to avoid "Size mismatch!" error from rna_xml.xml2rna()

import bpy
import xml.dom.minidom as minidom

def prep_rna(root_xmlnode, # must be XML node with name SequenceEditor
              toScene = bpy.data.scenes[0], # scene index to add to, defaults first scene created
              toFrame = 1 # frame number to add to
              ):
    for xml_seq in root_xmlnode.getElementsByTagName('sequences').item(0).childNodes : # List of child nodes from the first (item(0)) and only 'sequences' node in the document
        
        # TODO: change to xml.ElementTree, this if is needed because DOM reads \n and whitespaces as Text nodes
        if xml_seq.nodeType == 3 : # type 3 is Text
            
            print("Ignoring Text node")
            pass
            
        if xml_seq.nodeName == 'MovieSequence' :
            
            print("MovieSequence", xml_seq.nodeType)
            # Retrieves values from XML (and converts to int when needed) for the required params of new_movie
            seq_name = xml_seq.getAttribute('name')
            seq_filepath = xml_seq.getAttribute('filepath')
            seq_channel = int(xml_seq.getAttribute('channel'))
            seq_start_frame = int(xml_seq.getAttribute('frame_start'))
            # Add it to the scene :
            toScene.sequence_editor.sequences.new_movie(seq_name, seq_filepath, seq_channel, seq_start_frame)
            del seq_name, seq_filepath, seq_channel, seq_start_frame # Clean up
            # Remove read-only attributes
            xml_seq.removeAttribute('frame_duration')
            xml_seq.removeAttribute('frame_offset_end')
            xml_seq.removeAttribute('frame_offset_start')
            xml_seq.removeAttribute('frame_still_end')
            xml_seq.removeAttribute('frame_still_start')
            #~ xml_seq.removeAttribute('modifiers')
            xml_seq.removeAttribute('type')
            xml_seq.removeAttribute('crop')
            xml_seq.removeAttribute('transform')
            xml_seq.removeAttribute('proxy')
            #~ xml_seq.removeAttribute('')
            
        if xml_seq.nodeName == 'SoundSequence' :
            
            print("SoundSequence", xml_seq.nodeType)
            # Retrieves values from XML (and converts to int when needed) for the required params of new_sound
            seq_name = xml_seq.getAttribute('name')
            seq_filepath = xml_seq.getAttribute('filepath')
            seq_channel = int(xml_seq.getAttribute('channel'))
            seq_start_frame = int(xml_seq.getAttribute('frame_start'))
            # Add it to the scene :
            toScene.sequence_editor.sequences.new_sound(seq_name, seq_filepath, seq_channel, seq_start_frame)
            del seq_name, seq_filepath, seq_channel, seq_start_frame # Clean up
            xml_seq.removeAttribute('frame_duration')   
            xml_seq.removeAttribute('frame_offset_end')   
            xml_seq.removeAttribute('frame_offset_start')   
            xml_seq.removeAttribute('frame_still_end')
            xml_seq.removeAttribute('frame_still_start')
            #~ xml_seq.removeAttribute('modifiers')
            xml_seq.removeAttribute('type')
            #~ xml_seq.removeAttribute('')
            #~ xml_seq.removeAttribute('')
            
