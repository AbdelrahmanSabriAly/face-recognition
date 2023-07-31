import streamlit as st


def ABOUT():


    # Display header for the app
    st.title("Attendance monitoring using Face recognition")
    
    st.markdown("""---""")

    st.header("Models used:")
    st.markdown(
        """
        ### 1. YuNet:
        - Face detector model.
        - Light, can process up to 100 FPS.
        - works perfectly with covered faces such as masked faces.
        """
        , unsafe_allow_html=True)
    st.write("You can find the GitHub repo of YuNet in the following link")
    st.markdown("[YuNet GitHub](https://github.com/AbdelrahmanSabriAly/Churn_Prediction.git)")

    st.markdown(
        """
        ### 2. SFace:
        - Face recognition model.
        - Light and powerful, outperformed all other models.
        """
        , unsafe_allow_html=True)
    st.write("You can find the GitHub repo of YuNet in the following link")
    st.markdown("[SFace GitHub](https://github.com/fdbtrs/SFace-Privacy-friendly-and-Accurate-Face-Recognition-using-Synthetic-Data)")
    
    st.markdown("""---""")

    st.subheader("The GitHub repo of our peoject is in the following link")
    st.markdown("[GitHub Repo](https://github.com/AbdelrahmanSabriAly/Attendance_monitoring.git)")






