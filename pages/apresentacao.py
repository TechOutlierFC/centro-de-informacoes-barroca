# pages/apresentação.py

import streamlit as st

st.set_page_config(page_title="Apresentação Barroca", page_icon="🏆", layout="wide")

YELLOW = "#FFA500"

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
        display: flex;
        width: 100%;
        height: 100%;
        gap: 0; /* borda encostando */
      }}

      .barroca-col {{
        flex: 1 1 0;
        height: 100%;
        padding: 16px;
        box-sizing: border-box;
      }}

      /* Divisórias verticais amarelas com altura exata da área visível */
      .barroca-col:not(:last-child) {{
        border-right: var(--line-w) solid var(--line-color);
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- LAYOUT: 3 colunas vazias, barras com altura total visível ---
st.markdown(
    """
    <div class="barroca-shell">
      <div class="barroca-row">
        <div class="barroca-col"></div>
        <div class="barroca-col"></div>
        <div class="barroca-col"></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
