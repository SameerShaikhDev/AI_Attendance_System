import streamlit as st


def header_home():

    LOGO_PATH ='https://i.ibb.co/67SwJvpR/yes-maam-college-logo.png'
    
    st.markdown(f"""
         <div style='disaply :flex; text-align:center; justify-content: center; margin-bottom:30px; margin-top:30px; '>
            <img src='{LOGO_PATH}' style='height:200px;'/>
            <h1 style='font-size:16px;'>YES MA'AM</h1>
        </div>
    """, unsafe_allow_html=True)

def header_dashbaord():
    LOGO_PATH ='https://i.ibb.co/67SwJvpR/yes-maam-college-logo.png'
    
    st.markdown(f"""
        <div style='disaply :flex; text-align:center; justify-content: center; margin-bottom:30px; margin-top:30px; '>
            <img src='{LOGO_PATH}' style='height:200px;'/>
        </div>
    """, unsafe_allow_html=True)
