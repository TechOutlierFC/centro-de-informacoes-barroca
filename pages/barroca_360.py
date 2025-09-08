import streamlit as st

st.set_page_config(page_title="Barroca 360°", page_icon="👤", layout="wide")

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
    "Idealizze": "💡",
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
    "Idealizze",
    "Livro",
    "Mercado",
    "Outlier"
]

# ==== Layout principal: 2 colunas ====
def create_buttons_grid(buttons_list):
    """Cria um grid de botões com 2 colunas por linha"""
    html = '<div class="buttons-grid">'
    for button_text in buttons_list:
        icon = icons.get(button_text, "📁")  # Fallback para ícone genérico
        html += f'<a class="folder-btn" href="#" title="{button_text}"><span class="btn-icon">{icon}</span><span class="btn-text">{button_text}</span></a>'
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
