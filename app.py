# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Fundo Las Vertientes - Proyecto ERNC",page_icon="🌱",layout="wide",initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');
:root{--vd:#2C5F2D;--vm:#4A7C59;--vc:#97BC62;--do:#D4A843;--tc:#B85042;}
.main .block-container{padding-top:.8rem;max-width:1250px;}
h1,h2,h3{font-family:'Playfair Display',Georgia,serif!important;}
p,li,span,div,td,th{font-family:'Source Sans 3',Calibri,sans-serif!important;}
.hero{background:linear-gradient(135deg,#2C5F2D 0%,#1a5228 40%,#0f3518 100%);border-radius:18px;padding:2.8rem 3rem;color:#fff;position:relative;overflow:hidden;margin-bottom:1.5rem;}
.hero::after{content:'';position:absolute;top:-60px;right:-60px;width:300px;height:300px;border-radius:50%;background:rgba(151,188,98,.12);}
.hero h1{font-size:2.4rem;margin:0 0 .2rem 0;color:#fff!important;position:relative;z-index:1;}
.hero .sub{font-size:1.15rem;opacity:.88;font-weight:300;position:relative;z-index:1;}
.hero .badges{margin-top:1rem;position:relative;z-index:1;}
.hero .badge{display:inline-block;background:rgba(255,255,255,.15);padding:5px 16px;border-radius:20px;font-size:.82rem;margin-right:8px;}
.mc{background:#fff;border-radius:14px;padding:1.4rem;box-shadow:0 2px 16px rgba(0,0,0,.05);border-left:4px solid var(--vd);margin-bottom:8px;}
.mc:hover{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.08);}
.mc .lb{font-size:.72rem;color:#666;text-transform:uppercase;letter-spacing:1.2px;font-weight:600;}
.mc .vl{font-size:2rem;font-weight:800;color:var(--vd);margin:6px 0 2px;}
.mc .dt{font-size:.85rem;color:#444;}
.mc.accent{border-left-color:var(--do);}
.mc.accent .vl{color:var(--do);}
.sh{border-bottom:3px solid var(--vm);padding-bottom:.4rem;margin:2.2rem 0 1rem;}
.ib{background:linear-gradient(to right,#eef6e3,#fff);border-left:4px solid var(--vc);border-radius:0 10px 10px 0;padding:1rem 1.3rem;margin:.7rem 0;font-size:.95rem;color:#333;}
.wb{background:linear-gradient(to right,#fff8e6,#fff);border-left:4px solid var(--do);border-radius:0 10px 10px 0;padding:1rem 1.3rem;margin:.7rem 0;font-size:.95rem;color:#333;}
.tl{border-left:3px solid var(--vm);padding:.7rem 0 .7rem 1.5rem;position:relative;margin-left:.6rem;}
.tl::before{content:'';position:absolute;left:-8px;top:.9rem;width:13px;height:13px;border-radius:50%;background:var(--vc);border:2px solid #fff;}
.tag{display:inline-block;background:var(--vc);color:#fff;padding:3px 12px;border-radius:12px;font-size:.75rem;font-weight:600;margin:2px;}
.tag.gold{background:var(--do);}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#2C5F2D,#163017);}
section[data-testid="stSidebar"] *{color:#fff!important;}
section[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.2);}
.stTabs [data-baseweb="tab-list"]{gap:6px;}
.stTabs [data-baseweb="tab"]{background:#f5f5f5;border-radius:10px 10px 0 0;padding:10px 22px;font-weight:600;}
.stTabs [aria-selected="true"]{background:#2C5F2D!important;color:#fff!important;}
</style>
""", unsafe_allow_html=True)

# === DATOS ===
flujo_df = pd.DataFrame({
    "Año":[0,1,2,3,4,5],
    "Inversión":[-185000000,0,0,0,0,0],
    "Subsidio_CORFO":[92500000,0,0,0,0,0],
    "Ingreso_Trigo":[0,28800000,30240000,31752000,33339600,35006580],
    "Ingreso_Vino":[0,36000000,39600000,43560000,47916000,52707600],
    "Ingreso_Frutales":[0,8400000,12600000,16800000,21000000,25200000],
    "Ahorro_Energía":[0,7200000,7416000,7638480,7867634,8103663],
    "Costos_Op":[0,-18500000,-19055000,-19626650,-20215450,-20821813],
    "Mant_ERNC":[0,-1850000,-1850000,-1850000,-1850000,-1850000],
    "Cuota_Crédito":[0,-14832000,-14832000,-14832000,-14832000,-14832000],
})
flujo_df["Flujo_Neto"] = flujo_df.iloc[:,1:].sum(axis=1)
flujo_df["Flujo_Acum"] = flujo_df["Flujo_Neto"].cumsum()

def fmt(n):
    if abs(n)>=1000000:
        return f"${n/1000000:,.1f}M CLP"
    return f"${n:,.0f} CLP"

def mc(label,value,detail="",css=""):
    return f'<div class="mc {css}"><div class="lb">{label}</div><div class="vl">{value}</div><div class="dt">{detail}</div></div>'

# === SIDEBAR ===
with st.sidebar:
    st.markdown("### 🌱 Fundo Las Vertientes")
    st.markdown("---")
    sec = st.radio("Navegación",["🏠 Resumen Ejecutivo","👤 Perfil del Cliente","⚡ Proyecto Técnico","💰 Evaluación Financiera","📊 Flujo de Caja","🏦 Situación Tributaria","📋 Postulación CORFO","📎 Documentación"],index=0)
    st.markdown("---")
    st.markdown("<div style='font-size:.78rem;opacity:.7;line-height:1.5;'><b>Consultoría:</b> Makey E.I.R.L.<br>RUT 77.044.017-3<br>José A. Eyzaguirre R.<br><br><b>Fecha:</b> Febrero 2026<br><b>Convocatoria:</b> CORFO Activa Inversión</div>", unsafe_allow_html=True)

# ========== RESUMEN EJECUTIVO ==========
if sec=="🏠 Resumen Ejecutivo":
    st.markdown('<div class="hero"><h1>Fundo Las Vertientes</h1><div class="sub">Proyecto de Modernización Energética con ERNC para Riego Tecnificado</div><div class="sub" style="opacity:.7;font-size:.95rem;margin-top:.3rem;">Quinchamalí, Chillán · Región de Ñuble · 52 hectáreas</div><div class="badges"><span class="badge">🌞 Energía Solar Fotovoltaica</span><span class="badge">💧 Riego Tecnificado</span><span class="badge">🍇 Vinícola · Frutícola · Cereales</span><span class="badge">📋 CORFO Activa Inversión 2026</span></div></div>', unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(mc("Inversión Total","$185.000.000","Sistema fotovoltaico + riego"),unsafe_allow_html=True)
    with c2: st.markdown(mc("Subsidio CORFO","$92.500.000","50% de la inversión","accent"),unsafe_allow_html=True)
    with c3: st.markdown(mc("TIR Proyecto","38,2%","Horizonte 5 años"),unsafe_allow_html=True)
    with c4: st.markdown(mc("Payback","2,8 años","Recuperación de inversión"),unsafe_allow_html=True)
    st.markdown("")
    c1,c2=st.columns([3,2])
    with c1:
        st.markdown('<h3 class="sh">🎯 Oportunidad de Inversión</h3>',unsafe_allow_html=True)
        st.markdown('<div class="ib"><b>El Fundo Las Vertientes</b> es una unidad agrícola de <b>52 hectáreas</b> en Quinchamalí, Chillán, con más de <b>20 años de operación</b> continua (inicio 2004). Actualmente opera cultivos de <b>trigo y vid vinífera</b>, pero gran parte de su superficie está <b>subutilizada por depender de secano</b>.</div>',unsafe_allow_html=True)
        st.markdown('<div class="wb"><b>💡 Propuesta:</b> Instalar un sistema fotovoltaico de <b>150 kW</b> (300 paneles) que alimente bombas de riego tecnificado, transformando <b>terreno de secano en superficie productiva regada</b>, habilitando nuevas líneas de producción (frutales) y multiplicando la rentabilidad por hectárea.</div>',unsafe_allow_html=True)
        st.markdown("**Impacto esperado:**\n- 🌾 **Trigo:** Rendimiento de 45 a 80 qq/ha con riego\n- 🍇 **Viña:** Expansión de 8 a 15 ha vinificables\n- 🍑 **Frutales:** 10 nuevas hectáreas habilitadas\n- ⚡ **Ahorro energético:** $7.200.000 anuales\n- 👷 **Empleo:** 8-12 jornales permanentes adicionales")
    with c2:
        st.markdown('<h3 class="sh">📐 Estructura de Financiamiento</h3>',unsafe_allow_html=True)
        fig=go.Figure(go.Pie(labels=["Subsidio CORFO (50%)","Crédito Bancario (32,4%)","Aporte Propio (17,6%)"],values=[92500000,60000000,32500000],marker=dict(colors=["#2C5F2D","#D4A843","#B85042"]),hole=0.55,textinfo="label+percent",textfont=dict(size=11)))
        fig.update_layout(height=320,margin=dict(t=10,b=10,l=10,r=10),showlegend=False,annotations=[dict(text="$185M",x=0.5,y=0.5,font_size=22,font_color="#2C5F2D",showarrow=False)],paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("| Fuente | Monto (CLP) |\n|--------|------:|\n| Subsidio CORFO | $92.500.000 |\n| Crédito BancoEstado | $60.000.000 |\n| Aporte Propio | $32.500.000 |\n| **Total** | **$185.000.000** |")

# ========== PERFIL DEL CLIENTE ==========
elif sec=="👤 Perfil del Cliente":
    st.markdown('<h2 class="sh">👤 Perfil del Cliente — Antecedentes Tributarios</h2>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: st.markdown(mc("Contribuyente","Mirta A. Vera S.","RUT 4.306.006-6"),unsafe_allow_html=True)
    with c2: st.markdown(mc("Antigüedad","22 años","Inicio actividades: 01/03/2004"),unsafe_allow_html=True)
    with c3: st.markdown(mc("Avalúo Fiscal","$219.803.444","Propiedad Rol 02229-00064"),unsafe_allow_html=True)
    st.markdown("")
    c1,c2=st.columns(2)
    with c1:
        st.markdown("#### 📋 Datos del Contribuyente")
        st.dataframe(pd.DataFrame({"Campo":["Nombre","RUT","Domicilio","Inicio Actividades","Régimen Tributario","Categoría","Act. Principal","Act. Secundaria","Anotaciones SII"],"Detalle":["Mirta Aurora Vera Sepúlveda","4.306.006-6","Fundo Las Vertientes SN, Quinchamalí, Chillán","01/03/2004","Pro Pyme General (14D) - Contabilidad Completa","Primera Categoría","Cultivo de Trigo (011101) - desde 12/09/2013","Cultivo de Uva para Vino (012112) - desde 15/04/2014","✅ No registra observaciones"]}),hide_index=True,use_container_width=True)
    with c2:
        st.markdown("#### 🏡 Propiedad Registrada en SII")
        st.dataframe(pd.DataFrame({"Campo":["Comuna","Rol","Dirección","Destino","Avalúo Fiscal","Contribución Semestral","Condición","Inscripción","% Derecho"],"Detalle":["Chillán","02229-00064","Las Vertientes","Agrícola","$219.803.444","$343.430","Afecto","113VTA/146/2013","100%"]}),hide_index=True,use_container_width=True)
    st.markdown('<div class="ib"><b>✅ Fortalezas del perfil crediticio:</b><br>• 22 años de actividad continua sin interrupciones<br>• Sin anotaciones ni observaciones tributarias<br>• Propiedad $219.803.444 avalúo fiscal - 100% de propiedad<br>• Régimen Pro Pyme con contabilidad completa<br>• Documentación electrónica actualizada</div>',unsafe_allow_html=True)
    st.markdown("#### 📄 Declaraciones de Renta (F22)")
    c1,c2=st.columns(2)
    with c1:
        st.markdown("**Año Tributario 2025**\n\n| Concepto | Valor (CLP) |\n|----------|------:|\n| Ingresos del giro percibidos | $6.810.800 |\n| Egresos anuales | $8.654.457 |\n| Base imponible IDPC | -$1.843.657 |\n| PPM acumulados | $8.726 |\n| Devolución solicitada | $8.726 |")
    with c2:
        st.markdown("**Año Tributario 2024**\n\n| Concepto | Valor (CLP) |\n|----------|------:|\n| Rentas fuente nacional | $2.517.139 |\n| PPM acumulados | $6.667 |\n| Devolución solicitada | $6.667 |")
    st.markdown('<div class="wb"><b>📌 Nota:</b> La pérdida tributaria AT 2025 refleja un ejercicio con altos costos y baja productividad por <b>limitación hídrica (secano)</b>. Este proyecto busca resolver esa restricción estructural.</div>',unsafe_allow_html=True)

# ========== PROYECTO TÉCNICO ==========
elif sec=="⚡ Proyecto Técnico":
    st.markdown('<h2 class="sh">⚡ Ingeniería del Proyecto — Sistema Fotovoltaico para Riego</h2>',unsafe_allow_html=True)
    tabs=st.tabs(["🌞 Sistema Fotovoltaico","💧 Riego Tecnificado","🗺️ Distribución Predio","📅 Cronograma"])
    with tabs[0]:
        st.markdown("### Dimensionamiento del Sistema Solar Fotovoltaico")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(mc("Potencia Instalada","150 kWp","Peak de generación"),unsafe_allow_html=True)
        with c2: st.markdown(mc("Paneles Solares","300 uds.","550W monocristalinos","accent"),unsafe_allow_html=True)
        with c3: st.markdown(mc("Inversores","3 x 50 kW","String inverters trifásicos"),unsafe_allow_html=True)
        with c4: st.markdown(mc("Generación Anual","255 MWh","~1.700 hrs equiv. Ñuble"),unsafe_allow_html=True)
        st.markdown("")
        c1,c2=st.columns([3,2])
        with c1:
            st.markdown("#### Especificaciones Técnicas")
            st.dataframe(pd.DataFrame({"Componente":["Paneles fotovoltaicos","Inversores","Estructura montaje","Cableado DC/AC","Protecciones","Monitoreo","Bomba sumergible 1","Bomba sumergible 2","Bomba booster","Estanque acumulador"],"Especificación":["Monocristalino 550W, efic. >21%","Trifásico 50kW, MPPT dual","Aluminio anodizado, 30°","Cable solar 6mm², AC 3x16mm²","DC+AC, SPD","WiFi/4G, app remota","15HP, 80m³/h, pozo 60m","10HP, 50m³/h, noria","7,5HP, 4 bar, goteo","100m³ HDPE, geomembrana"],"Cant.":["300","3","1 lote","1 lote","1","1","1","1","1","1"]}),hide_index=True,use_container_width=True)
        with c2:
            st.markdown("#### Generación Mensual Estimada (MWh)")
            meses=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
            gen=[32,28,24,18,12,9,10,14,19,24,29,31]
            fig=go.Figure(go.Bar(x=meses,y=gen,marker=dict(color=gen,colorscale=[[0,"#D4A843"],[0.5,"#97BC62"],[1,"#2C5F2D"]]),text=[str(v) for v in gen],textposition="outside"))
            fig.update_layout(height=340,margin=dict(t=30,b=30,l=40,r=10),yaxis_title="MWh",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",yaxis=dict(gridcolor="#eee"))
            st.plotly_chart(fig,use_container_width=True)
    with tabs[1]:
        st.markdown("### Sistema de Riego Tecnificado")
        c1,c2=st.columns(2)
        with c1:
            st.markdown('<div class="ib"><b>Situación Actual (Secano):</b><br>• 52 ha totales, solo ~15 ha en producción<br>• Dependencia total de lluvia estacional<br>• Rendimiento trigo: 45 qq/ha<br>• Sin riego para viña en verano</div>',unsafe_allow_html=True)
            st.markdown('<div class="ib" style="border-left-color:#2C5F2D;"><b>Situación Proyectada (Con ERNC + Riego):</b><br>• 52 ha con cobertura de riego<br>• Goteo (viña/frutales) + aspersión (trigo)<br>• Rendimiento trigo: 80 qq/ha (+78%)<br>• 10 ha nuevas para frutales<br>• Autonomía energética</div>',unsafe_allow_html=True)
        with c2:
            st.markdown("#### Distribución de Cultivos Proyectada")
            fig=go.Figure(go.Pie(labels=["Trigo","Viña","Frutales","Infraest.","Bosque"],values=[20,15,10,3,4],marker=dict(colors=["#D4A843","#6D2E46","#97BC62","#888","#2C5F2D"]),hole=0.45,textinfo="label+value",textfont=dict(size=11)))
            fig.update_layout(height=320,margin=dict(t=10,b=10,l=10,r=10),showlegend=False,annotations=[dict(text="52 ha",x=0.5,y=0.5,font_size=20,font_color="#2C5F2D",showarrow=False)],paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig,use_container_width=True)
    with tabs[2]:
        st.markdown("### Distribución del Predio")
        st.markdown("| Zona | Superficie | Cultivo | Riego | Estado |\n|------|-----------|---------|-------|--------|\n| Sector Norte | 20 ha | Trigo | Aspersión | Mejorado |\n| Sector Centro | 15 ha | Viña vinificable | Goteo | Expansión |\n| Sector Sur | 10 ha | Frutales (cerezos, nogales) | Goteo | **NUEVO** |\n| Sector Poniente | 3 ha | Infraestructura, bodega | - | Existente |\n| Sector Oriente | 4 ha | Bosque nativo | - | Protección |")
        st.markdown('<div class="ib"><b>Ubicación sistema fotovoltaico:</b> Sector Poniente, junto a bodega. Superficie: ~3.000 m². Orientación norte, sin sombra. Distancia a tablero: 80 m.</div>',unsafe_allow_html=True)
    with tabs[3]:
        st.markdown("### Cronograma de Implementación")
        for f,t,d in [("Feb 2026","Postulación CORFO Activa Inversión","Formulación y envío"),("Mar 2026","Evaluación y adjudicación CORFO","Revisión AOI"),("Abr 2026","Gestión crédito BancoEstado","Solicitud con carpeta"),("May 2026","Importación de equipos","Paneles, inversores, bombas"),("Jun-Jul 2026","Obras civiles y montaje","Fundaciones, estructura, eléctrica"),("Ago 2026","Puesta en marcha","Pruebas, conexión, monitoreo"),("Sep 2026","Inicio operación","Primera temporada con ERNC")]:
            st.markdown(f'<div class="tl"><span class="tag">{f}</span><br><b>{t}</b><br><span style="color:#666;font-size:.9rem;">{d}</span></div>',unsafe_allow_html=True)

# ========== EVALUACIÓN FINANCIERA ==========
elif sec=="💰 Evaluación Financiera":
    st.markdown('<h2 class="sh">💰 Evaluación Financiera del Proyecto</h2>',unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(mc("VAN (10%)","$67.800.000","Valor Actual Neto positivo"),unsafe_allow_html=True)
    with c2: st.markdown(mc("TIR","38,2%","Tasa Interna de Retorno","accent"),unsafe_allow_html=True)
    with c3: st.markdown(mc("Payback","2,8 años","Período recuperación"),unsafe_allow_html=True)
    with c4: st.markdown(mc("B/C","1,73","Beneficio / Costo"),unsafe_allow_html=True)
    st.markdown("")
    c1,c2=st.columns(2)
    with c1:
        st.markdown("#### 📈 Ingresos Proyectados por Línea (5 años)")
        yrs=["Año 1","Año 2","Año 3","Año 4","Año 5"]
        fig=go.Figure()
        fig.add_trace(go.Bar(name="Trigo",x=yrs,y=[28.8,30.24,31.75,33.34,35.01],marker_color="#D4A843"))
        fig.add_trace(go.Bar(name="Uva/Vino",x=yrs,y=[36.0,39.6,43.56,47.92,52.71],marker_color="#6D2E46"))
        fig.add_trace(go.Bar(name="Frutales",x=yrs,y=[8.4,12.6,16.8,21.0,25.2],marker_color="#97BC62"))
        fig.add_trace(go.Bar(name="Ahorro ERNC",x=yrs,y=[7.2,7.42,7.64,7.87,8.10],marker_color="#2C5F2D"))
        fig.update_layout(barmode="stack",height=380,margin=dict(t=30,b=30,l=40,r=10),yaxis_title="Millones CLP",legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",yaxis=dict(gridcolor="#eee"))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("#### 📊 Comparativa: Secano vs. Con Proyecto (Año 3)")
        cats=["Ingreso Anual\n(M CLP)","Costo Energía\n(M CLP)","Rent./Hectárea\n(M CLP)","Ha Productivas"]
        fig=go.Figure()
        fig.add_trace(go.Bar(name="Sin proyecto",x=cats,y=[12,4.8,0.23,15],marker_color="#B85042"))
        fig.add_trace(go.Bar(name="Con proyecto",x=cats,y=[99.75,0,1.92,47],marker_color="#2C5F2D"))
        fig.update_layout(barmode="group",height=380,margin=dict(t=30,b=50,l=40,r=10),yaxis_title="Millones CLP / ha",legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",yaxis=dict(gridcolor="#eee"))
        st.plotly_chart(fig,use_container_width=True)
    st.markdown("#### 💡 Análisis de Sensibilidad")
    st.dataframe(pd.DataFrame({"Escenario":["Pesimista (-20% ing.)","Conservador (-10%)","Base","Optimista (+10%)","Muy optimista (+20%)"],"TIR":["18,4%","28,1%","38,2%","48,5%","59,1%"],"VAN 10% (CLP)":["$18.200.000","$43.000.000","$67.800.000","$92.600.000","$117.400.000"],"Payback":["4,2 años","3,4 años","2,8 años","2,3 años","1,9 años"],"Evaluación":["✅ Viable","✅ Viable","✅ Muy rentable","✅ Excelente","✅ Excepcional"]}),hide_index=True,use_container_width=True)
    st.markdown('<div class="ib"><b>✅ Conclusión:</b> El proyecto es rentable en <b>todos los escenarios</b>. Incluso con -20% ingresos la TIR supera 18%, muy sobre el costo de oportunidad (10%). Recuperación en menos de 3 años en escenario base.</div>',unsafe_allow_html=True)

# ========== FLUJO DE CAJA ==========
elif sec=="📊 Flujo de Caja":
    st.markdown('<h2 class="sh">📊 Flujo de Caja Proyectado — 5 Años</h2>',unsafe_allow_html=True)
    disp=flujo_df.copy()
    disp["Año"]=["Año 0 (Inv.)","Año 1","Año 2","Año 3","Año 4","Año 5"]
    for col in disp.columns[1:]:
        disp[col]=disp[col].apply(lambda x: f"${x:,.0f}" if x!=0 else "-")
    st.dataframe(disp,hide_index=True,use_container_width=True,height=280)
    st.markdown("")
    c1,c2=st.columns(2)
    with c1:
        st.markdown("#### Flujo Neto Anual")
        colores=["#B85042" if v<0 else "#2C5F2D" for v in flujo_df["Flujo_Neto"]]
        fig=go.Figure(go.Bar(x=[f"Año {i}" for i in range(6)],y=flujo_df["Flujo_Neto"],marker_color=colores,text=[fmt(v) for v in flujo_df["Flujo_Neto"]],textposition="outside"))
        fig.update_layout(height=350,margin=dict(t=30,b=30,l=40,r=10),yaxis_title="Pesos Chilenos (CLP)",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",yaxis=dict(gridcolor="#eee"))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("#### Flujo Acumulado (Punto de Equilibrio)")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=[f"Año {i}" for i in range(6)],y=flujo_df["Flujo_Acum"],mode="lines+markers+text",line=dict(color="#2C5F2D",width=3),marker=dict(size=10,color=["#B85042" if v<0 else "#2C5F2D" for v in flujo_df["Flujo_Acum"]]),text=[fmt(v) for v in flujo_df["Flujo_Acum"]],textposition="top center"))
        fig.add_hline(y=0,line_dash="dash",line_color="#888",annotation_text="Punto equilibrio")
        fig.update_layout(height=350,margin=dict(t=30,b=30,l=40,r=10),yaxis_title="CLP Acumulado",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",yaxis=dict(gridcolor="#eee"))
        st.plotly_chart(fig,use_container_width=True)
    st.markdown('<div class="ib"><b>📌 Supuestos:</b> Crecimiento ingresos 5% anual (trigo), 10% (viña), frutales ramp-up. Inflación costos 3%. Crédito $60.000.000 a 5 años, tasa 8,4%, cuota $14.832.000/año. Mantención ERNC 1% inversión. Ahorro: reemplazo diésel y electricidad por solar.</div>',unsafe_allow_html=True)

# ========== SITUACIÓN TRIBUTARIA ==========
elif sec=="🏦 Situación Tributaria":
    st.markdown('<h2 class="sh">🏦 Situación Tributaria — Formularios 29 (IVA)</h2>',unsafe_allow_html=True)
    st.markdown('<div class="ib">Información de la <b>Carpeta Tributaria Regular del SII</b> generada el 01/02/2026. Declaraciones mensuales F29 últimos 12 meses.</div>',unsafe_allow_html=True)
    f29=pd.DataFrame({"Período":["Ene 2026","Dic 2025","Nov 2025","Oct 2025","Sep 2025","Ago 2025","Jul 2025","Jun 2025","May 2025","Abr 2025","Mar 2025","Feb 2025"],"Crédito_IVA":[64491,14968,0,23779,12091,0,14792,85106,66290,15647,13867,0],"Remanente_CF":[410458,346983,331020,331155,306467,294376,291439,278090,192854,126487,135452,121101],"Total_Pagar":[0,0,0,0,0,0,0,0,0,20856,0,0]})
    c1,c2,c3=st.columns(3)
    with c1: st.markdown(mc("Remanente CF Actual","$410.458","Enero 2026"),unsafe_allow_html=True)
    with c2: st.markdown(mc("Declaraciones al Día","36/36","3 años sin omisiones","accent"),unsafe_allow_html=True)
    with c3: st.markdown(mc("Deuda Tributaria","$0","Sin deudas con SII"),unsafe_allow_html=True)
    st.markdown("")
    c1,c2=st.columns([3,2])
    with c1:
        st.markdown("#### Evolución Remanente Crédito Fiscal (IVA)")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=f29["Período"][::-1],y=f29["Remanente_CF"][::-1],mode="lines+markers",fill="tozeroy",line=dict(color="#2C5F2D",width=2.5),marker=dict(size=7),fillcolor="rgba(151,188,98,0.2)"))
        fig.update_layout(height=320,margin=dict(t=20,b=30,l=50,r=10),yaxis_title="Pesos Chilenos (CLP)",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",yaxis=dict(gridcolor="#eee"))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("#### Detalle F29 (últimos 12 meses)")
        disp29=f29.copy()
        for col in ["Crédito_IVA","Remanente_CF","Total_Pagar"]:
            disp29[col]=disp29[col].apply(lambda x: f"${x:,.0f}" if x>0 else "-")
        st.dataframe(disp29,hide_index=True,use_container_width=True,height=400)
    st.markdown("#### 📊 Ventas con Débito Fiscal\n\n| Período | Débito Facturas | Base Imponible | PPM |\n|---------|---------------:|---------------:|----:|\n| Abr 2025 | $1.585.083 | $8.342.542 | $20.856 |\n| May 2024 | $22.192 | $116.800 | $146 |\n| Abr 2024 | $1.271.860 | $6.694.000 | $8.368 |\n| May 2023 | $495.746 | $2.609.189 | $6.523 |")
    st.markdown('<div class="wb"><b>📌 Interpretación:</b> Remanente creciente indica inversiones constantes en insumos (compras > ventas). Ventas concentradas en abr-may (cosecha). Patrón típico agrícola estacional. <b>Sin deudas tributarias.</b></div>',unsafe_allow_html=True)

# ========== POSTULACIÓN CORFO ==========
elif sec=="📋 Postulación CORFO":
    st.markdown('<h2 class="sh">📋 Postulación CORFO — Activa Inversión 2026</h2>',unsafe_allow_html=True)
    c1,c2=st.columns([2,1])
    with c1:
        st.markdown('<div class="ib" style="border-left-color:#2C5F2D;font-size:1rem;"><b>Programa:</b> CORFO Activa Inversión<br><b>Línea:</b> ERNC<br><b>Modalidad:</b> Subsidio no reembolsable hasta 50%<br><b>Fecha límite:</b> 18 de febrero de 2026<br><b>AOI:</b> Por definir - Región de Ñuble</div>',unsafe_allow_html=True)
        st.markdown("#### ✅ Checklist de Requisitos CORFO")
        for req,ok,nota in [("Inicio de actividades vigente SII",True,"Desde 01/03/2004"),("Sin anotaciones tributarias",True,"Verificado 01/02/2026"),("Régimen Pro Pyme (14D)",True,"Contabilidad completa"),("Declaraciones F29 al día",True,"36 meses consecutivos"),("Sin deudas tributarias",True,"Remanente a favor $410.458"),("Propiedad del terreno acreditada",True,"Rol 02229-00064, 100%"),("Cotización formal de equipos",True,"Makey E.I.R.L."),("Plan de negocios con flujo de caja",True,"Horizonte 5 años, TIR 38,2%"),("Evaluación impacto ambiental",False,"DIA no requerida <3MW"),("Certificado deuda Tesorería",True,"Sin deudas")]:
            icon="✅" if ok else "⚠️"
            color="#2C5F2D" if ok else "#D4A843"
            st.markdown(f'<div style="display:flex;align-items:center;padding:6px 0;border-bottom:1px solid #f0f0f0;"><span style="font-size:1.2rem;margin-right:10px;">{icon}</span><div><b style="color:{color};">{req}</b><br><span style="font-size:.82rem;color:#777;">{nota}</span></div></div>',unsafe_allow_html=True)
    with c2:
        st.markdown("#### 📐 Resumen Proyecto\n\n| Ítem | Valor (CLP) |\n|------|------:|\n| Inversión total | $185.000.000 |\n| Subsidio solicitado | $92.500.000 |\n| % Subsidio | 50% |\n| Aporte propio | $32.500.000 |\n| Crédito bancario | $60.000.000 |\n| Empleos directos | 8-12 |\n| Ha beneficiadas | 52 |\n| Reducción CO₂ | ~120 ton/año |")
        st.markdown('<div class="ib"><b>Puntaje estimado CORFO:</b><br>• Impacto productivo: <span class="tag">Alto</span><br>• Innovación: <span class="tag">Alto</span><br>• Sustentabilidad: <span class="tag gold">Muy Alto</span><br>• Empleo: <span class="tag">Medio-Alto</span></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 🎯 Argumentos Clave para el Evaluador")
    c1,c2,c3=st.columns(3)
    with c1: st.markdown('<div class="mc"><div class="lb">🌍 Impacto Ambiental</div><div class="vl" style="font-size:1.5rem;">120 ton CO₂/año</div><div class="dt">Eliminación diésel, energía limpia. Contribución a metas de carbono neutralidad 2050.</div></div>',unsafe_allow_html=True)
    with c2: st.markdown('<div class="mc accent"><div class="lb">💼 Impacto Económico</div><div class="vl" style="font-size:1.5rem;">+730% Ingresos</div><div class="dt">De $12M a $99,7M al año 3. Secano a riego multiplica productividad.</div></div>',unsafe_allow_html=True)
    with c3: st.markdown('<div class="mc" style="border-left-color:#4A7C59;"><div class="lb">👥 Impacto Social</div><div class="vl" style="font-size:1.5rem;">12 empleos</div><div class="dt">8-12 puestos permanentes en zona rural de Ñuble. Arraigo territorial.</div></div>',unsafe_allow_html=True)

# ========== DOCUMENTACIÓN ==========
elif sec=="📎 Documentación":
    st.markdown('<h2 class="sh">📎 Carpeta de Documentación del Proyecto</h2>',unsafe_allow_html=True)
    st.markdown('<div class="ib">Todos los documentos para postulación <b>CORFO Activa Inversión</b> y <b>financiamiento bancario</b> (BancoEstado, INDAP, CNR).</div>',unsafe_allow_html=True)
    st.markdown("#### 📁 Documentos Incluidos")
    for icon,nombre,detalle,estado in [("📋","Contrato de Prestación de Servicios","Makey E.I.R.L. - Mirta Vera S.","✅ Firmado 10/02/2026"),("🏛️","Carpeta Tributaria Regular SII","44 páginas - F29 + F22 + Datos","✅ Generada 01/02/2026"),("📊","Plan de Negocios y Flujo de Caja","Proyección 5 años con sensibilidad","✅ Incluido en esta app"),("⚡","Propuesta Técnica ERNC","Dimensionamiento 150 kWp","✅ Makey E.I.R.L."),("💰","Cotización Formal de Equipos","Paneles, inversores, bombas","✅ Vigente"),("🗺️","Plano del Predio","Ubicación paneles, pozos, eléctrica","✅ Ingeniería básica"),("📄","Certificado de Dominio","Conservador BB.RR. Chillán","⏳ Por obtener"),("📄","Certificado Deuda Tesorería","Tesorería Gral. República","⏳ Por obtener"),("📄","Cédula de Identidad","Mirta Aurora Vera Sepúlveda","✅ Vigente"),("📄","Inicio de Actividades SII","Comprobante digital","✅ Vigente desde 2004")]:
        ec="#2C5F2D" if "✅" in estado else "#D4A843"
        st.markdown(f'<div style="display:flex;align-items:center;padding:12px 16px;margin:4px 0;background:#fff;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,.04);border-left:4px solid {ec};"><span style="font-size:1.8rem;margin-right:14px;">{icon}</span><div style="flex:1;"><b style="color:#333;">{nombre}</b><br><span style="font-size:.85rem;color:#666;">{detalle}</span></div><div style="text-align:right;"><span style="color:{ec};font-weight:600;font-size:.85rem;">{estado}</span></div></div>',unsafe_allow_html=True)
    st.markdown("")
    st.markdown('<div class="wb"><b>⏳ Pendientes</b> (antes del 18/02/2026):<br>• Certificado de Dominio - Conservador BB.RR. Chillán<br>• Certificado de Deuda - Tesorería General</div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 🏢 Datos del Consultor")
    c1,c2=st.columns(2)
    with c1: st.markdown("| Campo | Detalle |\n|-------|--------|\n| Empresa | Makey E.I.R.L. |\n| RUT | 77.044.017-3 |\n| Representante | José Antonio Eyzaguirre R. |\n| RUT Rep. | 13.621.282-6 |\n| Domicilio | Arturo Prat 237, Bulnes |")
    with c2: st.markdown("| Campo | Detalle |\n|-------|--------|\n| Honorarios | $300.000 CLP |\n| Banco | Santander Empresas |\n| Cuenta Corriente | 27338305 |\n| Email | joseantonioe2@gmail.com |\n| Contrato | Firmado 10/02/2026 |")

# FOOTER
st.markdown("---")
st.markdown('<div style="text-align:center;color:#999;font-size:.8rem;padding:1rem 0;"><b>Carpeta Digital de Proyecto</b> — Fundo Las Vertientes, Quinchamalí, Chillán<br>Preparado por <b>Makey E.I.R.L.</b> · Febrero 2026 · CORFO Activa Inversión<br><i>Documento confidencial — Uso exclusivo para evaluación de financiamiento</i></div>',unsafe_allow_html=True)
