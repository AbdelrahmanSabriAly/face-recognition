import streamlit as st
from datetime import datetime
import pandas as pd
import os
from io import BytesIO


def create_attendance_list(attendance_file, students_file,current_date):
    students_file[current_date] = 0
    for i in range(len(attendance_file)):
        index = students_file.index[students_file['ID'] == attendance_file['ID'][i]].tolist()[0]
        students_file[current_date][index] = 1
    return students_file


def DOWNLOAD():
    st.warning("3. Please upload students' names")
    students_file = st.file_uploader(' ',type=['xlsx','xls'])
    if students_file:
        students_file = pd.read_excel(students_file)
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        attendance_file_path = current_date + '.csv'

        if os.path.exists(attendance_file_path):

            attendance_file = pd.read_csv(attendance_file_path)
            output_file = create_attendance_list(attendance_file, students_file,current_date)
            excel_file = BytesIO()

            # Write the DataFrame to the in-memory Excel writer
            output_file.to_excel(excel_file, index=False)  # Set `index=False` if you don't want the index column in the Excel file

            # Move the cursor to the beginning of the file (important step)
            excel_file.seek(0)

            # Now, you can use the st.download_button() function with the in-memory Excel file as 'data'
            st.download_button(
                label="Download Attendance List",
                data=excel_file,
                file_name='attendance_list.xlsx',
                )







        else:
            st.error("Please take attendance first")