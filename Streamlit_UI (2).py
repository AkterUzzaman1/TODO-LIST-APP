import streamlit as st
# import Image from pillow to open images
from PIL import Image
import base64
from Deploy import get_task,toggle_Completed,create_task


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_bg_from_local('BG.jpg')


img = Image.open("logo.png")



col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.write("")

with col2:
    # display image using streamlit
    # width is used to set the width of an image to be set
    st.image(img, width=200)

with col3:
    st.write("")


st.markdown("<h1 style='text-align: center; color: white;'>  Ethereum TODO List Dapp </h1>", unsafe_allow_html=True)

new_task = st.text_input("Enter Your name", "Type Here ...")

if st.button("Create Task"):
    result = create_task(new_task)
    st.success("Task Created")


completed_task = st.text_input("Enter Your Task number that is completed ", "Type Here ...")

if st.button("Mark Completed"):
    completed_task = int(completed_task)
    result = toggle_Completed(completed_task)


task = st.text_input("Enter Your Task to retrieve", "Type Here ...")

if st.button("Retrieve Task"):
    result = get_task(int(task))
    st.success(result[1])

task = st.text_input("Enter Your Task to Get the full status", "Type Here ...")

if st.button("Check task status"):
    result = get_task(int(task))
    st.success(result)


