"""
# Blender Version 2.91.2 (2.91.2 2021-01-19)

# What does this script do?
The script runs the MediaPipe motion tracking AI on the specified video file and creates bones that move and rotate based on the tracked landmarks.

# How to use this script?
Open "make_bvh_files.blend". Now go to the scripting tab in Blender and open this script if it is not already there or reload it with "Text > Reload". 
Run the script and wait for the result. Go to the animation tab and press the play button to see it.

The result can be exported as a BVH file via "File > Export > Motion Capture (.bvh)".
To make a new BVH file, delete all items in the Scene Collection, change video_file_name and video_file_path and rerun the script.
"""

import bpy, cv2, pathlib
import mediapipe as mp


########## Variables ##########

## Video file name and path to be processed
video_file_name = 'Brauchen Sie eine Arbeitsunfähigkeitsbescheinigung II.mov'
video_file_path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/sign_videos/' + video_file_name

## Landmark arrays
pose_landmarks = []
left_hand_landmarks = []
right_hand_landmarks = []
face_landmarks = []

## Landmark names
pose_landmark_names = [
  "NOSE",
  "LEFT_EYE_INNER",
  "LEFT_EYE",
  "LEFT_EYE_OUTER",
  "RIGHT_EYE_INNER",
  "RIGHT_EYE",
  "RIGHT_EYE_OUTER",
  "LEFT_EAR",
  "RIGHT_EAR",
  "MOUTH_LEFT",
  "MOUTH_RIGHT",
  "LEFT_SHOULDER",
  "RIGHT_SHOULDER",
  "LEFT_ELBOW",
  "RIGHT_ELBOW",
  "LEFT_WRIST",
  "RIGHT_WRIST",
  "LEFT_PINKY",
  "RIGHT_PINKY",
  "LEFT_INDEX",
  "RIGHT_INDEX",
  "LEFT_THUMB",
  "RIGHT_THUMB",
  "LEFT_HIP",
  "RIGHT_HIP",
  "LEFT_KNEE",
  "RIGHT_KNEE",
  "LEFT_ANKLE",
  "RIGHT_ANKLE",
  "LEFT_HEEL",
  "RIGHT_HEEL",
  "LEFT_FOOT_INDEX",
  "RIGHT_FOOT_INDEX"
]

hand_landmark_names = [
  "WRIST",
  "THUMB_CMC",
  "THUMB_MCP",
  "THUMB_IP",
  "THUMB_TIP",
  "INDEX_FINGER_MCP",
  "INDEX_FINGER_PIP",
  "INDEX_FINGER_DIP",
  "INDEX_FINGER_TIP",
  "MIDDLE_FINGER_MCP",
  "MIDDLE_FINGER_PIP",
  "MIDDLE_FINGER_DIP",
  "MIDDLE_FINGER_TIP",
  "RING_FINGER_MCP",
  "RING_FINGER_PIP",
  "RING_FINGER_DIP",
  "RING_FINGER_TIP",
  "PINKY_MCP",
  "PINKY_PIP",
  "PINKY_DIP",
  "PINKY_TIP"
]

## Landmark connections (create bones out of two landmarks)
pose_landmark_connections = [
  ("LEFT_SHOULDER", "LEFT_ELBOW"),
  ("LEFT_ELBOW", "LEFT_WRIST"),
  ("RIGHT_SHOULDER", "RIGHT_ELBOW"),
  ("RIGHT_ELBOW", "RIGHT_WRIST"),

  ("RIGHT_WRIST", "RIGHT_INDEX"), # hand bone right
  ("LEFT_WRIST", "LEFT_INDEX"), # hand bone left
  
  ("LEFT_SHOULDER", "RIGHT_SHOULDER"), # for left collar (invert all axes)
  ("RIGHT_SHOULDER", "LEFT_SHOULDER"), # for right collar (invert all axes)
  
  ("152", "0", "NECK"), # below jaw to lip upper middle to simulate neck bone
  ("0", "6", "HEAD"), # lip upper middle to mid nose bridge to simulate head bone
  ("152", "10", "HEAD_NECK") # below jaw to highest face point
]

hand_landmark_connections = [
  ("WRIST", "THUMB_MCP"),
  ("THUMB_MCP", "THUMB_IP"),
  ("THUMB_IP", "THUMB_TIP"),

  ("WRIST", "INDEX_FINGER_MCP"),
  ("INDEX_FINGER_MCP", "INDEX_FINGER_PIP"),
  ("INDEX_FINGER_PIP", "INDEX_FINGER_DIP"),
  ("INDEX_FINGER_DIP", "INDEX_FINGER_TIP"),
  
  ("WRIST", "MIDDLE_FINGER_MCP"),
  ("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP"),
  ("MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"),
  ("MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP"),
  
  ("WRIST", "RING_FINGER_MCP"),
  ("RING_FINGER_MCP", "RING_FINGER_PIP"),
  ("RING_FINGER_PIP", "RING_FINGER_DIP"),
  ("RING_FINGER_DIP", "RING_FINGER_TIP"),
  
  ("WRIST", "PINKY_MCP"),
  ("PINKY_MCP", "PINKY_PIP"),
  ("PINKY_PIP", "PINKY_DIP"),
  ("PINKY_DIP", "PINKY_TIP")
]

face_landmark_connections = [
    ("RIGHT_EYE", "133"), # right eyelid inner
    ("RIGHT_EYE", "33"),  # right eyelid outer
    ("RIGHT_EYE", "159"), # right eyelid upper
    ("RIGHT_EYE", "160"), # right eyelid upper outer
    ("RIGHT_EYE", "158"), # right eyelid upper inner
    ("RIGHT_EYE", "144"), # right eyelid lower outer
    ("RIGHT_EYE", "153"), # right eyelid lower inner
    ("RIGHT_EYE", "145"), # right eyelid lower

    ("LEFT_EYE", "362"), # left eyelid inner
    ("LEFT_EYE", "263"), # left eyelid outer
    ("LEFT_EYE", "386"), # left eyelid upper
    ("LEFT_EYE", "387"), # left eyelid upper outer
    ("LEFT_EYE", "385"), # left eyelid upper inner
    ("LEFT_EYE", "373"), # left eyelid lower outer
    ("LEFT_EYE", "380"), # left eyelid lower inner
    ("LEFT_EYE", "374"),  # left eyelid lower
    
    ("RIGHT_EYE", "RIGHT_EYE_INNER"),
    ("RIGHT_EYE", "RIGHT_EYE_OUTER"),
    ("LEFT_EYE", "LEFT_EYE_INNER"),
    ("LEFT_EYE", "LEFT_EYE_OUTER")
]

# Single bones for face
pose_landmark_single_bones = [
    # right eye
    "RIGHT_EYE",
    # left eye
    "LEFT_EYE"
]

face_landmark_single_bones = [
    # right eyebrow
    107, 105, 70,
    # left eyebrow
    336, 334, 300,        
    # center brow
    9,
    # mid nose bridge
    6,
    # nose
    4,
    # right nostril
    218,
    # left nostril
    438,
    # right nasolabial middle
    36,
    # left nasolabial middle
    266,
    # right nasolabial upper
    47,
    # left nasolabial upper
    277,
    # right nasolabial lower
    202,
    # left nasolabial lower
    422,
    # right squint inner
    22,
    # left squint inner
    252,
    # right squint outer
    110,
    # left squint outer
    339,
    # right cheek upper
    117,
    # right cheek lower
    187,
    # left cheek upper
    346,
    # left cheek lower
    411,
    # right lip below nose
    167,
    # left lip below nose
    393,
    # right nasolabial crease
    92,
    # left nasolabial crease
    322,
    # right nasolabial mouth corner
    216,
    # left nasolabial mouth corner
    436,
    # right lip corner
    57,
    # left lip corner
    287,
    # lip upper middle
    0,
    # lip lower middle
    17,
    # right lip upper inner
    39,
    # left lip upper inner
    269,
    # right lip upper outer
    40,
    # left lip upper outer
    270,
    # right lip lower outer
    321,
    # left lip lower outer
    91,
    # right lip lower inner
    84,
    # left lip lower inner
    314,
    # lip below
    18,
    # chin
    175,
    # below jaw
    152,
    # right jaw clench
    177,
    # left jaw clench
    401
]

########## Method definitions ##########

def get_landmarks(vid_name, frame_list):
    mp_holistic = mp.solutions.holistic

    # For static images:
    holistic = mp_holistic.Holistic(static_image_mode=True)
    for image in frame_list:
        # Convert the BGR image to RGB before processing.
        results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # save landmarks in arrays
        pose_landmarks.append(results.pose_landmarks)
        left_hand_landmarks.append(results.left_hand_landmarks)
        right_hand_landmarks.append(results.right_hand_landmarks)
        face_landmarks.append(results.face_landmarks)
        
    holistic.close()


def get_video_frames(file_url):
    vidcap = cv2.VideoCapture(file_url)
    success, image = vidcap.read()
    # array of objects with class 'numpy.ndarray'
    frames = []
    while success:
        frames.append(image)
        success, image = vidcap.read()

    return frames


def load_landmarks_into_scene(landmarks = [], names = [], l_count = 0, first_char = ""):
    for frame in range (0, len(landmarks)):
        lm_for_curr_frame = landmarks[frame]
        if lm_for_curr_frame is not None:
            for id in range(0, l_count):
                # get landmark name
                name = first_char + (str(id) if not names else names[id])
                # get 3D coords of the landmark
                l = lm_for_curr_frame.landmark[id]
                location = (l.x * 30 * 2, l.y * (20) * 2, l.z * (20) * 2)
                
                # check if we need to create the ico sphere for the current landmark for the first time
                if frame == 0:
                    # create new object
                    bpy.ops.mesh.primitive_ico_sphere_add(enter_editmode=False, align='WORLD', location=location, scale=(0.1, 0.1, 0.1))
                    # rename object
                    bpy.context.object.name = name

                # set location for next frame
                obj = bpy.context.scene.objects[name]
                obj.location = location
                # insert keyframe
                obj.keyframe_insert(data_path='location', frame = frame)
                

def create_bones(landmark_connections = [], first_char = "", armature_exists = False):
    for idx, lc in enumerate(landmark_connections):
        if idx == 0 and not armature_exists:
            # Create armature with a single bone
            bpy.ops.object.posemode_toggle()
            bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        else:
            # add another single bone to the armature
            bpy.ops.object.editmode_toggle()
            bpy.ops.armature.bone_primitive_add()

        # toggle into pose mode to set bone constraints
        bpy.ops.object.posemode_toggle()
        # assign start and target landmark names
        start_lm = first_char + lc[0]
        target_lm = first_char + lc[1]

        # name bone after target landmark if no other name is given
        bone_name = target_lm if len(lc) < 3 else lc[2]    
        bpy.context.object.pose.bones["Bone"].name = bone_name
                
        # set constraint 'COPY_LOCATION'
        bone_const_cl = bpy.data.objects['Armature'].pose.bones[bone_name].constraints.new('COPY_LOCATION')
        bone_const_cl.target = bpy.data.objects[start_lm]
        # set constraint 'STRETCH_TO'
        bone_const_st = bpy.data.objects['Armature'].pose.bones[bone_name].constraints.new('STRETCH_TO')
        bone_const_st.target = bpy.data.objects[target_lm]
        
        
def create_90d_bones(landmark_single_bones = []):
    for lm in landmark_single_bones:
        # add single bone in 90d angle to the armature
        bpy.ops.object.editmode_toggle()
        bpy.ops.armature.bone_primitive_add()
        
        # toggle into pose mode to set bone constraints
        bpy.ops.object.posemode_toggle()
        # get the bone name as string
        lm_name = lm
        if isinstance(lm, int):
            lm_name = str(lm)
        # name bone after landmark 
        bpy.context.object.pose.bones["Bone"].name = lm_name
        # set constraint 'COPY_LOCATION'
        bone_const_cl = bpy.data.objects['Armature'].pose.bones[lm_name].constraints.new('COPY_LOCATION')
        bone_const_cl.target = bpy.data.objects[lm_name]
        


########## Execute methods ##########

# Get landmarks into arrays
get_landmarks(video_file_name, get_video_frames(video_file_path))

# Load Pose Landmarks
load_landmarks_into_scene(landmarks = pose_landmarks, names = pose_landmark_names, l_count = 33)

# Load Right Hand Landmarks
load_landmarks_into_scene(landmarks = right_hand_landmarks, names = hand_landmark_names, l_count = 21, first_char = "R")

# Load Left Hand Landmarks
load_landmarks_into_scene(landmarks = left_hand_landmarks, names = hand_landmark_names, l_count = 21, first_char = "L")

# Load Face Landsmarks
load_landmarks_into_scene(landmarks = face_landmarks, l_count = 468)


# Create pose bones (only arms)
create_bones(landmark_connections = pose_landmark_connections)

# Create bones for left hand
create_bones(landmark_connections = hand_landmark_connections, first_char = "L", armature_exists = True)

# Create bones for right hand
create_bones(landmark_connections = hand_landmark_connections, first_char = "R", armature_exists = True)

# Create face bones
# face bones will currently not be mapped onto a 3D character in assign_animation_to_avatar.py
create_bones(landmark_connections = face_landmark_connections, armature_exists = True)
create_90d_bones(face_landmark_single_bones)
create_90d_bones(pose_landmark_single_bones)
