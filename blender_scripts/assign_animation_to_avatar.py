"""
# Blender Version 2.91.2 (2.91.2 2021-01-19)

# What does this script do?
The script maps the bone rotations of the interpreter avatar's armature to the bone rotations of the BVH file armature.

# How to use this script?
Make a copy of "animate_avatar.blend" and give the new .blend file a name that fits to the desired animation, e.g. the name of the BVH file.
Open the .blend file and import the BVH file to be mapped. Now a new armature should appear in the scene collection. 
Duplicate that armature with copy paste.

Now go to the scripting tab in Blender and open this script if it is not already there or reload it with "Text > Reload". 
Run the script and wait for the result. Go to the animation tab and press the play button to see it.

The result can be baked as an animation. To do this, switch to "Object Mode" and choose "Genesis8Female" in the scene collection. 
Then go to "Object > Animation > Bake Action". Set the start frame to 0 and check the correct end frame in the animation Tab. 
Unselect "Only Selected Bones" and select "Visual Keying", "Clear Constraints" and "Clear Parents". Set "Bake Data" to "Pose".

Delete the two BVH armatures. If the avatar does not change its pose, the baking was successful.
"""

import bpy


########## Variable declarations ##########

## Name of imported BVH and its copy
arm_title = "Arbeitsunfähigkeitsbescheinigung" # x-axis will be rotated to -210d
arm_title_head = "Arbeitsunfähigkeitsbescheinigung.001" # x-axis will be rotated to -180d to map the neck and head bones

## Bone Mapping

# mapping_list = [ (0:MEDIA_PIPE_BONE, 1:DAZ_BONE), ...]

neck_bone_mapping = [
    ("NECK","abdomenLower"),
    ("NECK","abdomenUpper"),
    ("NECK","chestLower"),
    ("NECK","chestUpper"),
    ("NECK","neckUpper"),
    ("NECK","neckLower"),
    ("HEAD", "head")
]

collar_bones_mapping = [
    ("RIGHT_SHOULDER", "lCollar"),
    ("LEFT_SHOULDER", "rCollar")
]

pose_bones_mapping = [
    ("LEFT_ELBOW", "lShldrBend"),
    ("LEFT_WRIST", "lForearmBend"),
    ("RIGHT_ELBOW", "rShldrBend"),
    ("RIGHT_WRIST", "rForearmBend"),

    ("RIGHT_INDEX", "rHand"),
    ("LEFT_INDEX", "lHand")
]

lhand_bones_mapping = [
    ("LTHUMB_MCP", "lThumb1"),
    ("LTHUMB_IP", "lThumb2"),
    ("LTHUMB_TIP", "lThumb3"),

    ("LINDEX_FINGER_MCP", "lCarpal1"),
    ("LINDEX_FINGER_PIP", "lIndex1"),
    ("LINDEX_FINGER_DIP",  "lIndex2"),
    ("LINDEX_FINGER_TIP", "lIndex3"),
    
    ("LMIDDLE_FINGER_MCP", "lCarpal2"),
    ("LMIDDLE_FINGER_PIP", "lMid1"),
    ("LMIDDLE_FINGER_DIP", "lMid2"),
    ("LMIDDLE_FINGER_TIP", "lMid3"),
      
    ("LRING_FINGER_MCP", "lCarpal3"),
    ("LRING_FINGER_PIP", "lRing1"),
    ("LRING_FINGER_DIP", "lRing2"),
    ("LRING_FINGER_TIP", "lRing3"),
      
    ("LPINKY_MCP", "lCarpal4"),
    ("LPINKY_PIP", "lPinky1"),
    ("LPINKY_DIP", "lPinky2"),
    ("LPINKY_TIP", "lPinky3")
]

rhand_bones_mapping = [
    ("RTHUMB_MCP", "rThumb1"),
    ("RTHUMB_IP", "rThumb2"),
    ("RTHUMB_TIP", "rThumb3"),

    ("RINDEX_FINGER_MCP", "rCarpal1"),
    ("RINDEX_FINGER_PIP", "rIndex1"),
    ("RINDEX_FINGER_DIP",  "rIndex2"),
    ("RINDEX_FINGER_TIP", "rIndex3"),
    
    ("RMIDDLE_FINGER_MCP", "rCarpal2"),
    ("RMIDDLE_FINGER_PIP", "rMid1"),
    ("RMIDDLE_FINGER_DIP", "rMid2"),
    ("RMIDDLE_FINGER_TIP", "rMid3"),
      
    ("RRING_FINGER_MCP", "rCarpal3"),
    ("RRING_FINGER_PIP", "rRing1"),
    ("RRING_FINGER_DIP", "rRing2"),
    ("RRING_FINGER_TIP", "rRing3"),
      
    ("RPINKY_MCP", "rCarpal4"),
    ("RPINKY_PIP", "rPinky1"),
    ("RPINKY_DIP", "rPinky2"),
    ("RPINKY_TIP", "rPinky3")
]

"""
face_bones_mapping = [
    ## 90d bones
    # right eyebrow inner
    ("107", "rBrowInner"), 
    # right eyebrow middle
    ("105", "rBrowMid"), 
    # right eyebrow outer
    ("70", "rBrowOuter"),
    # left eyebrow inner
    ("336",  "lBrowInner"), 
    # left eyebrow middle
    ("334", "lBrowMid"), 
    # left eyebrow outer
    ("300", "lBrowOuter"),        
    # center brow
    ("9", "CenterBrow"),
    # mid nose bridge
    ("6", "MidNoseBridge"),
    # nose
    ("4", "Nose"),
    # right nostril
    ("218", "rNostril"),
    # left nostril
    ("438", "lNostril"),
    # right nasolabial middle
    ("36", "rNasolabialMiddle"),
    # left nasolabial middle
    ("266", "lNasolabialMiddle"),
    # right nasolabial upper
    ("47", "rNasolabialUpper"),
    # left nasolabial upper
    ("277", "lNasolabialUpper"),
    # right nasolabial lower
    ("202", "rNasolabialLower"),
    # left nasolabial lower
    ("422", "lNasolabialLower"),
    # right squint inner
    ("22", "rSquintInner"),
    # left squint inner
    ("252", "lSquintInner"),
    # right squint outer
    ("110", "rSquintOuter"),
    # left squint outer
    ("339", "lSquintOuter"),
    # right cheek upper
    ("117", "rCheekUpper"),
    # right cheek lower
    ("187", "rCheekLower"),
    # left cheek upper
    ("346", "lCheekUpper"),
    # left cheek lower
    ("411", "lCheekLower"),
    # right lip below nose
    ("167", "rLipBelowNose"),
    # left lip below nose
    ("393", "lLipBelowNose"),
    # right nasolabial crease
    ("92", "rLipNasolabialCrease"),
    # left nasolabial crease
    ("322", "lLipNasolabialCrease"),
    # right nasolabial mouth corner
    ("216", "rNasolabialMouthCorner"),
    # left nasolabial mouth corner
    ("436", "lNasolabialMouthCorner"),
    # right lip corner
    ("57", "rLipCorner"),
    # left lip corner
    ("287", "lLipCorner"),
    # lip upper middle
    ("0", "LipUpperMiddle"),
    # lip lower middle
    ("17", "LipLowerMiddle"),
    # right lip upper inner
    ("39", "rLipUpperInner"),
    # left lip upper inner
    ("269", "lLipUpperInner"),
    # right lip upper outer
    ("40", "rLipUpperOuter"),
    # left lip upper outer
    ("270", "lLipUpperOuter"),
    # right lip lower outer
    ("321", "rLipLowerOuter"),
    # left lip lower outer
    ("91", "lLipLowerOuter"),
    # right lip lower inner
    ("84", "rLipLowerInner"),
    # left lip lower inner
    ("314", "lLipLowerInner"),
    # lip below
    ("18", "LipBelow"),
    # chin
    ("175", "Chin"),
    # below jaw
    ("152", "BelowJaw"),
    # right jaw clench
    ("177", "rJawClench"),
    # left jaw clench
    ("401", "lJawClench"),

    ## eyelids
    ("133", "rEyelidInner"), # right eyelid inner
    ("33", "rEyelidOuter"),  # right eyelid outer
    ("159", "rEyelidUpper"), # right eyelid upper
    ("160", "rEyelidUpperOuter"), # right eyelid upper outer
    ("158", "rEyelidUpperInner"), # right eyelid upper inner
    ("144", "rEyelidLowerOuter"), # right eyelid lower outer
    ("153", "rEyelidLowerInner"), # right eyelid lower inner
    ("145", "rEyelidLower"), # right eyelid lower

    ("362", "lEyelidInner"), # left eyelid inner
    ("263", "lEyelidOuter"), # left eyelid outer
    ("386", "lEyelidUpper"), # left eyelid upper
    ("387", "lEyelidUpperOuter"), # left eyelid upper outer
    ("385", "lEyelidUpperInner"), # left eyelid upper inner
    ("373", "lEyelidLowerOuter"), # left eyelid lower outer
    ("380", "lEyelidLowerInner"), # left eyelid lower inner
    ("374", "lEyelidLower"),  # left eyelid lower
]
"""

########## Method definitions ##########

def rotate_bvh_armatures(at="", ath=""):
    bpy.data.objects[at].rotation_euler[0] = -3.66519 # -210d
    bpy.data.objects[ath].rotation_euler[0] = -3.14159 # -180d


def map_bones(mapping_list = [], armature_title = "", invert_all = False, use_y = True):
    for m in mapping_list:
        # set constraint 'COPY_ROTATION'
        bone_const_cr = bpy.data.objects['Genesis8Female'].pose.bones[m[1]].constraints.new('COPY_ROTATION')
        bone_const_cr.target = bpy.data.objects[armature_title]
        bone_const_cr.subtarget = m[0]
        set_invert_xyz(bone_const_cr, invert_all)
        bone_const_cr.use_y = use_y
        
        if 'ForearmBend' in m[1] or 'neckUpper' in m[1]:
            bone_const_cr.influence = 0.95
        if invert_all: # we know, this is only set true for collar bones
            bone_const_cr.influence = 0.0
            
def set_invert_xyz(const, invert = False):
    const.invert_x = invert
    const.invert_y = invert
    const.invert_z = invert
            

########## Execute methods ##########

## Rotate armatures 
rotate_bvh_armatures(at=arm_title, ath=arm_title_head)

## Map Pose Bones
map_bones(mapping_list=pose_bones_mapping, armature_title=arm_title)

## Map Hand Bones
# Left
map_bones(mapping_list=lhand_bones_mapping, armature_title=arm_title)
# Right
map_bones(mapping_list=rhand_bones_mapping, armature_title=arm_title)

## Map Neck Bones
map_bones(mapping_list=neck_bone_mapping, armature_title=arm_title_head, use_y = False)

## Map Collar Bones
map_bones(mapping_list=collar_bones_mapping, armature_title=arm_title, invert_all = True)

## Map Face Bones 
# caution: will create creepy deformations. a different mapping method is needed
# map_bones(mapping_list=face_bones_mapping, armature_title=arm_title_head)
