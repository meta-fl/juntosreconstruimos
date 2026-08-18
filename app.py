import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='META - Juntos Reconstruimos', layout='wide')

st.title('Tablero de Monitoreo META - Juntos Reconstruimos')
st.markdown('**Fundación Luker | Manizales y Caldas**')

@st.cache_data
def load_data():
    df = pd.read_csv('data/matriz_maestra.csv')
    return df

df = load_data()

# Resumen General
st.header('Resumen General (Fase 1)')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Necesidades', len(df))
col2.metric('Urgencia Alta', len(df[df['Urgencia'] == 'Alta']))
col3.metric('Decisiones Pendientes', len(df[df['Estado_Decision'] == 'Pendiente']))
col4.metric('Beneficiarios Estimados', df['Beneficiarios'].sum())

st.divider()

# Monitoreo por Líneas
st.header('Monitoreo por Líneas de Acción')
fig = px.histogram(df, x='Linea_Accion', color='Estado_Decision', title='Estado de Necesidades por Línea de Acción', barmode='group')
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Protocolo de Ayudas - Decisiones Pendientes
st.header('Gestión de Decisiones (Comité Semanal)')
pendientes = df[df['Estado_Decision'] == 'Pendiente']

if not pendientes.empty:
    st.dataframe(pendientes[['Linea_Accion', 'Necesidad', 'Urgencia', 'Brecha', 'Aporte_Luker', 'Responsable']], use_container_width=True)
else:
    st.success('No hay decisiones pendientes en este momento.')

# Filtros Dinámicos
st.divider()
st.header('Explorar Matriz Completa')
linea_filtro = st.selectbox('Filtrar por Línea de Acción', ['Todas'] + list(df['Linea_Accion'].unique()))
if linea_filtro != 'Todas':
    st.dataframe(df[df['Linea_Accion'] == linea_filtro], use_container_width=True)
else:
    st.dataframe(df, use_container_width=True)

