# Script to load and run from Blender

import bpy, rna_xml, prep_rna
import xml.dom.minidom as minidom

# Ensure a sequence_editor object is present (this object is created only when a first strip is added to the sequencer)
if not bpy.data.scenes[0].sequence_editor :
		bpy.data.scenes[0].sequence_editor_create()

# Parsing
fhandle = open("xmlol2.xml", 'r')
xmldoc = minidom.parse(fhandle)
fhandle.close()


# Ensure the root node of the provided XML file is of type SequencerEditor
sequence_editorNode = xmldoc.documentElement	
if sequence_editorNode.nodeName != 'SequenceEditor' :
	raise Exception('Incorrect root node type')

# prep_rna("node element with name SequenceEditor", "scene to add to", "frame to add at")
prep_rna.prep_rna(sequence_editorNode)

# xml2rna
rna_xml.xml2rna(sequence_editorNode, bpy.data.scenes[0].sequence_editor)
