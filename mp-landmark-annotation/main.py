"""
# PyCharm Professional 2020.3

# What does this script do?
The script runs the MediaPipe motion tracking AI on the video file which URL is passed to the 
method get_video_frames in line 58. It annotates all video frames and saves the result in the folder "annotated_images".
Tracked landmarks are depicted as red dots and joint connections between landmarks as green lines.

# How to use this script?
Make sure that the packages cv2 and mediapipe are installed in your Python environment and run the script with an
IDE like PyCharm or Visual Studio Code or run it in the terminal.
"""

import cv2
import mediapipe as mp


def get_landmarks(vid_name, frame_list):
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    # For static images:
    holistic = mp_holistic.Holistic(static_image_mode=True)
    for idx, image in enumerate(frame_list):
        image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Draw pose, left and right hands, and face landmarks on the image.
        annotated_image = image.copy()  # cv2.resize(image.copy(), (1920, 1080))
        mp_drawing.draw_landmarks(
            annotated_image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        mp_drawing.draw_landmarks(
            annotated_image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            annotated_image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        # save annotated frames
        cv2.imwrite('./annotated_images/' + vid_name + "_" + str(idx) + '.png', annotated_image)
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


if __name__ == '__main__':
    get_landmarks('Brauchen Sie eine Arbeitsunfähigkeitsbescheinigung II.mov', get_video_frames('../sign_videos/Brauchen Sie eine Arbeitsunfähigkeitsbescheinigung II.mov'))
