import os, shutil, streamlit as st
from reduvis import run_reduvis
from PIL import Image
from tqdm import tqdm
import tempfile
import yaml

st.set_page_config(page_title="ReduVis - Raw Images Redundancy Reduction and Similarity Analysis", layout="wide")

st.title("ReduVis - Redundancy and Similarity Analyzer")
st.markdown("### Remove redundant or near duplicate images before photogrammetry reconstruction.")

st.sidebar.header("Settings")
cfg_path = st.sidebar.text_input("Configuration File", value="config.yaml")
output_root = st.sidebar.text_input("Output Directory", value="outputs")

# Initialize session state for temp_dir and result
if "temp_dir" not in st.session_state:
    st.session_state.temp_dir = None
if "result" not in st.session_state:
    st.session_state.result = None


# File/Images Upload

upload_files = st.file_uploader(
    "Upload Multiple Images",
    accept_multiple_files=True,
    type=["png", "jpeg", "jpg"]
)

if upload_files:
    # Remove old temp folder if it exists
    if st.session_state.temp_dir and os.path.exists(st.session_state.temp_dir):
        shutil.rmtree(st.session_state.temp_dir)
        
    # Create temporary working directory
    temp_dir = tempfile.mkdtemp(prefix="images_input")
    # Save uploaded files
    for file in tqdm(upload_files, desc="Saving Uploaded Images"):
        img_path = os.path.join(temp_dir, file.name)
        with open(img_path, "wb") as f:
            f.write(file.read())
    st.success(f"{len(upload_files)} images uploaded to {temp_dir}")
    
    if st.button("Run ReduVis Analysis"):
        with st.spinner("Running redundancy analysis...... Please wait "):
            st.session_state.result = run_reduvis(temp_dir, config_path=cfg_path, output_root=output_root)
        st.success("Redundancy Analysis Completed!")
# Display Results if available
if st.session_state.result:
    result = st.session_state.result
         
     # Summary
    st.subheader("Summary:")
    st.write(result.get('summary', "No summary available."))

    # Heatmap
    if os.path.exists(result.get('heatmap_path', '')):
        st.subheader("Heatmap")
        st.image(Image.open(result['heatmap_path']), caption="Similarity Heatmap", width='stretch')

    # Download Kept Images as ZIP
    if os.path.exists(result.get('kept_dir', '')):
        kept_zip = os.path.join(output_root, "kept_images.zip")
        shutil.make_archive(kept_zip.replace(".zip", ""), "zip", result['kept_dir'])
        with open(kept_zip, "rb") as f:
            st.download_button("Download Kept Images (ZIP)", f, file_name="kept_images.zip")

    # Download CSV Report
    if os.path.exists(result.get('report_csv', '')):
        with open(result['report_csv'], "rb") as f:
            st.download_button("Download CSV Report", f, file_name="reduvis_report.csv")
