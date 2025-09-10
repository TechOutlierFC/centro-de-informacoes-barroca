import streamlit as st

st.set_page_config(page_title="Barroca 360°", page_icon="👤", layout="wide")

try:
    query_params = st.query_params
    # Abrir modal via query param
    if "modal" in query_params:
        st.session_state.modal_barroca = query_params["modal"]
        query_params.clear()
    elif "go" in query_params:
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
        flex-direction: column;
        align-items: flex-start;
        box-sizing: border-box;
        width: 100%;
        height: calc(100vh - 2 * var(--vpad));
      }}

      .barroca-row {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        width: 100%;
        height: 100%;
        gap: clamp(20px, 4vh, 40px);
      }}

      .barroca-col {{
        height: calc(100vh - 2 * var(--vpad));
        max-height: calc(100vh - 2 * var(--vpad));
        padding: clamp(15px, 3vh, 30px);
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        gap: clamp(12px, 2vh, 18px);
        overflow-y: auto;
        overflow-x: hidden;
      }}

      .buttons-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        width: 100%;
        max-width: 560px;
        margin: 0 auto;
      }}

      .section-title {{
        margin-bottom: 20px !important;
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
        width: 100%;
        text-align: center;
      }}

      /* ===== Modal (st.dialog) custom styling ===== */
      [data-testid="stDialog"] > div {{
        padding: 28px 32px !important;
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.18) !important;
      }}
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
      .modal-header-row {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
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
      a.modal-btn:hover {{
        transform: scale(1.03);
        box-shadow: 6px 6px 0px 0px #FABB48;
        color: #202020 !important;
        border: 2px solid #FABB48;
        background-color: white !important;
        filter: none !important;
        opacity: 1 !important;
      }}
      .modal-options-container {{
        max-height: 400px;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 10px 25px 10px 10px;
        margin-right: -25px;
      }}

      /* Botão-âncora com visual padronizado (igual ao Centro de Informações) */
      a.folder-btn {{
        background-color: white;
        color: #202020 !important;
        padding: 10px 20px;
        border-radius: 15px;
        text-align: center;
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
        justify-content: center;
        width: 90%;
        height: 60px;
        text-decoration: none !important;
        margin-bottom: 12px;
        word-wrap: break-word;
        hyphens: auto;
        line-height: 1.2;
        gap: 8px;
      }}

      .btn-icon {{
        font-size: 20px;
        flex-shrink: 0;
      }}

      .btn-text {{
        flex: 1;
        text-align: center;
        font-size: 16px;
      }}
      a.folder-btn:hover {{
        transform: scale(1.03);
        box-shadow: 6px 6px 0px 0px #FABB48;
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
        .barroca-col {{
          border-right: none !important;
          border-bottom: var(--line-w) solid var(--line-color);
          height: auto;
          max-height: none;
          overflow-y: visible;
        }}
        .barroca-col:last-child {{ border-bottom: none; }}

        /* Ajustes para mobile */
        .buttons-grid {{
          gap: 8px;
          max-width: none;
          padding: 0 10px;
        }}

        a.folder-btn {{
          height: 45px;
          font-size: 12px;
          border-radius: 10px;
          padding: 6px 8px;
          line-height: 1.1;
          gap: 6px;
        }}

        .btn-icon {{
          font-size: 16px;
        }}

        .btn-text {{
          font-size: 10px;
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
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Ícones para os botões
icons = {
    # Pessoal
    "Fé": "✝️",
    "Férias e Lazer": "🏖️",
    "Metas do Futuro": "🎯",
    "Obrigações Familiares": "👨‍👩‍👧‍👦",
    "Planejamento Financeiro": "💰",
    "Saúde e Qualidade de Vida": "🏃‍♂️",
    # Profissional
    "A-Rio": "🌊",
    "Comunicação": "💬",
    "Cursos": "🎓",
    "Eduardo Uram": "👤",
    "Escritório": "🏢",
    "Estudos": "📚",
    "Ideallize": "💡",
    "Livro": "📖",
    "Mercado": "📈",
    "Outlier": "📊"
}

# Botões da coluna pessoal (em ordem alfabética)
pessoal_buttons = [
    "Fé",
    "Férias e Lazer",
    "Metas do Futuro",
    "Obrigações Familiares",
    "Planejamento Financeiro",
    "Saúde e Qualidade de Vida"
]

# Botões da coluna profissional (em ordem alfabética)
profissional_buttons = [
    "A-Rio",
    "Comunicação",
    "Cursos",
    "Eduardo Uram",
    "Escritório",
    "Estudos",
    "Ideallize",
    "Livro",
    "Mercado",
    "Outlier"
]

# ===== Modais Barroca 360 (profissional/pessoal) =====

# SVGs (linha, 20x20) para itens dos modais
handshake_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M12 5l3 3-7 7-3-3z"></path><path d="M18 8l3 3-7 7-3-3"></path><path d="M2 12l3 3"></path></svg>
"""
history_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M3 3v5h5"></path><path d="M3.05 13A9 9 0 1 0 8 3.46"></path><path d="M12 7v5l3 3"></path></svg>
"""
calendar_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
"""
shield_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
"""
target_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><circle cx="12" cy="12" r="8"></circle><circle cx="12" cy="12" r="3"></circle><line x1="12" y1="2" x2="12" y2="5"></line><line x1="12" y1="19" x2="12" y2="22"></line><line x1="2" y1="12" x2="5" y2="12"></line><line x1="19" y1="12" x2="22" y2="12"></line></svg>
"""
tools_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M3 7l2 2 3-3-2-2"></path><path d="M13 7l8 8"></path><path d="M7 13l-4 4 4 4 4-4"></path></svg>
"""
repeat_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path></svg>
"""
layers_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
"""
file_dollar_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M9 13h6"></path><path d="M12 10v6"></path></svg>
"""
link_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M10 13a5 5 0 0 1 7 0l1 1a5 5 0 0 1 0 7 5 5 0 0 1-7 0l-1-1"></path><path d="M14 11a5 5 0 0 1-7 0l-1-1a5 5 0 0 1 0-7 5 5 0 0 1 7 0l1 1"></path></svg>
"""
briefcase_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"></path></svg>
"""
umbrella_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M3 14a9 9 0 0 1 18 0Z"></path><path d="M12 14v7"></path><path d="M12 18a4 4 0 0 1-4 4"></path></svg>
"""
rocket_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M5 13l4 4"></path><path d="M14 4l6 6"></path><path d="M5 13a10 10 0 0 1 14-7l-7 14a10 10 0 0 1-7-7z"></path></svg>
"""
cart_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 12.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
"""
sliders_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line></svg>
"""
star_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><polygon points="12 2 15 8.5 22 9.3 17 14 18.5 21 12 17.8 5.5 21 7 14 2 9.3 9 8.5 12 2"></polygon></svg>
"""
award_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><circle cx="12" cy="8" r="7"></circle><path d="M8.21 13.89L7 23l5-3 5 3-1.21-9.11"></path></svg>
"""
mic_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><rect x="9" y="2" width="6" height="11" rx="3" ry="3"></rect><path d="M5 10v2a7 7 0 0 0 14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
"""
file_text_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
"""
slash_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><line x1="4" y1="19" x2="20" y2="5"></line></svg>
"""
alert_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="modal-icon"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
"""

modal_configs = {
    # Profissional
    "ideallize": {
        "dialog_title": "Barroca Profissional",
        "subtitle": "Ideallize - Acessoria de Imprensa",
        "options": [
            {"icon": handshake_icon, "label": "Prospecção"},
            {"icon": history_icon, "label": "Histórico"},
            {"icon": calendar_icon, "label": "Reuniões"},
            {"icon": shield_icon, "label": "Defesa de Imagem"},
            {"icon": target_icon, "label": "Pré e Pós-Jogos"},
        ],
    },
    "outlier": {
        "dialog_title": "Barroca Profissional",
        "subtitle": "Outlier",
        "options": [
            {"icon": tools_icon, "label": "Apoio Técnico"},
            {"icon": repeat_icon, "label": "Rotinas"},
            {"icon": layers_icon, "label": "Construções"},
        ],
    },
    "a_rio": {
        "dialog_title": "Barroca Profissional",
        "subtitle": "A-Rio - Contábil",
        "options": [
            {"icon": file_dollar_icon, "label": "IR"},
            {"icon": link_icon, "label": "Footlink"},
            {"icon": briefcase_icon, "label": "EB Serviços Esportivos"},
            {"icon": umbrella_icon, "label": "Aposentadoria"},
        ],
    },
    "livro": {
        "dialog_title": "Barroca Profissional",
        "subtitle": "Livro",
        "options": [
            {"icon": rocket_icon, "label": "Lançamento"},
            {"icon": cart_icon, "label": "Vendas"},
            {"icon": sliders_icon, "label": "Controle"},
            {"icon": target_icon, "label": "Alcance"},
            {"icon": mic_icon, "label": "Mídia"},
        ],
    },
    "escritorio": {
        "dialog_title": "Barroca Profissional",
        "subtitle": "Escritório",
        "options": [
            {"icon": tools_icon, "label": "Produção"},
            {"icon": star_icon, "label": "Reputação"},
        ],
    },
    "cursos": {
        "dialog_title": "Barroca Profissional",
        "subtitle": "Cursos",
        "options": [
            {"icon": award_icon, "label": "CBF Academy"},
            {"icon": mic_icon, "label": "Palestras em Geral"},
        ],
    },
    "eduardo_uram": {
        "dialog_title": "Barroca Profissional",
        "subtitle": "Eduardo Uram",
        "options": [
            {"icon": file_text_icon, "label": "Contratos"},
            {"icon": slash_icon, "label": "Recisões"},
            {"icon": alert_icon, "label": "Passivos em Geral"},
        ],
    },
}

def render_barroca_modal(config):
    # Título interno do conteúdo do modal deve ser o título específico da opção
    header_html = (
        f'<div class="modal-header-row">'
        f'<div class="modal-title-text">{config.get("subtitle", "")}</div>'
        f'</div>'
    )

    options_html = ""
    for opt in config["options"]:
        # Links ainda não prontos: href="#" e sem target
        options_html += (
            f'<a class="modal-btn" role="button" href="#">{opt["icon"]}'
            f'<span class="modal-btn-text">{opt["label"]}</span></a>'
        )

    full_html = (
        f'<div class="custom-modal-content">'
        f'{header_html}'
        f'<div class="modal-subtitle">Selecione uma das opções abaixo:</div>'
        f'<div class="modal-options-container">{options_html}</div>'
        f'</div>'
    )

    st.markdown(full_html, unsafe_allow_html=True)

# Exibir modal quando query param definir
modal_key = st.session_state.get('modal_barroca')
if modal_key and modal_key in modal_configs:
    # Limpa para evitar reabertura em re-renders
    st.session_state.modal_barroca = None

    config = modal_configs[modal_key]

    @st.dialog(config["dialog_title"])
    def show_barroca_modal():
        render_barroca_modal(config)

    show_barroca_modal()

# Mapeamento de botões para slugs de modal
button_to_modal = {
    "Ideallize": "ideallize",
    "Outlier": "outlier",
    "A-Rio": "a_rio",
    "Livro": "livro",
    "Escritório": "escritorio",
    "Cursos": "cursos",
    "Eduardo Uram": "eduardo_uram",
}

# ==== Layout principal: 2 colunas ====
def create_buttons_grid(buttons_list):
    """Cria um grid de botões com 2 colunas por linha"""
    html = '<div class="buttons-grid">'
    for button_text in buttons_list:
        icon = icons.get(button_text, "📁")  # Fallback para ícone genérico
        modal_slug = button_to_modal.get(button_text)
        href = f'?modal={modal_slug}' if modal_slug else '#'
        html += f'<a class="folder-btn" href="{href}" target="_self" title="{button_text}"><span class="btn-icon">{icon}</span><span class="btn-text">{button_text}</span></a>'
    html += '</div>'
    return html

pessoal_buttons_html = create_buttons_grid(pessoal_buttons)
profissional_buttons_html = create_buttons_grid(profissional_buttons)

st.markdown(
    f"""
    <div class="barroca-shell">
      <div class="barroca-row">
        <div class="barroca-col">
          <div class="section-title">Eduardo Barroca - Pessoal</div>
          {pessoal_buttons_html}
        </div>
        <div class="barroca-col">
          <div class="section-title">Eduardo Barroca - Profissional</div>
          {profissional_buttons_html}
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
