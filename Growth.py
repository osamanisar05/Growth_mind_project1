import streamlit as st;
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title= "Data Sweeper",layout='wide')
#Custom CSS
st.markdown(
        """
        <style>
        .stApp{
            background-color: black;
            colour: White;
            }
        </style>
        """,
        unsafe_allow_html=True
)

#Title and Description
st.title("Data Sweeper sterling Integrator by Osama Nisar")
st.write("Transform your files between CSv and Excel formats")

#file ipl;oader 
uploaded_files = st.file_uploader("Upload your files (except csv and excel):",type=["cvs","xlsx"],accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
                df = pd.read_excel(file)
        else:
            st.error("Unsupported file type: {file_ext}")
            continue

        #file details
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())

        #data cleaning options                   symbol icons website
        st.subheader("Data cleaning options")
        if st.checkbox("Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates
                    st.write("Duplicates Removed")

            with col2:
                if st.button("fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include={"number"}).colums
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("missing values has been print")

        st.subheader("Select Columns to keep")
        columns = st.multiselect ("choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #Data Visiualization
        st.subheader("Data Visualization")
        if st.checkbox("Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
        #conversion options

        st.subheader("Conversion options")
        conversion_type = st.radio ("convert {file.name} to:", ["cvs" , "Excel"], key = file.name)
        if st.button("convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "csv":
                df.to.csv(buffer, index = False)
                file_name = file.name.repalce(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index = False)
                file_name = file.name.repalce(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                lebel = "download {file.name} as {conversion_type}",
                data = buffer;
                file_name= file_name,
                mime = mime_type

            )
st.success ("All files processed successfully")
