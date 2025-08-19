import streamlit as st

st.set_page_config(
    page_title="Centro de Informações Barroca",
    page_icon="📂",
    layout="wide"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Bem-vindo ao Centro de Informações do Eduardo Barroca!")
st.write("Esta é a página inicial da nossa futura aplicação.")