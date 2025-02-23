import streamlit as st
import pandas as pd
import os
from io import BytesIO
import chardet  # For detecting encoding

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

        # Use an expander for each file
        with st.expander(f"📄 {file.name}", expanded=True):
            try:
                # Detect file encoding (for CSV)
                if file_ext == ".csv":
                    rawdata = file.read(10000)
                    file.seek(0)  # Reset pointer
                    result = chardet.detect(rawdata)
                    encoding = result["encoding"] if result["encoding"] else "utf-8"

                    # Allow user to override encoding
                    encoding = st.text_input(f"Detected encoding for {file.name} is '{encoding}'. Enter a different encoding if needed:", value=encoding)
                    df = pd.read_csv(file, encoding=encoding, on_bad_lines="skip")

                elif file_ext == ".xlsx":
                    df = pd.read_excel(file)

                else:
                    st.error(f"File type not supported: {file_ext}")
                    continue

                # File Details
                st.write(f"🔍 Preview of {file.name}")
                st.dataframe(df.head())

                # Data Cleaning Options
                st.subheader("🛠️ Data Cleaning Options")
                if st.checkbox(f"Clean data for {file.name}", key=f"clean_{file.name}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(f"Remove duplicates from {file.name}", key=f"remove_duplicates_{file.name}"):
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
                        numeric_cols = df.select_dtypes(include='number').columns
                        if len(numeric_cols) >= 2:
                            selected_cols = st.multiselect(f"Select columns to visualize for {file.name}", numeric_cols, default=numeric_cols[:2], key=f"viz_cols_{file.name}")
                            st.bar_chart(df[selected_cols])
                        else:
                            st.warning("Not enough numeric columns for visualization.")

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
                        df.to_excel(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".xlsx")
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

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
