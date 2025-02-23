
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS for dark mode
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

# Title and description
st.title("Data Sweeper: Smart Data Cleaning & Processing")
st.write("Streamline Your CSV & Excel Files with One Click")

# File uploader
uploaded_files = st.file_uploader("Upload CSV or Excel file:", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue  # Skip unsupported files

        # Show Data Preview
        st.write(f"### 📋 Preview of `{file.name}`")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean data for `{file.name}`"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from `{file.name}`"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for `{file.name}`"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled!")

            # Select Columns to Keep
            st.subheader("📌 Select Columns to Keep")
            columns = st.multiselect(f"Choose columns for `{file.name}`", df.columns, default=df.columns)
            df = df[columns]

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show visualization for `{file.name}`"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 2:
                    st.bar_chart(df[numeric_cols].iloc[:, :2])
                else:
                    st.warning("⚠️ Not enough numeric columns for visualization!")

            # Conversion Options
            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert `{file.name}`"):
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
                    label=f"⬇️ Download `{file.name}` as `{conversion_type}`",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

st.success("✅ All files processed successfully!")
