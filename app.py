import streamlit as st
import os
import base64
from path import Path

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

st.title("📄 Documents de Projet: ")

img_file_buffer = st.file_uploader("Upload a Pdf Files", type=["png", "jpg", "jpeg","pdf"],accept_multiple_files=False)
if img_file_buffer is not None:
    file_details = {"FileName":img_file_buffer.name,"FileType":img_file_buffer.type}

    with open(os.path.join("tempDir", img_file_buffer.name), "wb") as f:
        f.write(img_file_buffer.getbuffer())
    st.success("Saved File")
    st.markdown("---")

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download</a>'
    return href


files = os.listdir("tempDir")
for l in range(len(files)):
    with st.beta_expander(files[l]):
        st.image("./images/pdf.png")
        st.markdown(get_binary_file_downloader_html('./tempDir/'+files[l], files[l]), unsafe_allow_html=True)
st.sidebar.title("Doctorante Amira Benhjal")
st.sidebar.subheader("")
st.sidebar.image("./images/amira.jpg",width=250)
st.sidebar.markdown("""

A étudié à Faculté de science compus lmanar

De Menzel Bou Zelfa, Nabul, Tunisia
""")
