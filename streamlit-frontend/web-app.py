import streamlit as st
import requests
from PIL import Image

from utils import convert_image_to_base64

st.markdown("<h1 style='text-align: center;'>Welcome to the  Optical Character Recognition (OCR) web app 📝🔍</h1>", unsafe_allow_html=True)
st.write('This is a simple web app to extract text from images.')
st.write('It uses the Tesseract OCR engine to recognize text from images.')
image_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg', 'tiff', 'tif'])

if image_file is not None:

    # Load the image
    image = Image.open(image_file)

    # Convert the image to base64
    image_base64 = convert_image_to_base64(image)

    # Prepare the JSON payload
    payload = {
        "image_data": image_base64
    }
    headers = {
        "Content-Type": "application/json"
    }

    # The user can choose the option sync or async
    # If the user chooses sync, the request will be made synchronously
    # If the user chooses async, the request will be made asynchronously
    st.write('Choose the processing mode:')
    processing_mode = st.selectbox("Processing Mode", ('None', 'Synchronous', 'Asynchronous'))

    if processing_mode == 'Synchronous':

        st.write('Processing the image synchronously...')

        # Make the request to the FastAPI server
        response = requests.post("http://ocr-api:5000/image-sync", json=payload, headers=headers)
        if response.status_code == 200:
            recognized_text = response.json()['text']
            st.write('### *Recognized Text:*')
            st.write(recognized_text)

            # Display the image
            st.image(image, caption=f"Uploaded Image named '{image_file.name}'", use_column_width=True)
            
        else:
            st.error("Failed to process the image. Error: " + response.text)

    elif processing_mode == 'Asynchronous':

        # Button to allow the user to choose to process the image asynchronously
        st.write('Click the button below to process the image asynchronously')
        request = st.button('Process the image asynchronously')

        if request:
            st.write('Processing the image asynchronously...')
            # Make the request to the FastAPI server
            response_post = requests.post("http://ocr-api:5000/image", json=payload, headers=headers)
            if response_post.status_code == 200:
                task_id = response_post.json()['task_id']
                st.write(f'*Task ID:* **{task_id}**')
                if 'task_ids' not in st.session_state:
                    st.session_state['task_ids'] = []
                st.session_state['task_ids'].append(task_id)

            else:
                st.error("Failed to process the image asynchronously. Error: " + response_post.text)

        if 'task_ids' in st.session_state and st.session_state['task_ids']:
            # Ask if the user wants to poll the server for the result
            st.write('Do you want to poll the server?') 
            # Button to allow the user to choose to poll the server
            if st.checkbox('Poll the server'):
                # Ensuring that the state of 'poll_clicked' is maintained across re-runs
                st.session_state['poll_clicked'] = True
            else:
                st.session_state['poll_clicked'] = False
            
            # Check if 'poll_clicked' is in the session state and is True
            if 'poll_clicked' in st.session_state and st.session_state['poll_clicked']:
                id_list = st.session_state['task_ids']
                list_id = ['None']+[str(i) for i in id_list]
                id = st.selectbox("Choose the Task ID to poll amongst the dropdown menu", list_id)

                if id != 'None':
                    
                    task_id = id
                    # Prepare the JSON payload
                    payload = {
                        "task_id": task_id
                    }
                    headers = {
                        "Content-Type": "application/json"
                    }
                    st.write('Polling the server for the Task ID...')
                    response_get = requests.get(f"http://ocr-api:5000/image", json=payload, headers=headers)
                    if response_get.status_code == 200:
                        recognized_text = response_get.json()['task_id']
                        if recognized_text:
                            st.write(f'*Task ID:* **{task_id}**')
                            st.write('### *Recognized Text:*')
                            st.write(recognized_text)
                        else:
                            st.write('The OCR operation is still in progress. Please try again later.')
                    else:
                        st.error("Failed to poll the server for the Task ID. Error: " + response_get.text)
                else:
                    st.write('')
        else:   
            st.write('Task ID is not available. Please process the image asynchronously first.')                 
    else:
        st.write('')

