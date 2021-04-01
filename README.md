# sl-animation-blender
A project where motion capture data is created based on the AI solution MediaPipe Holistic and applied to a 3D character in Blender

## Prerequisites 
The noted versions are the ones that were used during the project.
* Blender 2.91.2
* Python 3.8
* mediapipe 0.8.3.1
* opencv-python 4.5.1.48


## Folder contents
### animation_results
* `.blend` file that contains a 3D character with animation actions 
* exported `.bvh` motion capture files
* exported `.fbx` version of the .blend file
### blender_scripts
* `load_mp_landmarks.py`, a script to create motion capture data from RBG videos. Is attached to `make_bvh_files.blend`
* `assign_animation_to_avatar.py`, a script to map bone rotations from .bvh files to a 3D character. Is attached to `animate_avatar.blend` that contains the prepared character

Both scripts have an instruction of how to use them at the top of the file. To test them, please open the prepared Blender files.

### mp-landmark-annotation
* `main.py`, a script that analyzes video files with the MediaPipe AI, annotates all video frames and saves them in the folder `annotated_images`

### sign_videos
* German Sign Language video clips to capture the motion data from
* Sign language interpreter: Mathias Schäfer


## 3D character
The 3D character was created in Daz Studio and is customized with free assets. It has been transferred to Blender with the Daz to Blender Bridge.
