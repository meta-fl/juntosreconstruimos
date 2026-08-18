import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title='Sistema MEL - Juntos Reconstruimos', layout='wide')

# --- ESTILOS CSS INYECTADOS ---
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #2B2620;
    }
    
    /* Fondo principal */
    .stApp { background-color: #EDE8DE; }
    
    /* Tipografía Títulos */
    h1, h2, h3 { font-family: 'Fraunces', serif !important; color: #2B1B11 !important; }
    h1 { font-size: clamp(30px,4.6vw,50px) !important; font-weight: 600 !important; }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(43,27,17,.94); border-radius: 8px; padding: 5px; }
    .stTabs [data-baseweb="tab"] { color: rgba(255,255,255,.72); font-weight: 500; }
    .stTabs [aria-selected="true"] { background-color: #C8935A !important; color: #2B1B11 !important; border-radius: 4px; }
    
    /* Tarjetas de Métricas */
    div[data-testid="stMetricValue"] { font-family: 'Fraunces', serif !important; color: #2B1B11 !important; font-size: 26px !important; }
    
    /* Botones */
    div.stButton > button:first-child, div.stFormSubmitButton > button:first-child {
        background-color: #46613F !important; color: white !important;
        border-radius: 999px !important; font-weight: 600 !important; border: none !important; padding: 10px 24px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- CABECERA (HERO) ---
st.markdown("<p style='font-family:monospace; color:#8B5A2B; font-weight:600; font-size:12px; text-transform:uppercase;'>— Fundación Luker · Manizales y Caldas</p>", unsafe_allow_html=True)
st.markdown("<h1>De la emergencia al <em>territorio preparado</em></h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B5F50; font-size:16px; margin-bottom:20px;'>Un mismo lugar para levantar el diagnóstico, decidir qué ayuda se da y hacer seguimiento a lo que ese aporte deja instalado.</p>", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
CSV_PATH = 'data/matriz_maestra.csv'

def load_data():
    if os.path.exists(CSV_PATH): return pd.read_csv(CSV_PATH)
    return pd.DataFrame()

df = load_data()

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3, tab4 = st.tabs(["01 Teoría de Cambio", "02 Diagnóstico", "03 Registro de Ayudas", "04 Matriz MEL"])

with tab1:
    st.header("Teoría de Cambio (Síntesis)")
    st.info("**SI** Fundación Luker articula actores públicos, privados y comunitarios; identifica necesidades con rigor; y canaliza recursos propios y de aliados hacia las brechas no cubiertas...")
    st.success("**ENTONCES** se reducirá el impacto del sismo sobre el bienestar, la población albergada, la red de salud y la continuidad educativa...")
    st.warning("**PORQUE** la Fundación aporta capacidad técnica de diagnóstico, articulación y movilización de recursos que complementa (sin duplicar) la respuesta pública y ciudadana.")
    
    st.divider()
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown("**1. Emergencia Inmediata (0-30 días)**")
        st.caption("Monitoreo de alta frecuencia enfocado en necesidades y cobertura.")
    with colB:
        st.markdown("**2. Estabilización (1-3 meses)**")
        st.caption("Monitoreo quincenal/mensual y primeras evaluaciones de proceso.")
    with colC:
        st.markdown("**3. Reconstrucción (3-24 meses)**")
        st.caption("Evaluación de impacto, sistematización de aprendizajes y resiliencia.")

with tab2:
    st.header("Diagnóstico General")
    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Líneas Activas", df['Linea_Accion'].nunique())
        c2.metric("Total Necesidades Registradas", len(df))
        c3.metric("Beneficiarios Estimados", int(df['Beneficiarios'].sum()))
        c4.metric("Urgencia Alta", len(df[df['Urgencia'] == 'Alta']))
        st.divider()
        fig = px.pie(df, names='Linea_Accion', title='Distribución por Línea')
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Registro de Ayudas")
    with st.expander("+ Registrar Nueva Iniciativa", expanded=False):
        with st.form("registro_form"):
            col1, col2 = st.columns(2)
            with col1:
                necesidad = st.text_input("Necesidad identificada *")
                linea = st.selectbox("Línea de Acción", ["Equipo y aliados", "Ayuda humanitaria", "Salud y salud mental", "Legado e instituciones religiosas", "Reconstrucción educativa", "Relacionamiento y recursos"])
                urgencia = st.selectbox("Urgencia", ["Alta", "Media", "Baja"])
            with col2:
                quien_atiende = st.text_input("¿Quién la atiende hoy?")
                brecha = st.text_input("Brecha existente")
                fase = st.selectbox("Fase actual", ["Diagnóstico", "Priorización", "Formalización"])
            
            aporte = st.text_input("Posible aporte Fundación Luker")
            beneficiarios = st.number_input("Beneficiarios estimados", min_value=0, value=0)
            
            submit = st.form_submit_button("Guardar Iniciativa")
            if submit and necesidad:
                nuevo_id = df['ID'].max() + 1 if not df.empty else 1
                nueva_fila = {"ID": nuevo_id, "Linea_Accion": linea, "Necesidad": necesidad, "Evidencia_Diagnostico": "Pendiente", "Urgencia": urgencia, "Atendido_Por": quien_atiende if quien_atiende else "Por confirmar", "Brecha": brecha if brecha else "Por definir", "Aporte_Luker": aporte if aporte else "Por definir", "Fase": fase, "Beneficiarios": beneficiarios, "Fuente_Datos": "Formulario MEL", "Responsable": "META-FL", "Fecha_Corte": datetime.now().strftime("%Y-%m-%d")}
                df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
                df.to_csv(CSV_PATH, index=False)
                st.success("¡Iniciativa registrada!")
                st.rerun()

    st.subheader("Iniciativas Actuales")
    if not df.empty:
        f_linea = st.selectbox("Filtrar por Línea", ["Todas"] + list(df['Linea_Accion'].unique()))
        df_show = df[df['Linea_Accion'] == f_linea] if f_linea != "Todas" else df
        st.dataframe(df_show[['Necesidad', 'Linea_Accion', 'Urgencia', 'Brecha', 'Fase']], use_container_width=True, hide_index=True)

with tab4:
    st.header("Matriz Completa")
    st.dataframe(df, use_container_width=True)
