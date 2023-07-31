import streamlit as st
import os
import pickle
import cv2
from datetime import datetime
import csv
import sys
import time


COSINE_THRESHOLD = 0.5
dirname = ""
directory = 'data'
temp = st.empty()
added_names=[]
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

if "Recognition" not in st.session_state:
    st.session_state['Recognition'] = True

if 'time' not in st.session_state:
    st.session_state['time'] = False


def match(recognizer, feature1, dictionary):
    max_score = 0.0
    sim_user_id = ""
    for user_id, feature2 in zip(dictionary.keys(), dictionary.values()):
        score = recognizer.match(
            feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
        if score >= max_score:
            max_score = score
            sim_user_id = user_id
    if max_score < COSINE_THRESHOLD:
        return False, ("", 0.0)
    return True, (sim_user_id, max_score)

def recognize_face(image, face_detector, face_recognizer, file_name=None):
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    if image.shape[0] > 1000:
        image = cv2.resize(image, (0, 0),
                           fx=500 / image.shape[0], fy=500 / image.shape[0])

    height, width, _ = image.shape
    face_detector.setInputSize((width, height))
    try:
        _, faces = face_detector.detect(image)
        if file_name is not None:
            assert len(faces) > 0, f'the file {file_name} has no face'

        faces = faces if faces is not None else []
        features = []
        for face in faces:

            aligned_face = face_recognizer.alignCrop(image, face)
            feat = face_recognizer.feature(aligned_face)

            features.append(feat)
        return features, faces
    except Exception as e:
        print(e)
        print(file_name)
        return None, None


def get_valid_camera_index():
    # Check for available camera indices and return the first valid index
    num_cameras = 10  # You can adjust this based on your system's configuration
    for index in range(num_cameras):
        capture = cv2.VideoCapture(index)
        if capture.isOpened():
            capture.release()
            return index
    return None

def start_webcam():
    # Get the valid camera index and start the webcam
    camera_index = get_valid_camera_index()
    if camera_index is not None:
        return cv2.VideoCapture(camera_index)
    else:
        st.error("Error: Webcam not available. The attendance monitoring feature is disabled.")
        return None


def start_from_video(face_detector, face_recognizer, dictionary):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    if os.path.exists(current_date + '.csv'):
        os.remove(current_date + '.csv')

    f = open(current_date + '.csv', 'w+', newline='',encoding='utf-8')
    lnwriter = csv.writer(f)
    students = list(dictionary.keys())
    lnwriter.writerow(["ID"])

    # Create a placeholder to display the webcam feed
    webcam_placeholder = st.empty()

    capture = cv2.VideoCapture('Test_video.mov')
    
    # Get video properties
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    fps = int(capture.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter("Output_Video.mp4", fourcc, fps, (frame_width, frame_height))

    if capture == None:
        return

    if not capture.isOpened():
        sys.exit()

    while capture.isOpened():
        result, image = capture.read()
        if result is False:
            cv2.waitKey(0)
            break

        fetures, faces = recognize_face(image, face_detector, face_recognizer)
        if faces is None:
            continue

        for idx, (face, feature) in enumerate(zip(faces, fetures)):
            result, user = match(face_recognizer, feature, dictionary)
            box = list(map(int, face[:4]))
            color = (0, 255, 0) if result else (0, 0, 255)
            thickness = 2
            cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

            id, score = user if result else (f"unknown_{idx}", 0.0)
            text = "{0} ({1:.2f})".format(id, score)
            position = (box[0], box[1] - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.6
            cv2.putText(image, text, position, font, scale,
                        color, thickness, cv2.LINE_AA)

            if not (id in added_names):
                if id in students:
                    added_names.append(id)
                    students.remove(id)
                    print(students)
                    print(id)
                    lnwriter.writerow([id])

        # Display the webcam feed in the Streamlit app
        # Write the frame with rectangles and recognized names to the output video
        output_video.write(image)
        webcam_placeholder.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)

        key = cv2.waitKey(1)

    capture.release()
    webcam_placeholder.empty()
    output_video.release()
    cv2.destroyAllWindows()
    f.close()
    
    st.success("Attendance has been taken, Please go to Download tab in order to download the attendance list")




def start_real_time(face_detector, face_recognizer, dictionary, duration_in_seconds,index):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    if os.path.exists(current_date + '.csv'):
        os.remove(current_date + '.csv')

    f = open(current_date + '.csv', 'w+', newline='',encoding='utf-8')
    lnwriter = csv.writer(f)
    students = list(dictionary.keys())
    lnwriter.writerow(["ID"])

    # Create a placeholder to display the webcam feed
    webcam_placeholder = st.empty()
    # , 'External "Mobile"'
    capture = cv2.VideoCapture(index)


    if not capture.isOpened():
        sys.exit()

    start_time = time.time()
    while time.time() - start_time < duration_in_seconds:
        result, image = capture.read()
        if result is False:
            cv2.waitKey(0)
            break

        fetures, faces = recognize_face(image, face_detector, face_recognizer)
        if faces is None:
            continue

        for idx, (face, feature) in enumerate(zip(faces, fetures)):
            result, user = match(face_recognizer, feature, dictionary)
            box = list(map(int, face[:4]))
            color = (0, 255, 0) if result else (0, 0, 255)
            thickness = 2
            cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

            id, score = user if result else (f"unknown_{idx}", 0.0)
            text = "{0} ({1:.2f})".format(id, score)
            position = (box[0], box[1] - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.6
            cv2.putText(image, text, position, font, scale,
                        color, thickness, cv2.LINE_AA)

            if not (id in added_names):
                if id in students:
                    added_names.append(id)
                    students.remove(id)
                    print(students)
                    print(id)
                    lnwriter.writerow([id])

        # Display the webcam feed in the Streamlit app
        webcam_placeholder.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)

        key = cv2.waitKey(1)

    capture.release()
    webcam_placeholder.empty()
    cv2.destroyAllWindows()
    f.close()
    st.session_state['time'] = False
    
    st.success("Attendance has been taken, Please go to Download tab in order to download the attendance list")


def load_db():
    choice = st.radio('Upload Database', ['From computer', 'Download'])
    if choice == 'From computer':
        file = st.file_uploader("Upload Database",type=['pkl'])
        if file:
            # Load the pickled data
            dictionary = pickle.load(file)
            return dictionary

    else:
        st.markdown("[Database Downloader](https://databasedownloader-8bjsdmthh9xf4q9daya7be.streamlit.app/)")
        file = st.file_uploader("Upload Database",type=['pkl'])
        if file:
            # Load the pickled data
            dictionary = pickle.load(file)
            return dictionary
        
    
def rec_pg(face_detector, face_recognizer):
    st.warning("1. Please select the camera device")
    index = st.number_input(' ', 0,4)

    st.warning("2. Please upload a database or download one")

    dictionary = load_db()
    if dictionary:
        duration_in_seconds = None
        # choice = st.radio('Recognition type?', ['Real-time', 'From Video'])
        # if choice == 'Real-time':
        # Get user input for the duration in hours, minutes, and seconds
        st.warning("3. Please specify the duration of attendance taking")
        left,middle,right = st.columns(3)
        hours = left.number_input("Enter hours", min_value=0, max_value=24, step=1, value=0)
        minutes = middle.number_input("Enter minutes", min_value=0, max_value=59, step=1, value=0)
        seconds = right.number_input("Enter seconds", min_value=0, max_value=59, step=1, value=0)
        # Convert the user input to total seconds

        duration_in_seconds = hours * 3600 + minutes * 60 + seconds
            
        start_rt_button = st.button("Start Recognition", on_click = start_real_time, args = (face_detector, face_recognizer ,dictionary,duration_in_seconds,index))

        