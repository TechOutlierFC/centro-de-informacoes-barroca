"""Valor de mercado ao longo do tempo por jogador — OutlierFC."""

from __future__ import annotations

import html
import json
import math
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Agregação de Valor", page_icon="📈", layout="wide")

YELLOW = "#FABB48"
ORANGE = "#FFA500"
BG_APP = "#202020"
BG_PANEL = "#2a2a2a"
TEXT_PRIMARY = "rgba(255, 255, 255, 0.92)"
TEXT_MUTED = "rgba(255, 255, 255, 0.55)"
GRID = "rgba(255, 255, 255, 0.1)"
LINE_SERIE = "#ECECEC"
FILL_SERIE = "rgba(250, 187, 72, 0.2)"
MARKER_LINE = "#202020"

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

st.markdown(
    '<a href="?go=outlier" target="_self" class="back-button" title="Voltar à OutlierFC"> &#x21A9; </a>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Anton&display=swap');

      html, body, .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {BG_APP} !important;
      }}
      .block-container {{
        background: transparent !important;
        padding-top: 1rem;
      }}
      [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] [data-testid="stMarkdownContainer"] p,
      .stMarkdown {{
        color: {TEXT_PRIMARY};
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
        border: 2px solid {ORANGE};
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
      }}
      .top-section {{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: clamp(12px, 2vh, 24px);
        padding-bottom: 0px;
        box-sizing: border-box;
      }}
      /* Como não temos subtítulo aqui, usamos o mesmo espaçamento inferior do subtítulo do Centro de Informações */
      .top-section .page-title {{
        margin-bottom: clamp(16px, 3vh, 24px);
      }}

      .chart-card-title {{
        font-family: 'Anton', sans-serif !important;
        font-size: 20px;
        text-transform: uppercase;
        margin-bottom: 8px;
        letter-spacing: 0.02em;
        color: {TEXT_PRIMARY};
      }}
      .player-card-head {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 6px;
      }}
      .player-card-head .chart-card-title {{
        margin-bottom: 4px;
      }}
      /* Foto inteira (sem crop): mantém proporção e não corta rosto */
      .player-headshot {{
        height: 72px;
        width: auto;
        max-width: 72px;
        flex-shrink: 0;
        box-sizing: border-box;
        border-radius: 10px;
        border: 2px solid {YELLOW};
        background-color: {BG_APP};
        object-fit: contain;
        display: block;
      }}
      .player-headshot--empty {{
        height: 72px;
        width: 72px;
        flex-shrink: 0;
        border-radius: 10px;
        border: 2px dashed rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.06);
      }}
      .player-card-head-text {{
        flex: 1;
        min-width: 0;
      }}
      /* Container com borda (cards dos jogadores): fundo igual ao app */
      div[data-testid="stLayoutWrapper"] > div[data-testid="stExpander"],
      [data-testid="stVerticalBlockBorderWrapper"] {{
        background: {BG_APP} !important;
        border-color: rgba(255,255,255,0.12) !important;
      }}

      [data-testid="stPlotlyChart"] {{
        margin-bottom: -4px !important;
      }}

      @media (max-width: 768px) {{
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


@st.cache_data(show_spinner=False)
def load_clubes(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    df["id"] = df["id"].astype(str)
    return df


@st.cache_data(show_spinner=False)
def load_jogadores(path: str) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def parse_historico(valor_raw: Any) -> list[dict[str, Any]]:
    if pd.isna(valor_raw) or valor_raw == "":
        return []
    if isinstance(valor_raw, str):
        try:
            data = json.loads(valor_raw)
        except json.JSONDecodeError:
            return []
    elif isinstance(valor_raw, (list, dict)):
        data = valor_raw
    else:
        return []
    if not isinstance(data, list):
        return []
    return data


def preparar_serie(historico: list[dict[str, Any]]) -> pd.DataFrame | None:
    rows = []
    for item in historico:
        if not isinstance(item, dict):
            continue
        cid = str(item.get("clubid", "")).strip()
        try:
            v = float(item.get("valor", 0))
        except (TypeError, ValueError):
            v = 0.0
        d = item.get("data")
        if d is None or d == "":
            continue
        ts = pd.to_datetime(d, errors="coerce")
        if pd.isna(ts):
            continue
        rows.append({"data": ts, "valor": v, "clubid": cid})
    if not rows:
        return None
    out = pd.DataFrame(rows)
    out = out.sort_values("data").reset_index(drop=True)
    return out


def clubes_primeira_aparicao(serie: pd.DataFrame) -> pd.DataFrame:
    """Primeiro ponto de cada clube na sequência temporal ordenada."""
    if serie.empty:
        return pd.DataFrame(columns=["data", "valor", "clubid", "y_logo"])
    prev: str | None = None
    idxs: list[int] = []
    for i, cid in enumerate(serie["clubid"]):
        if i == 0 or cid != prev:
            idxs.append(i)
        prev = cid
    logos = serie.iloc[idxs].copy()
    ymax = float(serie["valor"].max())
    ymin = float(serie["valor"].min())
    span = ymax - ymin if ymax > ymin else max(ymax, 1.0)
    logos["y_logo"] = logos["valor"] + span * 0.11
    return logos


def merge_logos_foto(logos: pd.DataFrame, clubes: pd.DataFrame) -> pd.DataFrame:
    if logos.empty:
        return logos
    m = logos.merge(
        clubes[["id", "foto", "nome"]],
        left_on="clubid",
        right_on="id",
        how="left",
    )
    m["foto"] = m["foto"].fillna("")
    return m


def fmt_valor_eur(v: float) -> str:
    if v >= 1_000_000:
        return f"€ {v / 1_000_000:.1f}M"
    if v >= 1_000:
        return f"€ {v / 1_000:.0f}k"
    return f"€ {v:.0f}"


def tickvals_apenas_anos(x_min: pd.Timestamp, x_max: pd.Timestamp) -> list[pd.Timestamp]:
    """Marca de 1º de jan em cada ano dentro do domínio (eixo X só com ano no rótulo)."""
    x_min = pd.Timestamp(x_min)
    x_max = pd.Timestamp(x_max)
    if x_max < x_min:
        x_min, x_max = x_max, x_min
    out: list[pd.Timestamp] = []
    for y in range(x_min.year, x_max.year + 1):
        t = pd.Timestamp(year=y, month=1, day=1)
        if x_min <= t <= x_max:
            out.append(t)
    return out if out else [x_min, x_max]


def dominio_x_temporal(x_min: pd.Timestamp, x_max: pd.Timestamp) -> tuple[pd.Timestamp, pd.Timestamp]:
    """Limites exatos do eixo X (sem `nice`), para o desenho ocupar toda a largura entre 1º e último evento."""
    x_min = pd.Timestamp(x_min)
    x_max = pd.Timestamp(x_max)
    if x_max < x_min:
        x_min, x_max = x_max, x_min
    if x_max <= x_min or (x_max - x_min) < pd.Timedelta(hours=1):
        pad = pd.Timedelta(days=120)
        x_min = x_min - pad
        x_max = x_max + pad
    return x_min, x_max


def _nice_step(approx: float) -> float:
    if approx <= 0:
        return 1.0
    exp = math.floor(math.log10(approx))
    f = approx / (10**exp)
    if f < 1.5:
        nf = 1
    elif f < 3.5:
        nf = 2
    elif f < 7.5:
        nf = 5
    else:
        nf = 10
    return nf * (10**exp)


def eixo_y_uniforme(y_need_max: float, max_marcas: int = 11) -> tuple[float, list[float]]:
    """Eixo Y [0, teto] com **mesmo passo** entre todas as marcas; o teto do eixo = n×passo (n inteiro), alinhado ao último rótulo."""
    if y_need_max <= 0:
        return 1.0, [0.0, 1.0]
    step = _nice_step(y_need_max / 5.0)
    n = max(1, int(math.ceil(y_need_max / step - 1e-15)))
    for _ in range(24):
        if n + 1 <= max_marcas:
            break
        step = _nice_step(step * 2.0)
        n = max(1, int(math.ceil(y_need_max / step - 1e-15)))
    y_teto = float(n * step)
    ticks = [float(i * step) for i in range(n + 1)]
    return y_teto, ticks


def fmt_valor_eixo_y_abrev(v: float) -> str:
    """10k, 0.1M, 1M, 10M — só rótulos do eixo (sem €)."""
    av = abs(float(v))
    if av >= 1_000_000:
        x = v / 1_000_000
        if abs(x - round(x)) < 1e-6:
            return f"{int(round(x))}M"
        s = f"{x:.2f}".rstrip("0").rstrip(".")
        return f"{s}M"
    if av >= 100_000:
        x = v / 1_000_000
        s = f"{x:.2f}".rstrip("0").rstrip(".")
        return f"{s}M"
    if av >= 1_000:
        k = v / 1_000
        if abs(k - round(k)) < 1e-6:
            return f"{int(round(k))}k"
        s = f"{k:.1f}".rstrip("0").rstrip(".")
        return f"{s}k"
    if abs(v - round(v)) < 1e-6:
        return str(int(round(v)))
    return f"{v:.0f}"


def chart_jogador(
    serie: pd.DataFrame,
    logos: pd.DataFrame,
    barroca: pd.Timestamp | None,
    clubes_map: dict[str, str],
) -> go.Figure:
    """Plotly: eixo de datas e rótulos %Y funcionam de forma estável no Streamlit (Altair/Vega falhava)."""
    ymax = float(serie["valor"].max())
    ymin = float(serie["valor"].min())
    span = ymax - ymin if ymax > ymin else max(ymax, 1.0)
    y_headroom = ymax + span * 0.18
    y_ceiling, y_ticks = eixo_y_uniforme(y_headroom)
    y_tick_text = [fmt_valor_eixo_y_abrev(t) for t in y_ticks]

    x_min = serie["data"].min()
    x_max = serie["data"].max()
    if barroca is not None and pd.notna(barroca):
        x_min = min(x_min, barroca)
        x_max = max(x_max, barroca)

    x_min = pd.Timestamp(x_min)
    x_max = pd.Timestamp(x_max)
    x_min, x_max = dominio_x_temporal(x_min, x_max)

    tv = tickvals_apenas_anos(x_min, x_max)
    # Range real do eixo X pode ser expandido para caber escudos sem “empurrar” o centro do ponto
    x_min_plot = x_min
    x_max_plot = x_max

    fig = go.Figure()
    plot = serie.copy()
    plot["club_nome"] = plot["clubid"].astype(str).map(clubes_map).fillna("—")

    fig.add_trace(
        go.Scatter(
            x=plot["data"],
            y=plot["valor"],
            mode="lines+markers",
            line=dict(color=LINE_SERIE, width=2, shape="spline"),
            marker=dict(size=9, color=YELLOW, line=dict(color=MARKER_LINE, width=1.5)),
            fill="tozeroy",
            fillcolor=FILL_SERIE,
            customdata=plot[["valor", "club_nome"]].values,
            hovertemplate=(
                "<b>%{x|%Y-%m-%d}</b><br>"
                "<span style='color:rgba(255,255,255,0.7)'>Clube</span>: %{customdata[1]}<br>"
                "<span style='color:rgba(255,255,255,0.7)'>Valor</span>: <b>€ %{customdata[0]:,.0f}</b>"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    # Logos (URLs externas — mesmo comportamento do Altair)
    layout_images: list[dict[str, object]] = []
    if not logos.empty and logos["foto"].str.len().gt(0).any():
        img_src = logos[logos["foto"].str.len() > 0]
        x_rng_ns = max(x_max.value - x_min.value, 1)
        # Escudos maiores e com tamanho proporcional ao range do gráfico
        sizex_ms = max(x_rng_ns / 1e6 / 14, 18 * 24 * 3600 * 1000)
        sizey = y_ceiling * 0.075
        # Expande o range do eixo para o escudo caber sem sair do plot
        pad_td = pd.Timedelta(milliseconds=sizex_ms * 0.8)
        x_min_plot = x_min - pad_td
        x_max_plot = x_max + pad_td
        for _, r in img_src.iterrows():
            url = str(r.get("foto", "")).strip()
            if not url:
                continue
            x_img = pd.Timestamp(r["data"])
            layout_images.append(
                dict(
                    source=url,
                    xref="x",
                    yref="y",
                    x=x_img,
                    y=float(r["y_logo"]),
                    sizex=sizex_ms,
                    sizey=sizey,
                    xanchor="center",
                    yanchor="middle",
                    layer="above",
                    sizing="contain",
                )
            )

    if barroca is not None and pd.notna(barroca):
        bc = pd.Timestamp(barroca)
        fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0=bc,
            x1=bc,
            y0=0,
            y1=y_ceiling,
            line=dict(color=ORANGE, width=2, dash="dash"),
            layer="above",
        )
        fig.add_annotation(
            xref="x",
            yref="y",
            x=bc,
            y=ymax + span * 0.02,
            text="▼",
            showarrow=False,
            font=dict(color=ORANGE, size=18),
            xanchor="center",
            yanchor="bottom",
        )
        fig.add_annotation(
            xref="x",
            yref="y",
            x=bc,
            y=ymax + span * 0.075,
            text="Barroca",
            showarrow=False,
            font=dict(color=ORANGE, size=13),
            xanchor="center",
            yanchor="bottom",
        )

    fig.update_layout(
        height=380,
        margin=dict(l=66, r=14, t=22, b=28),
        font=dict(color=TEXT_PRIMARY, family="system-ui, sans-serif", size=12),
        paper_bgcolor=BG_APP,
        plot_bgcolor=BG_APP,
        hovermode="closest",
        images=layout_images,
        hoverlabel=dict(
            bgcolor=BG_PANEL,
            font_size=12,
            font_color=TEXT_PRIMARY,
            bordercolor="rgba(255,255,255,0.15)",
        ),
        xaxis=dict(
            type="date",
            range=[x_min_plot, x_max_plot],
            tickvals=tv,
            tickformat="%Y",
            showgrid=True,
            gridcolor=GRID,
            zeroline=False,
            tickangle=0,
            title=dict(text=None),
            tickfont=dict(color=TEXT_MUTED, size=11),
            showline=True,
            linecolor=GRID,
            layer="below traces",
            mirror=False,
        ),
        yaxis=dict(
            title=dict(text=None),
            range=[0, y_ceiling],
            tickmode="array",
            tickvals=y_ticks,
            ticktext=y_tick_text,
            showgrid=True,
            gridcolor=GRID,
            zeroline=False,
            tickfont=dict(color=TEXT_MUTED, size=11),
            showline=True,
            linecolor=GRID,
            layer="below traces",
            mirror=False,
        ),
    )
    return fig


# --- Conteúdo ---
st.markdown(
    '<div class="top-section">'
    '<div class="page-title">Agregação de Valor</div>'
    "</div>",
    unsafe_allow_html=True,
)

clubes_df = load_clubes("db/cadastro_clubes.csv")
jogadores_df = load_jogadores("db/cadastro_jogadores.csv")
clubes_map = dict(zip(clubes_df["id"].astype(str), clubes_df["nome"].astype(str)))

itens: list[dict[str, object]] = []
for _, row in jogadores_df.iterrows():
    nome = str(row.get("nome", "—"))
    historico = parse_historico(row.get("valor"))
    serie = preparar_serie(historico)
    if serie is None or serie.empty:
        continue

    barroca_raw = row.get("barroca")
    barroca_ts = pd.to_datetime(barroca_raw, errors="coerce")
    if pd.isna(barroca_ts):
        barroca_ts = None

    logos_base = clubes_primeira_aparicao(serie)
    logos_m = merge_logos_foto(logos_base, clubes_df)

    ultimo = float(serie["valor"].iloc[-1])
    itens.append(
        {
            "row": row,
            "nome": nome,
            "serie": serie,
            "logos": logos_m,
            "barroca": barroca_ts,
            "ultimo": ultimo,
        }
    )

itens.sort(key=lambda x: float(x["ultimo"]), reverse=True)

renderizados = 0
for it in itens:
    row = it["row"]
    nome = str(it["nome"])
    serie = it["serie"]
    logos_m = it["logos"]
    barroca_ts = it["barroca"]
    ultimo = float(it["ultimo"])

    foto_url = str(row.get("foto", "") or "").strip()
    nome_safe = html.escape(nome)
    if foto_url:
        img_block = (
            f'<img src="{html.escape(foto_url)}" class="player-headshot" alt="" '
            f'loading="lazy" decoding="async" />'
        )
    else:
        img_block = '<div class="player-headshot--empty" aria-hidden="true"></div>'

    with st.container(border=True):
        st.markdown(
            f'<div class="player-card-head">'
            f"{img_block}"
            f'<div class="player-card-head-text">'
            f'<div class="chart-card-title">{nome_safe}</div>'
            f'<div style="font-size:14px;color:rgba(255,255,255,0.55);">'
            f'Valor atual: <strong style="color:rgba(255,255,255,0.95)">{html.escape(fmt_valor_eur(ultimo))}</strong>'
            f"</div></div></div>",
            unsafe_allow_html=True,
        )
        fig = chart_jogador(serie, logos_m, barroca_ts, clubes_map)
        # `theme=None` (Streamlit recente) evita sobrescrever fundo do gráfico
        _pc = dict(width="stretch", config={"displayModeBar": False})
        try:
            st.plotly_chart(fig, theme=None, **_pc)
        except TypeError:
            st.plotly_chart(fig, **_pc)
        renderizados += 1
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

if renderizados == 0:
    st.warning("Nenhum jogador com histórico de valor de mercado disponível no cadastro.")
