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
    .stApp { background-color: #EDE8DE; }
    h1, h2, h3 { font-family: 'Fraunces', serif !important; color: #2B1B11 !important; }
    h1 { font-size: clamp(30px,4.6vw,50px) !important; font-weight: 600 !important; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(43,27,17,.94); border-radius: 8px; padding: 5px; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: rgba(255,255,255,.72) !important; font-weight: 500; background-color: transparent !important; border: none !important; }
    .stTabs [data-baseweb="tab"]:hover { color: #C8935A !important; }
    .stTabs [aria-selected="true"] { background-color: #C8935A !important; color: #2B1B11 !important; border-radius: 4px; }
    .stTabs [aria-selected="true"]:hover { color: #2B1B11 !important; }
    
    div[data-testid="stMetricValue"] { font-family: 'Fraunces', serif !important; color: #2B1B11 !important; font-size: 26px !important; }
    div.stButton > button:first-child, div.stFormSubmitButton > button:first-child {
        background-color: #46613F !important; color: white !important; border-radius: 999px !important; font-weight: 600 !important; border: none !important; padding: 10px 24px !important;
    }
    
    /* Cajas personalizadas para Teoría de Cambio */
    .toc-box {
        background-color: #FFFCF6;
        border-left: 5px solid #8B5A2B;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .toc-title {
        font-family: 'Fraunces', serif;
        font-size: 20px;
        color: #402A1C;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .toc-box.entonces { border-left-color: #46613F; }
    .toc-box.porque { border-left-color: #B8722A; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- CABECERA (HERO) ---
st.markdown("<p style='font-family:monospace; color:#8B5A2B; font-weight:600; font-size:12px; text-transform:uppercase;'>— Fundación Luker · Manizales y Caldas</p>", unsafe_allow_html=True)
st.markdown("<h1>De la emergencia al <em>territorio preparado</em></h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B5F50; font-size:16px; margin-bottom:20px;'>Un mismo lugar para levantar el diagnóstico, decidir qué ayuda se da y hacer seguimiento a lo que ese aporte deja instalado.</p>", unsafe_allow_html=True)

CSV_PATH = 'data/matriz_maestra.csv'
def load_data():
    if os.path.exists(CSV_PATH): return pd.read_csv(CSV_PATH)
    return pd.DataFrame()
df = load_data()

tab1, tab2, tab3, tab4 = st.tabs(["01 Teoría de Cambio", "02 Diagnóstico", "03 Registro de Ayudas", "04 Matriz MEL"])

with tab1:
    st.header("Teoría de Cambio y Objetivos MEL")
    st.markdown("El propósito de la intervención de **Fundación Luker** tras el sismo del 10 de agosto de 2026, estructurado a través de una hipótesis de impacto clara:")
    
    st.markdown("""
    <div class="toc-box">
        <div class="toc-title">SI (Insumos y Actividades)</div>
        Fundación Luker articula actores públicos, privados, de cooperación y comunitarios; identifica con rigor las necesidades diferenciales en cada línea; y canaliza recursos propios y de aliados hacia las brechas no cubiertas...
    </div>
    <div class="toc-box entonces">
        <div class="toc-title">ENTONCES (Resultados e Impacto)</div>
        Se reducirá el impacto del sismo sobre el bienestar del equipo, la población albergada, la red de salud, el patrimonio/legado institucional y, de forma prioritaria, la continuidad educativa de niños, niñas y jóvenes...
    </div>
    <div class="toc-box porque">
        <div class="toc-title">PORQUE (Nuestra Propuesta de Valor)</div>
        La Fundación aporta capacidad técnica de diagnóstico, articulación interinstitucional y movilización de recursos que complementa —sin duplicar— la respuesta pública y ciudadana.
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    colA, colB = st.columns([1.5, 1])
    with colA:
        st.subheader("Fases de la Intervención")
        st.markdown("**1. Emergencia Inmediata (0–30 días, en curso)**")
        st.caption("Monitoreo de alta frecuencia (semanal/diario), enfocado en necesidades y cobertura.")
        st.markdown("**2. Estabilización (1–3 meses)**")
        st.caption("Monitoreo quincenal/mensual y primeras evaluaciones de proceso.")
        st.markdown("**3. Reconstrucción y Resiliencia (3–24 meses)**")
        st.caption("Evaluación de medio término y final, indicadores de resultado/impacto, sistematización de aprendizajes.")
    
    with colB:
        st.subheader("Objetivos del MEL")
        st.markdown('''
        * **O1.** Dar seguimiento continuo a las 5 líneas + relacionamiento.
        * **O2.** Verificar el uso de recursos captados (campaña $1:$1).
        * **O3.** Evaluar la articulación para evitar duplicidades.
        * **O4.** Medir resultados, especialmente en la línea educativa (106 sedes).
        * **O5.** Documentar aprendizajes para futuras respuestas a emergencias.
        ''')

with tab2:
    st.header("Diagnóstico General (Fase 1)")
    st.markdown("Registro del alcance y acceso actual basado en el protocolo.")
    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Líneas Activas", df['Linea_Accion'].nunique())
        c2.metric("Total Necesidades Registradas", len(df))
        c3.metric("Beneficiarios Estimados", int(df['Beneficiarios'].sum()))
        c4.metric("Urgencia Alta", len(df[df['Urgencia'] == 'Alta']))
        
        st.divider()
        st.subheader("Registro de Diagnóstico (Protocolo)")
        df_diag = df[df['Fase'] == 'Diagnóstico']
        if not df_diag.empty:
            st.dataframe(df_diag[['Necesidad', 'Linea_Accion', 'Urgencia', 'Atendido_Por', 'Brecha', 'Beneficiarios']], use_container_width=True, hide_index=True)
        else:
            st.info("No hay iniciativas en fase de Diagnóstico en este momento.")
            
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
