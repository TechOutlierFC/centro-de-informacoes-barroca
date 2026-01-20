import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="OutlierFC", page_icon="🧠", layout="wide")

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

try:
    query_params = st.query_params
    if "go" in query_params and query_params["go"] == "home":
        query_params.clear()
        try:
            st.switch_page("pages/home.py")
        except Exception:
            st.markdown("""
            <script>
            try { window.location.href = './home'; } catch (e) {}
            </script>
            """, unsafe_allow_html=True)
except AttributeError:
    pass

st.markdown('<a href="?go=home" target="_self" class="back-button" title="Voltar à página inicial"> &#x21A9; </a>', unsafe_allow_html=True)

YELLOW = "#FFA500"

folder_icons = {
    "Números na Carreira": "📊",
    "Em Breve": "⏳"
}

folders = ["Números na Carreira", "Em Breve"]

folder_links = {
    "Números na Carreira": "/numeros_carreira"
}

st.markdown(
    f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Anton&display=swap');

      html, body, .stApp, [data-testid="stAppViewContainer"],
      section.main, .main, .block-container {{
        height: 100dvh !important;
        max-height: 100dvh !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
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

      /* Botão-âncora para pastas que redirecionam */
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

      /* Espaçamento entre botões (mesma linha e entre linhas) */
      [data-testid="column"] {{
        padding-left: 14px !important;
        padding-right: 14px !important;
        box-sizing: border-box;
      }}
      div[data-testid="stButton"] {{
        margin-bottom: 20px !important;
      }}

      /* ====== MOBILE ONLY ====== */
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

        /* Empilhar tudo em coluna com espaçamento adequado */
        .folders-grid [data-testid="stHorizontalBlock"] {{
          display: flex !important;
          flex-direction: column !important;
          gap: 0 !important;
          width: 100% !important;
          margin: 0 !important;
          padding: 0 !important;
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
          margin-bottom: 0 !important;
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
        div[data-testid="stButton"] > button p {{
          font-size: 16px !important;
          line-height: 1.2 !important;
          white-space: nowrap !important;
          overflow: hidden !important;
          text-overflow: ellipsis !important;
        }}
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

        /* Botão de voltar levemente menor */
        .back-button {{
          width: 36px;
          height: 36px;
          top: 14px;
          left: 14px;
        }}
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

st.markdown(
    """
    <div class="top-section">
        <div class="page-title">OutlierFC</div>
        <div class="page-subtitle">Selecione a página abaixo para ser direcionado ao painel correspondente.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Layout com 2 colunas para os botões
left_pad, content_col, right_pad = st.columns([0.1, 0.8, 0.1])

with content_col:
    st.markdown('<div class="folders-grid">', unsafe_allow_html=True)
    
    # Primeira linha com 2 botões
    cols = st.columns([1, 0.1, 1])
    
    # Botão "Números na Carreira"
    with cols[0]:
        icon = folder_icons.get("Números na Carreira", "📊")
        st.markdown(
            f'<a class="folder-btn" role="button" href="{folder_links["Números na Carreira"]}" target="_self">{icon} Números na Carreira</a>',
            unsafe_allow_html=True,
        )
    
    # Botão "Em Breve"
    with cols[2]:
        icon = folder_icons.get("Em Breve", "⏳")
        st.button(
            label=f'{icon} Em Breve',
            key="folder_em_breve",
            width='stretch'
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
