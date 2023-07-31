import streamlit as st
from streamlit_option_menu import option_menu  # Importing a custom option menu widget
import pandas as pd
import os
import cv2

from utils.Recognition_page import rec_pg
from utils.download import DOWNLOAD
from utils.About import ABOUT

# CSS style to hide Streamlit's main menu and footer
hide_st_style = """
<style>
footer {visibility: hidden;}
</style>
"""
dictionary = {}
# Applying the CSS style to hide Streamlit's main menu and footer
st.markdown(hide_st_style, unsafe_allow_html=True)

if "database" not in st.session_state:
    st.session_state['database'] = False


# ======================================================================================================


directory = 'data'
def load_models():
    
    # Init models face detection & recognition
    weights = os.path.join(directory, "models2",
                           "face_detection_yunet_2023mar_int8.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
    face_detector.setScoreThreshold(0.87)

    weights = os.path.join(directory, "models2", "face_recognition_sface_2021dec_int8.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
    return face_detector,face_recognizer


face_detector,face_recognizer = load_models()


with st.sidebar:
    # Creating a sidebar menu with different options
    choose = option_menu("Main Menu", ["About the Project", "Start Taking Attendance","Download Attendance list"],
                         icons=['house', 'file-slides','person lines fill',"box arrow in down"],
                         menu_icon="list", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#0E1117"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )


if choose == "About the Project":
    ABOUT()
    #st.success("Hello world")

elif choose == "Start Taking Attendance":

    rec_pg(face_detector, face_recognizer)


elif choose == "Download Attendance list":
    DOWNLOAD()


