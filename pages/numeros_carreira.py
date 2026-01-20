import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(page_title="Números na Carreira", page_icon="📊", layout="wide")

try:
    query_params = st.query_params
    if "go" in query_params:
        dest = query_params["go"]
        query_params.clear()
        try:
            if dest == "outlier":
                st.switch_page("pages/outlier_fc.py")
        except Exception:
            st.markdown(
                """
                <script>
                try { window.location.href = './outlier_fc'; } catch (e) {}
                </script>
                """,
                unsafe_allow_html=True,
            )
except AttributeError:
    pass

# Botão voltar seguindo padrão (usa query param e fallback de redirect do Streamlit)
st.markdown('<a href="?go=outlier" target="_self" class="back-button" title="Voltar à OutlierFC"> &#x21A9; </a>', unsafe_allow_html=True)

YELLOW = "#FFA500"

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

      .back-button {{
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 9999;
        background-color: white;
        border: 2px solid {YELLOW};
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

      .page-title {{
        font-size: clamp(2rem, 6vmin, 3.5rem);
        font-weight: bold;
        margin-bottom: 8px;
        font-family: 'Anton', sans-serif;
        text-align: center;
      }}

      .page-subtitle {{
        font-size: clamp(1rem, 3vmin, 1.5rem);
        color: #555;
        margin-bottom: clamp(16px, 3vh, 24px);
        text-align: center;
      }}

      @media (max-width: 768px) {{
        .back-button {{
          width: 36px;
          height: 36px;
          top: 14px;
          left: 14px;
        }}
      }}
      
      .viz-box {{
        background-color: white;
        color: #202020;
        padding: 8px 16px;
        border-radius: 14px;
        box-shadow: 6px 6px 0px 0px {YELLOW};
        border: 2px solid {YELLOW};
        box-sizing: border-box;
        overflow: hidden;
      }}
      .viz-title {{
        font-family: 'Anton', sans-serif !important;
        font-size: 18px;
        text-transform: uppercase;
        margin-bottom: 0px;
      }}
      .viz-value {{
        font-family: 'Anton', sans-serif !important;
        font-size: 36px;
      }}
      
      /* Compactação dos widgets de filtro */
      div[data-testid="stSelectbox"],
      div[data-testid="stDateInput"] {{
        margin-bottom: 6px !important;
      }}
      /* Unificar altura dos inputs */
      div[data-testid="stSelectbox"] div[role="combobox"],
      div[data-testid="stDateInput"] input {{
        min-height: 36px !important;
        height: 36px !important;
        line-height: 36px !important;
        padding: 4px 8px !important;
      }}
      /* Estilo de cores dos selects e valores selecionados */
      div[data-baseweb="select"] > div {{
        background-color: #fff !important;
        color: #000 !important;
        border-color: #ddd !important;
      }}
      div[data-baseweb="select"] * {{
        color: #000 !important;
      }}
      /* Dropdown options: fundo branco, texto preto; item ativo com destaque */
      ul[role="listbox"], div[role="listbox"] {{
        background: #fff !important;
        color: #000 !important;
        max-height: 260px !important;
      }}
      li[role="option"], div[role="option"] {{
        background: #fff !important;
        color: #000 !important;
        padding: 6px 10px !important;
        font-size: 14px !important;
      }}
      [role="option"][aria-selected="true"],
      [role="option"]:hover {{
        background: {YELLOW} !important;
        color: #000 !important;
      }}
      /* Remover gaps/paddings padrão do wrapper vertical do bloco de filtros */
      [data-testid="stVerticalBlock"]:has(#filters-box) {{
        gap: 8px !important;
        padding: 8px 20px 8px 20px !important;
        margin: 0px 0px 5px 0px !important;
      }}

      /* Remover gaps/paddings padrão do wrapper vertical do bloco de filtros */
      [data-testid="stVerticalBlock"]:has(#kpi-box) {{
        margin: 0px 0px 2px 0px !important;
      }}

      .kpi-stack {{
        display: flex;
        flex-direction: column;
        padding: 20px 5px 25px 5px;
        gap: 20px;
      }}

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="page-title">Números na Carreira</div>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    # Normaliza colunas essenciais
    required_cols = [
        "Data", "Equipa", "Resultado", "Local", "Competição",
        "OUTLIER", "Minutagem", "Golos", "TEMPO"
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes no CSV: {', '.join(missing)}")
    # Parse de datas
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    # Tipos numéricos seguros
    df["Golos"] = pd.to_numeric(df["Golos"], errors="coerce").fillna(0)
    return df


df = load_data("db/data.csv")

# Base: apenas ótica do cliente
client_df = df[df["OUTLIER"] == "Barroca"].copy()

# ===== Filtros (na página) =====
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown('<div class="page-inner">', unsafe_allow_html=True)

# Equipe / Resultado / Local / Competição
equipes = sorted(client_df["Equipa"].dropna().unique().tolist())
resultado_opcoes = ["Vitória", "Empate", "Derrota"]
locais = ["Casa", "Fora"]
locais_existentes = sorted(set(client_df["Local"].dropna().unique()).intersection(locais)) or locais
competicoes = sorted(client_df["Competição"].dropna().unique().tolist())

filters_box = st.container(border=True)
with filters_box:
    st.markdown('<div id="filters-box"></div>', unsafe_allow_html=True)
    st.markdown("<div class='viz-title'>FILTROS</div>", unsafe_allow_html=True)
    # Contextos e Data
    bins_min = [15, 30, 45, 60, 75, 90]
    label_bins = [
        "0-15min",
        "15-30min",
        "30-45min",
        "45-60min",
        "60-75min",
        "75-90min",
    ]
    label_to_min = {
        "0-15min": "15min",
        "15-30min": "30min",
        "30-45min": "45min",
        "45-60min": "60min",
        "60-75min": "75min",
        "75-90min": "90min",
    }

    min_data = pd.to_datetime(client_df["Data"].min())
    max_data = pd.to_datetime(client_df["Data"].max())

    # Todos os inputs em uma única linha
    st.markdown('<div id="filters-wrapper">', unsafe_allow_html=True)
    row = st.columns([2, 1.2, 1, 1.4, 1.4, 1.4, 2])
    with row[0]:
        sel_equipes = st.selectbox("Equipe", ["Todos"] + equipes, index=0)
    with row[1]:
        sel_resultados = st.selectbox("Resultado", ["Todos"] + resultado_opcoes, index=0)
    with row[2]:
        sel_locais = st.selectbox("Local", ["Todos"] + locais_existentes, index=0)
    with row[3]:
        sel_competicoes = st.selectbox("Competição", ["Todos"] + competicoes, index=0)
    with row[4]:
        ctx_ofensivo = st.selectbox("Marcou Gol", ["Sem filtro"] + label_bins, index=0)
    with row[5]:
        ctx_defensivo = st.selectbox("Sofreu Gol", ["Sem filtro"] + label_bins, index=0)
    with row[6]:
        sel_date_range = st.selectbox(
            "Data da partida",
            [
                "Todo período",
                "Última semana",
                "Último mês",
                "Últimos 3 meses",
                "Últimos 6 meses",
                "Últimos 12 meses",
            ],
            index=0,
        )
    st.markdown('</div>', unsafe_allow_html=True)


# Aplica filtros base (somente ótica do cliente)
filtered_client = client_df.copy()
if sel_equipes and sel_equipes != "Todos":
    filtered_client = filtered_client[filtered_client["Equipa"] == sel_equipes]
if sel_resultados and sel_resultados != "Todos":
    filtered_client = filtered_client[filtered_client["Resultado"] == sel_resultados]
if sel_locais and sel_locais != "Todos":
    filtered_client = filtered_client[filtered_client["Local"] == sel_locais]
if sel_competicoes and sel_competicoes != "Todos":
    filtered_client = filtered_client[filtered_client["Competição"] == sel_competicoes]
# Faixa de datas por seleção (sem calendário)
start_dt = None
end_dt = None
if pd.notnull(max_data):
    end_dt = pd.to_datetime(max_data)
if sel_date_range and sel_date_range != "Todo período" and end_dt is not None:
    if sel_date_range == "Última semana":
        candidate_start = end_dt - pd.DateOffset(weeks=1)
    elif sel_date_range == "Último mês":
        candidate_start = end_dt - pd.DateOffset(months=1)
    elif sel_date_range == "Últimos 3 meses":
        candidate_start = end_dt - pd.DateOffset(months=3)
    elif sel_date_range == "Últimos 6 meses":
        candidate_start = end_dt - pd.DateOffset(months=6)
    elif sel_date_range == "Últimos 12 meses":
        candidate_start = end_dt - pd.DateOffset(months=12)
    else:
        candidate_start = None
    if candidate_start is not None:
        start_dt = candidate_start
        if pd.notnull(min_data):
            start_dt = max(pd.to_datetime(min_data), candidate_start)

if start_dt is not None and end_dt is not None:
    filtered_client = filtered_client[(filtered_client["Data"] >= start_dt) & (filtered_client["Data"] <= end_dt)]

# Conjunto inicial de partidas (identificador sugerido: Data + OUTLIER)
allowed_dates = set(filtered_client["Data"].dropna().unique().tolist())

# Aplica contexto ofensivo (na ótica do cliente)
if ctx_ofensivo and ctx_ofensivo != "Sem filtro":
    mins_sel = {label_to_min[ctx_ofensivo]}
    off_rows = filtered_client[
        filtered_client["Minutagem"].isin(mins_sel) & (filtered_client["Golos"] > 0)
    ]
    allowed_dates = allowed_dates.intersection(set(off_rows["Data"].unique().tolist()))

# Aplica contexto defensivo (na ótica do adversário, mas restrito às mesmas partidas)
if ctx_defensivo and ctx_defensivo != "Sem filtro":
    mins_sel_d = {label_to_min[ctx_defensivo]}
    opp_rows_base = df[(df["OUTLIER"] != "Barroca") & (df["Data"].isin(allowed_dates))]
    def_rows = opp_rows_base[
        opp_rows_base["Minutagem"].isin(mins_sel_d) & (opp_rows_base["Golos"] > 0)
    ]
    allowed_dates = allowed_dates.intersection(set(def_rows["Data"].unique().tolist()))

# Dataset final de cliente
client_final = filtered_client[filtered_client["Data"].isin(allowed_dates)].copy()

# Nova disposição: 3 colunas na mesma linha, com larguras proporcionais (menores para KPIs e pizza)
col_kpi, col_pie, col_bars = st.columns([1.0, 1.0, 3.0])

# Número de jogos (únicos por Data)
num_jogos = client_final["Data"].nunique()

# Aproveitamento (abaixo)
client_final_90 = client_final[client_final["TEMPO"].astype(str).str.lower() == "90min"].copy()
if client_final_90.empty and not client_final.empty:
    client_final_90 = (
        client_final.sort_values(["Data", "Minutagem"]).groupby("Data").tail(1)
    )

total_90 = len(client_final_90)
wins = int((client_final_90["Resultado"] == "Vitória").sum())
draws = int((client_final_90["Resultado"] == "Empate").sum())
aproveitamento = (wins + draws / 3) / total_90 * 100 if total_90 > 0 else 0.0

with col_kpi:
    kpi_box = st.container(border=True)
    with kpi_box:
        st.markdown("<div class='viz-title' style='padding-left: 5px;'>KPIS</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div id="kpi-box"></div>
            <div class="kpi-stack">
              <div class="viz-box">
                <div class="viz-title">Número de jogos</div>
                <div class="viz-value">""" + str(num_jogos) + """</div>
              </div>
              <div class="viz-box">
                <div class="viz-title">Aproveitamento</div>
                <div class="viz-value">""" + f"{aproveitamento:.1f}%" + """</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Pizza de resultados com rótulos internos e contraste
res_counts = (
    client_final_90["Resultado"].value_counts().reindex(resultado_opcoes, fill_value=0).reset_index()
)
res_counts.columns = ["Resultado", "Quantidade"]
total_pie = max(int(res_counts["Quantidade"].sum()), 1)
res_counts["Perc"] = res_counts["Quantidade"] / total_pie
res_counts["Label"] = res_counts.apply(
    lambda r: f"{r['Resultado']} {int(r['Quantidade'])} ({r['Perc']*100:.0f}%)", axis=1
)

base_pie = alt.Chart(res_counts)
pie = base_pie.mark_arc(outerRadius=80, innerRadius=30).encode(
    theta=alt.Theta("Quantidade:Q"),
    color=alt.Color(
        "Label:N",
        scale=alt.Scale(
            domain=res_counts["Label"].tolist(),
            range=["#2ecc71", "#f1c40f", "#e74c3c"],
        ),
        legend=alt.Legend(
            title="",
            orient="bottom",
            direction="vertical",
            labelLimit=400,
            symbolType="circle",
        ),
    ),
    tooltip=["Resultado:N", "Quantidade:Q", alt.Tooltip("Perc:Q", title="%", format=".0%")]
)
chart_pie = (
    pie
    .properties(height=238.5, padding={"bottom": 0, "top": 5, "left": 0, "right": 0})
    .configure_legend(padding=0)
    .configure_view(stroke=None)
)

with col_pie:
    pie_box = st.container(border=True)
    with pie_box:
        st.markdown("<div class='viz-title' style='padding-left: 5px;'>Aproveitamento</div>", unsafe_allow_html=True)
        st.markdown('<div id="pie-box"></div>', unsafe_allow_html=True)
        st.altair_chart(chart_pie, width='stretch')


# Gols feitos x sofridos por faixa de minutagem
order_min = [f"{m}min" for m in bins_min]

gf = (
    client_final.groupby("Minutagem", as_index=False)["Golos"].sum().rename(columns={"Golos": "Feitos"})
)

opp_final = df[(df["OUTLIER"] != "Barroca") & (df["Data"].isin(allowed_dates))].copy()
gs = (
    opp_final.groupby("Minutagem", as_index=False)["Golos"].sum().rename(columns={"Golos": "Sofridos"})
)

gols_merge = pd.merge(gf, gs, on="Minutagem", how="outer").fillna(0)
gols_merge = gols_merge[gols_merge["Minutagem"].isin(order_min)]
gols_merge["Minutagem"] = pd.Categorical(gols_merge["Minutagem"], categories=order_min, ordered=True)
gols_long = gols_merge.melt(id_vars=["Minutagem"], value_vars=["Feitos", "Sofridos"], var_name="Tipo", value_name="Gols")

bars = (
    alt.Chart(gols_long)
    .mark_bar(width=35)
    .encode(
        x=alt.X("Minutagem:N", sort=order_min, title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Gols:Q", title=None),
        color=alt.Color("Tipo:N", scale=alt.Scale(domain=["Feitos", "Sofridos"], range=["#2ecc71", "#e74c3c"]), legend=alt.Legend(title="", orient="top", direction="horizontal", padding=0)),
        xOffset="Tipo:N",
        tooltip=["Minutagem", "Tipo", "Gols"],
    )
)

labels = (
    alt.Chart(gols_long)
    .mark_text(dy=-4, fontSize=12)
    .encode(
        x=alt.X("Minutagem:N", sort=order_min, title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Gols:Q", title=None),
        xOffset="Tipo:N",
        text=alt.Text("Gols:Q", format=".0f"),
        opacity=alt.condition(alt.datum.Gols > 0, alt.value(1), alt.value(0)),
        color=alt.value("#fff"),
    )
)

chart_gols = (
    (bars + labels)
    .properties(height=238.5, width=780, padding={"bottom": 0, "top": 0, "left": 10, "right": 0})
)

with col_bars:
    bars_box = st.container(border=True)
    with bars_box:
        st.markdown("<div class='viz-title' style='padding-left: 5px;'>Gols feitos e sofridos — por intervalo de tempo</div>", unsafe_allow_html=True)
        st.markdown('<div id="bars-box"></div>', unsafe_allow_html=True)
        st.altair_chart(chart_gols, width='content')

# ===== Bloco: Métricas por intervalo de tempo (ocupando largura total) =====
metrics_box = st.container(border=True)
with metrics_box:
    header_cols = st.columns([4, 3])
    with header_cols[0]:
        st.markdown("<div class='viz-title' style='padding-left: 5px;'>Métricas por intervalo de tempo</div>", unsafe_allow_html=True)
    # Mapeamento de rótulos -> colunas do CSV
    metric_label_to_col = {
        "Gols esperados": "Golos esperados",
        "Finalizações": "Remates / à baliza",
        "Finalizações ao alvo": "...10",
        "Passes": "Passes / certos",
        "Passes certos": "...13",
        "Posse de bola (%)": "Posse, %",
        "Perdas": "Perdas / curto/ médio / longo",
        "Perdas baixas": "...17",
        "Perdas médias": "...18",
        "Perdas altas": "...19",
        "Recuperações": "Recuperações / curto / médio / longo",
        "Recuperações baixas": "...21",
        "Recuperações médias": "...22",
        "Recuperações altas": "...23",
        "Finalizações de fora da área": "Remates de fora da área / no alvo",
        "Finalizações de fora da área no alvo": "...28",
        "Ataques posicionais": "Ataques posicionais / com remates",
        "Ataques posicionais com finalização": "...31",
        "Contra ataques": "Contra-ataques / com remates",
        "Contra ataques com finalização": "...34",
        "Bolas paradas": "Bolas paradas / com remates",
        "Bolas paradas com finalização": "...37",
        "Escanteios": "Cantos / com remates",
        "Escanteios com finalização": "...40",
        "Penaltis": "Penaltis / convertidos",
        "Penaltis convertidos": "...46",
        "Cruzamentos": "Cruzamentos / certos",
        "Cruzamentos certos": "...49",
        "Cruzamentos em profundidade recebidos": "Cruzamentos em profundidade recebidos",
        "Passes em profundidade recebidos": "Passes em profundidade recebidos",
        "Entradas na grande área com corridas": "Entradas na grande área (corridas/cruzamentos)",
        "Entradas na grande área com cruzamentos": "...54",
        "Duelos ofensivos": "Duelos ofensivos / ganhos",
        "Duelos ofensivos ganhos": "...58",
        "Duelos defensivos": "Duelos defensivos / ganhos",
        "Duelos defensivos ganhos": "...66",
        "Faltas": "Faltas",
        "Passes para a frente": "Passes para a frente / certos",
        "Passes para a frente certos": "...80",
        "Passes para trás": "Passes para trás / certos",
        "Passes para trás certos": "...83",
        "Passes laterais": "Passes laterais / certos",
        "Passes laterais certos": "...86",
        "Passes longos": "Passes longos / certos",
        "Passes longos certos": "...89",
        "Passes para terço final": "Passes para terço final / certos",
        "Passes para terço final certos": "...92",
        "Passes progressivos": "Passes progressivos / precisos",
        "Passes progressivos precisos": "...95",
        "Passes inteligentes": "Passes inteligentes / certos",
        "Passes inteligentes certos": "...98",
        "Lançamentos": "Lançamentos / certos",
        "Lançamentos certos": "...101",
    }

    # Apenas métricas existentes no dataset E que têm dados válidos (não apenas NaN/vazios)
    available_labels = []
    for label, col in metric_label_to_col.items():
        if col in df.columns:
            # Verifica se há pelo menos um valor não-nulo na coluna para partidas filtradas
            # Considera tanto dados do cliente quanto dos adversários nas partidas permitidas
            relevant_data = df[df["Data"].isin(allowed_dates)][col]
            if relevant_data.notna().any() and (pd.to_numeric(relevant_data, errors="coerce").notna().any()):
                available_labels.append(label)
    
    available_labels = sorted(available_labels)
    default_label = available_labels[0] if available_labels else None
    with header_cols[1]:
        lab_col, input_col, spacer_col = st.columns([1, 7, 0.8])
        with lab_col:
            st.markdown("<div style='padding-top:8px'>Métrica</div>", unsafe_allow_html=True)
        with input_col:
            if available_labels:
                sel_metric_label = st.selectbox(
                    "Métrica",
                    available_labels,
                    index=0,
                    label_visibility="collapsed",
                )
            else:
                sel_metric_label = None

    if not available_labels or sel_metric_label is None:
        st.info("Nenhuma métrica qualitativa disponível no arquivo de dados para as partidas filtradas. Algumas partidas podem não ter dados qualitativos.")
    else:
        # Se usuário deixar "Todas", exibimos a primeira métrica disponível como padrão
        effective_metric_label = sel_metric_label
        metric_col = metric_label_to_col[effective_metric_label]

        # Prepara dados (respeitando filtros anteriores e allowed_dates)
        # Cliente (Barroca)
        client_metric_df = client_final[["Minutagem", metric_col]].copy()
        client_metric_df[metric_col] = pd.to_numeric(client_metric_df[metric_col], errors="coerce")
        # Remove linhas onde a métrica é NaN (partidas sem dados qualitativos)
        client_metric_df = client_metric_df[client_metric_df[metric_col].notna()]
        client_metric_avg = (
            client_metric_df.groupby("Minutagem", as_index=False)[metric_col].mean()
            .rename(columns={metric_col: "Valor"})
        )
        client_metric_avg = client_metric_avg[client_metric_avg["Minutagem"].isin(order_min)]
        client_metric_avg["Minutagem"] = pd.Categorical(client_metric_avg["Minutagem"], categories=order_min, ordered=True)
        client_metric_avg["Lado"] = "Barroca"

        # Adversários
        opponents_df = df[(df["OUTLIER"] != "Barroca") & (df["Data"].isin(allowed_dates))].copy()
        opp_metric_df = opponents_df[["Minutagem", metric_col]].copy()
        opp_metric_df[metric_col] = pd.to_numeric(opp_metric_df[metric_col], errors="coerce")
        # Remove linhas onde a métrica é NaN (partidas sem dados qualitativos)
        opp_metric_df = opp_metric_df[opp_metric_df[metric_col].notna()]
        opp_metric_avg = (
            opp_metric_df.groupby("Minutagem", as_index=False)[metric_col].mean()
            .rename(columns={metric_col: "Valor"})
        )
        opp_metric_avg = opp_metric_avg[opp_metric_avg["Minutagem"].isin(order_min)]
        opp_metric_avg["Minutagem"] = pd.Categorical(opp_metric_avg["Minutagem"], categories=order_min, ordered=True)
        opp_metric_avg["Lado"] = "Adversários"

        metrics_long = pd.concat([client_metric_avg, opp_metric_avg], ignore_index=True)

        # Verifica se há dados para exibir
        if metrics_long.empty or metrics_long["Valor"].isna().all():
            st.info(f"Nenhum dado disponível para a métrica '{effective_metric_label}' nas partidas filtradas.")
        else:
            # Gráfico de linhas
            line_chart = (
                alt.Chart(metrics_long)
                .mark_line(point=True)
                .encode(
                    x=alt.X("Minutagem:N", sort=order_min, title=None, axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("Valor:Q", title=effective_metric_label),
                    color=alt.Color(
                        "Lado:N",
                        scale=alt.Scale(domain=["Barroca", "Adversários"], range=["#2ecc71", "#e74c3c"]),
                        legend=alt.Legend(title="", orient="top", direction="horizontal", padding=0),
                    ),
                    tooltip=["Minutagem:N", "Lado:N", alt.Tooltip("Valor:Q", title=effective_metric_label, format=".2f")],
                )
            )

            chart_metrics = (
                line_chart
                .properties(height=260, padding={"bottom": 0, "top": 0, "left": 10, "right": 10})
                .configure_view(stroke=None)
            )

            st.altair_chart(chart_metrics, width='stretch')

st.markdown('</div>', unsafe_allow_html=True)



