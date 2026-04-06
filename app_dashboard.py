
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Dashboard Psicológico Infantil")

# Cargar datos
df = pd.read_excel("Matriz valoración infantil Alpha 2026.xlsx")
df.columns = [c.strip() for c in df.columns]

# Identificar columnas
genero = [c for c in df.columns if "genero" in c.lower() or "género" in c.lower() or "sexo" in c.lower()][0]
comunidad = [c for c in df.columns if "comunidad" in c.lower()][0]

auto_items = [c for c in df.columns if c.upper().startswith("E")]
dep_items = [c for c in df.columns if c.upper().startswith("D")]

df["AUTOESTIMA_TOTAL"] = df[auto_items].sum(axis=1)
df["DEPORTE_TOTAL"] = df[dep_items].sum(axis=1)

# Filtros
col1, col2 = st.columns(2)
with col1:
    filtro_genero = st.multiselect("Filtrar por género", df[genero].unique(), default=df[genero].unique())
with col2:
    filtro_comunidad = st.multiselect("Filtrar por comunidad", df[comunidad].unique(), default=df[comunidad].unique())

df = df[df[genero].isin(filtro_genero)]
df = df[df[comunidad].isin(filtro_comunidad)]

# KPIs
st.subheader("Indicadores")
k1, k2, k3 = st.columns(3)
k1.metric("Total niños", len(df))
k2.metric("Autoestima promedio", round(df["AUTOESTIMA_TOTAL"].mean(),2))
k3.metric("Satisfacción deportiva promedio", round(df["DEPORTE_TOTAL"].mean(),2))

# Conteo
st.subheader("Distribución")
c1, c2 = st.columns(2)

with c1:
    fig = px.histogram(df, x=genero, title="Niños por género")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.histogram(df, x=comunidad, title="Niños por comunidad")
    st.plotly_chart(fig, use_container_width=True)

# Autoestima por comunidad
st.subheader("Autoestima por comunidad")
auto_com = df.groupby(comunidad)["AUTOESTIMA_TOTAL"].mean().reset_index()
fig = px.bar(auto_com, x=comunidad, y="AUTOESTIMA_TOTAL")
st.plotly_chart(fig, use_container_width=True)

# Deporte por comunidad
st.subheader("Satisfacción deportiva por comunidad")
dep_com = df.groupby(comunidad)["DEPORTE_TOTAL"].mean().reset_index()
fig = px.bar(dep_com, x=comunidad, y="DEPORTE_TOTAL")
st.plotly_chart(fig, use_container_width=True)

# Tabla
st.subheader("Datos filtrados")
st.dataframe(df)
