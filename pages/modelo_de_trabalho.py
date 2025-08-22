import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Modelo de Trabalho", page_icon="🛠️", layout="wide")

LOGO_DIR = Path("public/logos")


def get_image_as_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Arquivo de imagem não encontrado em: {path}")
        return ""


def get_logo_html(filename: str, link: str = "#", class_name: str = "logo-img") -> str:
    logo_path = LOGO_DIR / filename
    ext = logo_path.suffix.strip('.')
    encoded_logo = get_image_as_base64(logo_path)
    if not encoded_logo:
        return ""
    target = "_blank"
    return (
        f'<a href="{link}" target="{target}">'
        f'<img class="{class_name}" src="data:image/{ext};base64,{encoded_logo}" alt="{filename}"></a>'
    )


try:
    query_params = st.query_params
    if "go" in query_params:
        dest = query_params["go"]
        query_params.clear()
        try:
            if dest == "centro":
                st.switch_page("pages/centro_de_informacoes.py")
        except Exception:
            st.markdown(
                """
                <script>
                try { window.location.href = './centro_de_informacoes'; } catch (e) {}
                </script>
                """,
                unsafe_allow_html=True,
            )
except AttributeError:
    pass

st.markdown('<a href="?go=centro" target="_self" class="back-button" title="Voltar ao Centro de Informações"> &#x21A9; </a>', unsafe_allow_html=True)

YELLOW = "#FFA500"

# Lista de logos externos (mesmos clubes da seção "Modelo de Trabalho")
work_model_logos_files = [
    "ajax.png",
    "bilbao.png",
    "atletico_madrid.png",
    "leverkusen.png",
    "dortmund.png",
    "monchengladbach.png",
    "chelsea.png",
    "brugge.png",
    "crystal_palace.png",
    "everton.png",
    "barcelona.png",
    "bayern.png",
    "schalke.png",
    "mainz.png",
    "hibernian.png",
    "inter.png",
    "liverpool.png",
    "mallorca.png",
    "city.png",
    "napoli.png",
    "psg.png",
    "leipzig.png",
    "stuttgart.png",
    "villarreal.png",
    "wolfsburg.png",
]

# Links (mesmos da seção original em Centro de Informações)
external_logo_links = {
    "ajax.png": "https://drive.google.com/drive/u/1/folders/1oD6D3bXOjuJ9l6Ub1-xTKtCP2yDhwlXu",
    "bilbao.png": "https://drive.google.com/drive/u/1/folders/1B_TsMNUG7R4oIfjwquMbiVCCQEmPdtUJ",
    "atletico_madrid.png": "https://drive.google.com/drive/u/1/folders/1YqfxUpfsG9cj-bKK61wrLBq4POOLTQa3",
    "leverkusen.png": "https://drive.google.com/drive/u/1/folders/1s2L4-wc3RlRZEBoWbkSrRQDHqnZjuUlc",
    "dortmund.png": "https://drive.google.com/drive/u/1/folders/1z-ApLoWgZ2YEKYcR8wLNIM9C8ysG5Qys",
    "monchengladbach.png": "https://drive.google.com/drive/u/1/folders/1j3KDH_5HJAtdTvUgWQDGCINtylQD01Zd",
    "chelsea.png": "https://drive.google.com/drive/u/1/folders/14xrFUZIgsXfPM0OuzLTdw3rDxrOOWRwN",
    "brugge.png": "https://drive.google.com/drive/u/1/folders/1d7Tl8wZUUHJcHmFtfrtcB51TLo_A_fN3",
    "crystal_palace.png": "https://drive.google.com/drive/u/1/folders/1rIeecrBHq-Gwhd3RqV5cCAccaB7WEI3w",
    "everton.png": "https://drive.google.com/drive/u/1/folders/15q38rIw5ZaG1629GoVMfR7PtXA4-yHTf",
    "barcelona.png": "https://drive.google.com/drive/u/1/folders/1vKw088JhgDQpOsBPcwwwnNXV6TnS1A_7",
    "bayern.png": "https://drive.google.com/drive/u/1/folders/1BRYpF3uLrQdyY9fAlnAXkuGLxIziqfOo",
    "schalke.png": "https://drive.google.com/drive/u/1/folders/1hQsJmx2yBVKfKKR9DtmwSA35Qh6rjd4t",
    "mainz.png": "https://drive.google.com/drive/u/1/folders/1ie_bQ8Atr-cjOCDi3khoVU5ZzKi9PigU",
    "hibernian.png": "https://drive.google.com/drive/u/1/folders/1FNqRUklzi3YV8xAtRaxbd6M0e_Esc-Dt",
    "inter.png": "https://drive.google.com/drive/u/1/folders/1eWqQ6or_3RAzaYtjrXxmPM3atyUY8UyQ",
    "liverpool.png": "https://drive.google.com/drive/u/1/folders/18-1zg-DaWqWjTGsclcqk7XvStl-l5_jD",
    "mallorca.png": "https://drive.google.com/drive/u/1/folders/1_yWWVwNzRikp5xC0hElPJdqm1Ob21-4L",
    "city.png": "https://drive.google.com/drive/u/1/folders/1db5Q6SLyhjMqBBy1B_5p5PVHOnkcQB40",
    "napoli.png": "https://drive.google.com/drive/u/1/folders/1yZqkzkrll-jbRdBaWPrM19Ctupr0I6Tx",
    "psg.png": "https://drive.google.com/drive/u/1/folders/1LmOv7srn2h-E_37zFLF45w_6D6peJKqX",
    "leipzig.png": "https://drive.google.com/drive/u/1/folders/1EaXMf8NL8neRNECQV9YjHVV67FUxwl0j",
    "stuttgart.png": "https://drive.google.com/drive/u/1/folders/1QUGlh47uM-6VwbvXOpPvDHjadhYfrKta",
    "villarreal.png": "https://drive.google.com/drive/u/1/folders/10U-YB78Bqsny7cQ8iMFeb76ff41UzIh-",
    "wolfsburg.png": "https://drive.google.com/drive/u/1/folders/1RznACZfDV30ew-4cLQsQnMDCxOK0ck7V",
}


# ===== CSS / Layout =====
st.markdown(
    f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Anton&display=swap');

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
        --vpad: clamp(24px, 6vh, 56px);
        --line-w: 4px;
        --line-color: {YELLOW};
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

      .barroca-shell {{
        position: fixed;
        inset: var(--vpad) 0 var(--vpad) 0;
        display: flex;
        align-items: stretch;
        justify-content: stretch;
        box-sizing: border-box;
        width: 100%;
        height: auto;
      }}

      .barroca-row {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        width: 100%;
        height: 100%;
      }}

      .barroca-col {{
        height: 100%;
        padding: clamp(12px, 2vh, 24px);
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        gap: clamp(12px, 2vh, 24px);
      }}

      .barroca-col:not(:last-child) {{
        border-right: var(--line-w) solid var(--line-color);
      }}

      .section-title {{
        font-family: 'Anton', sans-serif;
        font-size: clamp(1.2rem, 4vmin, 2.2rem);
        font-weight: bold;
        color: var(--line-color);
        text-decoration: underline;
        text-underline-offset: 8px;
        margin-bottom: clamp(18px, 4vh, 36px);
      }}

      .logos-grid-externos {{
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: clamp(12px, 2vmin, 24px);
        align-items: center;
        justify-items: center;
        width: 100%;
      }}
      .logo-img {{
        height: clamp(72px, 10vh, 110px);
        width: clamp(72px, 10vh, 110px);
        object-fit: contain;
        transition: transform 0.2s ease-in-out;
      }}
      .logo-img:hover {{
        transform: scale(1.1);
      }}

      /* Botão-âncora com visual padronizado (igual ao Centro de Informações) */
      a.folder-btn {{
        background-color: white;
        color: #202020 !important;
        padding: 10px 20px;
        border-radius: 15px;
        text-align: left;
        font-size: 18px;
        font-family: 'Anton', sans-serif !important;
        font-weight: 400;
        text-transform: uppercase;
        box-shadow: 6px 6px 0px 0px #FABB48;
        border: 2px solid #FABB48;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        cursor: pointer;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        height: 72px;
        text-decoration: none !important;
      }}
      a.folder-btn:hover {{
        transform: scale(1.03);
        box-shadow: 8px 8px 0px 0px #FABB48;
        color: #202020 !important;
        border: 2px solid #FABB48;
        background-color: white !important;
        filter: none !important;
        opacity: 1 !important;
      }}

      /* Mobile */
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
        .barroca-shell {{ position: static; inset: auto; height: auto; width: 100%; }}
        .barroca-row {{ display: flex; flex-direction: column; gap: 0; height: auto; }}
        .barroca-col {{ border-right: none !important; border-bottom: var(--line-w) solid var(--line-color); }}
        .barroca-col:last-child {{ border-bottom: none; }}
        .logos-grid-externos {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
        a.folder-btn {{ height: 64px; font-size: 16px; border-radius: 14px; }}
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ==== Layout principal: 2 colunas ====
logos_html = "".join(
    [get_logo_html(logo, external_logo_links.get(logo, "#")) for logo in work_model_logos_files]
)

col2_buttons_html = """
<a class="folder-btn" role="button" href="https://drive.google.com/drive/u/1/folders/1dPULBvah1pSCTufASiBEQfGKbPO_Gzke" target="_blank">🚧 Modelos De Trabalho na Prática</a>
<div style="height: 28px;"></div>
<a class="folder-btn" role="button" href="https://drive.google.com/drive/u/1/folders/1rA8IBOzfegLLJRtl_9GgFh0tSjzxCOB3" target="_blank">✅ Checklist</a>
<div style="height: 28px;"></div>
<a class="folder-btn" role="button" href="https://drive.google.com/drive/u/1/folders/1k3GpCbc5nQWIMz9qw0zellwHgYmO912G" target="_blank">👤 Modelos de Trabalhos Autorais</a>
"""

st.markdown(
    f"""
    <div class="barroca-shell">
      <div class="barroca-row">
        <div class="barroca-col">
          <div class="section-title">Modelos de Trabalho Externos</div>
          <div class="logos-grid-externos">
            {logos_html}
          </div>
        </div>
        <div class="barroca-col">
          <div class="section-title">Modelos de Trabalho Internos</div>
          <div style="width: 100%; max-width: 560px; margin: 0 auto;">{col2_buttons_html}</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


