import streamlit as st
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Informações Barroca",
    page_icon="⚽️",
    layout="wide"
)

# --- CSS PARA OCULTAR ELEMENTOS NATIVOS DO STREAMLIT ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stSidebar"] {display: none;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# --- IMPORTAÇÃO DA FONTE E ESTILO CSS ---
# Este bloco define a aparência das "caixinhas"
button_style = """
    <style>
    /* Importa a fonte Anton do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Anton&display=swap');

    .custom-box {
        background-color: white;
        color: #202020; /* Cor do texto dentro da caixa */
        padding: 25px 20px;
        border-radius: 15px;
        text-align: center;
        font-family: 'Anton', sans-serif !important; /* Força a aplicação da fonte */
        font-size: 24px; /* Tamanho da fonte aumentado */
        font-weight: 400;
        text-transform: uppercase; /* Coloca o texto em caixa alta */
        /* Sombra sólida para criar efeito de borda */
        box-shadow: 6px 6px 0px 0px #FABB48;
        border: 2px solid #FABB48; /* Borda fina para complementar */
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        cursor: pointer;
        margin-bottom: 24px; /* Espaçamento entre os botões */
    }
    .custom-box:hover {
        transform: scale(1.03);
        box-shadow: 8px 8px 0px 0px #FABB48;
    }
    
    .title-text {
        font-family: 'Anton', sans-serif !important; /* Força a aplicação da fonte */
        text-align: center;
        text-transform: uppercase;
    }
    .logo-img {
        width: 50%;
        height: auto;
        display: inline-block;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHorizontalBlock"],
    .block-container,
    [data-testid="column"] {
        overflow: hidden !important;
    }
    .fixed-update {
        position: fixed;
        font-size: 18px;
        left: 16px;
        bottom: 12px;
        font-style: italic;
        color: #ffffff;
        background: transparent;
        z-index: 9999;
        pointer-events: none;
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)


# --- CONTEÚDO DA PÁGINA ---

# Título centralizado, em caixa alta e com a nova fonte
st.markdown("<h1 class='title-text'>Centro de Informações - Eduardo Barroca</h1>", unsafe_allow_html=True)

# Espaçamento vertical aumentado
st.markdown("<br><br>", unsafe_allow_html=True)

# Colunas ajustadas para reduzir o comprimento dos botões
_, col_central, _ = st.columns([1.2, 1, 1.2]) 

with col_central:
    # A div usa a classe 'custom-box' que definimos no CSS acima
    st.markdown("""
        <a href='/apresentacao' target='_self' style='text-decoration: none;'>
            <div class='custom-box'>Apresentação</div>
        </a>
    """, unsafe_allow_html=True)
    st.markdown("""
        <a href='/centro_de_informacoes' target='_self' style='text-decoration: none;'>
            <div class='custom-box'>Centro de Informações</div>
        </a>
    """, unsafe_allow_html=True)
    # Logo Outlier FC no terceiro "botão"
    _logo_path = "public/outlierfc.png"
    try:
        with open(_logo_path, "rb") as _f:
            _logo_b64 = base64.b64encode(_f.read()).decode("utf-8")
        st.markdown(f"""
            <a href='/outlier_fc' target='_self' style='text-decoration: none;'>
                <div class='custom-box'>
                    <img src='data:image/png;base64,{_logo_b64}' class='logo-img' alt='Outlier FC' />
                </div>
            </a>
        """, unsafe_allow_html=True)
    except Exception:
        st.markdown("<div class='custom-box'>Logo não encontrada</div>", unsafe_allow_html=True)


st.markdown("<div class='fixed-update'><em>Última atualização em 09/10/2025</em></div>", unsafe_allow_html=True)