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
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #2B2620; }
    .stApp { background-color: #EDE8DE; }
    h1, h2, h3 { font-family: 'Fraunces', serif !important; color: #2B1B11 !important; }
    h1 { font-size: clamp(30px,4.6vw,50px) !important; font-weight: 600 !important; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(43,27,17,.94); border-radius: 8px; padding: 5px; gap: 5px; }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"] { display: none !important; }
    
    .stTabs [data-baseweb="tab"] { color: rgba(255,255,255,.72) !important; font-weight: 500; background-color: transparent !important; border: none !important; padding: 10px 16px; }
    .stTabs [data-baseweb="tab"]:hover { color: #C8935A !important; }
    .stTabs [aria-selected="true"] { background-color: #C8935A !important; color: #2B1B11 !important; border-radius: 4px; }
    .stTabs [aria-selected="true"]:hover { color: #2B1B11 !important; }
    
    div[data-testid="stMetricValue"] { font-family: 'Fraunces', serif !important; color: #2B1B11 !important; font-size: 26px !important; }
    div.stButton > button:first-child, div.stFormSubmitButton > button:first-child { background-color: #46613F !important; color: white !important; border-radius: 999px !important; font-weight: 600 !important; border: none !important; padding: 10px 24px !important; }
    
    .toc-box { background-color: #FFFCF6; border-left: 5px solid #8B5A2B; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .toc-title { font-family: 'Fraunces', serif; font-size: 20px; color: #402A1C; margin-bottom: 10px; font-weight: 600; }
    .toc-box.entonces { border-left-color: #46613F; }
    .toc-box.porque { border-left-color: #B8722A; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<p style='font-family:monospace; color:#8B5A2B; font-weight:600; font-size:12px; text-transform:uppercase;'>— Fundación Luker · Manizales y Caldas</p>", unsafe_allow_html=True)
st.markdown("<h1>Juntos reconstruimos</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B5F50; font-size:16px; margin-bottom:20px;'>Un mismo lugar para levantar el diagnóstico, decidir qué ayuda se da y hacer seguimiento a lo que ese aporte deja instalado.</p>", unsafe_allow_html=True)

# --- DATOS ---
CSV_PATH = 'data/matriz_maestra.csv'
CSV_DIAG = 'data/diagnostico.csv'

def load_data(path):
    if os.path.exists(path): return pd.read_csv(path)
    return pd.DataFrame()

df = load_data(CSV_PATH)
df_d = load_data(CSV_DIAG)

# Asegurar columnas si no existen (retrocompatibilidad)
if 'Evidencia_Diagnostico' not in df.columns:
    df['Evidencia_Diagnostico'] = 'No registrada'
if 'Decision_Pendiente' not in df.columns:
    df['Decision_Pendiente'] = 'Por definir'

tab1, tab2, tab3, tab4 = st.tabs(["01 Teoría de Cambio", "02 Diagnóstico", "03 Registro de Ayudas", "04 Matriz MEL"])

with tab1:
    st.header("Teoría de Cambio y Objetivos MEL")
    st.markdown("""
    <div class="toc-box"><div class="toc-title">SI (Insumos y Actividades)</div>Fundación Luker articula actores públicos, privados, de cooperación y comunitarios; identifica con rigor las necesidades diferenciales en cada línea; y canaliza recursos propios y de aliados hacia las brechas no cubiertas...</div>
    <div class="toc-box entonces"><div class="toc-title">ENTONCES (Resultados e Impacto)</div>Se reducirá el impacto del sismo sobre el bienestar del equipo, la población albergada, la red de salud, el patrimonio/legado institucional y la continuidad educativa...</div>
    <div class="toc-box porque"><div class="toc-title">PORQUE (Nuestra Propuesta de Valor)</div>La Fundación aporta capacidad técnica de diagnóstico, articulación interinstitucional y movilización de recursos que complementa la respuesta pública.</div>
    """, unsafe_allow_html=True)

with tab2:
    st.header("Diagnóstico General (Fase 1)")
    with st.expander("+ Agregar Nuevo Diagnóstico", expanded=False):
        with st.form("diag_form"):
            col1, col2 = st.columns(2)
            with col1:
                linea_d = st.selectbox("Línea de Acción", ["Equipo y aliados", "Ayuda humanitaria", "Salud y salud mental", "Legado e instituciones religiosas", "Reconstrucción educativa", "Relacionamiento y recursos"], key="ld")
                indicador_d = st.text_input("Indicador (ej. Sedes caracterizadas) *")
            with col2:
                valor_d = st.number_input("Valor Actual", min_value=0, value=0)
                meta_d = st.number_input("Meta Esperada", min_value=1, value=1)
            submit_d = st.form_submit_button("Guardar Diagnóstico")
            if submit_d and indicador_d:
                pct = round((valor_d / meta_d) * 100, 2) if meta_d > 0 else 0
                nueva_fila_d = {"Linea_Accion": linea_d, "Indicador": indicador_d, "Valor": valor_d, "Meta": meta_d, "Porcentaje": pct}
                df_d = pd.concat([df_d, pd.DataFrame([nueva_fila_d])], ignore_index=True)
                df_d.to_csv(CSV_DIAG, index=False)
                st.success("Diagnóstico registrado!")
                st.rerun()

    if not df_d.empty:
        st.subheader("Indicadores de Alcance y Acceso")
        st.dataframe(df_d, use_container_width=True, hide_index=True)
        st.divider()
        fig_bar = px.bar(df_d, x='Indicador', y='Porcentaje', color='Linea_Accion', title='Avance de Diagnóstico (%)')
        fig_bar.update_layout(yaxis_range=[0,100])
        st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.header("Registro de Ayudas")
    with st.expander("+ Registrar Nueva Iniciativa", expanded=False):
        with st.form("registro_form"):
            st.markdown("Completa los datos según el protocolo del plan preliminar:")
            col1, col2 = st.columns(2)
            with col1:
                necesidad = st.text_input("Necesidad identificada *")
                evidencia = st.text_area("Evidencia / diagnóstico *", placeholder="Sustento de la necesidad...")
                linea = st.selectbox("Línea de Acción (Categoría)", ["Equipo y aliados", "Ayuda humanitaria", "Salud y salud mental", "Legado e instituciones religiosas", "Reconstrucción educativa", "Relacionamiento y recursos"])
                urgencia = st.selectbox("Urgencia (Categoría)", ["Alta", "Media", "Baja"])
            with col2:
                quien_atiende = st.text_input("Quién la está atendiendo")
                brecha = st.text_input("Brecha existente")
                aporte = st.text_input("Posible aporte Fundación Luker")
                decision = st.text_input("Decisión pendiente")
            
            st.markdown("---")
            col3, col4 = st.columns(2)
            with col3:
                fase = st.selectbox("Fase actual en el protocolo (Categoría)", ["Diagnóstico", "Priorización", "Formalización"])
            with col4:
                beneficiarios = st.number_input("Beneficiarios estimados", min_value=0, value=0)
            
            submit = st.form_submit_button("Guardar Iniciativa")
            if submit and necesidad and evidencia:
                nuevo_id = df['ID'].max() + 1 if not df.empty else 1
                nueva_fila = {
                    "ID": nuevo_id, "Linea_Accion": linea, "Necesidad": necesidad, 
                    "Evidencia_Diagnostico": evidencia, "Urgencia": urgencia, 
                    "Atendido_Por": quien_atiende if quien_atiende else "Por confirmar", 
                    "Brecha": brecha if brecha else "Por definir", 
                    "Aporte_Luker": aporte if aporte else "Por definir", 
                    "Decision_Pendiente": decision if decision else "Sin definir",
                    "Fase": fase, "Beneficiarios": beneficiarios, 
                    "Fuente_Datos": "Formulario MEL", "Responsable": "META-FL", "Fecha_Corte": datetime.now().strftime("%Y-%m-%d")
                }
                df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
                df.to_csv(CSV_PATH, index=False)
                st.success("¡Iniciativa registrada!")
                st.rerun()

    st.subheader("Iniciativas Actuales")
    if not df.empty:
        f_linea = st.selectbox("Filtrar por Línea", ["Todas"] + list(df['Linea_Accion'].unique()))
        df_show = df[df['Linea_Accion'] == f_linea] if f_linea != "Todas" else df
        
        # Mostrar exactamente las columnas solicitadas en la tabla
        columnas_mostrar = ['Necesidad', 'Evidencia_Diagnostico', 'Urgencia', 'Atendido_Por', 'Brecha', 'Aporte_Luker', 'Decision_Pendiente']
        
        # Asegurarnos de que existan para no romper la vista antigua
        for col in columnas_mostrar:
            if col not in df_show.columns:
                df_show[col] = "N/A"
                
        st.dataframe(
            df_show[columnas_mostrar].rename(columns={
                'Necesidad': 'Necesidad identificada',
                'Evidencia_Diagnostico': 'Evidencia / diagnóstico',
                'Atendido_Por': 'Quién la está atendiendo',
                'Brecha': 'Brecha existente',
                'Aporte_Luker': 'Posible aporte Fundación Luker',
                'Decision_Pendiente': 'Decisión pendiente'
            }), 
            use_container_width=True, hide_index=True
        )

with tab4:
    st.header("Matriz Completa")
    st.dataframe(df, use_container_width=True)
