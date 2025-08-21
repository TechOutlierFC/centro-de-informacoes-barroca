# pages/apresentacao.py

import streamlit as st
import base64
from pathlib import Path

LOGO_DIR = Path("public/logos")

def get_image_as_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Arquivo de imagem não encontrado em: {path}")
        return ""

def get_logo_html(filename, class_name="logo-img"):
    logo_path = LOGO_DIR / filename
    ext = logo_path.suffix.strip('.')
    encoded_logo = get_image_as_base64(logo_path)
    if encoded_logo:
        return f'<img class="{class_name}" src="data:image/{ext};base64,{encoded_logo}" alt="{filename}">'
    return ""


st.set_page_config(page_title="Apresentação Barroca", page_icon="🏆", layout="wide")

st.markdown('<a href="/" target="_self" class="back-button" title="Voltar à página inicial"> &#x21A9; </a>', unsafe_allow_html=True)

YELLOW = "#FFA500"

IMAGE_PATH = "public/barroca.webp"
encoded_image = get_image_as_base64(IMAGE_PATH)
image_html_src = f"data:image/webp;base64,{encoded_image}" if encoded_image else ""

# --- Logos HTML ---
logos_base = [
    get_logo_html("flamengo.png"),
    get_logo_html("corinthians.png"),
    get_logo_html("botafogo.png"),
    get_logo_html("brasil.png"),
]
logos_auxiliar = [
    get_logo_html("bahia.png"),
    get_logo_html("botafogo.png"),
    get_logo_html("fluminense.png"),
    get_logo_html("vasco.webp"),
]
logos_treinador = [
    get_logo_html("botafogo.png"),
    get_logo_html("goianiense.webp"),
    get_logo_html("coritiba.webp"),
    get_logo_html("vitoria.png"),
    get_logo_html("bahia.png"),
    get_logo_html("ceara.png"),
    get_logo_html("avai.png"),
    get_logo_html("mirassol.png"),
    get_logo_html("crb.png"),
]
logos_treinador_p1 = logos_treinador[:4]
logos_treinador_p2 = logos_treinador[4:]

# --- Conquistas HTML ---
conquistas = [
    f"""<div class="conquista-item">
            <div class="formacao-ano">2012</div>
            {get_logo_html('bahia.png', 'conquista-logo')}
            <div class="conquista-desc">Campeonato Baiano</div>
       </div>""",
    f"""<div class="conquista-item">
            <div class="formacao-ano">2015</div>
            {get_logo_html('vasco.webp', 'conquista-logo')}
            <div class="conquista-desc">Campeonato Carioca</div>
       </div>""",
    f"""<div class="conquista-item">
            <div class="formacao-ano">2016</div>
            {get_logo_html('botafogo.png', 'conquista-logo')}
            <div class="conquista-desc">Campeonato Brasileiro Sub-20</div>
       </div>""",
    f"""<div class="conquista-item">
            <div class="formacao-ano">2019</div>
            {get_logo_html('goianiense.webp', 'conquista-logo')}
            <div class="conquista-desc">Acesso à 1ª Divisão</div>
       </div>""",
    f"""<div class="conquista-item">
            <div class="formacao-ano">2022</div>
            {get_logo_html('bahia.png', 'conquista-logo')}
            <div class="conquista-desc">Acesso à 1ª Divisão</div>
       </div>""",
    f"""<div class="conquista-item">
            <div class="formacao-ano">2023</div>
            {get_logo_html('ceara.png', 'conquista-logo')}
            <div class="conquista-desc">Copa do Nordeste</div>
       </div>""",
]


st.markdown(
    f"""
    <style>
      /* Travar qualquer rolagem e zerar paddings que causam overflow */
      html, body, .stApp, [data-testid="stAppViewContainer"],
      section.main, .main, .block-container {{
        height: 100dvh !important;
        max-height: 100dvh !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin: 0 !important;
      }}

      #MainMenu {{visibility: hidden;}}
      footer {{visibility: hidden;}}
      header {{visibility: hidden;}}
      [data-testid="stSidebar"] {{display: none;}}

      :root {{
        --vpad: clamp(24px, 6vh, 56px);  /* recuo superior e inferior idêntico */
        --line-w: 4px;                   /* espessura das divisórias */
        --line-color: {YELLOW};
      }}

      /* Container fixo ocupando a viewport com recuos */
      .barroca-shell {{
        position: fixed;
        inset: var(--vpad) 0 var(--vpad) 0; /* top, right, bottom, left */
        display: flex;
        align-items: stretch;
        justify-content: stretch;
        box-sizing: border-box;
        height: auto;    /* altura = viewport - (top+bottom) */
        width: 100%;
      }}

      .barroca-row {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        width: 100%;
        height: 100%;
        gap: 0; /* borda encostando */
      }}

      .barroca-col {{
        height: 100%;
        padding: clamp(12px, 2vh, 24px);
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        gap: clamp(12px, 2vh, 24px);
      }}

      .header-col {{
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: clamp(8px, 2vh, 16px);
      }}

      .titulo-principal {{
        font-size: clamp(1.5rem, 6vmin, 3.2rem);
        font-weight: bold;
      }}

      .barroca-img {{
        border-radius: 16px;
        width: clamp(200px, 40vmin, 450px);
        height: clamp(133px, 27vmin, 300px);
        object-fit: cover;
        border: 4px solid var(--line-color);
      }}

      .titulo-secundario {{
        font-size: clamp(1rem, 4vmin, 2.2rem);
        font-weight: bold;
        color: var(--line-color);
        text-decoration: underline;
        text-underline-offset: 8px;
        margin-bottom: clamp(8px, 1.5vh, 16px);
      }}

      .lista-formacao {{
        display: flex;
        flex-direction: column;
        gap: clamp(8px, 2vh, 24px);
        align-items: flex-start;
        width: 100%;
        padding: 0 16px;
      }}

      .formacao-item {{
          display: flex;
          align-items: center;
          gap: 16px;
          text-align: left;
      }}

      .formacao-ano {{
          font-size: clamp(1.2rem, 5vmin, 2.8rem);
          font-weight: bold;
          color: var(--line-color);
          text-align: center;
      }}

      .conquista-item .formacao-ano {{
          font-size: clamp(1.4rem, 5.5vmin, 3.0rem);
      }}

      .formacao-desc {{
          font-size: clamp(0.7rem, 2.5vmin, 1.6rem);
      }}

      .col-trabalhos {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: clamp(24px, 4vh, 48px);
      }}

      .logos-container {{
        display: flex;
        flex-direction: column;
        gap: clamp(8px, 2vh, 16px);
        align-items: center;
      }}

      .logos-row {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: clamp(12px, 3vmin, 32px);
      }}

      .logo-img {{
        height: clamp(56px, 10vh, 110px);
        width: clamp(56px, 10vh, 110px);
        object-fit: contain;
      }}

      .col-conquistas {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }}

      .lista-conquistas {{
        display: flex;
        flex-direction: column;
        gap: clamp(24px, 4vh, 48px);
        width: 100%;
      }}

      .conquista-item {{
          display: grid;
          grid-template-columns: 0.6fr 0.6fr 1.8fr;
          align-items: center;
          text-align: left;
          width: 100%;
          padding: 0 clamp(8px, 2vmin, 16px);
      }}

      .conquista-logo {{
        height: clamp(50px, 8vh, 105px);
        width: clamp(50px, 8vh, 105px);
        object-fit: contain;
        justify-self: center;
      }}

      .conquista-desc {{
        font-size: clamp(0.9rem, 3.5vmin, 2.1rem);
        flex: 1;
      }}

      /* --- Media Query para Telas Menores (Notebooks, etc.) --- */
      @media (max-width: 1366px) {{
        .titulo-principal {{ font-size: 1.8rem; }}
        .barroca-img {{ width: 300px; height: 200px; }}
        .titulo-secundario {{ font-size: 1.4rem; }}
        .formacao-ano {{ font-size: 1.6rem; }}
        .formacao-desc {{ font-size: 0.9rem; }}

        .logo-img {{ height: 90px; width: 90px; }}

        .conquista-item .formacao-ano {{ font-size: 1.8rem; }}
        .conquista-logo {{ height: 65px; width: 65px; }}
        .conquista-desc {{ font-size: 1.2rem; }}
        .conquista-item {{ grid-template-columns: 0.7fr 0.7fr 1.6fr; }}
      }}

      /* Divisórias verticais amarelas com altura exata da área visível */
      .barroca-col:not(:last-child) {{
        border-right: var(--line-w) solid var(--line-color);
      }}

      .back-button {{
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 9999;
        background-color: white;
        border: 2px solid var(--line-color);
        border-radius: 8px;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: black !important;
        text-decoration: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transition: all 0.2s ease-in-out;
      }}
      .back-button:hover {{
        transform: scale(1.1);
        background-color: #f8f8f8;
      }}
      
      /* --- Mobile: empilhado e rolável --- */
      @media (max-width: 768px) {{
        :root {{
          --vpad: 12px;
          --line-w: 3px;
        }}

        html, body, .stApp, [data-testid="stAppViewContainer"],
        section.main, .main, .block-container {{
          height: auto !important;
          max-height: none !important;
          overflow-y: auto !important;
        }}

        .barroca-shell {{
          position: static;
          inset: auto;
          height: auto;
          width: 100%;
        }}

        .barroca-row {{
          display: flex;
          flex-direction: column;
          height: auto;
          gap: 0;
        }}

        .barroca-col {{
          height: auto;
          padding: clamp(12px, 3vh, 20px);
          border-right: none !important;
          border-bottom: var(--line-w) solid var(--line-color);
        }}

        .barroca-col:last-child {{
          border-bottom: none;
        }}

        .titulo-principal {{
          font-size: clamp(1.2rem, 6vw, 1.8rem);
        }}

        .barroca-img {{
          width: min(100%, 360px);
          height: auto;
        }}

        .logo-img {{
          height: clamp(40px, 9vh, 70px);
          width: clamp(40px, 9vh, 70px);
        }}

        .logos-row {{
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          justify-items: center;
        }}

        .conquista-item {{
          grid-template-columns: 0.6fr 0.6fr 1.6fr;
          padding: 0 8px;
        }}

        .conquista-logo {{
          height: clamp(38px, 7vh, 60px);
          width: clamp(38px, 7vh, 60px);
        }}

        .conquista-desc {{
          font-size: clamp(0.85rem, 3.8vw, 1.1rem);
        }}
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- LAYOUT: 3 colunas vazias, barras com altura total visível ---
st.markdown(
    f"""
    <div class="barroca-shell">
      <div class="barroca-row">
        <div class="barroca-col">
            <div class="header-col">
                <div class="titulo-principal">Eduardo Barroca</div>
                <img class="barroca-img" src="{image_html_src}" alt="Foto Eduardo Barroca">
            </div>
            <div>
                <div class="titulo-secundario">Formações e Cursos</div>
                <div class="lista-formacao">
                    <div class="formacao-item">
                        <div class="formacao-ano">2004</div>
                        <div class="formacao-desc">Graduação em Educação Física - UFRJ</div>
                    </div>
                    <div class="formacao-item">
                        <div class="formacao-ano">2006</div>
                        <div class="formacao-desc">Pós-Graduação em Treinamento Desportivo e Futebol - UFRJ</div>
                    </div>
                    <div class="formacao-item">
                        <div class="formacao-ano">2008</div>
                        <div class="formacao-desc">Pós-Graduação em Gestão de Pessoas - Estácio</div>
                    </div>
                    <div class="formacao-item">
                        <div class="formacao-ano">2010</div>
                        <div class="formacao-desc">Professor da CBF Academy - Curso de Treinadores de Futebol</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="barroca-col col-trabalhos">
            <div>
                <div class="titulo-secundario">Trabalhando na Base</div>
                <div class="logos-row">
                    {''.join(logos_base)}
                </div>
            </div>
            <div>
                <div class="titulo-secundario">Auxiliar Técnico</div>
                <div class="logos-row">
                    {''.join(logos_auxiliar)}
                </div>
            </div>
            <div>
                <div class="titulo-secundario">Treinador Principal</div>
                <div class="logos-container">
                    <div class="logos-row">
                        {''.join(logos_treinador_p1)}
                    </div>
                    <div class="logos-row">
                        {''.join(logos_treinador_p2)}
                    </div>
                </div>
            </div>
        </div>
        <div class="barroca-col col-conquistas">
            <div class="titulo-secundario">Principais Conquistas</div>
            <div class="lista-conquistas">
                {''.join(conquistas)}
            </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
