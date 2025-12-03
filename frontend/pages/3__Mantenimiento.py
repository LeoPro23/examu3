import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date
import os

st.set_page_config(page_title="Gestión de Mantenimiento", page_icon="🔧", layout="wide")

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

st.title("🔧 Gestión de Mantenimiento")

# Funciones auxiliares
def get_mantenimientos():
    try:
        response = requests.get(f"{API_URL}/api/mantenimientos/mantenimientos")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_equipos():
    try:
        response = requests.get(f"{API_URL}/api/equipos/equipos")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_proveedores():
    try:
        response = requests.get(f"{API_URL}/api/proveedores/proveedores")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_mantenimiento(data):
    try:
        response = requests.post(f"{API_URL}/api/mantenimientos/mantenimientos", json=data)
        return response
    except Exception as e:
        return None

# Tabs
tab1, tab2 = st.tabs(["📋 Listado de Mantenimientos", "➕ Registrar Mantenimiento"])

with tab1:
    st.subheader("Historial de Mantenimientos")
    
    mantenimientos = get_mantenimientos()
    
    if mantenimientos:
        df = pd.DataFrame(mantenimientos)
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro_estado = st.multiselect(
                "Filtrar por Estado",
                options=df['estado'].unique() if not df.empty else []
            )
        with col2:
            filtro_tipo = st.multiselect(
                "Filtrar por Tipo",
                options=df['tipo'].unique() if not df.empty else []
            )
            
        if filtro_estado:
            df = df[df['estado'].isin(filtro_estado)]
        if filtro_tipo:
            df = df[df['tipo'].isin(filtro_tipo)]
            
        st.dataframe(
            df,
            column_config={
                "costo": st.column_config.NumberColumn(format="$%.2f"),
                "fecha_programada": st.column_config.DateColumn(format="DD/MM/YYYY"),
                "fecha_realizada": st.column_config.DateColumn(format="DD/MM/YYYY"),
            },
            use_container_width=True
        )
    else:
        st.info("No hay mantenimientos registrados")

with tab2:
    st.subheader("Registrar Nuevo Mantenimiento")
    
    equipos = get_equipos()
    proveedores = get_proveedores()
    
    if not equipos:
        st.warning("No hay equipos registrados para dar mantenimiento")
    else:
        with st.form("form_mantenimiento"):
            col1, col2 = st.columns(2)
            
            with col1:
                equipo_opciones = {f"{e['nombre']} ({e['codigo_inventario']})": e['id'] for e in equipos}
                equipo_sel = st.selectbox("Equipo", options=list(equipo_opciones.keys()))
                
                tipo = st.selectbox("Tipo de Mantenimiento", ["preventivo", "correctivo"])
                prioridad = st.selectbox("Prioridad", ["baja", "media", "alta", "urgente"])
                
                fecha_programada = st.date_input("Fecha Programada", min_value=date.today())
                
            with col2:
                proveedor_opciones = {p['razon_social']: p['id'] for p in proveedores}
                proveedor_sel = st.selectbox("Proveedor (Opcional)", options=["Ninguno"] + list(proveedor_opciones.keys()))
                
                costo_estimado = st.number_input("Costo Estimado ($)", min_value=0.0, step=10.0)
                descripcion = st.text_area("Descripción del Trabajo")
                
            submitted = st.form_submit_button("Registrar Mantenimiento", use_container_width=True)
            
            if submitted:
                data = {
                    "equipo_id": equipo_opciones[equipo_sel],
                    "tipo": tipo,
                    "fecha_programada": str(fecha_programada),
                    "prioridad": prioridad,
                    "descripcion": descripcion,
                    "costo": costo_estimado,
                    "estado": "programado"
                }
                
                if proveedor_sel != "Ninguno":
                    data["proveedor_id"] = proveedor_opciones[proveedor_sel]
                
                response = create_mantenimiento(data)
                
                if response and response.status_code == 200:
                    st.success("✅ Mantenimiento registrado exitosamente")
                    st.rerun()
                else:
                    st.error("Error al registrar el mantenimiento")
