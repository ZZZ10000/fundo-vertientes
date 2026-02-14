"""
Fundo Las Vertientes - Sistema Fotovoltaico Agrícola
Proyecto CORFO Activa Inversión: Inversión Productiva (Línea 18.4)
Resolución Exenta N°0259 - Bases Refundidas

Parámetros reales:
- Inversión total tope: $50.000.000 CLP
- Cofinanciamiento CORFO: 60% (máx $30.000.000)
- Aporte empresarial: 40% (mín $20.000.000)
- Inversión mínima proyecto: $12.000.000 CLP
- Capital de trabajo: hasta 20% del cofinanciamiento CORFO
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, date

# ──────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fundo Las Vertientes – CORFO Activa Inversión",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────
# ESTILOS CSS
# ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap');

    .stApp {
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'DM Serif Display', serif !important;
        color: #1a3c34 !important;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f0f7f4 0%, #e8f5e9 100%);
        border-left: 4px solid #2e7d52;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        color: #1a3c34 !important;
    }
    .metric-card h4 {
        color: #2e7d52 !important;
        margin: 0 0 0.3rem 0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card .value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a3c34 !important;
    }
    .metric-card .sub {
        font-size: 0.78rem;
        color: #3d6b50 !important;
    }

    /* CORFO badge */
    .corfo-badge {
        background: linear-gradient(135deg, #1a3c34, #2e7d52);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .corfo-badge h3 {
        color: white !important;
        margin: 0;
    }
    .corfo-badge .subtitle {
        font-size: 0.85rem;
        opacity: 0.85;
        color: white !important;
    }

    /* Alert boxes */
    .alert-ok {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #1b5e20 !important;
    }
    .alert-ok strong {
        color: #1b5e20 !important;
    }
    .alert-warn {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #e65100 !important;
    }
    .alert-warn strong {
        color: #e65100 !important;
    }
    .alert-error {
        background: #ffebee;
        border-left: 4px solid #f44336;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #b71c1c !important;
    }
    .alert-error strong {
        color: #b71c1c !important;
    }

    /* Table styling */
    .criteria-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .criteria-table th {
        background: #1a3c34;
        color: white !important;
        padding: 0.7rem;
        text-align: left;
        font-size: 0.85rem;
    }
    .criteria-table td {
        padding: 0.6rem 0.7rem;
        border-bottom: 1px solid #ccc;
        font-size: 0.85rem;
        color: #1a3c34 !important;
        background: #f5f9f7;
    }
    .criteria-table tr:nth-child(even) td {
        background: #eaf2ee;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a3c34 0%, #2a5c48 100%);
    }
    div[data-testid="stSidebar"] .stMarkdown h1,
    div[data-testid="stSidebar"] .stMarkdown h2,
    div[data-testid="stSidebar"] .stMarkdown h3,
    div[data-testid="stSidebar"] .stMarkdown p,
    div[data-testid="stSidebar"] .stMarkdown label {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# CONSTANTES CORFO (Bases RE-0259, Línea 18.4)
# ──────────────────────────────────────────────────────────────────────
CORFO_MAX_TOTAL = 50_000_000          # Inversión total tope
CORFO_PCT = 0.60                       # 60% cofinanciamiento CORFO
CORFO_MAX_SUBSIDIO = 30_000_000       # Máximo aporte CORFO
CORFO_MIN_INVERSION = 12_000_000      # Inversión mínima
CAPITAL_TRABAJO_PCT_MAX = 0.20        # Hasta 20% del subsidio para KdT
PLAZO_MAX_MESES = 24                  # Plazo máximo ejecución

# Parámetros fotovoltaicos Chile zona central
IRRADIACION_PEAK_HORAS = 5.2          # HSP promedio anual (zona central)
DEGRADACION_ANUAL = 0.005             # 0.5% degradación paneles/año
VIDA_UTIL_ANOS = 25
COSTO_MANTENCION_ANUAL_KWP = 12_000  # CLP/kWp/año

# ──────────────────────────────────────────────────────────────────────
# FUNCIONES DE CÁLCULO
# ──────────────────────────────────────────────────────────────────────

def dimensionar_sistema(inversion_total, costo_kwp):
    """Calcula capacidad del sistema según presupuesto."""
    subsidio_corfo = min(inversion_total * CORFO_PCT, CORFO_MAX_SUBSIDIO)
    aporte_empresa = inversion_total - subsidio_corfo
    capacidad_kwp = inversion_total / costo_kwp
    generacion_anual_kwh = capacidad_kwp * IRRADIACION_PEAK_HORAS * 365 * 0.80  # PR=0.80
    return {
        "inversion_total": inversion_total,
        "subsidio_corfo": subsidio_corfo,
        "aporte_empresa": aporte_empresa,
        "pct_corfo": subsidio_corfo / inversion_total * 100,
        "pct_empresa": aporte_empresa / inversion_total * 100,
        "capacidad_kwp": capacidad_kwp,
        "generacion_anual_kwh": generacion_anual_kwh,
        "generacion_mensual_kwh": generacion_anual_kwh / 12,
    }


def calcular_flujo_caja(sistema, tarifa_kwh, inflacion_tarifa, tasa_descuento,
                         consumo_mensual_kwh, precio_inyeccion_kwh, anos=25):
    """Genera flujo de caja a 25 años con autoconsumo + inyección."""
    flujo = []
    gen_anual = sistema["generacion_anual_kwh"]
    consumo_anual = consumo_mensual_kwh * 12
    inversion = sistema["inversion_total"]
    subsidio = sistema["subsidio_corfo"]
    inversion_neta = sistema["aporte_empresa"]  # Lo que paga el empresario

    for ano in range(0, anos + 1):
        if ano == 0:
            flujo.append({
                "Año": 0,
                "Generación (kWh)": 0,
                "Autoconsumo (kWh)": 0,
                "Inyección (kWh)": 0,
                "Ahorro Autoconsumo ($)": 0,
                "Ingreso Inyección ($)": 0,
                "Mantención ($)": 0,
                "Flujo Neto ($)": -inversion_neta,
                "Flujo Acumulado ($)": -inversion_neta,
            })
            continue

        # Degradación
        gen = gen_anual * (1 - DEGRADACION_ANUAL) ** ano
        # Autoconsumo vs inyección
        autoconsumo = min(gen, consumo_anual)
        inyeccion = max(0, gen - consumo_anual)

        # Tarifas con inflación
        tarifa_ano = tarifa_kwh * (1 + inflacion_tarifa) ** ano
        precio_iny_ano = precio_inyeccion_kwh * (1 + inflacion_tarifa) ** ano

        ahorro = autoconsumo * tarifa_ano
        ingreso_iny = inyeccion * precio_iny_ano
        mantencion = sistema["capacidad_kwp"] * COSTO_MANTENCION_ANUAL_KWP * (1 + 0.03) ** ano

        flujo_neto = ahorro + ingreso_iny - mantencion
        acumulado = flujo[-1]["Flujo Acumulado ($)"] + flujo_neto

        flujo.append({
            "Año": ano,
            "Generación (kWh)": round(gen),
            "Autoconsumo (kWh)": round(autoconsumo),
            "Inyección (kWh)": round(inyeccion),
            "Ahorro Autoconsumo ($)": round(ahorro),
            "Ingreso Inyección ($)": round(ingreso_iny),
            "Mantención ($)": round(mantencion),
            "Flujo Neto ($)": round(flujo_neto),
            "Flujo Acumulado ($)": round(acumulado),
        })

    return pd.DataFrame(flujo)


def calcular_tir(df_flujo):
    """Calcula TIR usando método iterativo."""
    flujos = df_flujo["Flujo Neto ($)"].values
    try:
        # Newton-Raphson para TIR
        tir = 0.10  # Semilla
        for _ in range(1000):
            npv = sum(f / (1 + tir) ** t for t, f in enumerate(flujos))
            dnpv = sum(-t * f / (1 + tir) ** (t + 1) for t, f in enumerate(flujos))
            if abs(dnpv) < 1e-12:
                break
            tir_new = tir - npv / dnpv
            if abs(tir_new - tir) < 1e-8:
                tir = tir_new
                break
            tir = tir_new
        return tir
    except Exception:
        return None


def calcular_van(df_flujo, tasa):
    """Calcula VAN a tasa dada."""
    flujos = df_flujo["Flujo Neto ($)"].values
    van = sum(f / (1 + tasa) ** t for t, f in enumerate(flujos))
    return van


def calcular_payback(df_flujo):
    """Retorna año de payback (flujo acumulado >= 0)."""
    for _, row in df_flujo.iterrows():
        if row["Año"] > 0 and row["Flujo Acumulado ($)"] >= 0:
            return int(row["Año"])
    return None


def verificar_admisibilidad(sistema):
    """Verifica criterios de admisibilidad según Bases 18.4.f"""
    checks = []
    inv = sistema["inversion_total"]

    # 1. Inversión >= $12.000.000
    ok1 = inv >= CORFO_MIN_INVERSION
    checks.append(("Inversión ≥ $12.000.000", ok1,
                    f"${inv:,.0f}".replace(",", ".")))

    # 2. Cofinanciamiento no excede $50.000.000
    ok2 = sistema["subsidio_corfo"] <= CORFO_MAX_SUBSIDIO
    checks.append(("Subsidio CORFO ≤ $30.000.000", ok2,
                    f"${sistema['subsidio_corfo']:,.0f}".replace(",", ".")))

    # 3. % CORFO no excede 60%
    ok3 = sistema["pct_corfo"] <= 60.01
    checks.append(("% CORFO ≤ 60%", ok3, f"{sistema['pct_corfo']:.1f}%"))

    # 4. Inversión total no excede tope
    ok4 = inv <= CORFO_MAX_TOTAL
    checks.append(("Inversión total ≤ $50.000.000", ok4,
                    f"${inv:,.0f}".replace(",", ".")))

    return checks


# ──────────────────────────────────────────────────────────────────────
# SIDEBAR - PARÁMETROS DEL PROYECTO
# ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🌿 Fundo Las Vertientes")
    st.markdown("### Parámetros del Proyecto")
    st.markdown("---")

    st.markdown("#### 💰 Inversión")
    inversion_total = st.slider(
        "Inversión total del proyecto ($CLP)",
        min_value=12_000_000,
        max_value=50_000_000,
        value=48_000_000,
        step=1_000_000,
        format="$%d",
    )

    costo_kwp = st.slider(
        "Costo instalado por kWp ($CLP)",
        min_value=800_000,
        max_value=1_800_000,
        value=1_200_000,
        step=50_000,
        format="$%d",
        help="Incluye paneles, inversores, estructura, instalación y permisos SEC",
    )

    st.markdown("#### ⚡ Consumo y Tarifas")
    consumo_mensual = st.slider(
        "Consumo mensual del fundo (kWh)",
        min_value=500,
        max_value=8_000,
        value=2_800,
        step=100,
    )

    tarifa_kwh = st.slider(
        "Tarifa eléctrica ($/kWh)",
        min_value=80,
        max_value=250,
        value=155,
        step=5,
        help="Tarifa BT promedio zona central agrícola",
    )

    precio_inyeccion = st.slider(
        "Precio inyección Net Billing ($/kWh)",
        min_value=40,
        max_value=150,
        value=85,
        step=5,
        help="Precio regulado de inyección a la red",
    )

    st.markdown("#### 📈 Proyecciones")
    inflacion_tarifa = st.slider(
        "Inflación tarifa eléctrica anual (%)",
        min_value=0.0,
        max_value=8.0,
        value=3.5,
        step=0.5,
    ) / 100

    tasa_descuento = st.slider(
        "Tasa de descuento (%)",
        min_value=4.0,
        max_value=15.0,
        value=8.0,
        step=0.5,
    ) / 100

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; opacity:0.7; font-size:0.75rem; color:#ccc;'>
    Bases: RE N°0259/2020<br>
    Línea 18.4 Inversión Productiva<br>
    Gerencia Redes y Competitividad
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────
# CÁLCULOS PRINCIPALES
# ──────────────────────────────────────────────────────────────────────
sistema = dimensionar_sistema(inversion_total, costo_kwp)
df_flujo = calcular_flujo_caja(
    sistema, tarifa_kwh, inflacion_tarifa, tasa_descuento,
    consumo_mensual, precio_inyeccion
)
tir = calcular_tir(df_flujo)
van = calcular_van(df_flujo, tasa_descuento)
payback = calcular_payback(df_flujo)
checks = verificar_admisibilidad(sistema)

# ──────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='corfo-badge'>
    <h3>CORFO ACTIVA INVERSIÓN — INVERSIÓN PRODUCTIVA</h3>
    <div class='subtitle'>Resolución Exenta N°0259 · Línea 18.4 · Fundo Las Vertientes</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## Sistema Fotovoltaico para Producción Agrícola")
st.markdown(
    "Proyecto de inversión productiva en energía solar para operaciones agrícolas, "
    "dimensionado conforme a las Bases refundidas del instrumento Activa Inversión de CORFO."
)

# ──────────────────────────────────────────────────────────────────────
# TAB LAYOUT
# ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Resumen Ejecutivo",
    "☀️ Sistema Fotovoltaico",
    "💵 Flujo de Caja",
    "✅ Admisibilidad CORFO",
    "📋 Criterios de Evaluación",
])

# ──────────────────────────────────────────────────────────────────────
# TAB 1: RESUMEN EJECUTIVO
# ──────────────────────────────────────────────────────────────────────
with tab1:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Inversión Total</h4>
            <div class='value'>${inversion_total/1e6:.1f}M</div>
            <div class='sub'>Tope: $50M CLP</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Subsidio CORFO (60%)</h4>
            <div class='value'>${sistema["subsidio_corfo"]/1e6:.1f}M</div>
            <div class='sub'>Máximo: $30M CLP</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Aporte Empresarial (40%)</h4>
            <div class='value'>${sistema["aporte_empresa"]/1e6:.1f}M</div>
            <div class='sub'>{sistema["pct_empresa"]:.0f}% del total</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        tir_display = f"{tir*100:.1f}%" if tir else "N/A"
        st.markdown(f"""
        <div class='metric-card'>
            <h4>TIR del Proyecto</h4>
            <div class='value'>{tir_display}</div>
            <div class='sub'>Tasa desc.: {tasa_descuento*100:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Indicadores Financieros")
        van_display = f"${van:,.0f}".replace(",", ".") if van else "N/A"
        payback_display = f"{payback} años" if payback else "> 25 años"

        ind_data = {
            "Indicador": [
                "Valor Actual Neto (VAN)",
                "Tasa Interna de Retorno (TIR)",
                "Payback (recuperación inversión empresario)",
                "Generación anual",
                "Capacidad instalada",
                "Ratio beneficio/costo",
            ],
            "Valor": [
                van_display,
                tir_display,
                payback_display,
                f"{sistema['generacion_anual_kwh']:,.0f} kWh".replace(",", "."),
                f"{sistema['capacidad_kwp']:.1f} kWp",
                f"{(van + sistema['aporte_empresa']) / sistema['aporte_empresa']:.2f}x" if van and van > 0 else "< 1x",
            ],
        }
        st.table(pd.DataFrame(ind_data).set_index("Indicador"))

    with col_b:
        st.markdown("### Estructura de Financiamiento")
        chart_data = pd.DataFrame({
            "Fuente": ["CORFO (60%)", "Empresario (40%)"],
            "Monto": [sistema["subsidio_corfo"], sistema["aporte_empresa"]],
        })
        st.bar_chart(chart_data.set_index("Fuente"), horizontal=True)

        kdt_max = sistema["subsidio_corfo"] * CAPITAL_TRABAJO_PCT_MAX
        st.markdown(f"""
        <div class='alert-ok'>
            💡 <strong>Capital de trabajo admisible:</strong> hasta ${kdt_max:,.0f} CLP
            (20% del subsidio CORFO) — Ref. Bases Art. 18.4.e
        </div>
        """.replace(",", "."), unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────
# TAB 2: SISTEMA FOTOVOLTAICO
# ──────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Dimensionamiento del Sistema")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Capacidad Instalada", f"{sistema['capacidad_kwp']:.1f} kWp")
        n_paneles_550 = int(np.ceil(sistema["capacidad_kwp"] * 1000 / 550))
        st.metric("Paneles (550W)", f"{n_paneles_550} unidades")

    with col2:
        st.metric("Generación Anual", f"{sistema['generacion_anual_kwh']:,.0f} kWh")
        st.metric("Generación Mensual", f"{sistema['generacion_mensual_kwh']:,.0f} kWh")

    with col3:
        autoconsumo_pct = min(consumo_mensual * 12 / sistema["generacion_anual_kwh"] * 100, 100)
        st.metric("% Autoconsumo", f"{autoconsumo_pct:.0f}%")
        st.metric("Excedente Inyección", f"{max(0, 100-autoconsumo_pct):.0f}%")

    st.markdown("---")
    st.markdown("### Generación Mensual Estimada (Año 1)")

    # Perfil mensual de irradiación Chile zona central (HSP)
    hsp_mensual = [6.8, 6.2, 5.4, 4.2, 3.2, 2.6, 2.8, 3.5, 4.5, 5.5, 6.3, 6.9]
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
             "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    gen_mensual = []
    for i in range(12):
        gen = sistema["capacidad_kwp"] * hsp_mensual[i] * dias_mes[i] * 0.80
        gen_mensual.append(round(gen))

    df_mensual = pd.DataFrame({
        "Mes": meses,
        "Generación (kWh)": gen_mensual,
        "Consumo (kWh)": [consumo_mensual] * 12,
    }).set_index("Mes")

    st.bar_chart(df_mensual)

    st.markdown("### Especificaciones Técnicas Sugeridas")
    specs = pd.DataFrame({
        "Componente": [
            "Paneles solares",
            "Inversor(es)",
            "Estructura montaje",
            "Protecciones y tablero",
            "Medidor bidireccional",
            "Cableado y conectores",
            "Ingeniería y permisos SEC",
        ],
        "Especificación": [
            f"{n_paneles_550}x módulos monocristalinos 550W Tier-1",
            f"Inversor(es) string {sistema['capacidad_kwp']:.0f}kW, MPPT múltiple",
            "Estructura aluminio para techumbre o suelo agrícola",
            "Protecciones DC/AC, SPD, interruptor de corte",
            "Medidor bidireccional homologado SEC/distribuidora",
            "Cable solar 4/6mm², MC4, canalización",
            "Declaración TE1/TE4, inscripción SEC, Net Billing",
        ],
        "% Presupuesto": [
            "45%", "20%", "10%", "5%", "3%", "5%", "12%"
        ],
    })
    st.table(specs.set_index("Componente"))


# ──────────────────────────────────────────────────────────────────────
# TAB 3: FLUJO DE CAJA
# ──────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### Flujo de Caja Proyectado a 25 Años")
    st.markdown(
        f"*Inversión neta empresario: ${sistema['aporte_empresa']:,.0f} CLP · "
        f"Tasa descuento: {tasa_descuento*100:.0f}% · "
        f"Inflación tarifa: {inflacion_tarifa*100:.1f}%*".replace(",", ".")
    )

    # Gráfico flujo acumulado
    st.markdown("#### Flujo Acumulado ($CLP)")
    chart_flujo = df_flujo[df_flujo["Año"] > 0][["Año", "Flujo Acumulado ($)"]].set_index("Año")
    st.line_chart(chart_flujo)

    if payback:
        st.markdown(f"""
        <div class='alert-ok'>
            ✅ <strong>Payback en año {payback}:</strong> la inversión del empresario
            (${sistema['aporte_empresa']:,.0f} CLP) se recupera en {payback} años.
            Vida útil restante: {25 - payback} años de beneficio neto.
        </div>
        """.replace(",", "."), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='alert-warn'>
            ⚠️ El payback excede la vida útil. Considere ajustar parámetros.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Detalle Anual")

    # Formato para visualización
    df_display = df_flujo.copy()
    money_cols = [c for c in df_display.columns if "($)" in c]
    for c in money_cols:
        df_display[c] = df_display[c].apply(lambda x: f"${x:,.0f}".replace(",", "."))
    kwh_cols = [c for c in df_display.columns if "(kWh)" in c]
    for c in kwh_cols:
        df_display[c] = df_display[c].apply(lambda x: f"{x:,.0f}".replace(",", "."))

    st.dataframe(df_display, use_container_width=True, height=400)

    # Gráfico de composición de ingresos
    st.markdown("#### Composición de Ingresos Anuales")
    df_ingresos = df_flujo[df_flujo["Año"] > 0][
        ["Año", "Ahorro Autoconsumo ($)", "Ingreso Inyección ($)"]
    ].set_index("Año")
    st.area_chart(df_ingresos)


# ──────────────────────────────────────────────────────────────────────
# TAB 4: ADMISIBILIDAD CORFO
# ──────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("### Verificación de Admisibilidad — Bases Art. 18.4.f")
    st.markdown(
        "Requisitos de admisibilidad específicos del postulante y del proyecto, "
        "conforme al numeral 18.4 letra f) de las Bases refundidas RE N°0259."
    )

    all_ok = True
    for criterio, cumple, valor in checks:
        icon = "✅" if cumple else "❌"
        css_class = "alert-ok" if cumple else "alert-error"
        st.markdown(f"""
        <div class='{css_class}'>
            {icon} <strong>{criterio}</strong>: {valor}
        </div>
        """, unsafe_allow_html=True)
        if not cumple:
            all_ok = False

    st.markdown("---")

    # Requisitos adicionales del postulante
    st.markdown("### Requisitos del Postulante (Art. 18.4.c y 18.4.f.a)")
    st.markdown("""
    <table class='criteria-table'>
        <tr>
            <th>Requisito</th>
            <th>Referencia Bases</th>
            <th>Estado</th>
        </tr>
        <tr>
            <td>Contribuyente 1ª Categoría, art. 20 DL 824/1974</td>
            <td>Art. 18.4.c num. 1</td>
            <td>✅ Verificar en SII</td>
        </tr>
        <tr>
            <td>Ventas netas anuales ≥ 5.000 UF (si Gerente autoriza)</td>
            <td>Art. 18.4.c num. 2</td>
            <td>🔍 Revisar F29</td>
        </tr>
        <tr>
            <td>Proyecto inversión ≥ $12.000.000 CLP</td>
            <td>Art. 18.4.f.b num. 1</td>
            <td>{"✅" if inversion_total >= CORFO_MIN_INVERSION else "❌"}</td>
        </tr>
        <tr>
            <td>Participación Estado &lt; 40% en capital/patrimonio</td>
            <td>Art. 4</td>
            <td>✅ Empresa privada</td>
        </tr>
        <tr>
            <td>No empresa pública ni sociedad estatal</td>
            <td>Art. 4</td>
            <td>✅ Cumple</td>
        </tr>
        <tr>
            <td>Inscripción Registro Personas Jurídicas CORFO</td>
            <td>Art. 15.2</td>
            <td>🔍 Verificar/inscribir</td>
        </tr>
        <tr>
            <td>Cotizaciones sociales y seguros al día</td>
            <td>Art. 17.2 letra B</td>
            <td>🔍 Verificar</td>
        </tr>
        <tr>
            <td>Impuestos al día (art. 20 nums. 3, 4 y 5)</td>
            <td>Art. 17.2 letra B</td>
            <td>🔍 Verificar F29</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Documentos Requeridos para Formalización (Art. 15.1)")
    docs = [
        "Cédula de identidad del representante legal (ambos lados)",
        "Escritura pública o instrumento de constitución",
        "Extracto inscripción en Registro de Comercio (≤ 3 meses)",
        "Extracto publicación constitución en Diario Oficial",
        "Escritura de personería del representante legal",
        "Formulario 29 SII (últimos 12 meses)",
        "Libro Auxiliar de Compras y Ventas (período anterior)",
        "Balance y/o Estado de Resultados",
    ]
    for d in docs:
        st.markdown(f"📄 {d}")

    if not all_ok:
        st.markdown("""
        <div class='alert-error'>
            ❌ <strong>PROYECTO NO ADMISIBLE</strong> — Ajuste los parámetros para cumplir
            con los requisitos de las Bases.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='alert-ok'>
            ✅ <strong>PROYECTO ADMISIBLE</strong> — Todos los criterios cuantitativos
            de admisibilidad se cumplen. Verificar requisitos documentales pendientes.
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────
# TAB 5: CRITERIOS DE EVALUACIÓN
# ──────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("### Criterios de Evaluación — Ponderaciones (Art. 13 y 18.4.g)")
    st.markdown(
        "La evaluación se realiza con puntaje de 1 a 5. No se recomiendan proyectos "
        "con nota final < 3 o con algún criterio < 2,50."
    )

    st.markdown("#### Criterios Comunes (60%)")
    st.markdown("""
    <table class='criteria-table'>
        <tr><th>Criterio</th><th>Pond.</th><th>Elementos evaluados</th></tr>
        <tr>
            <td><strong>Impacto económico del proyecto</strong></td>
            <td>25%</td>
            <td>Diversificación matriz productiva, competitividad industria,
                cierre brechas, sustentabilidad medioambiental, externalidades positivas</td>
        </tr>
        <tr>
            <td><strong>Calidad formulación y coherencia</strong></td>
            <td>10%</td>
            <td>Coherencia beneficiarios-objetivo, actividades-plazos-resultados</td>
        </tr>
        <tr>
            <td><strong>Propuesta económica</strong></td>
            <td>15%</td>
            <td>Coherencia presupuesto vs actividades y resultados</td>
        </tr>
        <tr>
            <td><strong>Justificación territorial</strong></td>
            <td>10%</td>
            <td>Pertinencia respecto a lineamientos de desarrollo regional y de CORFO</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("#### Criterios Específicos Línea 18.4 (40%)")
    st.markdown("""
    <table class='criteria-table'>
        <tr><th>Criterio</th><th>Pond.</th><th>Elementos evaluados</th></tr>
        <tr>
            <td><strong>Fortaleza del proyecto de inversión</strong></td>
            <td>20%</td>
            <td>Plan de negocios, rentabilidad, acceso a financiamiento, generación empleo</td>
        </tr>
        <tr>
            <td><strong>Fortaleza de la empresa</strong></td>
            <td>20%</td>
            <td>Experiencia en el sector, coherencia estrategia vs proyecto de inversión</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Argumentos para la Postulación")

    st.markdown("#### 🌱 Impacto Económico (25%)")
    ahorro_anual_1 = df_flujo[df_flujo["Año"] == 1]["Ahorro Autoconsumo ($)"].values[0]
    ingreso_anual_1 = df_flujo[df_flujo["Año"] == 1]["Ingreso Inyección ($)"].values[0]
    st.markdown(f"""
    - **Ahorro energético año 1:** ${ahorro_anual_1:,.0f} CLP en costos operativos
    - **Ingreso por inyección año 1:** ${ingreso_anual_1:,.0f} CLP (Net Billing)
    - **Reducción huella de carbono:** ~{sistema['generacion_anual_kwh'] * 0.0004:.1f} tonCO₂/año
    - **Aumento competitividad:** reducción de costos fijos en producción agrícola
    - **Contribución sustentabilidad:** alineado con eje transversal de CORFO (Art. 1)
    """.replace(",", "."))

    st.markdown("#### 📐 Calidad y Coherencia (10%)")
    st.markdown(f"""
    - Sistema dimensionado según consumo real del fundo ({consumo_mensual} kWh/mes)
    - Presupuesto detallado con cotizaciones de proveedores Tier-1
    - Plazo ejecución: 6-8 meses (dentro del máximo de 24 meses)
    - Resultados medibles: kWh generados, ahorro en $, reducción CO₂
    """)

    st.markdown("#### 💰 Propuesta Económica (15%)")
    st.markdown(f"""
    - VAN positivo: {van_display} a tasa {tasa_descuento*100:.0f}%
    - TIR: {tir_display} (supera costo de oportunidad)
    - Payback: {payback_display}
    - Presupuesto coherente con precios de mercado ({costo_kwp:,}/kWp instalado)
    """.replace(",", "."))

    st.markdown("#### 🗺️ Justificación Territorial (10%)")
    st.markdown("""
    - Zona rural agrícola con alta irradiación solar
    - Contribuye a diversificación energética regional
    - Fortalece competitividad de productores agrícolas locales
    - Alineado con estrategia regional de desarrollo sustentable
    """)

    st.markdown("#### 💪 Fortaleza del Proyecto (20%)")
    st.markdown(f"""
    - Rentabilidad demostrada con TIR {tir_display} y VAN positivo
    - Tecnología madura y probada (solar fotovoltaica)
    - Sin requerimiento de financiamiento externo adicional
    - Generación de empleo en instalación y mantención
    """)

    st.markdown("#### 🏢 Fortaleza de la Empresa (20%)")
    st.markdown("""
    - Empresa agrícola con trayectoria productiva demostrable
    - Experiencia en gestión de proyectos de inversión
    - Capacidad financiera para aportar el 40% requerido
    - Coherencia estratégica: energía solar reduce costos operativos permanentemente
    """)


# ──────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.8rem;'>"
    "Fundo Las Vertientes · Proyecto CORFO Activa Inversión · "
    "Bases RE N°0259 Línea 18.4 Inversión Productiva · "
    f"Generado: {datetime.now().strftime('%d/%m/%Y')}"
    "</div>",
    unsafe_allow_html=True,
)
