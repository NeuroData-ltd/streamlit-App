import streamlit as st
import requests
import requests
import time
import json
import pandas as pd
import os
url = 'https://app.nanonets.com/api/v2/OCR/Model/54ead1ca-698f-4e41-92c2-7cbde54f7e3b/LabelFile/'

st.set_page_config(
    page_title="NeuroData Extractor", layout="wide", page_icon="./images/logo.png"
)
list_options = ["invoice_number","seller_name ","seller_address","seller_vat_number"
    ,"buyer_address","invoice_date","payment_due_date","invoice_amount"]
st.title("NeuroData Extractor")
st.multiselect('Select selected Items',options=list_options)

st.sidebar.image("images/logo.png",width=120)
st.sidebar.title("PDF Scraper For Businesses")
st.sidebar.image(r"images/extractor.gif")
st.sidebar.title("Reduce your manual data entry costs")
st.sidebar.image(r"images/ocr_illustration.gif")

img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg","pdf"],accept_multiple_files=True)


tic = time.time()
if img_file_buffer is not None:
    file_details = {"FileName":img_file_buffer.name,"FileType":img_file_buffer.type}

    with open(os.path.join("app/tempDir", img_file_buffer.name), "wb") as f:
        f.write(img_file_buffer.getbuffer())
    st.success("Saved File")
    st.markdown("---")

    if st.button("Process Your Invoices"):
        data = {'file':open("./tempDir/"+img_file_buffer.name, 'rb')}
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('h-33coFJ6mzCX0iAed_boDQTsswBa-P7', ''), files=data)

        st.text("Processing Time... : {0:.2f} seconds!".format(time.time() - tic))
        json_data = json.loads(response.text)
        print(json_data)
        element = json_data["result"][0]["prediction"]
        columns = [element[items]["label"] for items in range(len(element))]
        values = [(element[items]["ocr_text"], element[items]["score"]) for items in range(len(element))]
        d = dict()
        for el in range(len(element)):
            d[columns[el]] = values[el]
            df = pd.DataFrame.from_dict(d, orient="index", columns=["Result", "Confidence"])
        st.dataframe(df,width=1000)




