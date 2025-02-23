import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & Description
st.title("Datasweeper Sterling Integrator By Tayyeba Ali")
st.write("Transform your file between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3!")

# File Upload
uploaded_files = st.file_uploader("Upload your file (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        try:
            # Read the file
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                try:
                    df = pd.read_excel(file, engine="openpyxl")
                except ImportError:
                    st.error("The 'openpyxl' package is required to read Excel files. Please install it using `pip install openpyxl`.")
                    continue
            else:
                st.error(f"File type not supported: {file_ext}")
                continue

            # File Details
            st.write(f"🔍 Preview the head of the Dataframe for {file.name}")
            st.dataframe(df.head())

            # Data Cleaning Options
            st.subheader("🛠️ Data Cleaning Options")
            if st.checkbox(f"Clean data for {file.name}", key=f"clean_{file.name}"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Remove duplicates from the file: {file.name}", key=f"remove_duplicates_{file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write("✅ Duplicates removed!")

                with col2:
                    if st.button(f"Fill missing values for {file.name}", key=f"fill_missing_{file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("✅ Missing values have been filled!")

                # Column Selection
                st.subheader("🎯 Select Columns to Keep")
                columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns, key=f"columns_{file.name}")
                df = df[columns]

                # Data Visualization
                st.subheader("📊 Data Visualization")
                if st.checkbox(f"Show visualization for {file.name}", key=f"visualize_{file.name}"):
                    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # Conversion Options
            st.subheader("🔄️ Conversion Options")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"conversion_{file.name}")
            if st.button(f"Convert {file.name}", key=f"convert_{file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    try:
                        df.to_excel(buffer, index=False, engine="openpyxl")
                        file_name = file.name.replace(file_ext, ".xlsx")
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    except ImportError:
                        st.error("The 'openpyxl' package is required to write Excel files. Please install it using `pip install openpyxl`.")
                        continue

                buffer.seek(0)

                st.download_button(
                    label=f"Download {file_name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                    key=f"download_{file.name}"
                )

        except Exception as e:
            st.error(f"An error occurred while processing {file.name}: {str(e)}")

    st.success("🎉 All files processed successfully!")
