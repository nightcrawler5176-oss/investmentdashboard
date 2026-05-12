import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Investment Analysis", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;400;700&display=swap');

    /* =========================
       GLOBAL FONT
    ========================= */

    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* =========================
       RTL TEXT ONLY
    ========================= */

    .main,
    .stMarkdown,
    h1, h2, h3, h4, h5, h6,
    p, label {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* =========================
       LIGHT THEME
    ========================= */

    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    .main {
        background-color: #ffffff !important;
    }

    /* =========================
       TEXT COLORS
    ========================= */

    p, label, span,
    .stMarkdown,
    [data-testid="stWidgetLabel"] p {
        color: #000000 !important;
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* =========================
       NUMBER INPUTS
    ========================= */

    div[data-testid="stNumberInput"] input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* =========================
       SLIDER FIX
    ========================= */

    /* IMPORTANT:
       DO NOT force RTL on slider internals
    */

    div[data-baseweb="slider"] {
        direction: ltr !important;
        padding-left: 10px;
        padding-right: 10px;
    }

    /* Slider labels and numbers */
    div[data-baseweb="slider"] span {
        font-family: 'Vazirmatn', sans-serif !important;
        color: black !important;
    }

    /* =========================
       SECTION HEADERS
    ========================= */
/* Fintech-style sidebar section cards */
.sidebar-section {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(41, 92, 171, 0.25);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 12px;
}

/* Section title inside sidebar cards */
.sidebar-title {
    color: #295cab;
    font-weight: bold;
    font-size: 0.95rem;
    margin-bottom: 10px;
    font-family: 'Vazirmatn', sans-serif;
}
    .section-header {
        color: #295cab !important;
        font-size: 1.2rem;
        font-weight: bold;
        border-bottom: 2px solid #0095da;
        padding-bottom: 5px;
        margin-top: 0px;
        margin-bottom: 5px;
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* =========================
       METRICS
    ========================= */

    div[data-testid="stMetricValue"] {
        color: #295cab !important;
        font-family: 'Vazirmatn', sans-serif !important;
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'Vazirmatn', sans-serif !important;
    }
/* =========================
   SIDEBAR LABEL FIX
========================= */
/* Hide Streamlit top-right menu (Deploy + 3 dots) */
#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
/* Remove ALL top padding in sidebar */
section[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
}

/* Remove padding/margin from first inner container (Streamlit wrapper) */
section[data-testid="stSidebar"] > div > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] > div:first-child > div {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
/* Remove weird collapse hover zone / arrow area */
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

/* Tighten sidebar content spacing */
section[data-testid="stSidebar"] {
    padding-top: 0rem !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: white !important;
    font-family: 'Vazirmatn', sans-serif !important;
}



/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #0e1117 !important;
}
    </style>
""", unsafe_allow_html=True)


# -------------------------
# Persian Number Converter
# -------------------------

def to_persian_digits(s):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    s = str(s)

    for en, fa in zip(english_digits, persian_digits):
        s = s.replace(en, fa)

    return s


# -------------------------
# Short Number Formatter
# -------------------------

def format_short(n):

    if abs(n) >= 1_000_000_000:
        val = f"{n / 1_000_000_000:.1f} B"

    elif abs(n) >= 1_000_000:
        val = f"{n / 1_000_000:.1f} M"

    else:
        val = f"{int(n):,}"

    return to_persian_digits(val)

st.markdown("""
<div style="
    margin-top: -70px;
    margin-bottom: 50px;
    font-size: 50px;
    font-weight: 700;
    color: #295cab;
    text-align: right;
    font-family: Vazirmatn;
">
🍃🏣 داشبورد تحلیل استراتژیک طرحهای زیستبوم
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.markdown("<div class='section-header'>۱. متغیرهای سرمایه‌گذاری</div>", unsafe_allow_html=True)
ti_billion = st.sidebar.number_input(
    "کل سرمایه‌گذاری (TI) [میلیارد تومان]",
    value=1000,
    step=10
)

# Convert to toman internally (DO NOT change model logic)
ti = ti_billion * 1_000_000_000
bp = st.sidebar.number_input("دوره ساخت (BP) [سال]", value=2, min_value=1)
tea = st.sidebar.number_input("متراژ مفید (TEA) [متر مربع]", value=22000, step=500)
tcp = st.sidebar.slider("درصد اعتبار مالیاتی (TCP) [%]", 0, 100, 100) / 100

st.sidebar.markdown("<div class='section-header'>۲. متغیرهای بازار</div>", unsafe_allow_html=True)
rent_m = st.sidebar.number_input("اجاره ماهیانه متر مربع [تومان]", value=859_000, step=50_000)
rent_inc = st.sidebar.slider("افزایش سالانه اجاره [%]", 0, 100, 25) / 100
dr = st.sidebar.slider("نرخ تنزیل (Discount Rate) [%]", 0, 100, 50) / 100

st.sidebar.markdown("<div class='section-header'>۳. اهرم‌های مذاکره</div>", unsafe_allow_html=True)
up = st.sidebar.slider("درصد بهره‌برداری (UP) [%]", 0, 100, 50) / 100
olp = st.sidebar.number_input("دوره بهره‌برداری (OLP) [سال]", value=15, min_value=1)

# --- CALCULATIONS ---
data = []
yearly_inv = ti / bp
# 18-month delayed tax shield calculation
tax_shield_pv = (yearly_inv * tcp) / ((1 + dr) ** 1.5)
net_cost = yearly_inv - tax_shield_pv

for y in range(int(bp)):
    data.append({"Year": y, "Val": -net_cost})

for y in range(int(bp), int(bp + olp)):
    annual_gain = (tea * up) * (rent_m * 12) * ((1 + rent_inc) ** y)
    data.append({"Year": y, "Val": annual_gain})

df = pd.DataFrame(data)
npv = sum([r['Val'] / ((1 + dr) ** r['Year']) for _, r in df.iterrows()])
# =========================
# DISCOUNTED ROI
# =========================

pv_inflows = sum([
    r['Val'] / ((1 + dr) ** r['Year'])
    for _, r in df.iterrows()
    if r['Val'] > 0
])

pv_outflows = sum([
    abs(r['Val']) / ((1 + dr) ** r['Year'])
    for _, r in df.iterrows()
    if r['Val'] < 0
])

roi = (
    ((pv_inflows - pv_outflows) / pv_outflows) * 100
    if pv_outflows > 0 else 0
)

# =========================
# DISCOUNTED PAYBACK PERIOD
# =========================

cumulative_cf = 0
payback_year = None

for _, r in df.iterrows():

    discounted_cf = r['Val'] / ((1 + dr) ** r['Year'])

    cumulative_cf += discounted_cf

    if cumulative_cf >= 0 and payback_year is None:
        payback_year = r['Year']

# =========================
# HEATMAP CALCULATION (OLP × UP)
# =========================

olp_range = range(1, 21)  # 1 to 20 years
up_range = np.linspace(0.1, 1.0, 10)  # 10% to 100%

heatmap_data = []

for up_test in up_range:
    row = []

    for olp_test in olp_range:

        yearly_inv = ti / bp
        tax_shield_pv = (yearly_inv * tcp) / ((1 + dr) ** 1.5)
        net_cost = yearly_inv - tax_shield_pv

        # construction cost
        cash_flows = [-net_cost] * bp

        # benefits
        for y in range(int(olp_test)):
            annual_gain = (tea * up_test) * (rent_m * 12) * ((1 + rent_inc) ** y)
            cash_flows.append(annual_gain)

        # NPV
        npv_test = sum([
            cf / ((1 + dr) ** i)
            for i, cf in enumerate(cash_flows)
        ])

        row.append(npv_test)

    heatmap_data.append(row)

# --- DISPLAY ---
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(
        "ارزش فعلی خالص (NPV)",
        to_persian_digits(f"{int(npv):,}") + " تومان"
    )
st.markdown("""
    <div style="position: relative; width: 100%; height: 0;">
        <img src="https://uploadkon.ir/uploads/28da12_26transaction.png"
             style="position: absolute;
                    top: -102px;
                    left: 1460px;
                    width: 60px;
                    opacity: 1.0;
                    z-index: 999;">
        <img src="https://uploadkon.ir/uploads/652912_26return-of-investment.png"
             style="position: absolute;
                    top: -115px;
                    left: 970px;
                    width: 80px;
                    opacity: 1.0;
                    z-index: 999;"> 
        <img src="https://uploadkon.ir/uploads/e7b612_26long-term-planning.png"
             style="position: absolute;
                    top: -113px;
                    left: 479px;
                    width: 71px;
                    opacity: 1.0;
                    z-index: 999;">  
        <img src="https://uploadkon.ir/uploads/360712_26Picture1.png"
             style="position: absolute;
                    top: -250px;
                    left: -50px;
                    width: 250px;
                    opacity: 1.0;
                    z-index: 999;">                
                                                        
    </div>
""", unsafe_allow_html=True)
with c2:
    st.metric(
        "نرخ بازده سرمایه (ROI)",
        to_persian_digits(f"{roi:.1f}") + "%"
    )
with c3:

    payback_text = (
        to_persian_digits(str(payback_year)) + " سال"
        if payback_year is not None
        else "عدم بازگشت"
    )

    st.metric(
        "دوره بازگشت سرمایه",
        payback_text
    )
st.divider()

# --- PLOTLY CHART ---
# =========================
# HEATMAP VISUALIZATION
# =========================

zmin = np.min(heatmap_data)
zmax = np.max(heatmap_data)
abs_max = max(abs(zmin), abs(zmax))

flat = [v for row in heatmap_data for v in row]
max_abs = max(abs(min(flat)), abs(max(flat)))

fig_heat = px.imshow(
    heatmap_data,
    x=list(olp_range),
    y=[round(u*100) for u in up_range],
    color_continuous_scale=["red", "white", "green"],
    zmin=-max_abs * 0.8,
    zmax=max_abs,
    labels=dict(
        x="OLP (سال)",
        y="UP (%)",
        color="NPV"
    ),
    aspect="auto"
)
fig_heat.update_layout(
    coloraxis_colorbar=dict(
        title="NPV",
        tickfont=dict(color="black"),
        title_font=dict(color="black")
    )
)
fig_heat.update_layout(
    height=750,
    font_family="Vazirmatn",
    margin=dict(t=40, b=40, l=60, r=20)
)
fig_heat.update_layout(
    font_family="Vazirmatn",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff"
)


df['color'] = df['Val'].apply(lambda x: '#ff4f00' if x < 0 else '#0095da')

fig = go.Figure(data=[
    go.Bar(
        x=[to_persian_digits(str(y)) for y in df['Year']],
        y=df['Val'],
        marker_color=df['color'],
        text=[format_short(v) for v in df['Val']],
        textposition='outside',
        textfont=dict(
            family="Vazirmatn",
            size=14,
            color="#000000"
        ),
        hovertext=[to_persian_digits(format_short(v)) for v in df['Val']],
        hoverinfo="text",
        cliponaxis=False
    )
])

fig.update_layout(
    font_family="Vazirmatn",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='white',
    xaxis=dict(
        title="سال",
        title_font=dict(color="#295cab"),
        tickfont=dict(color="#295cab"),
        color="#295cab",
        tickmode='linear',
        gridcolor="#f0f0f0"
    ),
    yaxis=dict(
        title="تومان",
        title_font=dict(color="#295cab"),
        tickfont=dict(color="#295cab"),
        color="#295cab",
        gridcolor='#f0f0f0'
    ),
    margin=dict(t=50, b=20, l=10, r=10),
    height=600
)
# =========================
# PAYBACK VISUAL MARKER
# =========================

# =========================
# PAYBACK VISUAL MARKER
# =========================

if payback_year is not None:

    # Thick transparent vertical line
    fig.add_shape(
        type="rect",
        x0=payback_year - 0.15,
        x1=payback_year + 0.15,

        y0=0,
        y1=max(df['Val']),

        fillcolor="rgba(41, 92, 171, 0.25)",
        line_width=0,
        layer="below"
    )

    # Label above chart
    fig.add_annotation(
        x=payback_year,
        y=max(df['Val']) * 1.08,
        text="بازگشت سرمایه",
        showarrow=False,
        font=dict(
            family="Vazirmatn",
            size=15,
            color="#295cab"
        ),
        bgcolor="rgba(255,255,255,0.7)"
    )
st.plotly_chart(fig, use_container_width=True)
st.subheader(" Heatmap مذاکره (OLP × UP)")
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown("""
<div style="
    text-align: right;
    margin-top: 25px;
    color: #295cab;
    font-size: 25px;
    font-family: Vazirmatn;
    padding-bottom: 10px;
">
طراحی توسط همراه‌فاند جهت ارائه به شرکت ناک
         <img src="https://uploadkon.ir/uploads/c07912_26nak-naghsh-aval-keifiat-logo.jpg"
             style="position: absolute;
                    top: 10px;
                    left: 100px;
                    width: 250px;
                    opacity: 1.0;
                    z-index: 999;">
                  
</div>
""", unsafe_allow_html=True)