import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Centro de Informações", page_icon="🗂️", layout="wide")

LOGO_DIR = Path("public/logos")

def get_image_as_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Arquivo de imagem não encontrado em: {path}")
        return ""

def get_logo_html(filename, class_name="logo-img", link="#"):
    logo_path = LOGO_DIR / filename
    ext = logo_path.suffix.strip('.')
    encoded_logo = get_image_as_base64(logo_path)
    if encoded_logo:
        target = "_self" if link.startswith("?") else "_blank"
        return f'<a href="{link}" target="{target}"><img class="{class_name}" src="data:image/{ext};base64,{encoded_logo}" alt="{filename}"></a>'
    return ""

if 'show_logos' not in st.session_state:
    st.session_state.show_logos = False
if 'active_logo_section' not in st.session_state:
    st.session_state.active_logo_section = None
if 'modal_team' not in st.session_state:
    st.session_state.modal_team = None

try:
    query_params = st.query_params
    if "modal" in query_params:
        st.session_state.modal_team = query_params["modal"]
        query_params.clear()
    # Navegação robusta para "voltar" (evita depender de "/" no Streamlit Cloud)
    elif "go" in query_params and query_params["go"] == "home":
        # Limpa os parâmetros para evitar loops e tenta trocar de página
        query_params.clear()
        try:
            st.switch_page("app.py")
        except Exception:
            # Fallback seguro para recarregar a raiz relativa
            st.markdown("""
            <script>
            try { window.location.href = './'; } catch (e) {}
            </script>
            """, unsafe_allow_html=True)
except AttributeError:
    pass

youtube_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon">
    <path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2A29 29 0 0 0 23 11.75a29 29 0 0 0-.46-5.33z"></path>
    <polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon>
</svg>
"""

drive_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon">
    <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
    <polyline points="2 17 12 22 22 17"></polyline>
    <polyline points="2 12 12 17 22 12"></polyline>
</svg>
"""

modal_configs = {
    "mirassol": {
        "title": "MIRASSOL",
        "logo": "mirassol.png",
        "dialog_title": "Treinos / Jogos e Compactos",
        "options": [
            {"icon": youtube_icon, "label": "Treinamentos", "link": "https://www.youtube.com/playlist?list=PLgcT6qQPwPHgfUi6bRCwuVt5jCS68my3M"},
            {"icon": youtube_icon, "label": "Resumo", "link": "https://www.youtube.com/playlist?list=PLgcT6qQPwPHi55ZWKRTf9hHrJUOhcJWYE"},
            {"icon": drive_icon, "label": "ProSoccer", "link": "https://drive.google.com/drive/folders/1y6OSjIA7ggzcrLSJaTPvplBdop2x39iD"},
            {"icon": drive_icon, "label": "Desenvolvimento Individual", "link": "https://drive.google.com/drive/u/1/folders/1UrFKAF0s8HKAirV0sXjZmB9uAw5YN3G2?hl=pt-br"},
        ]
    },
    "avai": {
        "title": "AVAÍ",
        "logo": "avai.png",
        "dialog_title": "Treinos / Jogos e Compactos",
        "options": [
            {"icon": drive_icon, "label": "Treinamentos", "link": "https://drive.google.com/drive/u/1/folders/1dzMCut0Wbt-Mqy0K_NUaS4EJP0_FGl6H?hl=pt-br"},
            {"icon": youtube_icon, "label": "Jogos Série B - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW9NQ0M06fy30nW_v4muAfYV"},
            {"icon": youtube_icon, "label": "Jogos Catarinense - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW-rvLi0FR8ukfBpx21xxCNM"},
            {"icon": youtube_icon, "label": "Compactos Série B - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW9LB18AHWXq0zFPLuYOF-o-"},
            {"icon": youtube_icon, "label": "Compactos Catarinense - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW_OzQCiIlX9jAGDGp0wd0B4"},
            {"icon": youtube_icon, "label": "Treinos Janeiro - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW91NqOTu-vki8rRYadN9Cq9"},
            {"icon": youtube_icon, "label": "Treinos Fevereiro - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW9RCqU1cUoMJZNljkWCjF8P"},
            {"icon": youtube_icon, "label": "Treinos Março - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW9XqOyAtBV9URr_O7JZVvIx"},
            {"icon": youtube_icon, "label": "Treinos Abril - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW_k2uSPD9FLqUVDs3OOyZ0B"},
            {"icon": youtube_icon, "label": "Treinos Maio - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW_ODB4yPRJcicxQ0uIP-bW4"},
            {"icon": youtube_icon, "label": "Treinos Junho - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW-Wp6oCkcJwRbJTQtlLBUmC"},
            {"icon": youtube_icon, "label": "Desenvolvimento Individual - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW-Wp6oCkcJwRbJTQtlLBUmC"},
            {"icon": youtube_icon, "label": "Intercorrências / Lesões - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW_wwlk6dHkTkM1-pkdwV-sk"},
        ]
    },
    "avai_prelecoes": {
        "title": "AVAÍ",
        "logo": "avai.png",
        "dialog_title": "Preleções",
        "options": [
            {"icon": drive_icon, "label": "Série B - 2024", "link": "https://drive.google.com/drive/folders/1EstvgKUL9NebBoHxHJkd5Ka23Xu48KWL"},
            {"icon": drive_icon, "label": "Catarinense - 2024", "link": "https://drive.google.com/drive/folders/1tAafifOJ6ZstMJyDgf1Syaw5QrpyPYwv"},
            {"icon": youtube_icon, "label": "Apresentações - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW_v2h7NPr4xvPpDG9cSNGtK"},
            {"icon": youtube_icon, "label": "TV - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW_WDJNfookf4KPg3yFLlM1V"},
            {"icon": drive_icon, "label": "Relatórios Mensais - 2024", "link": "https://drive.google.com/drive/folders/1S5HAAsnYeyYMaqVSVML3f3SnzJp5poUE"},
            {"icon": drive_icon, "label": "Estatísticas Série B - 2024", "link": "https://drive.google.com/drive/folders/1shwUfvzgQ9fy6p3ZxY1G6YRv2EijJeER"},
            {"icon": drive_icon, "label": "Estatísticas Catarinense - 2024", "link": "https://drive.google.com/drive/folders/1W9CRbTjkrKZPfkidk1LHqMSqCM6k1vFz"},
        ]
    },
    "mirassol_feedbacks": {
        "title": "MIRASSOL",
        "logo": "mirassol.png",
        "dialog_title": "Feedbacks",
        "options": [
            {"icon": youtube_icon, "label": "Feedbacks Profissional - 2025", "link": "https://www.youtube.com/playlist?list=PLgcT6qQPwPHgraumM8hYKDByMOKCOfGIR"},
            {"icon": drive_icon, "label": "Estudo OutlierFC", "link": "https://drive.google.com/drive/u/1/folders/1E5bkfK5FfFkFQfjrhaP9facCmVrdjffd?hl=pt-br"},
        ]
    },
    "avai_feedbacks": {
        "title": "AVAÍ",
        "logo": "avai.png",
        "dialog_title": "Feedbacks",
        "options": [
            {"icon": youtube_icon, "label": "Pós-Jogo Série B - 2024", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW9tEgrPuWh5KT5d9ZN7OIxo"},
            {"icon": youtube_icon, "label": "Pós-Jogo Catarinense", "link": "https://www.youtube.com/playlist?list=PLO-okjzqdIW-tfrnwYjuXdYDeNTBkkokx"},
        ]
    }
}

def team_modal(config):
    encoded_logo = get_image_as_base64(LOGO_DIR / config["logo"])
    header_html = (
        f'<div class="modal-header-row">'
        f'<img class="modal-logo" src="data:image/png;base64,{encoded_logo}" alt="{config["title"]}" />'
        f'<div class="modal-title-text">{config["title"]}</div>'
        f'</div>'
    ) if encoded_logo else (
        '<div class="modal-header-row">'
        f'<div class="modal-title-text">{config["title"]}</div>'
        '</div>'
    )

    options_html = "".join([
        f'<a class="modal-btn" role="button" href="{opt["link"]}" target="_blank">{opt["icon"]}<span class="modal-btn-text">{opt["label"]}</span></a>'
        for opt in config["options"]
    ])

    full_html = f"""
    <div class="custom-modal-content">
        {header_html}
        <div class="modal-subtitle">Selecione uma das opções abaixo:</div>
        <div class="modal-options-container">
            {options_html}
        </div>
    </div>
    """
    st.markdown(full_html, unsafe_allow_html=True)


team_to_show = st.session_state.get('modal_team')
if team_to_show and team_to_show in modal_configs:
    st.session_state.modal_team = None
    
    config = modal_configs[team_to_show]

    @st.dialog(config["dialog_title"])
    def show_generic_modal():
        team_modal(config)
    
    show_generic_modal()

def toggle_logos():
    st.session_state.show_logos = not st.session_state.show_logos

def hide_logos():
    st.session_state.show_logos = False

st.markdown('<a href="?go=home" target="_self" class="back-button" title="Voltar à página inicial"> &#x21A9; </a>', unsafe_allow_html=True)

YELLOW = "#FFA500"

folder_icons = {
    "Adversários": "🆚",
    "Bastidores": "🎬",
    "Clubes Alvo": "🎯",
    "Feedbacks": "💬",
    "Mercado e Banco de Dados": "📈",
    "Modelo de Jogo": "⚽",
    "Modelo de Trabalho": "🛠️",
    "Preleções": "🗣️",
    "Referências Externas": "🌐",
    "Referências OutlierFC": "🧠",
    "Treinos / Jogos e Compactos": "📼"
}

folders = sorted(folder_icons.keys())

folder_links = {
    "Referências Externas": "https://drive.google.com/drive/u/1/folders/1GjfWOd35YuA1FhpzXPUFG8a41ByANlhc",
    "Mercado e Banco de Dados": "https://drive.google.com/drive/u/1/folders/1er6TRhp4N4gB7nbo-XpxOv_2fadDpf2w",
    "Clubes Alvo": "https://drive.google.com/drive/u/1/folders/19HOmXsn-ewfPaD5TBipojWCXu8c8a3_k",
    "Referências OutlierFC": "https://drive.google.com/drive/u/1/folders/1G8EpSiV9yNHZlqV0v6PWtx2aXHOMhI83",
    "Modelo de Trabalho": "https://drive.google.com/drive/u/1/folders/1xuPsdW1XaCCiuPstdOxcMHYoTpsYBOFg"
}

model_logos_files = [
    "mirassol.png", "crb.png", "avai.png", "ceara.png",
    "vitoria.png", "coritiba.webp", "botafogo.png"
]
training_logos_files = [
    "mirassol.png", "avai.png", "vitoria.png", "coritiba.webp",
    "botafogo.png", "corinthians.png", "brasil.png", "crb.png"
]
model_logo_links = {
    "mirassol.png": "https://drive.google.com/file/d/1sAG41hCMiKccfndB08jQ8r6r0ubZAEIT/view",
    "crb.png": "https://drive.google.com/file/d/1iiHDqamKfmnfo6DI3-FNobaNRaBMZie6/view",
    "avai.png": "https://drive.google.com/file/d/14L690eI5qjkLePdTmpTpWDqbkDHq3ngk/view",
    "ceara.png": "https://drive.google.com/file/d/109HbeTFwMJVNPnam4wn5keJBTFHm-j1F/view",
    "vitoria.png": "https://drive.google.com/drive/u/1/folders/1zJcFNZ6Ai1x9TwsFN-ZwvA8rUYPFfh2f",
    "coritiba.webp": "https://drive.google.com/file/d/1Nr_uBLAvJ4uCCFWfhxdTbg_lIkalfXs-/view",
    "botafogo.png": "https://www.youtube.com/watch?v=jrPc_gdTRBc&ab_channel=BotafogoFRAnalise",
}

def build_logos_html(logo_files, section=None):
    links_map = dict(model_logo_links)
    if section and 'logo_link_overrides' in globals() and section in logo_link_overrides:
        links_map.update(logo_link_overrides[section])

    html_parts = []
    for logo in logo_files:
        class_name = "logo-item"
        if logo == "drive.png" and section == "Preleções":
            class_name += " drive-logo-prelecoes"
        html_parts.append(get_logo_html(logo, class_name, links_map.get(logo, "#")))

    return "".join(html_parts)

logo_sets = {
    "Modelo de Jogo": model_logos_files,
    "Adversários": ["crb.png", "avai.png"],
    "Treinos / Jogos e Compactos": training_logos_files,
    "Preleções": ["mirassol.png", "crb.png", "avai.png", "drive.png"],
    "Feedbacks": ["mirassol.png", "crb.png", "avai.png"],
    "Bastidores": ["crb.png"]
}

logo_link_overrides = {
    "Adversários": {
        "crb.png": "https://drive.google.com/drive/u/1/folders/1mqbqbGPaAvuqreEUx1vNZtfEBibv-LaY",
        "avai.png": "https://drive.google.com/drive/u/1/folders/1SHbQVTQVOAjF8Z65sujbBxDt-qV1zOXw",
    },
    "Treinos / Jogos e Compactos": {
        "mirassol.png": "?modal=mirassol",
        "avai.png": "?modal=avai",
        "vitoria.png": "https://drive.google.com/drive/u/1/folders/1ChLG6YEOAFG2reU8BKvnUFxL_KkwrDid?hl=pt-br",
        "coritiba.webp": "https://drive.google.com/drive/u/1/folders/1H7mn2PgIUHOlRJOxg0RFs_ricOpt1mdV?hl=pt-br",
        "botafogo.png": "https://drive.google.com/drive/u/1/folders/1FMlEn6qlpsH4ne-baCVYBra0XC9erurO?hl=pt-br",
        "corinthians.png": "https://drive.google.com/drive/u/1/folders/14sAmVS68jo7QNhLvR2flKTcLf7iNqrIL?hl=pt-br",
        "brasil.png": "https://drive.google.com/drive/u/1/folders/1G8yS3L5bP7toP2RjCl8nJycED7T7AkeR?hl=pt-br",
        "crb.png": "https://www.youtube.com/playlist?list=PLvHh7B7NkMhqXG9P0xNWlNT6IUPU9KmOn"
    },
    "Preleções": {
        "mirassol.png": "https://www.youtube.com/playlist?list=PLgcT6qQPwPHive6C_Mnty82kxH-z5ICy8",
        "crb.png": "https://drive.google.com/drive/folders/1Z8otxolgB7sZicz_c2owOHiKw9936ANS",
        "avai.png": "?modal=avai_prelecoes",
        "drive.png": "https://drive.google.com/drive/u/1/folders/1xG8Bbm2EypoWLFEee7u_vda9F22iQzGg"
    },
    "Feedbacks": {
        "mirassol.png": "?modal=mirassol_feedbacks",
        "crb.png": "https://www.youtube.com/playlist?list=PLvHh7B7NkMhqmM-UjXstIKW_mf9OXSMSG",
        "avai.png": "?modal=avai_feedbacks"
    },
    "Bastidores": {
        "crb.png": "https://www.youtube.com/playlist?list=PLvHh7B7NkMhpdXbKMGBU7JLtMGkk9fOkQ"
    }
}

def set_or_toggle_logos(section):
    if st.session_state.active_logo_section == section and st.session_state.show_logos:
        st.session_state.show_logos = False
        st.session_state.active_logo_section = None
    else:
        st.session_state.active_logo_section = section
        st.session_state.show_logos = True

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

      .info-shell {{
        position: fixed;
        inset: var(--vpad) 0 var(--vpad) 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0 clamp(24px, 5vw, 80px);
        box-sizing: border-box;
        width: 100%;
      }}

      .top-section {{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: clamp(12px, 2vh, 24px);
        flex: 1;
        overflow-y: auto;
        overflow-x: hidden;
        padding-bottom: 20px;
        padding-left: 20px;
        padding-right: 20px;
        box-sizing: border-box;
      }}

      .bottom-section {{
        width: 100%;
        min-height: 5vh;
        padding-top: 20px;
        flex-shrink: 0;
      }}

      .page-title {{
        font-size: clamp(2rem, 6vmin, 3.5rem);
        font-weight: bold;
        margin-bottom: 8px;
        font-family: 'Anton', sans-serif;
      }}
      .page-subtitle {{
        font-size: clamp(1rem, 3vmin, 1.5rem);
        color: #555;
        margin-bottom: clamp(16px, 3vh, 24px);
      }}

      div[data-testid="stButton"] > button {{
        background-color: white;
        color: #202020;
        padding: 10px 20px;
        border-radius: 15px;
        text-align: left;
        font-size: 18px;
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
      }}
      div[data-testid="stButton"] > button p {{
        font-family: 'Anton', sans-serif !important;
        font-size: 18px;
        font-weight: 400;
      }}
      div[data-testid="stButton"] > button:hover {{
        transform: scale(1.03);
        box-shadow: 8px 8px 0px 0px #FABB48;
        color: #202020;
        border: 2px solid #FABB48;
        background-color: white !important;
        filter: none !important;
        opacity: 1 !important;
      }}
      div[data-testid="stButton"] > button:focus {{
        box-shadow: 8px 8px 0px 0px #FABB48;
        color: #202020;
        border: 2px solid #FABB48;
        outline: none;
      }}

      /* Botão-âncora para pastas que redirecionam (p.ex. Referências Externas) */
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
        margin-bottom: 20px;
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
      a.folder-btn:focus {{
        box-shadow: 8px 8px 0px 0px #FABB48;
        color: #202020 !important;
        border: 2px solid #FABB48;
        outline: none;
      }}

      .logo-bar-container {{
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0;
        gap: 28px;
        flex-wrap: wrap;
        transition: all 0.3s ease-in-out;
        opacity: 0;
        transform: translateY(20px);
        visibility: hidden;
      }}
      .logo-bar-container.visible {{
        opacity: 1;
        transform: translateY(0);
        visibility: visible;
      }}
      .logo-item {{
        height: 85px;
        width: auto;
        transition: transform 0.2s ease-in-out;
      }}
      .logo-item:hover {{
        transform: scale(1.1);
      }}
      .drive-logo-prelecoes {{
        height: 70px; /* Altura reduzida para o logo do Drive */
      }}
      /* Desktop: largura total abaixo da linha de botões */
      .row-logos-wrapper {{
        width: 100%;
        padding: 0; /* sem padding extra */
        margin-top: -34px; /* aproxima ainda mais os logos da linha de botões */
        margin-bottom: 12px; /* leve respiro abaixo dos logos */
      }}
      .desktop-only .logo-bar-container {{
        width: 100%;
      }}
      .active-folder-underline {{ display: none; }}
      /* Linha de logos no desktop: ocupar toda a largura do container e não quebrar linha */
      .desktop-row-logos {{
        width: 100%;
        flex-wrap: wrap !important;
        justify-content: center !important;
        overflow: visible !important;
        padding: 0 24px !important; /* folga lateral para evitar scroll ao hover */
      }}
      /* Espaçamento entre botões (mesma linha e entre linhas) */
      [data-testid="column"] {{
        padding-left: 14px !important;
        padding-right: 14px !important;
        box-sizing: border-box;
      }}
      div[data-testid="stButton"] {{
        margin-bottom: 20px !important;
      }}

      /* ===== Modal (st.dialog) custom styling ===== */
      [data-testid="stDialog"] > div {{
        padding: 28px 32px !important;
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.18) !important;
      }}

      /* Close (X) button styling inside modal */
      [data-testid="stDialog"] button[aria-label="Close"],
      [data-testid="stDialog"] button[title="Close"],
      [data-testid="stDialog"] [aria-label="Close"] {{
        width: 36px !important;
        height: 36px !important;
        border-radius: 8px !important;
        background: white !important;
        border: 2px solid #FABB48 !important;
        box-shadow: none !important;
        outline: none !important;
        color: #202020 !important;
      }}
      [data-testid="stDialog"] button[aria-label="Close"]:hover,
      [data-testid="stDialog"] button[title="Close"]:hover,
      [data-testid="stDialog"] [aria-label="Close"]:hover {{
        transform: scale(1.03);
        box-shadow: none !important;
        outline: none !important;
        background-color: #f7f7f7 !important;
      }}

      .custom-modal-content {{
        padding: 8px 2px;
      }}
      .modal-options-container {{
        max-height: 400px; /* Altura máxima para os botões */
        overflow-y: auto; /* Adiciona scroll vertical se necessário */
        overflow-x: hidden;
        padding: 10px 25px 10px 10px; /* T R B L - Padding para hover e scroll */
        margin-right: -25px; /* Compensa o padding para esconder o scroll */
      }}
      .modal-header-row {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
      }}
      .modal-logo {{
        height: 32px;
        width: auto;
      }}
      .modal-title-text {{
        font-family: 'Anton', sans-serif !important;
        font-size: 20px;
        text-transform: uppercase;
        letter-spacing: 0.02em;
      }}
      .modal-subtitle {{
        font-size: 16px;
        color: #555;
        margin: 8px 0 16px 0;
      }}
      a.modal-btn {{
        background-color: white;
        color: #202020 !important;
        padding: 8px 16px;
        border-radius: 12px;
        text-align: left;
        font-size: 16px;
        font-family: 'Anton', sans-serif !important;
        font-weight: 400;
        text-transform: uppercase;
        box-shadow: 4px 4px 0px 0px #FABB48;
        border: 2px solid #FABB48;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        cursor: pointer;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        height: 56px;
        text-decoration: none !important;
        margin-bottom: 12px;
        gap: 12px;
      }}
      a.modal-btn .modal-btn-text {{
        flex-grow: 1;
      }}
      a.modal-btn:hover {{
        transform: scale(1.03);
        box-shadow: 6px 6px 0px 0px #FABB48;
        color: #202020 !important;
        border: 2px solid #FABB48;
        background-color: white !important;
        filter: none !important;
        opacity: 1 !important;
      }}
      /* Neutralizar margens/paddings de wrappers markdown no desktop dentro da grid */
      .folders-grid [data-testid="stMarkdownContainer"] {{
        margin: 0 !important;
        padding: 0 !important;
      }}
      .folders-grid [data-testid="stVerticalBlock"] {{
        margin: 0 !important;
        padding: 0 !important;
      }}
      /* Helpers para alternar layouts desktop/mobile sem afetar o desktop */
      .desktop-only {{ display: block; }}
      .mobile-only {{ display: none; }}
      .folder-spacer {{ height: 0; }}
      .row-spacer {{ height: 0; }}

      /* ====== MOBILE ONLY (não altera desktop) ====== */
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

        .top-section {{
          padding-top: 12px;
          padding-left: 12px;
          padding-right: 12px;
        }}

        /* Recuo lateral consistente do container de pastas */
        .folders-grid {{
          padding-left: clamp(12px, 4vw, 20px);
          padding-right: clamp(12px, 4vw, 20px);
        }}

        /* Lista mobile vertical (sem colunas do Streamlit) */
        .mobile-folders-list {{
          padding-left: clamp(12px, 4vw, 20px);
          padding-right: clamp(12px, 4vw, 20px);
        }}

        /* Empilhar tudo em coluna com espaçamento adequado */
        .folders-grid [data-testid="stHorizontalBlock"] {{
          display: flex !important;
          flex-direction: column !important;
          gap: 0 !important; /* evitamos gap para padronizar com margens controladas */
          width: 100% !important;
          margin: 0 !important;
          padding: 0 !important;
        }}
        /* Esconde colunas espaçadoras (2,4,6) no mobile para não gerar saltos de espaço */
        .folders-grid [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(2),
        .folders-grid [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(4),
        .folders-grid [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(6) {{
          display: none !important;
        }}
        .folders-grid [data-testid="column"] {{
          flex: 1 0 100% !important;
          width: 100% !important;
          padding-left: 6px !important;
          padding-right: 6px !important;
          padding-top: 0 !important;
          padding-bottom: 0 !important;
          margin: 0 !important;
        }}

        /* Zera margens/paddings internos de blocos verticais do Streamlit */
        .folders-grid [data-testid="stVerticalBlock"] {{
          margin: 0 !important;
          padding: 0 !important;
        }}

        /* Botões padronizados em tamanho/tipografia no mobile */
        div[data-testid="stButton"] > button,
        a.folder-btn {{
          height: 64px !important;
          font-size: 16px !important;
          border-radius: 14px !important;
          margin-bottom: 0 !important; /* espaçamento controlado pelo spacer */
          padding: 10px 16px !important;
          box-shadow: 5px 5px 0px 0px #FABB48 !important;
          width: min(560px, 88vw) !important;
          margin-left: auto !important;
          margin-right: auto !important;
          box-sizing: border-box !important;
          white-space: nowrap !important;
          overflow: hidden !important;
          text-overflow: ellipsis !important;
        }}
        /* O espaçamento entre itens será controlado apenas pelo spacer */
        div[data-testid="stButton"] > button {{
          margin-bottom: 0 !important; /* evita diferenças vs a.folder-btn */
          margin-top: 0 !important;
        }}
        div[data-testid="stButton"] > button p {{
          font-size: 16px !important;
          line-height: 1.2 !important;
          white-space: nowrap !important;
          overflow: hidden !important;
          text-overflow: ellipsis !important;
        }}
        /* Zera margens dos wrappers; espaçamento é controlado pelo spacer */
        div[data-testid="stButton"] {{
          margin-top: 0 !important;
          margin-bottom: 0 !important;
        }}
        a.folder-btn {{
          line-height: 1.2 !important;
          margin-top: 0 !important;
          margin-bottom: 0 !important;
        }}

        /* Padroniza espaçamento dos itens vindos de st.markdown (links de pasta) */
        .folders-grid [data-testid="stMarkdownContainer"] {{
          margin-top: 0 !important;
          margin-bottom: 0 !important;
        }}
        .folders-grid [data-testid="stMarkdownContainer"] p {{
          margin: 0 !important;
        }}

        /* Controla o espaçamento vertical padronizado entre itens */
        .folder-spacer {{ height: 24px; }}
        .row-spacer {{ height: 24px; }}

        /* Logos inline abaixo do botão clicado no mobile */
        .inline-logos-wrapper {{
          padding: 6px 8px 2px 8px;
          margin-top: 10px;
        }}
        .logo-bar-container {{
          display: grid !important;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          justify-items: center;
          gap: 16px;
          padding: 6px 0;
        }}
        .logo-item {{ height: 56px; }}
        .drive-logo-prelecoes {{ height: 52px; }}

        /* Alinhar logos inline à mesma largura do botão */
        .inline-logos-wrapper .logo-bar-container {{
          width: min(560px, 88vw);
          margin-left: auto;
          margin-right: auto;
        }}

        /* Modal refinado para mobile */
        [data-testid="stDialog"] > div {{
          padding: 20px 20px !important;
          width: min(92vw, 520px) !important;
          max-width: 92vw !important;
        }}
        .modal-title-text {{ font-size: 18px; }}
        .modal-subtitle {{ font-size: 14px; }}
        a.modal-btn {{
          height: 48px;
          font-size: 14px;
          gap: 10px;
          padding: 8px 12px;
          box-shadow: 3px 3px 0px 0px #FABB48;
        }}
        .modal-options-container {{
          max-height: 52vh;
          padding-right: 18px;
          margin-right: -18px;
        }}
        [data-testid="stDialog"] button[aria-label="Close"],
        [data-testid="stDialog"] button[title="Close"],
        [data-testid="stDialog"] [aria-label="Close"] {{
          width: 32px !important;
          height: 32px !important;
        }}

        /* Botão de voltar levemente menor */
        .back-button {{
          width: 36px;
          height: 36px;
          top: 14px;
          left: 14px;
        }}

        /* Alternância de visibilidade desktop/mobile */
        .desktop-only {{ display: none !important; }}
        .mobile-only {{ display: block !important; }}
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <script>
    (function() {
      function hideStrayDivText(root) {
        var nodes = root.querySelectorAll('p, div, span');
        for (var i = 0; i < nodes.length; i++) {
          var el = nodes[i];
          if (!el || !el.textContent) continue;
          var t = el.textContent.trim();
          if (t === '</div>' || t === '&lt;/div&gt;') {
            el.style.display = 'none';
          }
        }
      }
      var observer = new MutationObserver(function() { hideStrayDivText(document.body); });
      observer.observe(document.body, { childList: true, subtree: true });
      hideStrayDivText(document.body);
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

## Removido wrapper info-shell para evitar HTML desbalanceado entre re-renders

st.markdown(
    """
    <div class="top-section">
        <div class="page-title">Centro de Informações</div>
        <div class="page-subtitle">Selecione as pastas abaixo para ser redirecionado para o drive correspondente.</div>
    </div>
    """,
    unsafe_allow_html=True
)

rows = [folders[i:i + 4] for i in range(0, len(folders), 4)]
left_pad, content_col, right_pad = st.columns([0.05, 0.9, 0.05])

# Placeholders por pasta (mobile) e por linha (desktop)
folder_placeholders = {}
row_placeholders = {}

with content_col:
    st.markdown('<div class="folders-grid">', unsafe_allow_html=True)
    for row_index, row in enumerate(rows):
        cols = st.columns([1, 0.06, 1, 0.06, 1, 0.06, 1])
        for i, folder in enumerate(row):
            col = cols[i * 2]
            with col:
                icon = folder_icons.get(folder, "📁")
                if folder in ["Modelo de Jogo", "Adversários", "Treinos / Jogos e Compactos", "Preleções", "Feedbacks", "Bastidores"]:
                    is_active = (st.session_state.active_logo_section == folder and st.session_state.show_logos)
                    st.button(
                        label=f'{icon} {folder}',
                        on_click=lambda s=folder: set_or_toggle_logos(s),
                        key=f"folder_{folder}",
                        use_container_width=True
                    )
                    if is_active:
                        st.markdown('<div class="desktop-only active-folder-underline"></div>', unsafe_allow_html=True)
                elif folder in folder_links:
                    st.markdown(
                        f'<a class="folder-btn" role="button" href="{folder_links[folder]}" target="_blank">{icon} {folder}</a>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.button(
                        label=f'{icon} {folder}',
                        on_click=hide_logos,
                        key=f"folder_{folder}",
                        use_container_width=True
                    )

                # Placeholder mobile (logo abaixo do botão)
                folder_placeholders[folder] = st.empty()
                # Spacer padronizado (controla exclusivamente o espaçamento entre itens no mobile)
                st.markdown('<div class="folder-spacer mobile-only"></div>', unsafe_allow_html=True)
        # Placeholder desktop para a linha inteira de logos logo abaixo da linha de botões
        row_ph = st.empty()
        for f in row:
            row_placeholders[f] = row_ph
        # Spacer entre linhas (mobile)
        st.markdown('<div class="row-spacer mobile-only"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_logos and st.session_state.active_logo_section in logo_sets:
    section = st.session_state.active_logo_section
    logos_html = build_logos_html(logo_sets[section], section=section)
    
    # Limpa placeholders antes de renderizar o ativo
    for _name, _ph in folder_placeholders.items():
        _ph.empty()
    for _name, _rph in row_placeholders.items():
        _rph.empty()

    # Desktop: renderiza na largura total da linha (placeholder da linha)
    row_ph = row_placeholders.get(section)
    if row_ph is not None:
        row_ph.markdown(
            f"""
            <div class=\"row-logos-wrapper\">
              <div class=\"desktop-only\" style=\"width:100%;\">
                <div class=\"logo-bar-container visible desktop-row-logos\">
                  {logos_html}
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Mobile: renderiza no placeholder da pasta específica
    inline_ph = folder_placeholders.get(section)
    if inline_ph is not None:
        inline_ph.markdown(
            f"""
            <div class=\"mobile-only inline-logos-wrapper\">
              <div class=\"logo-bar-container visible\">
                {logos_html}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    # Não renderiza nada quando não há seção ativa
    pass

