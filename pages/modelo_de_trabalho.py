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
    "ajax.png": "https://drive.google.com/drive/u/7/folders/1XEQBTl-lrc29ycV75jmZU2kqUC4tykw9",
    "bilbao.png": "https://drive.google.com/drive/u/7/folders/15lJN7pKisilMm3RxqdRwHtEfqmPQ6Ltw",
    "atletico_madrid.png": "https://drive.google.com/drive/u/7/folders/174BoMTKqDYXXzZvLgIxvJhDylwO8_Tof",
    "leverkusen.png": "https://drive.google.com/drive/u/7/folders/1kg7jkVg3eQYutSq1lQJiHitXlac9HLv3",
    "dortmund.png": "https://drive.google.com/drive/u/7/folders/1NvTUfjU2Fytc2JWdzpD29iKC3DicjvD0",
    "monchengladbach.png": "https://drive.google.com/drive/u/7/folders/1BcyriJv_8HLRfVi-WwsDa8MJds2lHRCi",
    "chelsea.png": "https://drive.google.com/drive/u/7/folders/18o8m2wuBJswVkWAL9TjpzAAkJuSJ_Wlt",
    "brugge.png": "https://drive.google.com/drive/u/7/folders/1kl7UiLqEdDX82ZaY_9FNhyamjFB0q6PY",
    "crystal_palace.png": "https://drive.google.com/drive/u/7/folders/1axl7NXQ37sOe7ptFI_sWYTHPSs3m8DFh",
    "everton.png": "https://drive.google.com/drive/u/7/folders/1e5ul46khoOpUEJOX0YeLtjmI9pTV9Bv8",
    "barcelona.png": "https://drive.google.com/drive/u/7/folders/1msO86w_sAA7xOmtpJj32fnSggV1zjlwP",
    "bayern.png": "https://drive.google.com/drive/u/7/folders/1_qic_GgS5a3TpzTJBsgs_-U9FHGugRY_",
    "schalke.png": "https://drive.google.com/drive/u/7/folders/1Ls2vL5uwEmZpFYwiY6KvlBwjSKN9B_HU",
    "mainz.png": "https://drive.google.com/drive/u/7/folders/1RS4ZML8ByCqCv2LMvLzYvH8rxBD0gq01",
    "hibernian.png": "https://drive.google.com/drive/u/7/folders/1dFzt1_AnOdV2mzo0f3XkB_2RYy8k5QYa",
    "inter.png": "https://drive.google.com/drive/u/7/folders/1klpLsuyHqOlDbSZDska7fUWfcpmbFj0n",
    "liverpool.png": "https://drive.google.com/drive/u/7/folders/1_v5yxYzC7NKSX5Kde1nTjsVGhWvjFZyH",
    "mallorca.png": "https://drive.google.com/drive/u/7/folders/1sw7TCeHh-2KjacBYgsQzEUXYpeahczCA",
    "city.png": "https://drive.google.com/drive/u/7/folders/1yMbqSt8Moub0gr8Cw3rELCjc59cPRGId",
    "napoli.png": "https://drive.google.com/drive/u/7/folders/1zoCh_lbCRTZWIhmR1DQPTpz-BZaTgutU",
    "psg.png": "https://drive.google.com/drive/u/7/folders/1Is3jysjYXF--LfTRcV4gn2j6e3RTzylq",
    "leipzig.png": "https://drive.google.com/drive/u/7/folders/1kaH_Netawgy2KclrizCmIDQIEDrx3LEY",
    "stuttgart.png": "https://drive.google.com/drive/u/7/folders/1WEYZtGtLGmi3UHDeiufG8wDLml-Q3FCM",
    "villarreal.png": "https://drive.google.com/drive/u/7/folders/1khtfZI7K9VAMeykZjDvWQ2ETTXAm3Pzy",
    "wolfsburg.png": "https://drive.google.com/drive/u/7/folders/12f_VpGYFG3UCw7FVQIFVV1U0BVttiT8F",
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
<a class="folder-btn" role="button" href="https://drive.google.com/drive/u/7/folders/1tK_ew-TaFyBSUY5oDwSr3FIbFbYgG93I" target="_blank">✅ Checklist</a>
<div style="height: 28px;"></div>
<a class="folder-btn" role="button" href="https://drive.google.com/drive/u/7/folders/1aMjM3fQs7S_yqK0Yp_UG26C52yidxzLR" target="_blank">👤 Modelos de Trabalhos Autorais</a>
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


