import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="Gestión de Proveedores", page_icon="🏢", layout="wide")

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

st.title("🏢 Gestión de Proveedores")

# Funciones auxiliares
def get_proveedores():
    try:
        response = requests.get(f"{API_URL}/api/proveedores/proveedores")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_proveedor(data):
    try:
        response = requests.post(f"{API_URL}/api/proveedores/proveedores", json=data)
        return response
    except Exception as e:
        return None

# Tabs
tab1, tab2 = st.tabs(["📋 Listado de Proveedores", "➕ Registrar Proveedor"])

with tab1:
    st.subheader("Directorio de Proveedores")
    
    proveedores = get_proveedores()
    
    if proveedores:
        df = pd.DataFrame(proveedores)
        
        st.dataframe(
            df,
            column_config={
                "sitio_web": st.column_config.LinkColumn("Sitio Web"),
                "email": st.column_config.LinkColumn("Email"),
            },
            use_container_width=True
        )
    else:
        st.info("No hay proveedores registrados")

with tab2:
    st.subheader("Registrar Nuevo Proveedor")
    
    with st.form("form_proveedor"):
        col1, col2 = st.columns(2)
        
        with col1:
            razon_social = st.text_input("Razón Social *")
            ruc = st.text_input("RUC *")
            telefono = st.text_input("Teléfono")
            email = st.text_input("Email")
            
        with col2:
            contacto_nombre = st.text_input("Nombre de Contacto")
            contacto_telefono = st.text_input("Teléfono de Contacto")
            direccion = st.text_area("Dirección")
            sitio_web = st.text_input("Sitio Web")
            
        notas = st.text_area("Notas Adicionales")
        
        submitted = st.form_submit_button("Registrar Proveedor", use_container_width=True)
        
        if submitted:
            if not razon_social or not ruc:
                st.error("Razón Social y RUC son obligatorios")
            else:
                data = {
                    "razon_social": razon_social,
                    "ruc": ruc,
                    "telefono": telefono,
                    "email": email,
                    "contacto_nombre": contacto_nombre,
                    "contacto_telefono": contacto_telefono,
                    "direccion": direccion,
                    "sitio_web": sitio_web,
                    "notas": notas
                }
                
                response = create_proveedor(data)
                
                if response and response.status_code == 200:
                    st.success("✅ Proveedor registrado exitosamente")
                    st.rerun()
                elif response:
                    st.error(f"Error: {response.json().get('detail', 'Error desconocido')}")
                else:
                    st.error("Error de conexión con el servidor")
