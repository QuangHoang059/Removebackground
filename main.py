import streamlit as st
from PIL  import Image
from streamlit_image_coordinates import streamlit_image_coordinates as img_coordinates
from streamlit_dimensions import st_dimensions
import cv2,requests,base64
import numpy as np
import os
#set layout
st.set_page_config(layout='wide')
col01,col02=st.columns(2)
#file upload
file =col02.file_uploader('',type=['jpg', 'png','jpeg'])

if 'session_state' not in st.session_state:
    st.session_state['session_state'] ={'old_filename': ''}
#read img
if file is not None:
    img=Image.open(file).convert('RGB')
    img=img.resize((688,int(688*img.height/img.width)))

    col1,col2=col02.columns(2)

    placeholder0=col02.empty()
    with placeholder0: 
        value=img_coordinates(img)
        if value is not None:
            print(value)
            if col2.button('Remove background',type='primary',use_container_width=True):
                print(value)
                filename='{}_{}_{}.png'.format(file.name,value['x'],value['y'])
                if st.session_state.session_state['old_filename']==filename:
                    result_img=cv2.imread(filename,cv2.IMREAD_UNCHANGED)
                else:
                    st.session_state.session_state['old_filename']=filename
                    _,img_bytes=cv2.imencode('.png',np.asarray(img))
                    img_bytes=img_bytes.tobytes()
                    img_bytes_encoded_base64=base64.b64encode(img_bytes).decode('utf-8')
                    with st.spinner("Loading data..."):
                        api_url="https://quanghoang.ap-south-1.modelbit.com/v1/remove_background/latest"
                        api_data={'data':[img_bytes_encoded_base64,value['x'],value['y']]}
                        response= requests.post(api_url,json=api_data)
                        if 'data' not in response.json().keys():
                            col02.header(response.json()['error'])
                        else:
                            result_img_base64_encoding=response.json()['data']
                            result_img_bytes=base64.b64decode(result_img_base64_encoding)
                            result_img=cv2.imdecode(np.frombuffer(result_img_bytes,dtype=np.uint8),cv2.IMREAD_UNCHANGED)
                            # cv2.imwrite(filename,result_img)
                            placeholder0.empty()
                            placeholder2=col02.empty()
                            with placeholder2:
                                col02.image(result_img,use_column_width=True)
            if col1.button('Original',use_container_width=True):
                placeholder0.empty()
                placeholder1=col02.empty()
                with placeholder1:
                    col02.image(img,use_column_width=True)
            